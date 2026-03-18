# 太极 API - Taiji Nine Palaces Task Management System

🌌 基于中国传统太极哲学的智能任务管理系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-green.svg)](https://openclaw.ai)
[![Community Driven](https://img.shields.io/badge/community-driven-blue.svg)](https://github.com/ad7007/taiji-api)

---

## 📖 简介

> **⚠️ 社区共同维护项目** - 欢迎所有人参与贡献，一起改进太极 API！

太极 API 是一个基于九宫格哲学的任务管理系统，将中国传统智慧与现代 AI 技术相结合。

> "太极生两仪，两仪生四象，四象生八卦" - 《易经》

### 🌟 为什么需要你的参与

这个项目**不属于任何个人**，属于**整个开源社区**。

- ✅ **没有唯一维护者** - 大家一起决策、一起开发
- ✅ **有新版本一起用** - 社区审核、合并、发布
- ✅ **你的贡献有价值** - 每个 PR 都会被认真对待
- ✅ **共同受益** - 改进的功能所有人共享

### 核心特性

- 🎯 **九宫格任务管理** - 1-9 宫位各司其职
- ⚖️ **阴阳平衡** - 自动检测并调节负载平衡
- 🔄 **五行循环** - 金木水火土相生相克验证
- 🤖 **AI 深度集成** - OpenClaw 技能系统
- 📊 **L4 规则引擎** - 5 宫指挥官 + 7 宫 TDD 验收
- 💰 **Zero Token** - 零成本调用主流 AI 模型
- 🕷️ **Crawlee 集成** - 智能数据抓取防封禁

---

## 🏛️ 九宫格架构

```
┌─────────────┬─────────────┬─────────────┐
│ 4-品牌战略   │ 9-行业生态   │ 2-产品质量   │
│ 水 · 巽宫     │ 土 · 离宫     │ 金 · 坤宫     │
├─────────────┼─────────────┼─────────────┤
│ 3-技术团队   │ 5-中央控制   │ 7-法务框架   │
│ 木 · 震宫     │ 土 · 中宫     │ 金 · 兑宫     │
├─────────────┼─────────────┼─────────────┤
│ 8-营销客服   │ 1-数据采集   │ 6-物联监控   │
│ 木 · 艮宫     │ 土 · 坎宫     │ 火 · 乾宫     │
└─────────────┴─────────────┴─────────────┘
```

### 宫位职责

| 宫位 | 名称 | 职责 | 五行 |
|------|------|------|------|
| 1 宫 | 数据采集 | 网页抓取、数据收集 | 土 |
| 2 宫 | 产品质量 | 文档管理、质量把控 | 金 |
| 3 宫 | 技术团队 | 模型分配、代码管理 | 木 |
| 4 宫 | 品牌战略 | 身份管理、对外形象 | 水 |
| 5 宫 | 中央控制 | 指挥协调、任务调度 | 土 |
| 6 宫 | 物联监控 | 系统监控、配置备份 | 火 |
| 7 宫 | 法务框架 | 安全扫描、TDD 验收 | 金 |
| 8 宫 | 营销客服 | 客户服务、营销推广 | 木 |
| 9 宫 | 行业生态 | 生态建设、合作伙伴 | 土 |

---

## 🚀 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/ad7007/taiji-api.git
cd taiji-api

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 启动服务

```bash
# 启动 API 服务
python -m uvicorn api.taiji_api:app --host 0.0.0.0 --port 8000

# 开发模式（自动重载）
python -m uvicorn api.taiji_api:app --reload
```

### 访问文档

```
Swagger UI: http://localhost:8000/docs
ReDoc:      http://localhost:8000/redoc
Health:     http://localhost:8000/health
```

---

## 📋 API 端点

### 太极核心端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/taiji/palaces` | GET | 获取九宫状态 |
| `/api/taiji/balance` | GET | 阴阳平衡检查 |
| `/api/taiji/update-palace-load` | POST | 更新宫位负载 |
| `/api/taiji/switch-mode` | POST | 切换阴阳模式 |

### L4 规则层端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/l4/command` | POST | 5 宫指挥官命令 |
| `/api/l4/complete` | POST | 7 宫绿灯检查 |
| `/api/l4/status` | GET | L4 状态查询 |

### 3 宫模型分配端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/palace3/models` | GET | 模型能力列表 |
| `/api/palace3/compare/{task_type}` | GET | 模式对比 |
| `/api/palace3/cost-report` | GET | 成本报告 |

### 1 宫数据采集端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/palace1/modes` | GET | 抓取模式对比 |
| `/api/palace1/anti-block` | GET | 防封禁特性 |
| `/api/palace1/configure` | POST | 配置抓取任务 |
| `/api/palace1/report` | GET | 抓取报告 |

---

## 🔧 配置

### 环境变量

```bash
# API 配置
TAIJI_API_URL=http://localhost:8000

# 3 宫模型配置
PREFER_ZERO_TOKEN=true  # 优先使用 Zero Token 模式

# 6 宫备份配置
RCLONE_CONFIG=gdrive
BACKUP_SCHEDULE_NOON="0 12 * * *"
BACKUP_SCHEDULE_NIGHT="0 23 * * *"
```

### TOOLS.md 配置

```bash
# GitHub（3 宫）
GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"

# 飞书文档（2 宫）
FEISHU_APP_ID="cli_xxxxxxxxxxxxxxxxx"
FEISHU_APP_SECRET="xxxxxxxxxxxxxxxxx"
```

---

## 🤝 社区共同维护

> **这个项目需要你的参与！**

### 如何参与

#### 1️⃣ 提交代码（最直接）

```bash
# Fork → Clone → Branch → Develop → Commit → Push → PR
```

详见 [贡献指南](CONTRIBUTING.md)

#### 2️⃣ 报告问题（很重要）

- 发现 Bug？[提交 Issue](https://github.com/ad7007/taiji-api/issues/new?template=bug_report.md)
- 想要新功能？[提交建议](https://github.com/ad7007/taiji-api/issues/new?template=feature_request.md)

#### 3️⃣ 帮助他人（有价值）

- 回答 Issues 中的问题
- 帮助新人上手
- 分享使用经验

#### 4️⃣ 宣传推广（感谢）

- Star 项目 ⭐
- 推荐给朋友
- 写博客文章

### 维护者招募中 📢

**我们正在寻找共同维护者！**

如果你：
- ✅ 对太极哲学 + AI 感兴趣
- ✅ 有 Python 开发经验
- ✅ 愿意投入时间
- ✅ 认同社区共同维护理念

**请联系我们**：在 Issue 中留言或直接提交 PR 展示你的能力！

**维护者权益**：
- 🔑 代码合并权限
- 🎯 项目决策权
- 🏆 官方认可
- 🤝 社区影响力

### 贡献者名单

**创始人**:
- [@ad7007](https://github.com/ad7007) - 项目发起

**共同维护者**：
- 📢 **虚位以待** - 下一个就是你！

**贡献者**：
- 🌟 **等待你的名字出现在这里**

---

## 📅 路线图

### v2.0 (当前版本) ✅

- L4 规则层集成
- 3 宫模型分配
- 1 宫数据采集增强
- 定时备份系统

### v2.1 (2026 Q2) 📅

- 9 宫完整实现
- 六爻引擎集成
- 五行循环可视化
- 多语言支持

### v3.0 (2026 Q3) 🔮

- 插件系统
- 分布式部署
- 性能优化
- 企业版功能

详见 [ROADMAP.md](ROADMAP.md)

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 🙏 致谢

- [OpenClaw](https://openclaw.ai) - AI 智能体框架
- [Crawlee](https://crawlee.dev) - 网页抓取库
- [FastAPI](https://fastapi.tiangolo.com) - API 框架

---

## 📬 联系方式

- GitHub: https://github.com/ad7007/taiji-api
- Issues: https://github.com/ad7007/taiji-api/issues

---

**🌟 如果这个项目对你有帮助，请给一个 Star！**
