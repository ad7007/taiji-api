# API 使用示例

本文档提供太极 API 的实际使用示例。

---

## 🚀 快速开始

### 启动服务

```bash
# 安装依赖
pip install -r requirements.txt

# 启动 API
python -m uvicorn api.taiji_api:app --reload

# 访问文档
http://localhost:8000/docs
```

---

## 📊 九宫格管理

### 获取九宫状态

```bash
curl http://localhost:8000/api/taiji/palaces | jq
```

**响应**:
```json
{
  "palaces": {
    "1": {
      "name": "1-数据采集",
      "element": "土",
      "load": 0.75
    },
    "5": {
      "name": "5-中央控制",
      "element": "土",
      "load": 0.90
    }
  }
}
```

### 更新宫位负载

```bash
curl -X POST http://localhost:8000/api/taiji/update-palace-load \
  -H "Content-Type: application/json" \
  -d '{"palace_id": 1, "load": 0.8}'
```

---

## 🤖 L4 规则层

### 5 宫指挥官 - 接收任务

```bash
curl -X POST http://localhost:8000/api/l4/command \
  -H "Content-Type: application/json" \
  -d '{"command": "分析这份销售数据"}' | jq
```

**响应**:
```json
{
  "task_id": "task_20260318140000",
  "priority": "MEDIUM",
  "task_type": "data_analysis",
  "assigned_palaces": [1, 3, 7, 5],
  "model_allocation": {
    "model": "claude-sonnet",
    "access_mode": "zero_token",
    "estimated_cost": 0.0
  },
  "tdd_standards": [
    {"name": "数据来源", "required": true},
    {"name": "分析方法", "required": true},
    {"name": "核心洞察", "required": true}
  ]
}
```

### 7 宫 TDD - 完成任务

```bash
curl -X POST http://localhost:8000/api/l4/complete \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "task_20260318140000",
    "output": "# 数据分析报告\n\n## 数据来源\n...\n\n## 核心洞察\n1. ...\n2. ...\n3. ..."
  }' | jq
```

**响应**:
```json
{
  "status": "delivered",
  "check_result": {
    "passed": true,
    "details": [...]
  }
}
```

---

## 🎯 3 宫模型分配

### 获取模型列表

```bash
curl http://localhost:8000/api/palace3/models | jq
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
    "quality_level": 5
  },
  {
    "model": "qwen3.5-plus",
    "provider": "qwen",
    "access_mode": "api_token",
    "strengths": ["推理", "代码", "分析"],
    "cost_level": 3,
    "quality_level": 5
  }
]
```

### 模式对比

```bash
curl http://localhost:8000/api/palace3/compare/video_process | jq
```

**响应**:
```json
{
  "api_token": {
    "model": "qwen3.5-plus",
    "estimated_cost": 0.008
  },
  "zero_token": {
    "model": "gemini-pro",
    "estimated_cost": 0.0
  },
  "recommendation": "优先使用 Zero Token 模式"
}
```

### 成本报告

```bash
curl http://localhost:8000/api/palace3/cost-report | jq
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

## 🕷️ 1 宫数据采集

### 抓取模式对比

```bash
curl http://localhost:8000/api/palace1/modes | jq
```

**响应**:
```json
{
  "http_fast": {
    "speed": "极快",
    "suitable_for": ["简单文字信息", "结构化数据"],
    "proxy_recommended": true
  },
  "browser_render": {
    "speed": "较慢",
    "suitable_for": ["图片", "视频", "复杂 JavaScript"],
    "proxy_recommended": true
  }
}
```

### 防封禁特性

```bash
curl http://localhost:8000/api/palace1/anti-block | jq
```

**响应**:
```json
[
  {
    "feature": "模拟人类鼠标移动",
    "effectiveness": "高"
  },
  {
    "feature": "代理 IP 轮换",
    "effectiveness": "极高",
    "analogy": "100 个穿不同衣服的人轮流进去拿货"
  }
]
```

### 配置抓取任务

```bash
curl -X POST http://localhost:8000/api/palace1/configure \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "site_type": "anti_bot_site",
    "mode": "browser_render"
  }' | jq
```

---

## ⚖️ 阴阳平衡

### 获取平衡状态

```bash
curl http://localhost:8000/api/taiji/balance | jq
```

**响应**:
```json
{
  "balance": {
    "team_process": 0.93,
    "tech_quality": 0.86,
    "product_data": 0.86,
    "monitor_eco": 1.0
  },
  "imbalanced_pairs": []
}
```

### 切换模式

```bash
# 切换到阳模式（推进任务）
curl -X POST http://localhost:8000/api/taiji/switch-mode \
  -H "Content-Type: application/json" \
  -d '{"mode": "yang"}'

# 切换到阴模式（反思/Ask）
curl -X POST http://localhost:8000/api/taiji/switch-mode \
  -H "Content-Type: application/json" \
  -d '{"mode": "yin"}'
```

---

## 🐍 Python 示例

### 使用 Python 客户端

```python
import requests

BASE_URL = "http://localhost:8000"

# 获取九宫状态
response = requests.get(f"{BASE_URL}/api/taiji/palaces")
palaces = response.json()
print(palaces)

# 创建任务
response = requests.post(
    f"{BASE_URL}/api/l4/command",
    json={"command": "分析数据"}
)
task = response.json()
print(f"Task ID: {task['task_id']}")

# 完成任务
response = requests.post(
    f"{BASE_URL}/api/l4/complete",
    json={
        "task_id": task["task_id"],
        "output": "# 分析报告\n..."
    }
)
result = response.json()
print(f"Status: {result['status']}")
```

### 批量更新宫位负载

```python
import requests

BASE_URL = "http://localhost:8000"

# 批量更新
updates = [
    {"palace_id": 1, "load": 0.7},
    {"palace_id": 2, "load": 0.6},
    {"palace_id": 3, "load": 0.8},
]

for update in updates:
    response = requests.post(
        f"{BASE_URL}/api/taiji/update-palace-load",
        json=update
    )
    print(f"Palace {update['palace_id']}: {response.json()}")
```

---

## 💡 实际场景

### 场景 1: 自动处理抖音视频

```python
# 1. 接收任务
response = requests.post(
    "http://localhost:8000/api/l4/command",
    json={"command": "下载这个抖音视频并总结"}
)
task = response.json()

# 2. 执行（1 宫下载 + 转录）
# ... 实际执行逻辑 ...

# 3. 完成任务（7 宫验收）
response = requests.post(
    "http://localhost:8000/api/l4/complete",
    json={
        "task_id": task["task_id"],
        "output": "# 视频摘要\n..."
    }
)
```

### 场景 2: 成本优化

```python
# 获取成本报告
response = requests.get("http://localhost:8000/api/palace3/cost-report")
report = response.json()

print(f"Zero Token 使用率：{report['zero_token_ratio']*100:.1f}%")
print(f"节省成本：{report['savings']:.2f}元")

# 如果 Zero Token 使用率低，调整策略
if report['zero_token_ratio'] < 0.5:
    print("建议：提高 Zero Token 模式使用率")
```

---

## 🔗 更多资源

- [Swagger 文档](http://localhost:8000/docs)
- [ReDoc](http://localhost:8000/redoc)
- [README.md](../README.md)
- [CONTRIBUTING.md](../CONTRIBUTING.md)

---

**最后更新**: 2026-03-18
