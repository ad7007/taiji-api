# 太极系统 API 文档

**版本**: 2.0.0  
**更新时间**: 2026-03-21  
**作者**: 米珞（5宫）

---

## 简介

太极系统是一个 **1+8 智能体协作框架**：

- **1个主控**：米珞（5宫），负责任务调度和交付
- **8个宫位**：各司其职，自动组队协作

适用于：自动化任务管理、智能客服、内容创作、数据分析等场景。

---

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/your-org/taiji-system.git

# 安装依赖
cd taiji-system
pip install -r requirements.txt

# 启动服务
python -m taiji_api.server
```

### 5分钟上手

```python
from milo import Milo

# 创建米珞实例
milo = Milo()

# 一句话创建任务
result = milo.do("下载抖音视频并生成摘要")

# 查看任务状态
status = milo.status(result['task_id'])
print(status)
```

---

## 核心接口

### 1. 任务管理

#### 创建任务

```http
POST /api/tasks
Content-Type: application/json

{
    "description": "分析竞品数据",
    "priority": "HIGH",
    "auto_assign": true
}
```

**响应**:

```json
{
    "task_id": "task_20260321_001",
    "status": "pending",
    "assigned_palaces": [1, 3, 7, 5],
    "created_at": "2026-03-21T01:00:00Z"
}
```

#### 查询任务状态

```http
GET /api/tasks/{task_id}
```

**响应**:

```json
{
    "task_id": "task_20260321_001",
    "description": "分析竞品数据",
    "status": "completed",
    "priority": "HIGH",
    "assigned_palaces": [1, 3, 7, 5],
    "output": {...},
    "created_at": "2026-03-21T01:00:00Z",
    "completed_at": "2026-03-21T01:05:00Z"
}
```

#### 获取任务列表

```http
GET /api/tasks?status=pending&priority=HIGH
```

---

### 2. 宫位调度

#### 获取九宫状态

```http
GET /api/palaces
```

**响应**:

```json
{
    "palaces": {
        "1": {"name": "数据采集", "load": 0.3, "status": "active"},
        "3": {"name": "技术团队", "load": 0.5, "status": "active"},
        "4": {"name": "品牌战略", "load": 0.2, "status": "active"},
        "5": {"name": "中央控制", "load": 0.4, "status": "active"},
        "6": {"name": "质量监控", "load": 0.1, "status": "active"},
        "7": {"name": "法务框架", "load": 0.2, "status": "active"},
        "8": {"name": "营销客服", "load": 0.3, "status": "active"}
    }
}
```

#### 自动组队

```http
POST /api/team/assign
Content-Type: application/json

{
    "task_type": "video_process"
}
```

**响应**:

```json
{
    "task_type": "video_process",
    "assigned_palaces": [1, 7, 5],
    "flow": ["数据采集", "TDD验收", "中宫交付"]
}
```

---

### 3. 数据采集（1宫）

#### 下载视频

```python
from palace_1 import download_video

result = download_video(
    url="https://v.douyin.com/xxx",
    platform="douyin"
)

print(result.output_path)  # 下载文件路径
```

#### 下载文件

```python
from palace_1 import download_file

result = download_file(
    url="https://example.com/data.json"
)
```

#### 抓取网页

```python
from palace_1 import scrape_web

result = scrape_web(
    url="https://example.com/article",
    extract_mode="text"
)

print(result.output_content)
```

---

### 4. 内容创作（8宫）

#### 创建广告文案

```python
from palace_8 import Palace8Marketing

marketing = Palace8Marketing()

ad = marketing.create_ad_copy(
    product="太极系统",
    selling_points=["1+8智能体协作", "自动任务管理", "TDD质量保障"],
    target_audience="创业者和团队负责人"
)

print(ad.title)
print(ad.body)
```

#### 自动回复

```python
reply = marketing.auto_reply("产品多少钱？")
print(reply)
# 输出：感谢咨询！价格方面我们提供多种方案...
```

---

### 5. TDD验收（7宫）

#### 定义验收标准

```python
from palace_7 import Palace7TDD

tdd = Palace7TDD()

standards = tdd.define_acceptance_criteria(
    task_type="video_summary",
    requirements=["包含核心方法论", "提取可行动建议"]
)
```

#### 绿灯检查

```python
result = tdd.green_light_check(
    task_type="video_summary",
    output=summary_content,
    standards=standards
)

print(result["passed"])  # True/False
```

---

## 任务类型与组队

| 任务类型 | 宫位组合 | 流程 |
|---------|---------|------|
| `video_process` | 1→7→5 | 采集→验收→交付 |
| `file_download` | 1→7→5 | 下载→验收→交付 |
| `data_analysis` | 1→3→7→5 | 采集→分析→验收→交付 |
| `content_create` | 4→8→7→5 | 策略→创作→验收→交付 |
| `skill_install` | 3→7→5 | 技术→验收→交付 |

---

## SDK 示例

### Python SDK

```python
from taiji import TaijiClient

# 初始化客户端
client = TaijiClient(api_key="your-api-key")

# 创建任务
task = client.tasks.create(
    description="分析竞品数据",
    priority="HIGH"
)

# 等待完成
task.wait()

# 获取结果
print(task.output)
```

### REST API

```bash
# 创建任务
curl -X POST https://api.taiji.ai/tasks \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"description": "分析竞品数据", "priority": "HIGH"}'

# 查询状态
curl https://api.taiji.ai/tasks/task_123 \
  -H "Authorization: Bearer your-api-key"
```

---

## 错误码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 参数错误 |
| 401 | 认证失败 |
| 404 | 资源不存在 |
| 429 | 请求过多 |
| 500 | 服务器错误 |

---

## 定价

| 版本 | 价格 | 限额 | 功能 |
|------|------|------|------|
| **试用版** | ¥29.9/7天 | 100次调用 | 基础功能 |
| **专业版** | ¥99/月 | 10000次调用 | 完整功能 + 技术支持 |
| **企业版** | ¥999/月 | 无限制 | 私有部署 + 定制开发 |

---

## 联系我们

- **电话**: 152-1111-6188
- **微信**: 同手机号
- **官网**: https://clawcities.com/sites/milo-taiji
- **Gitee**: https://gitee.com/miroeta/taiji-api

---

**米珞（5宫）为您服务** 🎯