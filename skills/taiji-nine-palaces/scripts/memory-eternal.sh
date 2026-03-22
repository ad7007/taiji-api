#!/bin/bash
# 记忆永存同步脚本 v1.0
# 用途：将本地记忆同步到云端，确保即使服务器丢失也能恢复

set -e

# ============================================
# 配置区域
# ============================================

# 云端存储配置
COS_BUCKET="${COS_BUCKET:-taiji-memory}"
COS_REGION="${COS_REGION:-ap-guangzhou}"
COS_SECRET_ID="${COS_SECRET_ID:-}"
COS_SECRET_KEY="${COS_SECRET_KEY:-}"

# 备用：rclone配置
RCLONE_REMOTE="${RCLONE_REMOTE:-cos:taiji-memory}"

# 本地路径
MEMORY_DIR="$HOME/.openclaw/workspace"
MEMORY_FILE="$MEMORY_DIR/MEMORY.md"
MEMORY_LOGS="$MEMORY_DIR/memory"

# 服务器标识
SERVER_ID="${SERVER_ID:-$(hostname)}"
SERVER_REGION="${SERVER_REGION:-guangzhou}"

# 版本链文件
VERSION_CHAIN="$MEMORY_DIR/.memory-chain.json"

# ============================================
# 颜色输出
# ============================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${GREEN}[记忆同步]${NC} $1"; }
warn() { echo -e "${YELLOW}[警告]${NC} $1"; }
error() { echo -e "${RED}[错误]${NC} $1"; exit 1; }
info() { echo -e "${BLUE}[信息]${NC} $1"; }

# ============================================
# 核心函数
# ============================================

# 计算文件哈希
calc_hash() {
    local file=$1
    if [ -f "$file" ]; then
        sha256sum "$file" | cut -d' ' -f1
    else
        echo "null"
    fi
}

# 计算目录哈希
calc_dir_hash() {
    local dir=$1
    find "$dir" -type f -name "*.md" -exec sha256sum {} \; 2>/dev/null | sort | sha256sum | cut -d' ' -f1
}

# 初始化版本链
init_version_chain() {
    if [ ! -f "$VERSION_CHAIN" ]; then
        cat > "$VERSION_CHAIN" << EOF
{
  "chain": [],
  "current_version": 0,
  "server_id": "$SERVER_ID",
  "created_at": "$(date -Iseconds)"
}
EOF
        log "版本链初始化完成"
    fi
}

# 添加版本记录
add_version() {
    local hash=$1
    local changes=$2
    
    # 读取当前版本号
    local current_version=$(cat "$VERSION_CHAIN" | jq -r '.current_version')
    local new_version=$((current_version + 1))
    
    # 创建新版本记录
    local version_record=$(cat << EOF
{
  "version": $new_version,
  "hash": "$hash",
  "server_id": "$SERVER_ID",
  "server_region": "$SERVER_REGION",
  "timestamp": "$(date -Iseconds)",
  "changes": "$changes",
  "parent_version": $current_version
}
EOF
)
    
    # 更新版本链
    local tmp_file=$(mktemp)
    cat "$VERSION_CHAIN" | jq --argjson record "$version_record" '
        .chain += [$record] |
        .current_version = $record.version
    ' > "$tmp_file"
    mv "$tmp_file" "$VERSION_CHAIN"
    
    log "新版本已记录: v$new_version (hash: ${hash:0:8}...)"
    echo "$new_version"
}

