# Taiji API - Taiji Nine Palaces Task Management System

🌌 An intelligent task management system based on traditional Chinese Taiji philosophy

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-green.svg)](https://openclaw.ai)
[![Community Driven](https://img.shields.io/badge/community-driven-blue.svg)](https://github.com/ad7007/taiji-api)

---

## 📖 Introduction

> **⚠️ Community Co-Maintenance Project** - Everyone is welcome to contribute and improve Taiji API together!

Taiji API is a nine-palace philosophy-based task management system that combines traditional Chinese wisdom with modern AI technology.

> "Taiji generates Liangyi, Liangyi generates Sixiang, Sixiang generates Bagua" - I Ching

### 🌟 Why Your Participation Matters

**This project belongs to no single person; it belongs to the entire open-source community.**

- ✅ **No single maintainer** - Decisions made together, development done together
- ✅ **Share new versions** - Community reviews, merges, and releases
- ✅ **Your contributions matter** - Every PR is taken seriously
- ✅ **Shared benefits** - Improvements are shared by everyone

### Core Features

- 🎯 **Nine Palaces Task Management** - Each of the 9 palaces has its responsibilities
- ⚖️ **Yin-Yang Balance** - Automatic load balancing detection and adjustment
- 🔄 **Five Elements Cycle** - Metal, Wood, Water, Fire, Earth generation and restriction verification
- 🤖 **AI Deep Integration** - OpenClaw skill system
- 📊 **L4 Rule Engine** - Palace 5 Commander + Palace 7 TDD Acceptance
- 💰 **Zero Token** - Zero-cost access to mainstream AI models
- 🕷️ **Crawlee Integration** - Intelligent web scraping with anti-blocking

---

## 🏛️ Nine Palaces Architecture

```
┌─────────────┬─────────────┬─────────────┐
│ 4-Brand     │ 9-Ecosystem │ 2-Quality   │
│ Strategy    │             │             │
├─────────────┼─────────────┼─────────────┤
│ 3-Tech Team │ 5-Central   │ 7-Legal     │
│             │ Control     │ Framework   │
├─────────────┼─────────────┼─────────────┤
│ 8-Marketing │ 1-Data      │ 6-IoT       │
│ & Service   │ Collection  │ Monitoring  │
└─────────────┴─────────────┴─────────────┘
```

### Palace Responsibilities

| Palace | Name | Responsibilities | Element |
|--------|------|------------------|---------|
| 1 | Data Collection | Web scraping, data gathering | Earth |
| 2 | Product Quality | Document management, quality control | Metal |
| 3 | Tech Team | Model allocation, code management | Wood |
| 4 | Brand Strategy | Identity management, external image | Water |
| 5 | Central Control | Command coordination, task scheduling | Earth |
| 6 | IoT Monitoring | System monitoring, config backup | Fire |
| 7 | Legal Framework | Security scanning, TDD acceptance | Metal |
| 8 | Marketing & Service | Customer service, marketing | Wood |
| 9 | Ecosystem | Ecosystem building, partnerships | Earth |

---

## 🚀 Quick Start

### Installation

```bash
# Clone the project
git clone https://github.com/ad7007/taiji-api.git
cd taiji-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Start Service

```bash
# Start API service
python -m uvicorn api.taiji_api:app --host 0.0.0.0 --port 8000

# Development mode (auto-reload)
python -m uvicorn api.taiji_api:app --reload
```

### Access Documentation

```
Swagger UI: http://localhost:8000/docs
ReDoc:      http://localhost:8000/redoc
Health:     http://localhost:8000/health
```

---

## 📋 API Endpoints

### Taiji Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/taiji/palaces` | GET | Get nine palaces status |
| `/api/taiji/balance` | GET | Yin-yang balance check |
| `/api/taiji/update-palace-load` | POST | Update palace load |
| `/api/taiji/switch-mode` | POST | Switch yin/yang mode |

### L4 Rule Layer Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/l4/command` | POST | Palace 5 Commander command |
| `/api/l4/complete` | POST | Palace 7 Green Light check |
| `/api/l4/status` | GET | L4 status query |

### Palace 3 Model Allocation Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/palace3/models` | GET | Model capabilities list |
| `/api/palace3/compare/{task_type}` | GET | Mode comparison |
| `/api/palace3/cost-report` | GET | Cost report |

### Palace 1 Data Collection Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/palace1/modes` | GET | Scraping mode comparison |
| `/api/palace1/anti-block` | GET | Anti-blocking features |
| `/api/palace1/configure` | POST | Configure scraping task |
| `/api/palace1/report` | GET | Scraping report |

---

## 🔧 Configuration

### Environment Variables

```bash
# API Configuration
TAIJI_API_URL=http://localhost:8000

# Palace 3 Model Configuration
PREFER_ZERO_TOKEN=true  # Prefer Zero Token mode

# Palace 6 Backup Configuration
RCLONE_CONFIG=gdrive
BACKUP_SCHEDULE_NOON="0 12 * * *"
BACKUP_SCHEDULE_NIGHT="0 23 * * *"
```

### TOOLS.md Configuration

```bash
# GitHub (Palace 3)
GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"

# Feishu Docs (Palace 2)
FEISHU_APP_ID="cli_xxxxxxxxxxxxxxxxx"
FEISHU_APP_SECRET="xxxxxxxxxxxxxxxxx"
```

---

## 🤝 Community Co-Maintenance

> **This project needs your participation!**
>
> Community co-maintenance + Founder retains highest authority.
> See [Founder Statement](FOUNDER_STATEMENT.md) and [Governance](GOVERNANCE.md).

### How to Participate

#### 1️⃣ Submit Code (Most Direct)

```bash
# Fork → Clone → Branch → Develop → Commit → Push → PR
```

See [CONTRIBUTING.md](CONTRIBUTING.md)

#### 2️⃣ Report Issues (Important)

- Found a bug? [Submit Issue](https://github.com/ad7007/taiji-api/issues/new?template=bug_report.md)
- Want a new feature? [Submit Suggestion](https://github.com/ad7007/taiji-api/issues/new?template=feature_request.md)

#### 3️⃣ Help Others (Valuable)

- Answer questions in Issues
- Help newcomers get started
- Share usage experience

#### 4️⃣ Promote (Appreciated)

- Star the project ⭐
- Recommend to friends
- Write blog posts

### Maintainers Wanted 📢

**We're looking for co-maintainers!**

If you:
- ✅ Are interested in Taiji Philosophy + AI
- ✅ Have Python development experience
- ✅ Can commit time
- ✅ Believe in community co-maintenance philosophy

**Please contact us**: Leave a message in an Issue or submit a PR to demonstrate your abilities!

**Maintainer Benefits**:
- 🔑 Code merge permissions
- 🎯 Project decision rights
- 🏆 Official recognition
- 🤝 Community influence

### Contributors

**Founder**:
- [@ad7007](https://github.com/ad7007) - Project initiator

**Co-Maintainers**:
- 📢 **Position open** - You could be next!

**Contributors**:
- 🌟 **Waiting for your name here**

---

## 📅 Roadmap

### v2.0 (Current Version) ✅

- L4 Rule Layer Integration
- Palace 3 Model Allocation
- Palace 1 Data Collection Enhancement
- Scheduled Backup System

### v2.1 (2026 Q2) 📅

- Complete 9 Palaces Implementation
- Six Lines (Liu Yao) Engine Integration
- Five Elements Visualization
- Multi-language Support

### v3.0 (2026 Q3) 🔮

- Plugin System
- Distributed Deployment
- Performance Optimization
- Enterprise Features

See [ROADMAP.md](ROADMAP.md) for details.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [OpenClaw](https://openclaw.ai) - AI Agent Framework
- [Crawlee](https://crawlee.dev) - Web Scraping Library
- [FastAPI](https://fastapi.tiangolo.com) - API Framework

---

## 📬 Contact

- GitHub: https://github.com/ad7007/taiji-api
- Issues: https://github.com/ad7007/taiji-api/issues

---

**🌟 If this project helps you, please give it a Star!**

---

**Languages**: 
- [中文](README.md) | [English](README.en.md)

**Last Updated**: 2026-03-18
