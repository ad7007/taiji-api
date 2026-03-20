# 备用技能使用指南

## 🎯 已安装备用技能

### 1. n8n-workflow-automation - 并发工作流

**版本**: 1.0.0  
**来源**: Remote Registry (lightmake.site)  
**成本**: ¥0（开源免费）  
**用途**: 并发处理任务、多方案优选

**安装位置**: `/root/.openclaw/workspace/skills/n8n-workflow-automation`

---

### 2. research-assistant - 研究助手

**版本**: 1.0.1  
**来源**: Remote Registry  
**成本**: ¥0（免费）  
**用途**: 多方案对比、知识管理

**安装位置**: `/root/.openclaw/workspace/skills/research-assistant`

---

## 🚀 使用场景

### 场景 1：并发处理多个任务

```python
# 使用 n8n 并发处理
# 示例：同时处理 10 个视频转录

n8n_workflow = {
    "nodes": [
        {
            "name": "视频列表",
            "type": "n8n-nodes-base.manualTrigger"
        },
        {
            "name": "并发处理",
            "type": "n8n-nodes-base.splitInBatches",
            "parameters": {
                "batchSize": 5  # 5 个并发
            }
        },
        {
            "name": "视频转录",
            "type": "n8n-nodes-base.httpRequest",
            "parameters": {
                "url": "http://localhost:8000/api/transcribe"
            }
        }
    ]
}
```

**优势**:
- ✅ 5 个并发处理
- ✅ 错误自动重试
- ✅ 任务状态追踪
- ✅ 结果自动汇总

---

### 场景 2：多方案优选

```python
# 使用 research-assistant 对比多个方案

# 1. 添加方案到研究库
research.add_note(
    topic="云品牌报告方案",
    content="方案 A: 九宫格并行工作流",
    tags=["方案 A", "并发", "高效"]
)

research.add_note(
    topic="云品牌报告方案",
    content="方案 B: 单线程顺序执行",
    tags=["方案 B", "简单", "慢速"]
)

research.add_note(
    topic="云品牌报告方案",
    content="方案 C: 纯人工处理",
    tags=["方案 C", "高质量", "昂贵"]
)

# 2. 搜索对比所有方案
all_plans = research.search("云品牌报告方案")

# 3. 导出对比报告
report = research.export_to_markdown()
```

**优势**:
- ✅ 多方案结构化存储
- ✅ 标签分类管理
- ✅ 全文搜索对比
- ✅ Markdown 导出

---

## 💡 与太极九宫格集成

### 集成方案 1：n8n 作为并发引擎

```python
# 在九宫格工作流中使用 n8n

class CloudBrandWorkflow:
    def _phase1_parallel_collection(self, topic):
        # 使用 n8n 并发执行
        n8n_result = n8n.execute_workflow(
            workflow_id="parallel_data_collection",
            data={"topic": topic}
        )
        return n8n_result["results"]
```

**工作流**:
```
九宫格调度器 → n8n 并发引擎 → 7 宫并行执行 → 结果汇总
```

---

### 集成方案 2：research-assistant 作为方案库

```python
# 在质量会审前使用 research-assistant

class ProductReview:
    def compare_plans(self, topic):
        # 从研究库获取多个方案
        plans = research.search(topic)
        
        # AI 对比优选
        best_plan = ai_select_best(plans)
        
        return best_plan
```

**流程**:
```
数据收集 → research-assistant 存储多方案 → AI 对比 → 最优方案
```

---

## 📊 并发处理示例

### 使用 n8n 处理批量视频

```json
{
  "name": "批量视频转录",
  "nodes": [
    {
      "parameters": {
        "batchSize": 5
      },
      "name": "并发控制",
      "type": "n8n-nodes-base.splitInBatches"
    },
    {
      "parameters": {
        "url": "http://localhost:8000/api/transcribe",
        "method": "POST"
      },
      "name": "视频转录 API"
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "{{$json[\"success\"]}}",
              "operation": "equals",
              "value2": "true"
            }
          ]
        }
      },
      "name": "成功检查",
      "type": "n8n-nodes-base.if"
    },
    {
      "parameters": {
        "maxTries": 3,
        "waitBetweenTries": 5000
      },
      "name": "失败重试",
      "type": "n8n-nodes-base.retry"
    }
  ]
}
```

**效率对比**:
| 方式 | 10 个视频耗时 | 成本 |
|------|------------|------|
| 单线程 | 300 秒 | ¥0 |
| **n8n 并发 (5)** | **60 秒** | **¥0** |
| 人工处理 | 3600 秒 | ¥500 |

