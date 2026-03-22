#!/bin/bash
# 太极九宫任务管理系统 - 命令行工具

TAIJI_API="http://localhost:8000"

show_help() {
    cat << EOF
太极九宫任务管理系统 - 命令行工具

用法：$0 <命令> [参数]

命令:
  status          查看系统状态
  palaces         查看所有宫位
  palace <ID>     查看单个宫位 (1-9)
  balance         查看阴阳平衡状态
  load <ID> <值>  更新宫位负载 (值：0.0-1.0)
  mode <yang|yin> 切换模式
  zhengzhuan <节点> <值>  正转操作
  fanzhuan <节点>       反转操作
  five-elements   五行状态
  reset           重置引擎
  help            显示帮助

九宫格布局:
  4-品牌战略  9-行业生态  2-产品质量
  3-技术团队  5-中央控制  7-法务框架
  8-营销客服  1-数据采集  6-物联监控

示例:
  $0 status
  $0 palaces
  $0 load 5 0.8
  $0 mode yang
EOF
}

api_get() {
    curl -s "$TAIJI_API$1" | python3 -m json.tool 2>/dev/null || curl -s "$TAIJI_API$1"
}

api_post() {
    curl -s -X POST "$TAIJI_API$1" -H "Content-Type: application/json" -d "$2" | python3 -m json.tool 2>/dev/null || curl -s -X POST "$TAIJI_API$1" -H "Content-Type: application/json" -d "$2"
}

case "$1" in
    status)
        echo "=== 太极系统状态 ==="
        api_get "/api/state"
        ;;
    palaces)
        echo "=== 九宫格状态 ==="
        api_get "/api/taiji/palaces"
        ;;
    palace)
        if [ -z "$2" ]; then
            echo "错误：请指定宫位 ID (1-9)"
            exit 1
        fi
        api_get "/api/taiji/palace/$2"
        ;;
    balance)
        echo "=== 阴阳平衡状态 ==="
        api_get "/api/taiji/balance"
        ;;
    load)
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo "错误：用法：$0 load <宫位 ID> <负载值>"
            exit 1
        fi
        api_post "/api/taiji/update-palace-load" "{\"palace_id\": $2, \"load\": $3}"
        ;;
    mode)
        if [ -z "$2" ]; then
            echo "错误：请指定模式 (yang|yin)"
            exit 1
        fi
        api_post "/api/taiji/switch-mode" "{\"mode\": \"$2\"}"
        ;;
    zhengzhuan)
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo "错误：用法：$0 zhengzhuan <节点 ID> <值>"
            exit 1
        fi
        api_post "/api/zhengzhuan" "{\"node_id\": \"$2\", \"value\": $3}"
        ;;
    fanzhuan)
        if [ -z "$2" ]; then
            echo "错误：用法：$0 fanzhuan <节点 ID>"
            exit 1
        fi
        api_post "/api/fanzhuan" "{\"node_id\": \"$2\"}"
        ;;
    five-elements)
        echo "=== 五行循环状态 ==="
        api_get "/api/taiji/five-elements/status"
        ;;
    reset)
        echo "=== 重置引擎 ==="
        api_post "/api/taiji/reset-engine" "{\"reset_mode\": \"full\"}"
        ;;
    help|--help|-h|"")
        show_help
        ;;
    *)
        echo "未知命令：$1"
        show_help
        exit 1
        ;;
esac
