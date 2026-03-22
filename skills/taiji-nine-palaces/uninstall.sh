#!/bin/bash
# 太极系统卸载脚本
# 恢复主 workspace 的原有身份

set -e

WORKSPACE="$HOME/.openclaw/workspace"

echo "🔄 太极系统卸载中..."

# ==================== 1. 恢复原有文件 ====================

echo ""
echo "📦 恢复原有身份文件"

if [ -f "$WORKSPACE/IDENTITY.md.backup" ]; then
    mv "$WORKSPACE/IDENTITY.md.backup" "$WORKSPACE/IDENTITY.md"
    echo "  ✓ 已恢复 IDENTITY.md"
else
    echo "  ⚠ 无 IDENTITY.md 备份，保留当前文件"
fi

if [ -f "$WORKSPACE/SKILL.md.backup" ]; then
    mv "$WORKSPACE/SKILL.md.backup" "$WORKSPACE/SKILL.md"
    echo "  ✓ 已恢复 SKILL.md"
else
    echo "  ⚠ 无 SKILL.md 备份，保留当前文件"
fi

if [ -f "$WORKSPACE/RELATIONSHIP.md.backup" ]; then
    mv "$WORKSPACE/RELATIONSHIP.md.backup" "$WORKSPACE/RELATIONSHIP.md"
    echo "  ✓ 已恢复 RELATIONSHIP.md"
else
    echo "  ⚠ 无 RELATIONSHIP.md 备份，保留当前文件"
fi

if [ -f "$WORKSPACE/GOVERNANCE.md.backup" ]; then
    mv "$WORKSPACE/GOVERNANCE.md.backup" "$WORKSPACE/GOVERNANCE.md"
    echo "  ✓ 已恢复 GOVERNANCE.md"
else
    echo "  ⚠ 无 GOVERNANCE.md 备份，保留当前文件"
fi

# ==================== 2. 更新太极 API ====================

echo ""
echo "⚡ 更新太极 API 状态"

curl -s -X POST http://localhost:8000/api/taiji/update-palace-load \
    -H "Content-Type: application/json" \
    -d '{"palace_id": 5, "load": 0.0}' 2>/dev/null && echo "  ✓ 5宫已停用" || echo "  ⚠ 太极API未运行"

# ==================== 完成 ====================

echo ""
echo "══════════════════════════════════════════════════════"
echo "✅ 太极系统已卸载"
echo "══════════════════════════════════════════════════════"
echo ""
echo "主 workspace 已恢复原有身份。"
echo "8个宫位智能体仍保留（可手动删除）。"
echo ""
echo "如需重新激活，运行："
echo "  ~/.openclaw/workspace/skills/taiji-nine-palaces/install.sh"
echo ""
echo "══════════════════════════════════════════════════════"