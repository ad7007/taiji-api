#!/bin/bash
# 分布式太极远程调度脚本
# 用法: ./remote-dispatch.sh <server> <action> <params>

set -e

# 配置
declare -A PEERS
PEERS["guangzhou"]=""
PEERS["losangeles"]=""  # 需要填入实际IP

# 云端同步配置（用于服务器间通信）
RCLONE_REMOTE="${RCLONE_REMOTE:-gdrive:taiji-sync}"
SHARED_TOKEN="${TAIJI_SHARED_TOKEN:-milo-taiji-2026}"

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log() { echo -e "${GREEN}[DISPATCH]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# 检查远程服务器状态
check_peer() {
    local server=$1
    local peer_host=${PEERS[$server]}
    
    if [ -z "$peer_host" ]; then
        warn "服务器 $server 未配置IP"
        return 1
    fi
    
    # 检查连接
    if timeout 5 bash -c "echo >/dev/tcp/$peer_host/443" 2>/dev/null; then
        log "服务器 $server ($peer_host) 在线 ✅"
        return 0
    else
        warn "服务器 $server ($peer_host) 不可达"
        return 1
    fi
}

# 通过rclone传递任务（无需公网IP）
dispatch_via_cloud() {
    local server=$1
    local action=$2
    local params=$3
    local task_id=$(date +%Y%m%d_%H%M%S)_$(head -c 8 /dev/urandom | xxd -p)
    
    log "通过云端派发任务到 $server: $action"
    
    # 创建任务文件
    local task_file="/tmp/task_$task_id.json"
    cat > "$task_file" << EOF
{
    "taskId": "$task_id",
    "server": "$SERVER_ID",
    "target": "$server",
    "action": "$action",
    "params": $params,
    "createdAt": "$(date -Iseconds)",
    "status": "pending"
}
EOF
    
    # 上传到云端任务队列
    rclone copy "$task_file" "$RCLONE_REMOTE/tasks/$server/inbox/" 2>/dev/null || {
        error "无法上传任务到云端，请检查rclone配置"
    }
    
    rm -f "$task_file"
    
    log "任务已派发: $task_id"
    echo "$task_id"
}

# 直接调用远程API（需要公网IP）
dispatch_direct() {
    local server=$1
    local action=$2
    local params=$3
    local peer_host=${PEERS[$server]}
    
    if [ -z "$peer_host" ]; then
        error "服务器 $server 未配置IP"
    fi
    
    log "直接调用 $server API: $action"
    
    # 调用远程API
    local response
    response=$(curl -s -X POST "https://$peer_host/api/taiji/dispatch" \
        -H "Authorization: Bearer $SHARED_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"action\": \"$action\", \"params\": $params}" \
        --connect-timeout 10 \
        --max-time 300)
    
    if [ $? -eq 0 ]; then
        log "远程调用成功"
        echo "$response"
    else
        error "远程调用失败"
    fi
}

# 等待任务结果（通过云端）
wait_for_result() {
    local task_id=$1
    local timeout=${2:-300}  # 默认5分钟
    local start=$(date +%s)
    
    log "等待任务结果: $task_id"
    
    while true; do
        # 检查云端是否有结果
        local result_file="/tmp/result_$task_id.json"
        
        if rclone copy "$RCLONE_REMOTE/results/$task_id.json" "/tmp/" 2>/dev/null; then
            log "收到结果"
            cat "$result_file"
            rm -f "$result_file"
            return 0
        fi
        
        # 检查超时
        local now=$(date +%s)
        if [ $((now - start)) -gt $timeout ]; then
            error "任务超时"
        fi
        
        sleep 5
    done
}

# 采集任务（智能路由）
collect() {
    local url=$1
    local server_hint=${2:-auto}
    
    # 数据源路由
    local target_server=""
    
    if [ "$server_hint" = "auto" ]; then
        # 自动判断
        if [[ "$url" =~ (youtube|twitter|x\.com|tiktok|google|github|reddit|openai) ]]; then
            target_server="losangeles"
        elif [[ "$url" =~ (douyin|xiaohongshu|bilibili|weibo|zhihu|taobao|jd) ]]; then
            target_server="guangzhou"
        else
            # 默认本地
            target_server="local"
        fi
    else
        target_server="$server_hint"
    fi
    
    log "采集路由: $url → $target_server"
    
    if [ "$target_server" = "local" ]; then
        # 本地执行
        python3 ~/.openclaw/workspace/skills/taiji-nine-palaces/core/palace_1_collector.py collect "$url"
    else
        # 远程执行
        local task_id
        task_id=$(dispatch_via_cloud "$target_server" "collect" "{\"url\": \"$url\"}")
        wait_for_result "$task_id"
    fi
}

# 显示状态
status() {
    echo "=== 分布式太极状态 ==="
    echo ""
    echo "本服务器: ${SERVER_ID:-$(hostname)}"
    echo ""
    
    echo "对等服务器:"
    for server in "${!PEERS[@]}"; do
        if [ "$server" != "${SERVER_ID:-$(hostname)}" ]; then
            if check_peer "$server" 2>/dev/null; then
                echo "  - $server: ✅ 在线"
            else
                echo "  - $server: ❌ 离线"
            fi
        fi
    done
    
    echo ""
    echo "云端同步:"
    if rclone ls "$RCLONE_REMOTE" >/dev/null 2>&1; then
        echo "  - 状态: ✅ 已连接"
        echo "  - 待处理任务: $(rclone lsf "$RCLONE_REMOTE/tasks/$SERVER_ID/inbox/" 2>/dev/null | wc -l)"
    else
        echo "  - 状态: ❌ 未配置或无法连接"
    fi
}

# 主命令
SERVER_ID="${SERVER_ID:-$(hostname)}"

case "${1:-status}" in
    collect)
        collect "$2" "${3:-auto}"
        ;;
    dispatch)
        if [ -n "${PEERS[$2]}" ]; then
            dispatch_direct "$2" "$3" "$4"
        else
            dispatch_via_cloud "$2" "$3" "$4"
        fi
        ;;
    wait)
        wait_for_result "$2" "${3:-300}"
        ;;
    check)
        check_peer "$2"
        ;;
    status)
        status
        ;;
    *)
        echo "用法: $0 {collect|dispatch|wait|check|status}"
        echo ""
        echo "  collect <url> [server]  - 采集URL（自动路由）"
        echo "  dispatch <server> <action> <params> - 派发任务"
        echo "  wait <task_id> [timeout] - 等待任务结果"
        echo "  check <server>          - 检查服务器状态"
        echo "  status                  - 显示分布式状态"
        exit 1
        ;;
esac