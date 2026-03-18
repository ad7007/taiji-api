# 更新日志 (Changelog)

本文档记录太极 API 的所有重要更新。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [2.0.0] - 2026-03-18 ✅ 已发布

### ✨ Added

#### L4 规则层
- **5 宫指挥官** - 感知→决策→调配→闭环完整流程
- **7 宫 TDD 验收** - 红灯确认→标准定义→绿灯检查
- 任务自动优先级排序
- 宫位动态调配规则

#### 3 宫模型分配
- **Zero Token 模式** - 零成本调用主流 AI 模型
- 支持 Claude/DeepSeek/GPT/Gemini/Qwen
- 自动成本优化
- 优先级驱动分配

#### 1 宫数据采集
- **Crawlee 集成** - 智能数据抓取
- **双模式切换** - HTTP 快速 + 浏览器渲染
- **防封禁特性** - IP 轮换、鼠标模拟、UA 轮换
- 代理池支持

#### 定时备份
- 中午 12 点 + 晚上 23 点自动备份
- Rclone 云端存储支持
- 本地 + 云端双重备份

#### 社区治理
- 社区共同维护模式
- 创始人权限保留
- 维护者招募计划
- 中英双语文档

### 🔧 Changed
- 九宫格负载自动调节
- 阴阳平衡检测优化
- API 响应性能提升

### 📚 Documentation
- README.md / README.en.md - 完整项目说明
- CONTRIBUTING.md / CONTRIBUTING.en.md - 贡献指南
- GOVERNANCE.md / GOVERNANCE.en.md - 社区治理模式
- FOUNDER_STATEMENT.md / FOUNDER_STATEMENT.en.md - 创始人声明
- ROADMAP.md / ROADMAP_V2.1.md - 项目路线图
- ABOUT.en.md - 项目详细介绍
- CHANGELOG.md - 版本更新日志
- CODE_OF_CONDUCT.md - 行为准则
- SECURITY.md - 安全策略
- docs/API_EXAMPLES.md - API 使用示例
- docs/INTERNATIONALIZATION.md - 国际化指南
- MAINTAINERS_WANTED.md - 维护者招募
- QUICK_START_CONTRIBUTE.md - 快速开始指南

### 🏛️ Community
- MIT 许可证
- Issue/PR 模板
- 行为准则
- 社区共同维护模式
- 创始人权限保留

### 🚀 Deployment
- Dockerfile
- docker-compose.yml
- requirements.txt (完整依赖)
- .gitignore

---

## [未发布]

---

## [2.0.0] - 2026-03-18

### ✨ Added

#### L4 规则层
- **5 宫指挥官** - 感知→决策→调配→闭环完整流程
- **7 宫 TDD 验收** - 红灯确认→标准定义→绿灯检查
- 任务自动优先级排序
- 宫位动态调配规则

#### 3 宫模型分配
- **Zero Token 模式** - 零成本调用主流 AI 模型
- 支持 Claude/DeepSeek/GPT/Gemini/Qwen
- 自动成本优化
- 优先级驱动分配

#### 1 宫数据采集
- **Crawlee 集成** - 智能数据抓取
- **双模式切换** - HTTP 快速 + 浏览器渲染
- **防封禁特性** - IP 轮换、鼠标模拟、UA 轮换
- 代理池支持

#### 定时备份
- 中午 12 点 + 晚上 23 点自动备份
- Rclone 云端存储支持
- 本地 + 云端双重备份

### 🔧 Changed
- 九宫格负载自动调节
- 阴阳平衡检测优化
- API 响应性能提升

### 📚 Documentation
- README.md - 完整项目说明
- CONTRIBUTING.md - 贡献指南
- GOVERNANCE.md - 社区治理模式
- ROADMAP.md - 项目路线图
- MAINTAINERS_WANTED.md - 维护者招募
- QUICK_START_CONTRIBUTE.md - 快速开始

### 🏛️ Community
- MIT 许可证
- Issue/PR 模板
- 行为准则
- 社区共同维护模式

---

## [1.0.0] - 2026-01-15

### ✨ Added

#### 核心功能
- 九宫格任务管理 API
- 阴阳平衡检测
- 五行循环验证
- 六爻引擎基础

#### API 端点
- `/api/taiji/palaces` - 获取九宫状态
- `/api/taiji/balance` - 阴阳平衡检查
- `/api/taiji/update-palace-load` - 更新宫位负载
- `/api/taiji/switch-mode` - 切换阴阳模式

#### 基础架构
- FastAPI 框架
- 异步支持
- 自动文档（Swagger/ReDoc）
- 日志系统（Loguru）

---

## [0.1.0] - 2025-12-01

### ✨ Added
- 项目初始化
- 基础九宫格概念验证
- 简单 API 原型

---

## 版本说明

### 语义化版本

遵循 `MAJOR.MINOR.PATCH` 格式：

- **MAJOR** (2.x.x): 不兼容的 API 变更
- **MINOR** (x.2.x): 向后兼容的功能新增
- **PATCH** (x.x.2): 向后兼容的问题修复

### 发布周期

- **PATCH**: 随时（Bug 修复）
- **MINOR**: 每月 1 次
- **MAJOR**: 每季度 1 次

---

## 🤝 贡献

欢迎提交 PR 更新此文件！

**格式示例**:

```markdown
## [X.X.X] - YYYY-MM-DD

### Added
- 新功能描述

### Changed
- 变更描述

### Fixed
- Bug 修复描述

### Removed
- 移除的功能描述
```

---

**[未发布]**: 等待发布的新功能  
**[2.0.0]**: 2026-03-18 - L4 规则层 + 社区共同维护  
**[1.0.0]**: 2026-01-15 - 首次正式发布  
**[0.1.0]**: 2025-12-01 - 项目初始化
