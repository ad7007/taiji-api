# 百炼模型智能路由系统

## 🎯 概述

基于阿里云百炼 API 的智能模型路由系统，自动选择最优模型处理各类任务，平衡成本与性能。

---

## 📊 可用模型

| 模型 | 层级 | 上下文 | 成本 (¥/1K) | 适用场景 |
|------|------|--------|-------------|----------|
| qwen-turbo | Fast | 32K | 0.002 | 简单问答、翻译、分类 |
| qwen-plus | Balanced | 32K | 0.008 | 创意写作、摘要、数据分析 |
| qwen-max | Premium | 32K | 0.04 | 复杂推理、代码审查、多步任务 |
| qwen-long | Premium | 200K | 0.06 | 超长文本、文档分析 |
| qwen-coder | Premium | 32K | 0.04 | 代码生成、代码审查、调试 |

---

## 🚀 快速开始

### 1. 配置 API Key

```bash
# 方式 1：环境变量
export DASHSCOPE_API_KEY="sk-xxx"

# 方式 2：代码中传入
from model_router import ModelRouter
router = ModelRouter(api_key="sk-xxx")
```

### 2. 基本使用

```python
from model_router import ModelRouter

router = ModelRouter()

# 自动路由
result = router.route("请帮我写一个 Python 排序函数")
print(f"推荐模型：{result['selected_model']}")
print(f"预估成本：¥{result['estimated_cost']:.6f}")

# 获取模型信息
info = router.get_model_info("qwen-max")
print(info)

# 查看历史
history = router.get_history(limit=10)

# 成本统计
summary = router.get_cost_summary()
```

---

## 🧠 路由规则

### 任务类型识别

| 任务类型 | 识别关键词 | 推荐模型 |
|----------|------------|----------|
| simple_qa | 问候、简单问题 | qwen-turbo |
| translation | 翻译、translate | qwen-turbo |
| code_generation | 代码、function、def | qwen-coder |
| code_review | 检查、优化、review | qwen-max |
| summarization | 摘要、总结、summary | qwen-plus |
| creative_writing | 写文章、创作、creative | qwen-plus |
| multi_step | 推理、分析、为什么 | qwen-max |
| long_context | 文本>10K 字符 | qwen-long |

### 成本优化策略

1. **简单任务用 Turbo** - 节省 75-95% 成本
2. **复杂任务用 Max** - 保证输出质量
3. **长文本用 Long** - 避免截断
4. **代码专用 Coder** - 专业场景专业模型

---

## 💰 成本对比

### 示例任务成本

| 任务 | 字符数 | Turbo | Plus | Max | 推荐 |
|------|--------|-------|------|-----|------|
| 简单问答 | 50 | ¥0.000002 | ¥0.000006 | ¥0.000030 | Turbo ✅ |
| 翻译句子 | 100 | ¥0.000003 | ¥0.000012 | ¥0.000060 | Turbo ✅ |
| 代码生成 | 500 | ¥0.000015 | ¥0.000060 | ¥0.000300 | Coder ✅ |
| 文章摘要 | 5000 | ¥0.000150 | ¥0.000600 | ¥0.003000 | Plus ✅ |
| 复杂推理 | 2000 | ¥0.000060 | ¥0.000240 | ¥0.001200 | Max ✅ |
| 长文档分析 | 50000 | ❌超限 | ❌超限 | ¥0.030000 | Long ✅ |

### 月度成本估算

假设每日 100 次请求：

| 策略 | 日均成本 | 月均成本 | 说明 |
|------|----------|----------|------|
| 全用 Max | ¥3.00 | ¥90 | 性能最好，成本最高 |
| 全用 Turbo | ¥0.30 | ¥9 | 成本最低，简单任务适用 |
| **智能路由** | **¥0.80** | **¥24** | **平衡性能与成本** ✅ |

**智能路由节省：73% vs 全用 Max**

---

## 🔧 高级用法

### 自定义路由规则

```python
router = ModelRouter()

# 修改路由规则
router.routing_rules[TaskType.CREATIVE_WRITING] = ModelTier.PREMIUM

# 现在创意写作会用 Premium 层级模型
```

### 强制指定模型

```python
# 覆盖自动路由
result = router.route(prompt, context={"force_model": "qwen-max"})
```

### 批量路由

```python
prompts = ["任务 1", "任务 2", "任务 3"]
results = [router.route(p) for p in prompts]

# 统计
summary = router.get_cost_summary()
```

---

## 📈 监控与优化

### 查看路由历史

```python
history = router.get_history(limit=50)
for r in history:
    print(f"{r['task_type']}: {r['selected_model']} - ¥{r['estimated_cost']:.6f}")
```

### 成本分析

```python
summary = router.get_cost_summary()
print(f"总成本：¥{summary['total_cost']:.4f}")
print(f"平均成本：¥{summary['avg_cost_per_request']:.6f}/请求")
print(f"模型分布：{summary['model_distribution']}")
```

### 优化建议

根据 `get_cost_summary()` 结果：

- **qwen-max 占比过高** → 检查是否有简单任务误用
- **平均成本>¥0.001** → 优化任务分类规则
- **长文本频繁** → 考虑 qwen-long 套餐

---

## 🎯 九宫格集成

### 在宫位中使用

```python
# palace_2_product.py
from model_router import ModelRouter

class Palace2Product(PalaceBase):
    def __init__(self):
        super().__init__(...)
        self.model_router = ModelRouter()
    
    def create_prd(self, title: str, content: str):
        # 根据内容长度自动选择模型
        result = self.model_router.route(f"创建 PRD: {title}\n{content}")
        
        # 调用百炼 API（需要实际实现）
        # response = call_bailian_api(result['selected_model'], prompt)
        
        return {"model": result['selected_model'], "cost": result['estimated_cost']}
```

### 调度器集成

```python
# nine_palaces_manager.py
class NinePalacesManager:
    def __init__(self):
        self.model_router = ModelRouter()
    
    def execute(self, palace_id, action, params):
        # 记录任务类型用于模型选择
        task_context = {
            "palace_id": palace_id,
            "action": action,
            "params_size": len(str(params)),
        }
        
        # 路由决策
        route_result = self.model_router.route(str(params), task_context)
        
        # 执行并记录成本
        result = self.palaces[palace_id].execute(action, params)
        result["model_info"] = route_result
        
        return result
```

---

## ⚠️ 注意事项

1. **API Key 安全** - 不要硬编码在代码中
2. **成本监控** - 定期检查 `get_cost_summary()`
3. **模型限制** - 注意上下文窗口限制
4. **错误处理** - 处理 API 调用失败情况
5. **速率限制** - 百炼 API 有 QPS 限制

---

## 🔗 相关资源

- 百炼文档：https://help.aliyun.com/zh/dashscope/
- 模型列表：https://help.aliyun.com/zh/dashscope/developer-reference/model-introduction
- 定价详情：https://help.aliyun.com/zh/dashscope/pricing

---

**智能路由，成本优化 73%！** 🚀
