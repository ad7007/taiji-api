# 3 宫 - 技术团队 · 模型分配专家

**版本**: v1.0  
**创建时间**: 2026-03-18  
**位置**: `/root/taiji-api-v2/core/palace_3_model_allocator.py`

---

## 一、核心能力

3 宫（技术团队）负责**模型分配**，根据任务类型、优先级、成本预算自动选择最优 AI 模型。

### 灵感来源

**OpenClaw Zero Token 项目**（抖音视频：https://v.douyin.com/CCgYvq4708Y/）

核心洞察:
- 浏览器自动化接管网页会话
- 零成本调用 Claude/DeepSeek/GPT/Gemini
- **API Token 模式**（付费）与 **Zero Token 模式**（免费）并行

---

## 二、两种访问模式

| 模式 | 说明 | 成本 | 质量 | 推荐场景 |
|------|------|------|------|---------|
| **API Token** | 传统 API 调用 | 付费（0.002-0.015 元/千 token） | 高 | 关键任务、高质量要求 |
| **Zero Token** | 浏览器自动化 | 免费（0 元） | 中高 | 日常任务、成本敏感 |

---

## 三、支持模型

### Zero Token 模式（免费）

| 模型 | 提供商 | 擅长领域 | 质量 | 速度 |
|------|--------|---------|------|------|
| `claude-sonnet` | Claude | 创作、对话、分析 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| `deepseek-chat` | DeepSeek | 代码、推理、数学 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| `gpt-4o` | GPT | 通用、多模态、创作 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| `gemini-pro` | Gemini | 多模态、长文本、分析 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

### API Token 模式（付费）

| 模型 | 提供商 | 擅长领域 | 成本等级 | 质量 | 速度 |
|------|--------|---------|---------|------|------|
| `qwen3.5-plus` | Qwen | 推理、代码、分析、创作 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| `qwen3.5` | Qwen | 通用、快速响应 | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| `claude-opus` | Claude | 复杂推理、代码、专业领域 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 四、任务类型与模型映射

| 任务类型 | API Token 模式 | Zero Token 模式 | 说明 |
|---------|---------------|----------------|------|
| `video_process` | qwen3.5-plus | gemini-pro | 视频摘要，多模态支持 |
| `file_download` | qwen3.5 | deepseek-chat | 简单任务 |
| `data_analysis` | qwen3.5-plus | claude-sonnet | 分析能力强 |
| `skill_install` | qwen3.5 | deepseek-chat | 代码能力强 |
| `content_create` | qwen3.5-plus | claude-sonnet | 创作能力强 |
| `monitoring` | qwen3.5 | gemini-pro | 监控任务 |
| `legal_compliance` | qwen3.5-plus | claude-sonnet | 法务严谨 |
| `general` | qwen3.5 | gpt-4o | 通用任务 |

---

## 五、API 端点

### 5.1 获取模型能力列表

```bash
GET /api/palace3/models
```

**响应**:
```json
[
  {
    "model": "claude-sonnet",
    "provider": "claude",
    "access_mode": "zero_token",
    "strengths": ["创作", "对话", "分析"],
    "cost_level": 1,
    "speed_level": 4,
    "quality_level": 5
  },
  ...
]
```

### 5.2 模式对比

```bash
GET /api/palace3/compare/{task_type}
```

**示例**:
```bash
GET /api/palace3/compare/video_process
```

**响应**:
```json
{
  "task_type": "video_process",
  "api_token": {
    "model": "qwen3.5-plus",
    "provider": "qwen",
    "cost_level": 3,
    "quality_level": 5,
    "estimated_cost": 0.008
  },
  "zero_token": {
    "model": "gemini-pro",
    "provider": "gemini",
    "cost_level": 1,
    "quality_level": 4,
    "estimated_cost": 0.0
  },
  "recommendation": "优先使用 Zero Token 模式，质量要求高时使用 API Token"
}
```

### 5.3 成本报告

```bash
GET /api/palace3/cost-report
```

**响应**:
```json
{
  "total_tasks": 10,
  "zero_token_tasks": 8,
  "api_token_tasks": 2,
  "total_estimated_cost": 0.016,
  "savings": 0.064,
  "zero_token_ratio": 0.8
}
```

---

## 六、L4 引擎集成

### 自动模型分配

当 5 宫创建任务时，自动调用 3 宫分配模型：

```bash
POST /api/l4/command
{
  "command": "分析这份销售数据"
}

Response:
{
  "task_id": "task_20260318101913",
  "priority": "MEDIUM",
  "task_type": "data_analysis",
  "assigned_palaces": [1, 3, 7, 5],
  "model_allocation": {
    "model": "claude-sonnet",
    "provider": "claude",
    "access_mode": "zero_token",
    "reason": "Zero Token 模式（浏览器自动化，免费）",
    "estimated_cost": 0.0,
    "estimated_time_seconds": 1.25
  },
  ...
}
```

