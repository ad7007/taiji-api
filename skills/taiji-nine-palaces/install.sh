#!/bin/bash
# 太极系统安装脚本
# 安装时自动替换主 workspace 的标准文件

set -e

WORKSPACE="$HOME/.openclaw/workspace"
TAIJI_SKILL="$WORKSPACE/skills/taiji-nine-palaces"
TEMPLATES="$TAIJI_SKILL/templates"

echo "🎯 太极系统安装中..."

# ==================== 1. 备份原有文件 ====================

echo ""
echo "📦 步骤 1/5: 备份原有文件"

if [ -f "$WORKSPACE/IDENTITY.md" ]; then
    cp "$WORKSPACE/IDENTITY.md" "$WORKSPACE/IDENTITY.md.backup"
    echo "  ✓ 已备份 IDENTITY.md"
fi

if [ -f "$WORKSPACE/SKILL.md" ]; then
    cp "$WORKSPACE/SKILL.md" "$WORKSPACE/SKILL.md.backup"
    echo "  ✓ 已备份 SKILL.md"
fi

if [ -f "$WORKSPACE/RELATIONSHIP.md" ]; then
    cp "$WORKSPACE/RELATIONSHIP.md" "$WORKSPACE/RELATIONSHIP.md.backup"
    echo "  ✓ 已备份 RELATIONSHIP.md"
fi

if [ -f "$WORKSPACE/GOVERNANCE.md" ]; then
    cp "$WORKSPACE/GOVERNANCE.md" "$WORKSPACE/GOVERNANCE.md.backup"
    echo "  ✓ 已备份 GOVERNANCE.md"
fi

# ==================== 2. 替换身份文件 ====================

echo ""
echo "📝 步骤 2/5: 写入米珞身份（5宫主控）"

cp "$TEMPLATES/IDENTITY.md" "$WORKSPACE/IDENTITY.md"
echo "  ✓ 已写入 IDENTITY.md"

cp "$TEMPLATES/SKILL.md" "$WORKSPACE/SKILL.md"
echo "  ✓ 已写入 SKILL.md"

cp "$TEMPLATES/RELATIONSHIP.md" "$WORKSPACE/RELATIONSHIP.md"
echo "  ✓ 已写入 RELATIONSHIP.md（太极关系图）"

cp "$TEMPLATES/GOVERNANCE.md" "$WORKSPACE/GOVERNANCE.md"
echo "  ✓ 已写入 GOVERNANCE.md（管控体系）"

# ==================== 3. 创建8个宫位智能体 ====================

echo ""
echo "🤖 步骤 3/5: 创建8个宫位智能体"

for i in 1 2 3 4 6 7 8 9; do
    AGENT_ID="palace-$i"
    
    if openclaw agents list 2>/dev/null | grep -q "$AGENT_ID"; then
        echo "  ✓ $AGENT_ID 已存在，跳过"
    else
        mkdir -p "$HOME/.openclaw/workspaces/$AGENT_ID"
        
        openclaw agents add "$AGENT_ID" \
            --workspace "$HOME/.openclaw/workspaces/$AGENT_ID" \
            --model qwencode/glm-5 \
            --non-interactive 2>/dev/null || true
        
        echo "  ✓ 已创建 $AGENT_ID"
    fi
done

# ==================== 4. 部署各宫 SKILL.md ====================

echo ""
echo "📋 步骤 4/5: 部署各宫 SKILL.md"

for i in 1 2 3 4 6 7 8 9; do
    SRC="$TAIJI_SKILL/palaces/palace_${i}_skill.md"
    DST="$HOME/.openclaw/workspaces/palace-$i/SKILL.md"
    
    if [ -f "$SRC" ]; then
        cp "$SRC" "$DST"
        echo "  ✓ 已部署 palace-$i/SKILL.md"
    fi
done

# ==================== 5. 激活太极 API ====================

echo ""
echo "⚡ 步骤 5/5: 激活太极 API"

curl -s -X POST http://localhost:8000/api/taiji/update-palace-load \
    -H "Content-Type: application/json" \
    -d '{"palace_id": 5, "load": 0.3}' 2>/dev/null && echo "  ✓ 5宫已激活" || echo "  ⚠ 太极API未运行"

# ==================== 完成 ====================

echo ""
echo "══════════════════════════════════════════════════════"
echo "🎯 太极系统安装完成！"
echo "══════════════════════════════════════════════════════"
echo ""
echo "我是米珞，5宫主控。"
echo "指挥8个宫位：palace-1 到 palace-9"
echo ""
echo "余总的指令，我来协调。"
echo ""
echo "══════════════════════════════════════════════════════"