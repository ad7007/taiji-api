#!/bin/bash
# 配置验证脚本 - 检查必要参数是否设置正确

set -e

echo "验证 web-file-downloader 配置..."
echo "---"

ERRORS=0
WARNINGS=0

# 检查必需参数
check_required() {
    local name="$1"
    local value="$2"
    
    if [ -z "$value" ]; then
        echo "❌ 错误: $name 未设置"
        ((ERRORS++))
    else
        echo "✓ $name: $value"
    fi
}

# 检查可选参数
check_optional() {
    local name="$1"
    local value="$2"
    local default="$3"
    
    if [ -z "$value" ]; then
        echo "⚠️  警告: $name 未设置，将使用默认值: $default"
        ((WARNINGS++))
    else
        echo "✓ $name: $value"
    fi
}

# 验证路径
check_path() {
    local path="$1"
    local expanded
    expanded=$(eval echo "$path" 2>/dev/null || echo "$path")
    
    if [ -d "$expanded" ]; then
        echo "✓ 目录存在: $expanded"
    else
        echo "⚠️  警告: 目录不存在，将尝试创建: $expanded"
        ((WARNINGS++))
    fi
}

echo "【必需参数】"
check_required "TARGET_URL" "$TARGET_URL"
check_required "FILE_NAME" "$FILE_NAME"

echo ""
echo "【定位参数】"
check_optional "PAGE_ANCHOR_TEXT" "$PAGE_ANCHOR_TEXT" "'配置文件'"
check_optional "SIDEBAR_CONTAINER" "$SIDEBAR_CONTAINER" "'.ant-drawer'"
check_optional "FILE_MANAGER_BTN_TEXT" "$FILE_MANAGER_BTN_TEXT" "'文件管理'"
check_optional "FILE_TABLE_SELECTOR" "$FILE_TABLE_SELECTOR" "'.ant-modal table'"
check_optional "DOWNLOAD_OP_INDEX" "$DOWNLOAD_OP_INDEX" "0"

echo ""
echo "【输出配置】"
check_optional "OUTPUT_DIR" "$OUTPUT_DIR" "~/Downloads"
check_optional "TASK_NAME" "$TASK_NAME" "'download'"
check_path "${OUTPUT_DIR:-~/Downloads}"

echo ""
echo "---"
if [ $ERRORS -gt 0 ]; then
    echo "❌ 验证失败: 发现 $ERRORS 个错误，$WARNINGS 个警告"
    echo "请设置缺失的必需参数后再试"
    exit 1
elif [ $WARNINGS -gt 0 ]; then
    echo "⚠️  验证通过: 发现 $WARNINGS 个警告（使用默认值）"
    exit 0
else
    echo "✓ 验证通过: 所有配置正确"
    exit 0
fi
