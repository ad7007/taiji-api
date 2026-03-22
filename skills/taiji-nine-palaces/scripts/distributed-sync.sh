#!/bin/bash
# 分布式智能体同步脚本 v1.0
# 用法: ./distributed-sync.sh [push|pull|merge|status]

set -e

# 配置
RCLONE_REMOTE="${RCLONE_REMOTE:-gdrive:openclaw-distributed}"
LOCAL_OPENCLAW="$HOME/.openclaw"
WORKSPACE="$LOCAL_OPENCLAW/workspace"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SERVER_ID="${HOSTNAME:-$(hostname)}"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[SYNC]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# 检查依赖
check_deps() {
    command -v rclone >/dev/null || error "rclone未安装，请运行: curl https://rclone.org/install.sh | sudo bash"
    command -v python3 >/dev/null || error "python3未安装"
}

# 创建本地快照
create_snapshot() {
    local snapshot_dir="/tmp/openclaw-snapshot-$TIMESTAMP"
    mkdir -p "$snapshot_dir"/{memory,config,sessions,db}
    
    log "创建快照: $snapshot_dir"
    
    # 记忆层
    [ -f "$WORKSPACE/MEMORY.md" ] && cp "$WORKSPACE/MEMORY.md" "$snapshot_dir/"
    [ -d "$WORKSPACE/memory" ] && cp -r "$WORKSPACE/memory"/*.md "$snapshot_dir/memory/" 2>/dev/null || true
    
    # 配置层
    [ -f "$LOCAL_OPENCLAW/openclaw.json" ] && cp "$LOCAL_OPENCLAW/openclaw.json" "$snapshot_dir/config/"
    
    # 数据库
    [ -d "$LOCAL_OPENCLAW/memory" ] && cp "$LOCAL_OPENCLAW/memory"/*.sqlite "$snapshot_dir/db/" 2>/dev/null || true
    
    # 元数据
    cat > "$snapshot_dir/meta.json" << EOF
{
    "timestamp": "$TIMESTAMP",
    "server_id": "$SERVER_ID",
    "version": "1.0"
}
EOF
    
    # 创建哈希
    find "$snapshot_dir" -type f -exec sha256sum {} \; | sort > "$snapshot_dir/checksums.sha256"
    
    echo "$snapshot_dir"
}

# 推送到云端
push_snapshot() {
    check_deps
    
    local snapshot_dir=$(create_snapshot)
    
    log "推送快照到云端..."
    
    # 推送到云端（不覆盖）
    rclone copy "$snapshot_dir" "$RCLONE_REMOTE/snapshots/$SERVER_ID/$TIMESTAMP" \
        --exclude "*.log" \
        --exclude "*.tmp" \
        -v
    
    # 更新最新版本指针
    rclone copy - <(echo "$TIMESTAMP") "$RCLONE_REMOTE/snapshots/$SERVER_ID/LATEST" 2>/dev/null || true
    
    log "推送完成: $TIMESTAMP"
    rm -rf "$snapshot_dir"
}

# 从云端拉取
pull_snapshot() {
    check_deps
    
    local target_server="${1:-all}"
    local pull_dir="/tmp/openclaw-pull-$TIMESTAMP"
    mkdir -p "$pull_dir"
    
    log "拉取云端快照..."
    
    if [ "$target_server" = "all" ]; then
        # 拉取所有服务器的最新快照
        for server_dir in $(rclone lsf "$RCLONE_REMOTE/snapshots/" 2>/dev/null); do
            server_name=${server_dir%/}
            if [ "$server_name" != "$SERVER_ID" ]; then
                log "拉取服务器: $server_name"
                rclone copy "$RCLONE_REMOTE/snapshots/$server_name/" "$pull_dir/$server_name/" \
                    --max-depth 1 -v 2>/dev/null || warn "服务器 $server_name 无快照"
            fi
        done
    else
        rclone copy "$RCLONE_REMOTE/snapshots/$target_server/" "$pull_dir/$target_server/" -v
    fi
    
    echo "$pull_dir"
}

# 合并记忆
merge_memory() {
    local local_memory="$WORKSPACE/MEMORY.md"
    local pull_dir="$1"
    
    if [ ! -f "$local_memory" ]; then
        warn "本地MEMORY.md不存在，跳过合并"
        return
    fi
    
    log "合并记忆文件..."
    
    # 遍历拉取的其他服务器快照
    for server_dir in "$pull_dir"/*; do
        [ -d "$server_dir" ] || continue
        server_name=$(basename "$server_dir")
        
        # 查找最新的MEMORY.md
        latest_memory=$(find "$server_dir" -name "MEMORY.md" | head -1)
        
        if [ -f "$latest_memory" ]; then
            log "合并来自 $server_name 的记忆..."
            
            # 简单合并：将不同服务器的内容追加到本地
            # 如果有冲突，以时间戳较新的为准
            
            # 创建备份
            cp "$local_memory" "$local_memory.backup.$TIMESTAMP"
            
            # 使用Python脚本进行智能合并
            python3 << 'PYEOF'
import sys
import re
from datetime import datetime

def merge_memory(local_path, remote_path, output_path):
    """智能合并两个MEMORY.md文件"""
    
    def extract_update_log(content):
        """提取更新日志"""
        match = re.search(r'## 更新日志\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
        return match.group(1) if match else ""
    
    def extract_sections(content):
        """提取所有章节"""
        sections = {}
        current_name = None
        current_content = []
        
        for line in content.split('\n'):
            if line.startswith('## '):
                if current_name:
                    sections[current_name] = '\n'.join(current_content)
                current_name = line
                current_content = []
            else:
                current_content.append(line)
        
        if current_name:
            sections[current_name] = '\n'.join(current_content)
        
        return sections
    
    try:
        with open(local_path, 'r') as f:
            local_content = f.read()
        with open(remote_path, 'r') as f:
            remote_content = f.read()
    except:
        print("读取文件失败")
        return
    
    local_sections = extract_sections(local_content)
    remote_sections = extract_sections(remote_content)
    
    # 合并更新日志
    local_log = extract_update_log(local_content)
    remote_log = extract_update_log(remote_content)
    
    # 找出remote中有但local中没有的更新记录
    new_entries = []
    for line in remote_log.split('\n'):
        line = line.strip()
        if line and line.startswith('-') and line not in local_log:
            new_entries.append(line)
    
    if new_entries:
        # 在更新日志开头插入新条目
        updated_log = local_log
        for entry in new_entries:
            # 在第一个已有条目前插入
            if updated_log:
                updated_log = entry + '\n' + updated_log
            else:
                updated_log = entry
        
        # 替换更新日志
        if '## 更新日志' in local_content:
            local_content = re.sub(
                r'## 更新日志\n.*?(?=\n## |\Z)',
                f'## 更新日志\n{updated_log}\n',
                local_content,
                flags=re.DOTALL
            )
    
    # 写入结果
    with open(output_path, 'w') as f:
        f.write(local_content)
    
    print(f"合并完成，新增 {len(new_entries)} 条记录")

if __name__ == '__main__':
    import os
    local = os.environ.get('LOCAL_MEMORY')
    remote = os.environ.get('REMOTE_MEMORY')
    output = local
    
    if local and remote and os.path.exists(remote):
        merge_memory(local, remote, output)
PYEOF
            export LOCAL_MEMORY="$local_memory"
            export REMOTE_MEMORY="$latest_memory"
            python3 << 'PYEOF'
import os
import re

def merge_memory(local_path, remote_path, output_path):
    try:
        with open(local_path, 'r') as f:
            local = f.read()
        with open(remote_path, 'r') as f:
            remote = f.read()
    except Exception as e:
        print(f"读取失败: {e}")
        return
    
    # 提取更新日志
    def get_log(content):
        m = re.search(r'## 更新日志\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
        return m.group(1) if m else ""
    
    local_log = get_log(local)
    remote_log = get_log(remote)
    
    # 找新条目
    new = [l.strip() for l in remote_log.split('\n') if l.strip() and l.strip() not in local_log]
    
    if new:
        # 插入到日志开头
        updated = '\n'.join(new) + '\n' + local_log
        result = re.sub(
            r'## 更新日志\n.*?(?=\n## |\Z)',
            f'## 更新日志\n{updated}\n',
            local,
            flags=re.DOTALL
        )
        with open(output_path, 'w') as f:
            f.write(result)
        print(f"合并完成，新增 {len(new)} 条")
    else:
        print("无需合并")

merge_memory(
    os.environ.get('LOCAL_MEMORY'),
    os.environ.get('REMOTE_MEMORY'),
    os.environ.get('LOCAL_MEMORY')
)
PYEOF
        fi
    done
    
    log "记忆合并完成"
}

# 显示同步状态
show_status() {
    echo "=== 分布式智能体同步状态 ==="
    echo ""
    echo "服务器ID: $SERVER_ID"
    echo "时间: $(date)"
    echo ""
    
    # 本地状态
    echo "本地状态:"
    echo "  - MEMORY.md: $([ -f "$WORKSPACE/MEMORY.md" ] && echo "✅ $(wc -l < "$WORKSPACE/MEMORY.md") 行" || echo "❌ 不存在")"
    echo "  - memory/: $([ -d "$WORKSPACE/memory" ] && echo "✅ $(ls "$WORKSPACE/memory"/*.md 2>/dev/null | wc -l) 文件" || echo "❌ 不存在")"
    echo "  - 备份: $([ -d "$LOCAL_OPENCLAW/backups" ] && echo "✅ $(ls "$LOCAL_OPENCLAW/backups"/*.tar.gz 2>/dev/null | wc -l) 个" || echo "❌ 不存在")"
    echo ""
    
    # 云端状态
    echo "云端状态:"
    if rclone ls "$RCLONE_REMOTE/snapshots/" >/dev/null 2>&1; then
        echo "  - 连接: ✅"
        for server in $(rclone lsf "$RCLONE_REMOTE/snapshots/" 2>/dev/null); do
            server=${server%/}
            latest=$(rclone cat "$RCLONE_REMOTE/snapshots/$server/LATEST" 2>/dev/null || echo "未知")
            echo "  - $server: 快照 $latest"
        done
    else
        echo "  - 连接: ❌ 或无快照"
    fi
    echo ""
    
    # 最后同步时间
    if [ -f "$LOCAL_OPENCLAW/.last-distributed-sync" ]; then
        echo "最后同步: $(cat "$LOCAL_OPENCLAW/.last-distributed-sync")"
    else
        echo "最后同步: 从未"
    fi
}

# 主命令
case "${1:-status}" in
    push)
        push_snapshot
        echo "$TIMESTAMP" > "$LOCAL_OPENCLAW/.last-distributed-sync"
        ;;
    pull)
        pull_dir=$(pull_snapshot "${2:-all}")
        if [ -d "$pull_dir" ]; then
            merge_memory "$pull_dir"
            rm -rf "$pull_dir"
        fi
        ;;
    merge)
        pull_dir=$(pull_snapshot "${2:-all}")
        if [ -d "$pull_dir" ]; then
            merge_memory "$pull_dir"
            # 保留pull_dir供检查
            echo "合并完成，临时文件: $pull_dir"
        fi
        ;;
    status)
        show_status
        ;;
    *)
        echo "用法: $0 {push|pull|merge|status}"
        echo ""
        echo "  push   - 推送本地快照到云端"
        echo "  pull   - 从云端拉取并合并"
        echo "  merge  - 拉取并预览合并（不自动应用）"
        echo "  status - 显示同步状态"
        exit 1
        ;;
esac