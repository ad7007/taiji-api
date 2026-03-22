#!/bin/bash
# 快速配置向导 - 交互式帮助用户配置新平台

set -e

echo "========================================"
echo "  Web File Downloader - 配置向导"
echo "========================================"
echo ""

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 收集用户输入
read -p "目标平台URL (例如: https://a.taiji.woa.com): " TARGET_URL

if [ -z "$TARGET_URL" ]; then
    echo -e "${RED}错误: URL不能为空${NC}"
    exit 1
fi

echo ""
echo "正在检测平台类型..."
echo "---"

# 尝试自动检测
PLATFORM="unknown"
if [[ "$TARGET_URL" == *"taiji.woa.com"* ]]; then
    PLATFORM="taiji"
    echo -e "${GREEN}✓ 检测到: 太极平台${NC}"
elif [[ "$TARGET_URL" == *"console.cloud.tencent.com"* ]]; then
    PLATFORM="tencent"
    echo -e "${GREEN}✓ 检测到: 腾讯云控制台${NC}"
elif [[ "$TARGET_URL" == *"console.aliyun.com"* ]]; then
    PLATFORM="aliyun"
    echo -e "${GREEN}✓ 检测到: 阿里云控制台${NC}"
elif [[ "$TARGET_URL" == *"console.aws.amazon.com"* ]]; then
    PLATFORM="aws"
    echo -e "${GREEN}✓ 检测到: AWS 控制台${NC}"
elif [[ "$TARGET_URL" == *"cloud.google.com"* ]]; then
    PLATFORM="gcp"
    echo -e "${GREEN}✓ 检测到: Google Cloud${NC}"
else
    echo -e "${YELLOW}⚠ 未知平台，需要手动配置${NC}"
fi

echo ""
read -p "要下载的文件名: " FILE_NAME

if [ -z "$FILE_NAME" ]; then
    echo -e "${RED}错误: 文件名不能为空${NC}"
    exit 1
fi

read -p "任务名称 (用于生成目录名): [${FILE_NAME%.*}] " TASK_NAME
TASK_NAME="${TASK_NAME:-${FILE_NAME%.*}}"

echo ""
echo "========================================"
echo "  配置页面元素定位参数"
echo "========================================"
echo ""

# 根据平台预设默认值
case "$PLATFORM" in
    taiji)
        DEFAULT_ANCHOR="配置文件"
        DEFAULT_SIDEBAR=".ant-drawer"
        DEFAULT_BTN="文件管理"
        DEFAULT_TABLE=".ant-modal table"
        DEFAULT_OP="0"
        ;;
    tencent)
        DEFAULT_ANCHOR="下载配置"
        DEFAULT_SIDEBAR=".tc-dialog"
        DEFAULT_BTN="导出"
        DEFAULT_TABLE=".tc-table"
        DEFAULT_OP="0"
        ;;
    aliyun)
        DEFAULT_ANCHOR="下载"
        DEFAULT_SIDEBAR=".next-dialog"
        DEFAULT_BTN="下载配置"
        DEFAULT_TABLE=".next-table"
        DEFAULT_OP="0"
        ;;
    aws)
        DEFAULT_ANCHOR="Download"
        DEFAULT_SIDEBAR=".awsui-modal"
        DEFAULT_BTN="Download"
        DEFAULT_TABLE=".awsui-table"
        DEFAULT_OP="0"
        ;;
    gcp)
        DEFAULT_ANCHOR="Download"
        DEFAULT_SIDEBAR=".p6n-modal"
        DEFAULT_BTN="Download"
        DEFAULT_TABLE=".p6n-table"
        DEFAULT_OP="0"
        ;;
    *)
        DEFAULT_ANCHOR=""
        DEFAULT_SIDEBAR=""
        DEFAULT_BTN=""
        DEFAULT_TABLE=""
        DEFAULT_OP="0"
        ;;
esac

read -p "页面文本锚点 (用于确认页面加载) [$DEFAULT_ANCHOR]: " PAGE_ANCHOR
PAGE_ANCHOR="${PAGE_ANCHOR:-$DEFAULT_ANCHOR}"

