# 1 宫 - 数据采集 · Crawlee 增强版

**版本**: v2.0  
**创建时间**: 2026-03-18  
**位置**: `/root/taiji-api-v2/core/palace_1_data_collection.py`

---

## 一、核心能力升级

### 灵感来源

**Crawlee 项目**（GitHub 2 万 star）  
抖音视频：https://v.douyin.com/zD8x1PSYFgw/

**核心洞察**:
- 模拟人类鼠标移动 → 绕过行为检测
- 代理 IP 轮换 → "100 个穿不同衣服的人轮流进去拿货"
- 双模式切换 → HTTP 快速（文字）vs 浏览器渲染（图片/视频/JS）
- 完全开源免费

---

## 二、双模式对比

| 特性 | HTTP 快速模式 | 浏览器渲染模式 |
|------|-------------|---------------|
| **速度** | 极快 ⚡⚡⚡ | 较慢 🐢 |
| **适合** | 简单文字、结构化数据、API 接口 | 图片、视频、复杂 JS、动态内容 |
| **局限性** | 无法渲染 JS、无法获取图片/视频 | 速度慢、资源消耗大 |
| **代理推荐** | ✅ 推荐 | ✅ 推荐 |
| **使用场景** | 批量文字抓取 | 复杂网站、反爬网站 |

**建议**: 简单文字用 HTTP 模式，复杂内容用浏览器模式

---

## 三、防封禁特性

### 3.1 模拟人类鼠标移动

- **效果**: 让网站看起来像正常用户在浏览
- **有效性**: 高
- **实现**: Crawlee 自动模拟随机鼠标轨迹

### 3.2 代理 IP 轮换 ⭐⭐⭐⭐⭐

- **效果**: 配合代理池自动切换 IP 地址
- **有效性**: 极高
- **比喻**: "100 个穿不同衣服的人轮流进去拿货，谁也不会引起注意"
- **实现**: 每 20 页自动切换 IP

### 3.3 请求频率控制

- **效果**: 自动限制请求速度，避免触发反爬
- **有效性**: 中
- **实现**: 智能延迟（1-5 秒随机）

### 3.4 User-Agent 轮换

- **效果**: 模拟不同浏览器和设备
- **有效性**: 中
- **实现**: 随机切换 Chrome/Firefox/Safari/Edge

### 3.5 Cookie 管理

- **效果**: 自动处理会话和登录状态
- **有效性**: 高
- **实现**: 持久化 Cookie，自动刷新

---

## 四、API 端点

### 4.1 获取模式对比

```bash
GET /api/palace1/modes
```

**响应**:
```json
{
  "http_fast": {
    "mode": "http_fast",
    "speed": "极快",
    "suitable_for": ["简单文字信息", "结构化数据", "API 接口"],
    "limitations": ["无法渲染 JS", "无法获取图片/视频"],
    "proxy_recommended": true
  },
  "browser_render": {
    "mode": "browser_render",
    "speed": "较慢",
    "suitable_for": ["图片", "视频", "复杂 JavaScript 脚本", "动态内容"],
    "limitations": ["速度慢", "资源消耗大"],
    "proxy_recommended": true
  },
  "recommendation": "简单文字用 HTTP 模式，复杂内容用浏览器模式"
}
```

### 4.2 获取防封禁特性

```bash
GET /api/palace1/anti-block
```

**响应**:
```json
[
  {
    "feature": "模拟人类鼠标移动",
    "description": "让网站看起来像正常用户在浏览",
    "effectiveness": "高"
  },
  {
    "feature": "代理 IP 轮换",
    "description": "配合代理池自动切换 IP 地址",
    "effectiveness": "极高",
    "analogy": "100 个穿不同衣服的人轮流进去拿货"
  },
  ...
]
```

### 4.3 配置抓取任务

```bash
POST /api/palace1/configure
Content-Type: application/json

{
  "url": "https://example.com",
  "site_type": "anti_bot_site",
  "mode": "browser_render"
}
```

**响应**:
```json
{
  "url": "https://example.com",
  "mode": "browser_render",
  "use_proxy": true,
  "rotate_ip": true,
  "simulate_human": true,
  "max_pages": 100,
  "timeout": 60
}
```

### 4.4 获取抓取报告

```bash
GET /api/palace1/report
```

**响应**:
```json
{
  "total_tasks": 10,
  "success_rate": 0.95,
  "total_pages_crawled": 850,
  "total_time_seconds": 1200,
  "avg_pages_per_task": 85,
  "total_ip_rotations": 42,
  "http_fast_tasks": 6,
  "browser_render_tasks": 4
}
```

---

## 五、网站类型模板

### 5.1 simple_text（简单文字）

```python
{
  "mode": "http_fast",
  "use_proxy": False,
  "rotate_ip": False,
  "simulate_human": False,
  "max_pages": 50,
  "timeout": 30
}
```

**适用**: 博客、新闻站、文档站

### 5.2 anti_bot_site（反爬网站）⭐

```python
{
  "mode": "browser_render",
  "use_proxy": True,
  "rotate_ip": True,
  "simulate_human": True,
  "max_pages": 100,
  "timeout": 60
}
```

**适用**: 电商网站、社交媒体、有反爬措施的网站

### 5.3 media_rich（多媒体丰富）

```python
{
  "mode": "browser_render",
  "use_proxy": False,
  "rotate_ip": False,
  "simulate_human": False,
  "max_pages": 30,
  "timeout": 120
}
```

**适用**: 图片站、视频站、画廊

