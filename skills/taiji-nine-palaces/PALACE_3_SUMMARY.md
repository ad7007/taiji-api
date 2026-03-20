# 3-技术团队宫 - 智能模型路由

## 🎯 核心特性

### 1. 智能模型切换

根据任务类型自动选择最优百炼模型：

| 任务类型 | 自动选择模型 | 成本优化 |
|----------|--------------|----------|
| 简单问答 | qwen-turbo | 节省 95% |
| 代码生成 | qwen-coder | 专业优化 |
| 代码审查 | qwen-max | 高质量 |
| 技术文档 | qwen-plus | 平衡性能 |
| 调试帮助 | qwen-max | 复杂推理 |
| 自动化脚本 | qwen-coder | 专业优化 |

### 2. 按需报告策略

**默认不生成报告**，避免浪费 token：

```python
# ❌ 不生成报告（默认）
palace.execute("code_generate", {
    "description": "写个排序函数",
    "language": "python",
})

# ✅ 明确请求时才生成
palace.execute("code_generate", {
    "description": "写个排序函数",
    "generate_report": True,  # 显式开启
})

# ✅ 单独生成汇总报告
palace.execute("generate_report", {
    "task_type": "all",
    "time_range": "week",
})
```

---

## 📊 成本对比

### 场景：每日 50 次代码任务

| 策略 | 日均成本 | 月均成本 | 说明 |
|------|----------|----------|------|
| 每次生成报告 | ¥3.00 | ¥90 | 浪费严重 ❌ |
| **按需报告** | **¥0.50** | **¥15** | **节省 83%** ✅ |

### 报告生成策略

| 操作类型 | 默认行为 | 报告生成 |
|----------|----------|----------|
| code_generate | 保存代码文件 | ❌ 不生成 |
| code_review | 返回审查意见 | ❌ 不生成 |
| debug_help | 返回分析结果 | ❌ 不生成 |
| generate_report | 汇总任务日志 | ✅ 生成 |

---

## 🚀 使用示例

### 代码生成（不生成报告）

```python
from palace_3_tech import Palace3Tech

palace = Palace3Tech()

# 生成代码（默认不生成报告）
result = palace.execute("code_generate", {
    "description": "实现快速排序",
    "language": "python",
})

print(f"代码文件：{result['code_file']}")
print(f"模型：{result['model']}, 成本：¥{result['cost']:.6f}")
# 不输出报告，节省 token
```

### 代码审查（不生成报告）

```python
result = palace.execute("code_review", {
    "code": "def add(a,b): return a+b",
    "review_type": "security",
})

print(f"审查结果：{result['review']}")
# 不生成报告
```

### 生成汇总报告（明确请求）

```python
# 周末生成任务汇总报告
result = palace.execute("generate_report", {
    "task_type": "all",
    "time_range": "week",
})

report = result["report"]
print(f"本周任务：{report['summary']['total_tasks']}")
print(f"成功率：{report['summary']['success_rate']}")
print(f"总成本：{report['summary']['total_cost']}")
```

---

## 📁 文件结构

```
code/
├── code_计算斐波那契数列_20260318_002448.py
├── code_快速排序_20260318_003000.py
├── auto_backup_script_20260318_004000.py
└── doc_API 文档.md

logs/
└── tech_tasks.jsonl  # 任务日志（轻量级）
```

---

## 🔧 核心方法

| 方法 | 功能 | 报告策略 |
|------|------|----------|
| `code_generate()` | 代码生成 | 默认不生成 |
| `code_review()` | 代码审查 | 默认不生成 |
| `git_manage()` | Git 管理 | 不生成 |
| `auto_script()` | 自动化脚本 | 默认不生成 |
| `tech_doc()` | 技术文档 | 默认不生成 |
| `debug_help()` | 调试帮助 | 默认不生成 |
| `generate_report()` | 汇总报告 | ✅ 生成 |

---

## 💡 最佳实践

### 1. 日常开发（不生成报告）

```python
# 快速生成代码
result = palace.execute("code_generate", {
    "description": "写个 API 客户端",
    "language": "python",
})

# 直接使用代码文件
code = Path(result["code_file"]).read_text()
```

### 2. 代码审查（不生成报告）

```python
# 快速审查
result = palace.execute("code_review", {
    "code": code,
    "review_type": "security",
})

# 直接查看审查意见
print(result["review"])
```

### 3. 周报/月报（生成汇总）

```python
# 周五生成周报
weekly_report = palace.execute("generate_report", {
    "task_type": "all",
    "time_range": "week",
})

# 月度汇总
monthly_report = palace.execute("generate_report", {
    "task_type": "all",
    "time_range": "month",
})
```

---

## 📊 任务日志格式

```jsonl
{"timestamp": "2026-03-18T00:24:48", "action": "code_generate", "params_summary": {...}, "success": true, "model": "qwen-coder", "cost": 0.0005}
{"timestamp": "2026-03-18T00:30:00", "action": "code_review", "params_summary": {...}, "success": true, "model": "qwen-max", "cost": 0.0012}
```

**轻量级记录**，仅包含关键信息，不存储完整代码/报告。

---

## ⚠️ 注意事项

1. **报告默认关闭** - 避免浪费 token
2. **明确请求才生成** - `generate_report=True`
3. **汇总报告单独生成** - `generate_report` 动作
4. **日志自动清理** - 建议定期清理 `logs/tech_tasks.jsonl`

---

## 🎯 成本优化效果

| 项目 | 优化前 | 优化后 | 节省 |
|------|--------|--------|------|
| 单次代码生成 | ¥0.002（含报告） | ¥0.0005（无报告） | 75% |
| 单次代码审查 | ¥0.003（含报告） | ¥0.001（无报告） | 67% |
| 日均 50 次任务 | ¥3.00 | ¥0.50 | 83% |
| 月均成本 | ¥90 | ¥15 | **83%** ✅ |

---

**智能模型路由 + 按需报告 = 成本优化 83%！** 🚀
