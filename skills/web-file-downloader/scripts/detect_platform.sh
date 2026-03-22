#!/bin/bash
# 平台检测脚本 - 自动识别当前页面所属平台类型

set -e

URL="${1:-$(browser.currentUrl 2>/dev/null || echo '')}"

if [ -z "$URL" ]; then
    echo "错误: 无法获取当前URL"
    echo "用法: $0 <url>"
    exit 1
fi

echo "检测平台: $URL"
echo "---"

# 平台识别规则
detect_platform() {
    local url="$1"
    
    case "$url" in
        *"taiji.woa.com"*)
            echo "平台: 太极 (Tencent Taiji)"
            echo "配置:"
            echo "  ANCHOR_TEXT='配置文件'"
            echo "  SIDEBAR='.ant-drawer'"
            echo "  FILE_BTN='文件管理'"
            echo "  TABLE='.ant-modal table'"
            echo "  OP_INDEX=0"
            ;;
        *"console.cloud.tencent.com"*)
            echo "平台: 腾讯云控制台"
            echo "配置:"
            echo "  ANCHOR_TEXT='下载配置'"
            echo "  SIDEBAR='.tc-dialog'"
            echo "  FILE_BTN='导出'"
            echo "  TABLE='.tc-table'"
            echo "  OP_INDEX=0"
            ;;
        *"console.aliyun.com"*)
            echo "平台: 阿里云控制台"
            echo "配置:"
            echo "  ANCHOR_TEXT='下载'"
            echo "  SIDEBAR='.next-dialog'"
            echo "  FILE_BTN='下载配置'"
            echo "  TABLE='.next-table'"
            echo "  OP_INDEX=0"
            ;;
        *"console.aws.amazon.com"*)
            echo "平台: AWS 控制台"
            echo "配置:"
            echo "  ANCHOR_TEXT='Download'"
            echo "  SIDEBAR='.awsui-modal'"
            echo "  FILE_BTN='Download'"
            echo "  TABLE='.awsui-table'"
            echo "  OP_INDEX=0"
            ;;
        *"cloud.google.com"*)
            echo "平台: Google Cloud 控制台"
            echo "配置:"
            echo "  ANCHOR_TEXT='Download'"
            echo "  SIDEBAR='.p6n-modal'"
            echo "  FILE_BTN='Download'"
            echo "  TABLE='.p6n-table'"
            echo "  OP_INDEX=0"
            ;;
        *)
            echo "平台: 未知 (需要手动配置)"
            echo "建议:"
            echo "  1. 打开浏览器开发者工具 (F12)"
            echo "  2. 找到文件管理区域的 CSS 选择器"
            echo "  3. 查看 SKILL.md 中的'平台适配示例'章节"
            ;;
    esac
}

detect_platform "$URL"