### 5.4 large_scale（大规模抓取）

```python
{
  "mode": "http_fast",
  "use_proxy": True,
  "rotate_ip": True,
  "simulate_human": False,
  "max_pages": 1000,
  "timeout": 300
}
```

**适用**: 全站抓取、数据归档

---

## 六、Python 调用

### 基本用法

```python
from core.palace_1_data_collection import palace1_configure_crawl

# 配置抓取任务
config = palace1_configure_crawl(
    url="https://example.com",
    site_type="anti_bot_site",  # 反爬网站
    mode="browser_render"        # 浏览器模式
)

print(config)
# {
#   "url": "https://example.com",
#   "mode": "browser_render",
#   "use_proxy": True,
#   "rotate_ip": True,
#   "simulate_human": True,
#   ...
# }
```

### 获取模式对比

```python
from core.palace_1_data_collection import palace1_get_mode_comparison

comparison = palace1_get_mode_comparison()
print(f"HTTP 模式速度：{comparison['http_fast']['speed']}")
print(f"浏览器模式适合：{comparison['browser_render']['suitable_for']}")
```

### 获取防封禁特性

```python
from core.palace_1_data_collection import palace1_get_anti_block_features

features = palace1_get_anti_block_features()
for f in features:
    print(f"{f['feature']}: {f['effectiveness']}")
```

---

## 七、与 L4 引擎集成

### 任务闭环中的 1 宫

```
余总指令："抓取这个网站的产品数据"
    ↓
5 宫感知 → task_type="data_analysis"
    ↓
1 宫配置 → 选择 anti_bot_site 模板
    ↓
3 宫分配 → claude-sonnet (Zero Token)
    ↓
7 宫 TDD → 定义验收标准
    ↓
1 宫执行 → Crawlee 抓取（浏览器模式 + IP 轮换）
    ↓
7 宫验收 → 绿灯检查
    ↓
5 宫交付
```

### L4 自动调用

```python
from core.l4_rule_engine import L4RuleEngine

engine = L4RuleEngine()

# 创建任务（自动调用 1 宫配置）
result = engine.handle_user_command("抓取这个网站的产品数据")

# 返回包含 1 宫配置
print(result["assigned_palaces"])  # [1, 3, 7, 5]
```

---

## 八、Crawlee 集成指南

### 安装

```bash
pip install crawlee[playwright]
```

### 基本用法

```python
from crawlee.playwright_crawler import PlaywrightCrawler

crawler = PlaywrightCrawler(
    max_requests_per_crawl=100,
    headless=True,
    proxy_configuration={
        "proxy_url": "http://proxy.example.com:8080",
        "rotation": True
    }
)

# 模拟人类行为
@crawler.pre_navigation_hook
async def simulate_human(context):
    await context.page.mouse.move(100, 100)
    await context.page.mouse.click(100, 100)

# 执行抓取
await crawler.run(["https://example.com"])
```

### HTTP 快速模式

```python
from crawlee.http_crawler import HttpCrawler

crawler = HttpCrawler(
    max_requests_per_crawl=500,
    additional_http_headers={
        "User-Agent": "Mozilla/5.0 ..."
    }
)

await crawler.run(["https://example.com"])
```

---

## 九、代理池配置

### 免费代理（测试用）

```python
PROXY_POOLS = {
    "free": [
        "http://proxy1.example.com:8080",
        "http://proxy2.example.com:8080",
    ]
}
```

### 付费代理（生产用）

```python
PROXY_POOLS = {
    "paid": [
        "http://premium-proxy1.example.com:8080",
        "http://premium-proxy2.example.com:8080",
    ]
}
```

**推荐服务商**:
- Bright Data
- Oxylabs
- Smartproxy
- IPRoyal

---

## 十、监控与调试

### 查看抓取报告

```bash
curl http://localhost:8000/api/palace1/report | jq
```

### 查看配置

```bash
curl -X POST http://localhost:8000/api/palace1/configure \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "site_type": "anti_bot_site"}' | jq
```

### 日志查看

```bash
# API 日志
tail -f /root/taiji-api-v2/taiji_api.log

# 搜索 1 宫日志
grep "Palace 1" /root/taiji-api-v2/taiji_api.log
```

---

## 十一、最佳实践

### 1. 选择合适的模式

- **文字为主** → HTTP 快速模式
- **图片/视频/JS** → 浏览器渲染模式
- **不确定** → 先用 HTTP，失败再切换浏览器

### 2. 配置代理

- **小规模**（<100 页）→ 可不使用代理
- **中规模**（100-500 页）→ 使用代理，每 50 页切换
- **大规模**（>500 页）→ 使用代理池，每 20 页切换

### 3. 模拟人类行为

- **简单网站** → 可关闭
- **反爬网站** → 必须开启
- **社交媒体** → 必须开启 + 随机延迟

### 4. 错误处理

```python
try:
    result = palace1_execute_crawl(url, config)
    if not result["success"]:
        print(f"抓取失败：{result['error']}")
        # 切换模式重试
        config["mode"] = "browser_render"
        result = palace1_execute_crawl(url, config)
except Exception as e:
    print(f"异常：{e}")
```

---

## 十二、版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v2.0 | 2026-03-18 | 集成 Crawlee，新增双模式和防封禁特性 |
| v1.0 | - | 初始版本（基础下载） |

---

**1 宫数据采集能力已升级，支持 Crawlee 智能抓取。**

**灵感**: Crawlee 项目 - GitHub 2 万 star，让数据抓取像呼吸一样简单