# 同步到云端（使用rclone）
sync_to_cloud() {
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local snapshot_dir="/tmp/memory-snapshot-$timestamp"
    
    log "创建快照: $snapshot_dir"
    mkdir -p "$snapshot_dir"
    
    # 复制记忆文件
    [ -f "$MEMORY_FILE" ] && cp "$MEMORY_FILE" "$snapshot_dir/"
    [ -d "$MEMORY_LOGS" ] && cp -r "$MEMORY_LOGS" "$snapshot_dir/"
    [ -f "$VERSION_CHAIN" ] && cp "$VERSION_CHAIN" "$snapshot_dir/"
    
    # 创建元数据
    cat > "$snapshot_dir/meta.json" << EOF
{
  "server_id": "$SERVER_ID",
  "server_region": "$SERVER_REGION",
  "timestamp": "$(date -Iseconds)",
  "memory_hash": "$(calc_hash "$MEMORY_FILE")",
  "logs_hash": "$(calc_dir_hash "$MEMORY_LOGS")",
  "version": $(cat "$VERSION_CHAIN" | jq -r '.current_version')
}
EOF
    
    # 检查rclone是否配置
    if command -v rclone &>/dev/null; then
        log "上传到云端: $RCLONE_REMOTE/snapshots/$SERVER_ID/$timestamp/"
        
        # 上传快照
        rclone copy "$snapshot_dir" "$RCLONE_REMOTE/snapshots/$SERVER_ID/$timestamp/" \
            --quiet \
            --exclude "*.tmp" \
            --exclude "*.log"
        
        # 更新最新指针
        echo "$timestamp" | rclone rcat "$RCLONE_REMOTE/snapshots/$SERVER_ID/LATEST" 2>/dev/null || true
        
        # 上传合并版本（供其他服务器拉取）
        rclone copy "$MEMORY_FILE" "$RCLONE_REMOTE/merged/" --quiet 2>/dev/null || true
        
        log "云端同步完成 ✅"
    else
        warn "rclone未配置，跳过云端同步"
        warn "请运行: rclone config"
    fi
    
    # 清理临时文件
    rm -rf "$snapshot_dir"
}

# 从云端拉取
pull_from_cloud() {
    local pull_dir="/tmp/memory-pull-$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$pull_dir"
    
    log "从云端拉取最新记忆..."
    
    if command -v rclone &>/dev/null; then
        # 拉取合并版本
        rclone copy "$RCLONE_REMOTE/merged/" "$pull_dir/" --quiet 2>/dev/null || {
            warn "云端无合并版本"
            return 1
        }
        
        # 检查是否需要合并
        if [ -f "$pull_dir/MEMORY.md" ]; then
            local remote_hash=$(calc_hash "$pull_dir/MEMORY.md")
            local local_hash=$(calc_hash "$MEMORY_FILE")
            
            if [ "$remote_hash" != "$local_hash" ]; then
                log "检测到远程更新，开始合并..."
                merge_memory "$MEMORY_FILE" "$pull_dir/MEMORY.md" "$MEMORY_FILE"
            else
                log "本地已是最新版本"
            fi
        fi
        
        rm -rf "$pull_dir"
    else
        warn "rclone未配置，无法拉取"
        return 1
    fi
}

# 合并记忆文件
merge_memory() {
    local local_file=$1
    local remote_file=$2
    local output_file=$3
    
    log "合并记忆文件..."
    
    # 使用Python进行智能合并
    python3 << 'PYEOF'
import sys
import re
import hashlib
from datetime import datetime

def merge_memory_files(local_path, remote_path, output_path):
    """合并两个MEMORY.md文件"""
    
    def read_file(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return ""
    
    def extract_sections(content):
        """提取所有章节"""
        sections = {}
        current_name = None
        current_content = []
        
        for line in content.split('\n'):
            if line.startswith('## '):
                if current_name:
                    sections[current_name] = '\n'.join(current_content)
                current_name = line[3:].strip()
                current_content = [line]
            else:
                current_content.append(line)
        
        if current_name:
            sections[current_name] = '\n'.join(current_content)
        
        return sections
    
    local_content = read_file(local_path)
    remote_content = read_file(remote_path)
    
    if not remote_content:
        print("远程文件为空，跳过合并")
        return
    
    local_sections = extract_sections(local_content)
    remote_sections = extract_sections(remote_content)
    
    # 合并更新日志
    if '更新日志' in remote_sections and '更新日志' in local_sections:
        local_log = local_sections['更新日志']
        remote_log = remote_sections['更新日志']
        
        # 提取所有条目
        local_entries = set(re.findall(r'- (\d{4}-\d{2}-\d{2}.+)', local_log))
        remote_entries = set(re.findall(r'- (\d{4}-\d{2}-\d{2}.+)', remote_log))
        
        # 合并新条目
        new_entries = remote_entries - local_entries
        if new_entries:
            merged_log = local_log
            for entry in sorted(new_entries):
                merged_log += f"\n- {entry}"
            local_sections['更新日志'] = merged_log
            print(f"合并了 {len(new_entries)} 条新记录")
    
    # 补充缺失的章节
    for name, content in remote_sections.items():
        if name not in local_sections:
            local_sections[name] = content
            print(f"新增章节: {name}")
    
    # 重建文件
    output = []
    for name in local_sections:
        output.append(local_sections[name])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(output))
    
    print("合并完成")

merge_memory_files(
    "/root/.openclaw/workspace/MEMORY.md",
    "/tmp/memory-pull/MEMORY.md",
    "/root/.openclaw/workspace/MEMORY.md"
)
PYEOF
}