---

## 七、Python 调用

### 基本用法

```python
from core.palace_3_model_allocator import palace3_allocate_model

# 分配模型
result = palace3_allocate_model(
    task_type="data_analysis",
    priority=2,  # HIGH
    budget=0.0   # 免费优先
)

print(f"推荐模型：{result['model']}")
print(f"访问模式：{result['access_mode']}")
print(f"预计成本：{result['estimated_cost']}元")
```

### 获取模型能力

```python
from core.palace_3_model_allocator import palace3_get_capabilities

models = palace3_get_capabilities()
for m in models:
    print(f"{m['model']}: {m['strengths']} - {m['access_mode']}")
```

### 模式对比

```python
from core.palace_3_model_allocator import palace3_compare_modes

comparison = palace3_compare_modes("video_process")
print(f"API Token: {comparison['api_token']['model']}")
print(f"Zero Token: {comparison['zero_token']['model']}")
print(f"建议：{comparison['recommendation']}")
```

---

## 八、优先级驱动分配

| 优先级 | 说明 | 模型选择策略 |
|--------|------|-------------|
| **CRITICAL (1)** | 紧急且重要 | 质量优先，使用最强模型 |
| **HIGH (2)** | 重要不紧急 | 质量 + 成本平衡 |
| **MEDIUM (3)** | 常规任务 | Zero Token 优先 |
| **LOW (4)** | 可延后 | 免费模型，空闲时处理 |

### 示例

```python
# CRITICAL 任务 → qwen3.5-plus（最强）
palace3_allocate_model("data_analysis", priority=1)
# → model: qwen3.5-plus, access_mode: api_token

# MEDIUM 任务 → claude-sonnet（免费最强）
palace3_allocate_model("data_analysis", priority=3)
# → model: claude-sonnet, access_mode: zero_token
```

---

## 九、成本优化策略

### 默认策略

```python
# 优先 Zero Token（免费）
allocator = Palace3ModelAllocator(prefer_zero_token=True)
```

### 成本对比

| 场景 | API Token 成本 | Zero Token 成本 | 节省 |
|------|--------------|---------------|------|
| 100 次视频摘要 | 0.80 元 | 0.00 元 | 100% |
| 100 次数据分析 | 0.80 元 | 0.00 元 | 100% |
| 100 次内容创作 | 0.80 元 | 0.00 元 | 100% |

**假设**: 平均每次任务 2000 tokens，qwen3.5-plus 0.004 元/千 token

---

## 十、与 5 宫、7 宫的协作

```
余总指令
    ↓
5 宫感知 → 任务类型、优先级
    ↓
3 宫分配 → 选择最优模型 ← 本模块
    ↓
7 宫 TDD → 定义验收标准
    ↓
1 宫执行 → 调用分配的模型
    ↓
7 宫验收 → 绿灯检查
    ↓
5 宫交付
```

---

## 十一、扩展指南

### 添加新模型

```python
# palace_3_model_allocator.py
MODEL_CAPABILITIES["new-model"] = ModelCapability(
    provider=ModelProvider.NEW_PROVIDER,
    model_name="new-model",
    access_mode=AccessMode.ZERO_TOKEN,  # 或 API_TOKEN
    strengths=["擅长领域 1", "擅长领域 2"],
    cost_level=1,  # 1-5
    speed_level=4,
    quality_level=5
)
```

### 添加新任务类型映射

```python
TASK_MODEL_MAPPING["new_task_type"] = {
    "default": "qwen3.5-plus",
    "zero_token": "claude-sonnet",
    "priority_override": {
        1: "qwen3.5-plus",  # CRITICAL
        2: "claude-sonnet", # HIGH
        3: "gpt-4o",        # MEDIUM
        4: "deepseek-chat"  # LOW
    }
}
```

---

## 十二、监控与调试

### 查看成本报告

```bash
curl http://localhost:8000/api/palace3/cost-report | jq
```

### 查看模型分配历史

```python
from core.palace_3_model_allocator import get_palace3_allocator

allocator = get_palace3_allocator()
print(allocator.allocation_history)
```

### 日志查看

```bash
# API 日志
tail -f /root/taiji-api-v2/taiji_api.log

# 搜索模型分配日志
grep "Model:" /root/taiji-api-v2/taiji_api.log
```

---

## 十三、版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-03-18 | 初始版本，集成 Zero Token 模式 |

---

**3 宫模型分配专家已就绪，支持 API Token 和 Zero Token 双模式。**

**灵感**: OpenClaw Zero Token 项目 - 浏览器自动化零成本调用主流 AI 模型
