#!/bin/bash
# 太极系统安装验证脚本

echo "=== 太极系统安装验证 ==="
echo ""

# 检查Python依赖
echo "【Python依赖】"
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "  ✅ 虚拟环境已创建"
    pip list | grep -E "fastapi|uvicorn|requests" > /dev/null && echo "  ✅ 核心依赖已安装" || echo "  ❌ 缺少依赖"
else
    echo "  ❌ 虚拟环境未创建"
fi

echo ""
echo "【宫位智能体配置】"
for i in 1 2 3 4 6 7 8 9; do
    if [ -f "$HOME/.openclaw/agents/palace-$i/agent/agent.json" ]; then
        name=$(grep displayName "$HOME/.openclaw/agents/palace-$i/agent/agent.json" | cut -d'"' -f4)
        echo "  ✅ $name"
    else
        echo "  ❌ $i宫 未配置"
    fi
done

echo ""
echo "【Skill同步】"
if [ -d "$HOME/.openclaw/workspace/skills/taiji-nine-palaces" ]; then
    count=$(find "$HOME/.openclaw/workspace/skills/taiji-nine-palaces" -name "*.py" | wc -l)
    echo "  ✅ taiji-nine-palaces ($count 个Python文件)"
else
    echo "  ❌ Skill未同步"
fi

echo ""
echo "【API服务】"
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "  ✅ API服务运行中"
else
    echo "  ❌ API服务未启动"
fi

echo ""
echo "验证完成！"
