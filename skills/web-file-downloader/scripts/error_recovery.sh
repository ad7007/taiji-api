#!/bin/bash
# 错误处理和恢复脚本

set -e

# 日志函数
log_info() { echo "[INFO] $1"; }
log_warn() { echo "[WARN] $1"; }
log_error() { echo "[ERROR] $1"; }

# 重试函数
retry_with_backoff() {
    local max_attempts="${1:-3}"
    local delay="${2:-2}"
    shift 2
    local cmd="$@"
    
    for ((i=1; i<=max_attempts; i++)); do
        log_info "尝试 $i/$max_attempts: $cmd"
        
        if eval "$cmd"; then
            log_info "成功"
            return 0
        fi
        
        if [ $i -lt $max_attempts ]; then
            log_warn "失败，${delay}秒后重试..."
            sleep $delay
            delay=$((delay * 2))  # 指数退避
        fi
    done
    
    log_error "所有尝试都失败了"
    return 1
}

# 检查浏览器状态
check_browser_status() {
    log_info "检查浏览器状态..."
    
    # 检查 Chrome 是否运行
    if ! pgrep -x "chrome" > /dev/null && ! pgrep -x "Google Chrome" > /dev/null; then
        log_error "Chrome 浏览器未运行"
        return 1
    fi
    
    # 检查下载目录
    if [ ! -d "$HOME/Downloads" ]; then
        log_error "下载目录不存在: $HOME/Downloads"
        return 1
    fi
    
    log_info "浏览器状态正常"
    return 0
}

# 检查网络连接
check_network() {
    local url="$1"
    log_info "检查网络连接: $url"
    
    if ! curl -s --max-time 10 "$url" > /dev/null; then
        log_error "无法连接到目标URL"
        return 1
    fi
    
    log_info "网络连接正常"
    return 0
}

# 等待文件出现
wait_for_file() {
    local pattern="$1"
    local timeout="${2:-10}"
    local interval="${3:-1}"
    
    log_info "等待文件: $pattern (超时: ${timeout}s)"
    
    local elapsed=0
    while [ $elapsed -lt $timeout ]; do
        local file
        file=$(ls -t $pattern 2>/dev/null | head -1)
        
        if [ -n "$file" ] && [ -f "$file" ]; then
            log_info "文件已出现: $file"
            echo "$file"
            return 0
        fi
        
        sleep $interval
        elapsed=$((elapsed + interval))
    done
    
    log_error "等待文件超时"
    return 1
}

# 清理临时文件
cleanup_temp_files() {
    log_info "清理临时文件..."
    
    local patterns=(
        "$HOME/Downloads/.com.google.Chrome.*"
        "$HOME/Downloads/.com.google.Chrome.*.crdownload"
    )
    
    for pattern in "${patterns[@]}"; do
        if ls $pattern 1> /dev/null 2>&1; then
            rm -f $pattern
            log_info "已清理: $pattern"
        fi
    done
}

# 主恢复流程
main_recovery() {
    log_info "启动错误恢复流程..."
    
    # 1. 检查浏览器
    if ! check_browser_status; then
        log_error "浏览器检查失败，请手动启动 Chrome"
        exit 1
    fi
    
    # 2. 检查网络
    if [ -n "$TARGET_URL" ]; then
        if ! check_network "$TARGET_URL"; then
            log_error "网络检查失败"
            exit 1
        fi
    fi
    
    # 3. 清理可能卡住的临时文件
    cleanup_temp_files
    
    log_info "恢复流程完成，可以重试下载"
}

# 如果直接运行此脚本
if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
    main_recovery
fi