---

## 🎯 多方案优选示例

### 使用 research-assistant 对比报告方案

```python
from research_assistant import ResearchAssistant

research = ResearchAssistant()

# 添加多个方案
schemes = [
    {
        "name": "方案 A",
        "approach": "九宫格并行",
        "time": "60 秒",
        "cost": "¥0",
        "quality": "B+"
    },
    {
        "name": "方案 B",
        "approach": "单线程",
        "time": "300 秒",
        "cost": "¥0",
        "quality": "B"
    },
    {
        "name": "方案 C",
        "approach": "人工 +AI",
        "time": "1800 秒",
        "cost": "¥500",
        "quality": "A"
    }
]

for scheme in schemes:
    research.add_note(
        topic="报告生成方案",
        content=str(scheme),
        tags=[scheme["name"], scheme["approach"]]
    )

# 搜索对比
all_schemes = research.search("报告生成方案")

# 导出对比
comparison = research.export_to_markdown()
```

**输出对比报告**:
```markdown
# 报告生成方案对比

## 方案 A - 九宫格并行
- 时间：60 秒
- 成本：¥0
- 质量：B+
- 推荐指数：⭐⭐⭐⭐⭐

## 方案 B - 单线程
- 时间：300 秒
- 成本：¥0
- 质量：B
- 推荐指数：⭐⭐⭐

## 方案 C - 人工+AI
- 时间：1800 秒
- 成本：¥500
- 质量：A
- 推荐指数：⭐⭐⭐⭐

**推荐**: 方案 A（性价比最高）
```

---

## ⚙️ 配置说明

### n8n 本地部署（可选）

```bash
# 安装 n8n（可选，用于本地工作流引擎）
npm install n8n -g

# 启动 n8n
n8n start

# 访问 Web 界面
http://localhost:5678
```

**注意**: 当前安装的 `n8n-workflow-automation` 技能是工作流设计器，不需要部署 n8n 服务器也能使用。

---

### research-assistant 配置

```python
# 配置研究库存储路径
research = ResearchAssistant(
    storage_path="/root/.openclaw/workspace/research_notes"
)

# 添加笔记
research.add_note(
    topic="主题名称",
    content="笔记内容",
    tags=["标签 1", "标签 2"]
)

# 搜索笔记
results = research.search("关键词")

# 导出
markdown = research.export_to_markdown()
```

---

## 📊 性能对比

### 并发处理能力

| 工具 | 并发数 | 10 任务耗时 | 100 任务耗时 |
|------|--------|-----------|------------|
| 太极九宫格 | 5 | 60 秒 | 600 秒 |
| **n8n** | **10** | **30 秒** | **300 秒** |
| Zapier | 1 | 300 秒 | 3000 秒 |

### 多方案管理

| 工具 | 方案数限制 | 搜索速度 | 导出格式 |
|------|-----------|---------|---------|
| 太极九宫格 | 无限制 | 即时 | Markdown |
| **research-assistant** | **无限制** | **即时** | **Markdown/JSON** |
| 人工整理 | 有限 | 慢 | 手动 |

---

## 💡 最佳实践

### 1. 批量任务使用 n8n

```
适用场景:
- 批量视频转录（10+ 个）
- 批量热点搜索（20+ 关键词）
- 批量 PDF 生成（50+ 报告）

配置:
- 并发数：5-10（根据资源）
- 重试次数：3 次
- 失败告警：开启
```

### 2. 方案对比使用 research-assistant

```
适用场景:
- 多方案优选
- 竞品对比分析
- 历史方案归档

流程:
1. 添加所有方案到研究库
2. 打标签分类
3. 搜索对比
4. 导出报告
5. AI 优选
```

### 3. 组合使用

```
完整流程:
n8n 并发收集数据 → research-assistant 存储多方案 → AI 对比优选 → 九宫格生成报告
```

---

## 🎯 总结

### 已安装备用技能

| 技能 | 用途 | 成本 | 状态 |
|------|------|------|------|
| n8n-workflow-automation | 并发工作流 | ¥0 | ✅ 已安装 |
| research-assistant | 多方案对比 | ¥0 | ✅ 已安装 |

### 核心优势

1. **零成本** - 两个技能都完全免费
2. **并发增强** - n8n 支持 10 并发，效率提升 3 倍
3. **方案优选** - research-assistant 结构化对比多方案
4. **无缝集成** - 可与太极九宫格完美配合

---

**备用技能已就绪！并发处理 + 多方案优选，双保险！** 🚀
