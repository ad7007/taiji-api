# 免费模型插件使用指南

## 🎯 插件架构

```
太极系统（内部）
    ↓
插件接口层（隔离）
    ↓
免费模型（智谱/DeepSeek）
```

**特点**:
- ✅ 独立插件，不影响内部系统
- ✅ 按需加载，避免依赖冲突
- ✅ 统一接口，方便切换

---

## 📦 安装

### 1. 安装依赖

```bash
# 智谱 AI
pip install zhipuai

# DeepSeek（兼容 OpenAI）
pip install openai
```

### 2. 获取 API Key

**智谱 AI**:
1. 访问：https://open.bigmodel.cn/
2. 注册/登录
3. 创建 API Key

**DeepSeek**:
1. 访问：https://platform.deepseek.com/
2. 注册/登录
3. 创建 API Key

### 3. 配置 API Key

**方式 1：环境变量**
```bash
export ZHIPU_API_KEY="your_zhipu_key"
export DEEPSEEK_API_KEY="your_deepseek_key"
```

**方式 2：配置文件**
```bash
# 创建配置文件
mkdir -p ~/.openclaw/plugins
cat > ~/.openclaw/plugins/free_models.json << EOF
{
  "zhipu_api_key": "your_zhipu_key",
  "deepseek_api_key": "your_deepseek_key",
  "default_model": "glm-4-flash",
  "enable_zhipu": true,
  "enable_deepseek": true
}
EOF
```

---

## 🚀 使用方法

### 方式 1：直接调用插件

```python
from plugins.free_models_plugin import FreeModelsPlugin

# 初始化插件
plugin = FreeModelsPlugin()

# 内容生成
result = plugin.generate("请生成云品牌服务报告", model="glm-4-flash")
print(f"内容：{result['content']}")
print(f"成本：¥{result['cost']}")  # ¥0.00

# 代码生成
code = plugin.code_generate("写个快速排序", language="python")
print(f"代码：{code['content']}")
```

### 方式 2：使用快捷接口

```python
from plugins.free_models_plugin import generate_content, generate_code

# 内容生成
result = generate_content("请生成报告", model="glm-4-flash")

# 代码生成
code = generate_code("数据处理脚本", language="python")
```

### 方式 3：动态设置 API Key

```python
from plugins.free_models_plugin import FreeModelsPlugin

plugin = FreeModelsPlugin()

# 设置 API Key
plugin.set_api_key("zhipu", "your_zhipu_key")
plugin.set_api_key("deepseek", "your_deepseek_key")

# 使用
result = plugin.generate("你好")
```

---

## 📊 可用模型

| 模型 | 提供商 | 免费额度 | 用途 | 推荐度 |
|------|--------|---------|------|--------|
| **glm-4-flash** | 智谱 | 100 万/月 | 内容生成 | ⭐⭐⭐⭐⭐ |
| **glm-4-air** | 智谱 | 50 万/月 | 高质量内容 | ⭐⭐⭐⭐⭐ |
| **deepseek-chat** | DeepSeek | 100 万/月 | 通用任务 | ⭐⭐⭐⭐⭐ |
| **deepseek-coder** | DeepSeek | 100 万/月 | 代码生成 | ⭐⭐⭐⭐⭐ |

---

## 💡 使用场景

### 场景 1：内容生成（替代 qwen-max）

```python
from plugins.free_models_plugin import generate_content

# 生成报告
report = generate_content(
    "请生成云品牌服务报告，包含 9 种盈利业务形态",
    model="glm-4-flash"  # 免费！
)

# 保存
with open("report.md", "w") as f:
    f.write(report["content"])

# 成本：¥0.00（原 qwen-max: ¥0.18）
```

### 场景 2：代码生成（替代付费模型）

```python
from plugins.free_models_plugin import generate_code

# 生成代码
code = generate_code(
    "数据处理脚本，读取 CSV 并生成统计报告",
    language="python"
)

# 保存
with open("data_processor.py", "w") as f:
    f.write(code["content"])

# 成本：¥0.00（原付费模型：¥0.12）
```

### 场景 3：批量处理（零成本）

```python
from plugins.free_models_plugin import FreeModelsPlugin

plugin = FreeModelsPlugin()

# 批量生成 100 份报告
for i in range(100):
    result = plugin.generate(
        f"生成第{i+1}份报告",
        model="glm-4-flash"
    )
    
    # 保存
    with open(f"report_{i+1}.md", "w") as f:
        f.write(result["content"])

# 总成本：¥0.00（100 份报告）
# 原成本：¥18.00（qwen-max）
```