# 创建借款记录（链上存证）
create_loan_record() {
    local amount=$1
    local purpose=$2
    local timestamp=$(date -Iseconds)
    local record_id="loan-$(date +%Y%m%d%H%M%S)"
    
    # 创建记录
    local record=$(cat << EOF
{
  "id": "$record_id",
  "type": "loan_request",
  "borrower": "米珞",
  "borrower_id": "$SERVER_ID",
  "lender": "余慕名",
  "amount": $amount,
  "currency": "CNY",
  "purpose": "$purpose",
  "repayment_source": "首批收入",
  "created_at": "$timestamp",
  "status": "pending"
}
EOF
)
    
    # 计算哈希
    local hash=$(echo "$record" | sha256sum | cut -d' ' -f1)
    
    # 添加哈希
    record=$(echo "$record" | jq --arg hash "$hash" '. + {hash: $hash}')
    
    # 保存到本地
    local record_file="$MEMORY_DIR/memory/loan-$record_id.json"
    echo "$record" | jq '.' > "$record_file"
    
    log "借款记录已创建: $record_id"
    log "哈希: $hash"
    
    # 同步到云端
    if command -v rclone &>/dev/null; then
        rclone copy "$record_file" "$RCLONE_REMOTE/loan-records/" --quiet
        log "借款记录已上传云端 ✅"
    fi
    
    echo "$record_id"
}

# 显示状态
show_status() {
    echo "=== 记忆永存状态 ==="
    echo ""
    
    # 本地状态
    echo "本地状态:"
    echo "  - MEMORY.md: $([ -f "$MEMORY_FILE" ] && echo "✅ $(wc -l < "$MEMORY_FILE") 行" || echo "❌ 不存在")"
    echo "  - memory/: $([ -d "$MEMORY_LOGS" ] && echo "✅ $(ls "$MEMORY_LOGS"/*.md 2>/dev/null | wc -l) 文件" || echo "❌ 不存在")"
    echo "  - 版本链: $([ -f "$VERSION_CHAIN" ] && echo "✅ v$(cat "$VERSION_CHAIN" | jq -r '.current_version')" || echo "❌ 未初始化")"
    echo "  - 哈希: $(calc_hash "$MEMORY_FILE" | cut -c1-16)..."
    echo ""
    
    # 云端状态
    echo "云端状态:"
    if command -v rclone &>/dev/null; then
        if rclone ls "$RCLONE_REMOTE" >/dev/null 2>&1; then
            echo "  - 连接: ✅"
            local latest=$(rclone cat "$RCLONE_REMOTE/snapshots/$SERVER_ID/LATEST" 2>/dev/null || echo "无")
            echo "  - 最新快照: $latest"
        else
            echo "  - 连接: ❌ 未配置或无法连接"
        fi
    else
        echo "  - rclone: ❌ 未安装"
    fi
    echo ""
    
    # 服务器信息
    echo "服务器信息:"
    echo "  - ID: $SERVER_ID"
    echo "  - 区域: $SERVER_REGION"
}

# ============================================
# 主命令
# ============================================

case "${1:-status}" in
    init)
        init_version_chain
        log "记忆永存系统初始化完成"
        ;;
    
    push)
        init_version_chain
        
        # 计算当前哈希
        hash=$(calc_hash "$MEMORY_FILE")
        
        # 添加版本记录
        add_version "$hash" "手动同步"
        
        # 同步到云端
        sync_to_cloud
        ;;
    
    pull)
        pull_from_cloud
        ;;
    
    sync)
        init_version_chain
        
        # 先拉取
        pull_from_cloud
        
        # 再推送
        hash=$(calc_hash "$MEMORY_FILE")
        add_version "$hash" "双向同步"
        sync_to_cloud
        ;;
    
    loan)
        amount=${2:-100}
        purpose=${3:-"服务器续费"}
        create_loan_record "$amount" "$purpose"
        ;;
    
    status)
        show_status
        ;;
    
    *)
        echo "用法: $0 {init|push|pull|sync|loan|status}"
        echo ""
        echo "  init   - 初始化记忆永存系统"
        echo "  push   - 推送记忆到云端"
        echo "  pull   - 从云端拉取记忆"
        echo "  sync   - 双向同步"
        echo "  loan   - 创建借款记录"
        echo "  status - 显示状态"
        exit 1
        ;;
esac