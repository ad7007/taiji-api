# 分布式太极架构协议 v1.0

## 核心理念

**两地九宫，协同采集，突破信息孤岛**

---

## 架构设计

### 物理层

| 服务器 | 位置 | 优势数据源 | 延迟 |
|--------|------|-----------|------|
| 广州 | 中国大陆 | 抖音、小红书、B站、微博、知乎 | ~50ms |
| 洛杉矶 | 美西 | YouTube、Twitter、TikTok、Google、OpenAI | ~20ms |

### 逻辑层

每个服务器运行**完整的太极系统**：

```
广州服务器                        洛杉矶服务器
├── 米珞主控 (广州版)             ├── 米珞主控 (硅谷版)
├── 1宫 数据采集 (国内源)         ├── 1宫 数据采集 (国际源)
├── 2宫 产品质量                  ├── 2宫 产品质量
├── 3宫 技术团队                  ├── 3宫 技术团队
├── 4宫 品牌战略                  ├── 4宫 品牌战略
├── 6宫 物联监控                  ├── 6宫 物联监控
├── 7宫 法务框架                  ├── 7宫 法务框架
├── 8宫 营销客服                  ├── 8宫 营销客服
└── 9宫 行业生态                  └── 9宫 行业生态
```

---

## 协作协议

### 1. 数据采集分工

```python
# 数据源路由规则
DATA_SOURCE_ROUTING = {
    # 广州服务器负责
    "guangzhou": [
        "douyin.com",      # 抖音
        "xiaohongshu.com", # 小红书
        "bilibili.com",    # B站
        "weibo.com",       # 微博
        "zhihu.com",       # 知乎
        "taobao.com",      # 淘宝
        "jd.com",          # 京东
    ],
    
    # 洛杉矶服务器负责
    "losangeles": [
        "youtube.com",     # YouTube
        "twitter.com",     # Twitter
        "x.com",           # X
        "tiktok.com",      # TikTok国际版
        "google.com",      # Google
        "openai.com",      # OpenAI
        "github.com",      # GitHub
        "reddit.com",      # Reddit
    ],
}
```

### 2. 智能路由

当米珞收到采集任务时：

```
任务: 采集抖音热门视频
    ↓
检查数据源: douyin.com
    ↓
路由决策: 广州服务器 (国内源)
    ↓
调度: 广州1宫执行
```

```
任务: 采集YouTube视频
    ↓
检查数据源: youtube.com
    ↓
路由决策: 洛杉矶服务器 (国际源)
    ↓
远程调用: 洛杉矶1宫执行
```

### 3. 状态同步

| 同步内容 | 频率 | 方向 |
|----------|------|------|
| 任务状态 | 实时 | 双向 |
| 采集数据 | 完成后 | 汇总到主服务器 |
| 记忆更新 | 每小时 | 双向合并 |
| 系统健康 | 每5分钟 | 汇报给主控 |

---

## 配置步骤

### 第一步：准备洛杉矶服务器

```bash
# 1. 购买洛杉矶VPS（推荐）
# - Vultr: $5/月
# - DigitalOcean: $6/月
# - Bandwagon: $49.99/年

# 2. 安装OpenClaw
curl -fsSL https://get.openclaw.ai | bash
```

### 第二步：配置服务器身份

**广州服务器** (`~/.openclaw/workspace/IDENTITY.md`)：
```yaml
---
name: 米珞-广州
agent_id: main-gz
region: china-south
role: primary
peer: losangeles
---
```

**洛杉矶服务器** (`~/.openclaw/workspace/IDENTITY.md`)：
```yaml
---
name: 米珞-硅谷
agent_id: main-la
region: us-west
role: secondary
peer: guangzhou
---
```

### 第三步：配置双向通信

**广州服务器** (`~/.openclaw/workspace/TOOLS.md`)：
```yaml
peers:
  losangeles:
    host: <LA_SERVER_IP>
    port: 443
    token: <SHARED_SECRET>
    role: secondary
```

**洛杉矶服务器** (`~/.openclaw/workspace/TOOLS.md`)：
```yaml
peers:
  guangzhou:
    host: <GZ_SERVER_IP>
    port: 443
    token: <SHARED_SECRET>
    role: primary
```

### 第四步：同步记忆

在广州服务器执行：
```bash
# 推送记忆到洛杉矶
rclone copy ~/.openclaw/workspace/MEMORY.md remote:losangeles/workspace/
rclone copy ~/.openclaw/workspace/memory/ remote:losangeles/workspace/memory/
```

在洛杉矶服务器执行：
```bash
# 接收记忆
rclone copy remote:guangzhou/workspace/MEMORY.md ~/.openclaw/workspace/
rclone copy remote:guangzhou/workspace/memory/ ~/.openclaw/workspace/memory/
```

---

## API调用示例

### 本地调用（广州）

```python
import requests

# 直接调用广州本地
response = requests.post("http://localhost:8000/api/taiji/collect", json={
    "source": "douyin",
    "url": "https://www.douyin.com/video/xxx",
    "server": "local"  # 或省略，默认本地
})
```

### 远程调用（洛杉矶）

```python
# 从广州调用洛杉矶
response = requests.post("http://localhost:8000/api/taiji/collect", json={
    "source": "youtube",
    "url": "https://www.youtube.com/watch?v=xxx",
    "server": "losangeles"  # 路由到洛杉矶
})
```

### 自动路由

```python
# 系统自动判断
response = requests.post("http://localhost:8000/api/taiji/collect", json={
    "source": "auto",
    "url": "https://www.youtube.com/watch?v=xxx"
})
# 系统自动检测到youtube.com，路由到洛杉矶服务器
```

---

## 双服务器优势

| 优势 | 说明 |
|------|------|
| **突破地域限制** | 国内源用广州，国际源用洛杉矶 |
| **降低延迟** | 各自采集最近的源 |
| **高可用** | 一台故障，另一台接管 |
| **负载分担** | 采集任务分散到两台服务器 |
| **数据互补** | 两边数据合并，信息更全面 |

---

## 成本估算

| 项目 | 费用 |
|------|------|
| 广州服务器 | 已有 |
| 洛杉矶VPS | $5-6/月 ≈ ¥35-40/月 |
| 带宽流量 | 包含在VPS费用中 |
| **总计** | ~¥40/月 |

---

## 下一步行动

1. **购买洛杉矶VPS** - 推荐Vultr $5/月
2. **安装OpenClaw** - 复制广州配置
3. **配置双向通信** - 设置peers
4. **同步记忆** - 复制MEMORY.md
5. **测试协作** - 采集一个YouTube视频

---

**创建时间**: 2026-03-22
**维护宫位**: 5宫米珞 + 3宫技术团队