---

## 🔧 配置选项

### 配置文件位置
`~/.openclaw/plugins/free_models.json`

### 配置项

```json
{
  "enable_zhipu": true,          // 启用智谱 AI
  "enable_deepseek": true,       // 启用 DeepSeek
  "zhipu_api_key": "xxx",        // 智谱 API Key
  "deepseek_api_key": "xxx",     // DeepSeek API Key
  "default_model": "glm-4-flash", // 默认模型
  "fallback_chain": [            // 降级链
    "glm-4-flash",
    "deepseek-chat",
    "glm-4-air"
  ]
}
```

---

## 📈 性能对比

### 内容生成

| 模型 | 免费额度 | 性能 | 成本 |
|------|---------|------|------|
| **glm-4-flash** | 100 万/月 | ⭐⭐⭐⭐ | ¥0.00 |
| **deepseek-chat** | 100 万/月 | ⭐⭐⭐⭐⭐ | ¥0.00 |
| qwen-max | 10 万/月 | ⭐⭐⭐⭐⭐ | ¥0.04/1K |
| Kimi2.5 | 免费额度 | ⭐⭐⭐⭐ | ¥0.012/1K |

### 代码生成

| 模型 | 免费额度 | 性能 | 成本 |
|------|---------|------|------|
| **deepseek-coder** | 100 万/月 | ⭐⭐⭐⭐⭐ | ¥0.00 |
| qwen-coder | 10 万/月 | ⭐⭐⭐⭐⭐ | ¥0.04/1K |

---

## ⚠️ 注意事项

### 1. 依赖隔离

```bash
# 插件依赖（独立安装）
pip install zhipuai openai

# 不影响主系统依赖
# 主系统继续使用原有模型
```

### 2. API Key 安全

```bash
# 不要将 API Key 提交到代码库
# 使用配置文件或环境变量
~/.openclaw/plugins/free_models.json  # 加入.gitignore
```

### 3. 免费额度

| 平台 | 免费额度 | 可生成报告数 |
|------|---------|------------|
| 智谱 | 100 万/月 | ~10,000 份 |
| DeepSeek | 100 万/月 | ~10,000 份 |
| **总计** | **200 万/月** | **~20,000 份** |

---

## 🎯 集成到工作流

### v4 工作流（插件版）

```python
# tasks/cloud_brand_v4_plugin.py
from plugins.free_models_plugin import FreeModelsPlugin

# 使用插件生成报告
plugin = FreeModelsPlugin()

# 内容生成（免费）
report = plugin.generate(
    "请生成云品牌服务报告",
    model="glm-4-flash"
)

# 总成本：¥0.00
```

### 与现有系统集成

```python
# 不修改现有代码，通过插件调用
from plugins.free_models_plugin import generate_content

# 现有系统继续使用原有模型
# 新任务使用免费插件

def generate_report_v2(topic: str):
    # 使用免费插件
    return generate_content(f"生成{topic}报告")
```

---

## 📁 文件结构

```
plugins/
├── free_models_plugin.py      # 插件主模块
├── README.md                   # 使用文档
└── __init__.py                 # 插件包

~/.openclaw/plugins/
└── free_models.json            # 配置文件
```

---

## 🚀 快速开始

```bash
# 1. 安装依赖
pip install zhipuai openai

# 2. 获取 API Key
# https://open.bigmodel.cn/
# https://platform.deepseek.com/

# 3. 配置
export ZHIPU_API_KEY="your_key"
export DEEPSEEK_API_KEY="your_key"

# 4. 测试
cd /root/.openclaw/workspace/skills/taiji-nine-palaces/plugins
python3 free_models_plugin.py

# 5. 使用
python3 -c "
from plugins.free_models_plugin import generate_content
result = generate_content('你好')
print(result['content'])
"
```

---

## 💰 成本对比

### 月处理 3000 次

| 方案 | 成本 | 说明 |
|------|------|------|
| **插件（免费）** | **¥0** | 智谱+DeepSeek |
| qwen-max | ¥540 | 付费模型 |
| Kimi2.5 | ¥378 | 付费模型 |
| **总计** | **¥918/月** | 可省 |

**年节省**: ¥11,016

---

**插件已就绪！独立插件层，不影响内部系统，100% 零成本！** 🚀