read -p "侧边栏容器选择器 [$DEFAULT_SIDEBAR]: " SIDEBAR_CONTAINER
SIDEBAR_CONTAINER="${SIDEBAR_CONTAINER:-$DEFAULT_SIDEBAR}"

read -p "文件管理按钮文本 [$DEFAULT_BTN]: " FILE_MANAGER_BTN
FILE_MANAGER_BTN="${FILE_MANAGER_BTN:-$DEFAULT_BTN}"

read -p "文件表格选择器 [$DEFAULT_TABLE]: " FILE_TABLE
FILE_TABLE="${FILE_TABLE:-$DEFAULT_TABLE}"

read -p "下载按钮在操作列中的索引 [$DEFAULT_OP]: " OP_INDEX
OP_INDEX="${OP_INDEX:-$DEFAULT_OP}"

echo ""
read -p "输出目录 [~/Downloads]: " OUTPUT_DIR
OUTPUT_DIR="${OUTPUT_DIR:-~/Downloads}"

echo ""
echo "========================================"
echo "  配置完成"
echo "========================================"
echo ""

# 生成配置输出
echo "【环境变量配置】"
echo "复制以下命令到你的 shell:"
echo ""
echo "export TARGET_URL=\"$TARGET_URL\""
echo "export FILE_NAME=\"$FILE_NAME\""
echo "export TASK_NAME=\"$TASK_NAME\""
echo "export PAGE_ANCHOR_TEXT=\"$PAGE_ANCHOR\""
echo "export SIDEBAR_CONTAINER=\"$SIDEBAR_CONTAINER\""
echo "export FILE_MANAGER_BTN_TEXT=\"$FILE_MANAGER_BTN\""
echo "export FILE_TABLE_SELECTOR=\"$FILE_TABLE\""
echo "export DOWNLOAD_OP_INDEX=\"$OP_INDEX\""
echo "export OUTPUT_DIR=\"$OUTPUT_DIR\""
echo ""

# 生成配置文件
CONFIG_FILE="$HOME/.web-file-downloader-configs/${PLATFORM}_${TASK_NAME}.sh"
mkdir -p "$HOME/.web-file-downloader-configs"

cat > "$CONFIG_FILE" << EOF
#!/bin/bash
# 自动生成的配置 - $(date)
# 平台: $PLATFORM

export TARGET_URL="$TARGET_URL"
export FILE_NAME="$FILE_NAME"
export TASK_NAME="$TASK_NAME"
export PAGE_ANCHOR_TEXT="$PAGE_ANCHOR"
export SIDEBAR_CONTAINER="$SIDEBAR_CONTAINER"
export FILE_MANAGER_BTN_TEXT="$FILE_MANAGER_BTN"
export FILE_TABLE_SELECTOR="$FILE_TABLE"
export DOWNLOAD_OP_INDEX="$OP_INDEX"
export OUTPUT_DIR="$OUTPUT_DIR"

echo "配置已加载: $PLATFORM - $TASK_NAME"
EOF

chmod +x "$CONFIG_FILE"

echo "【配置文件】"
echo "配置已保存到: $CONFIG_FILE"
echo "加载方式: source $CONFIG_FILE"
echo ""

# 询问是否立即验证
echo "========================================"
read -p "是否立即验证配置? (y/n): " VERIFY

if [ "$VERIFY" == "y" ] || [ "$VERIFY" == "Y" ]; then
    echo ""
    echo "正在验证配置..."
    echo "---"
    
    # 导出变量供验证脚本使用
    export TARGET_URL FILE_NAME TASK_NAME PAGE_ANCHOR_TEXT \
           SIDEBAR_CONTAINER FILE_MANAGER_BTN_TEXT \
           FILE_TABLE_SELECTOR DOWNLOAD_OP_INDEX OUTPUT_DIR
    
    bash "$(dirname "$0")/validate_config.sh"
fi

echo ""
echo -e "${GREEN}✓ 配置向导完成${NC}"
echo ""
echo "下一步:"
echo "  1. 在浏览器中打开目标页面"
echo "  2. 加载配置: source $CONFIG_FILE"
echo "  3. 运行下载流程"
echo ""
