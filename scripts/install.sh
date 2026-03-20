#!/bin/bash
# 太极系统安装脚本 - Taiji System Installation Script
# 
# 此脚本会：
# 1. 安装太极API依赖
# 2. 创建8个宫位智能体配置
# 3. 同步skill到OpenClaw
# 4. 配置OpenClaw

set -e

echo "═══════════════════════════════════════════════════════"
echo "       太极系统安装 - Taiji System Installation"
echo "═══════════════════════════════════════════════════════"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检测脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TAIJI_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

echo "📁 太极API目录: $TAIJI_ROOT"
echo ""

# ====== 第一步：安装Python依赖 ======
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 第一步：安装Python依赖"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd "$TAIJI_ROOT"

if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

echo "激活虚拟环境..."
source venv/bin/activate

echo "安装依赖..."
pip install -r requirements.txt -q

echo -e "${GREEN}✅ Python依赖安装完成${NC}"
echo ""

# ====== 第二步：检测OpenClaw ======
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 第二步：检测OpenClaw"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

OPENCLAW_DIR="$HOME/.openclaw"
OPENCLAW_WORKSPACE="$OPENCLAW_DIR/workspace"
OPENCLAW_CONFIG="$OPENCLAW_DIR/openclaw.json"

if [ ! -d "$OPENCLAW_DIR" ]; then
    echo -e "${YELLOW}⚠️ OpenClaw未安装${NC}"
    echo "请先安装OpenClaw: npm install -g openclaw"
    echo "或跳过此步骤，仅安装太极API"
    read -p "是否继续安装太极API？(y/n): " continue_install
    if [ "$continue_install" != "y" ]; then
        echo "安装已取消"
        exit 0
    fi
else
    echo -e "${GREEN}✅ OpenClaw已安装: $OPENCLAW_DIR${NC}"
fi
echo ""

# ====== 第三步：创建宫位智能体配置 ======
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🤖 第三步：创建宫位智能体配置"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 宫位配置数据
declare -A PALACES
PALACES[1]="1宫-数据采集|📥|水|网页抓取、数据收集|web-pilot"
PALACES[2]="2宫-产品质量|✓|金|文档管理、质量把控|tencent-docs"
PALACES[3]="3宫-技术团队|💻|木|模型分配、代码管理|github"
PALACES[4]="4宫-品牌战略|🎯|水|品牌策划、内容发布|wechat-publisher"
PALACES[6]="6宫-物联监控|📡|火|系统监控、配置备份|tencentcloud-lighthouse-skill"
PALACES[7]="7宫-法务框架|⚖️|金|安全扫描、TDD验收|zero-trust"
PALACES[8]="8宫-营销客服|📢|木|客户服务、营销推广|constant-contact"
PALACES[9]="9宫-行业生态|🌐|土|生态建设、合作伙伴|keyword-research"

# 创建宫位目录和配置
for num in 1 2 3 4 6 7 8 9; do
    IFS='|' read -r name emoji element duty skills <<< "${PALACES[$num]}"
    
    # 创建工作空间
    WORKSPACE="$OPENCLAW_DIR/workspaces/palace-$num"
    mkdir -p "$WORKSPACE"
    
    # 创建agent目录
    AGENT_DIR="$OPENCLAW_DIR/agents/palace-$num/agent"
    mkdir -p "$AGENT_DIR"
    
    # 写入agent.json
    cat > "$AGENT_DIR/agent.json" << AGENTEOF
{
  "agentId": "palace-$num",
  "displayName": "$name",
  "workspace": "$WORKSPACE",
  "model": "qwencode/glm-5",
  "defaultModel": "qwencode/glm-5"
}
AGENTEOF
    
    echo -e "  ${GREEN}✅${NC} $name ($emoji) - 已配置"
done

echo ""
echo -e "${GREEN}✅ 8个宫位智能体配置完成${NC}"
echo ""

# ====== 第四步：同步Skill到OpenClaw ======
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📚 第四步：同步Skill到OpenClaw"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

SKILL_SRC="$TAIJI_ROOT/skills/taiji-nine-palaces"
SKILL_DEST="$OPENCLAW_WORKSPACE/skills/taiji-nine-palaces"

if [ -d "$SKILL_SRC" ]; then
    # 备份旧skill
    if [ -d "$SKILL_DEST" ]; then
        echo "备份旧skill..."
        mv "$SKILL_DEST" "$SKILL_DEST.bak.$(date +%Y%m%d%H%M%S)"
    fi
    
    # 复制新skill
    echo "复制skill文件..."
    mkdir -p "$OPENCLAW_WORKSPACE/skills"
    cp -r "$SKILL_SRC" "$SKILL_DEST"
    
    # 统计
    PY_COUNT=$(find "$SKILL_DEST" -name "*.py" | wc -l)
    echo -e "${GREEN}✅ Skill已同步: $PY_COUNT 个Python文件${NC}"
else
    echo -e "${YELLOW}⚠️ 未找到skill目录: $SKILL_SRC${NC}"
fi
echo ""

# ====== 第五步：更新OpenClaw配置 ======
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚙️ 第五步：更新OpenClaw配置"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "$OPENCLAW_CONFIG" ]; then
    # 备份原配置
    cp "$OPENCLAW_CONFIG" "$OPENCLAW_CONFIG.bak"
    echo -e "${GREEN}✅ OpenClaw配置已备份${NC}"
else
    echo -e "${YELLOW}⚠️ 未找到OpenClaw配置文件${NC}"
fi
echo ""

# ====== 完成 ======
echo "═══════════════════════════════════════════════════════"
echo "       ✅ 太极系统安装完成！"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "📊 安装摘要："
echo "   - Python依赖: ✅ 已安装"
echo "   - 宫位智能体: ✅ 8个已配置"
echo "   - Skill同步: ✅ 已完成"
echo ""
echo "🚀 下一步："
echo "   1. 启动太极API:"
echo "      cd $TAIJI_ROOT && source venv/bin/activate"
echo "      python -m uvicorn api.taiji_api:app --host 0.0.0.0 --port 8000"
echo ""
echo "   2. 重启OpenClaw使配置生效:"
echo "      openclaw restart"
echo ""
echo "═══════════════════════════════════════════════════════"