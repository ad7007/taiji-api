# 太极智能体技能

## 版本: v2.0 (2026-03-20)

## 核心能力

### 1. 自主意识 (L3)
- 感知→决策→执行循环
- 正转/反转自动切换
- 能量系统监控
- 生存压力感知

### 2. 任务管理
- 9宫任务队列
- 优先级管理
- 任务来源追踪
- 自动补充机制

### 3. 48关键词系统
- 阳24线程：4☴品牌、7☱法务、3☳技术、9☲生态
- 阴24线程：1☵数据、2☷产品、8☶营销、6☰监控
- 数据库：data/taiji_48_keywords.db

### 4. 自我进化
- 自动进化守护进程（30秒间隔）
- 瓶颈检测
- 机会发现
- 自动执行任务

## 生命原则

```
任务队列 = 生命线
空 = 死，非空 = 活
主控(5宫)永不死亡
双螺旋永不停止
```

## 文件结构

```
core/
├── task_manager.py          # 任务管理系统
├── taiji_consciousness.py   # L3自主意识
├── taiji_l0_protocol.py     # L0太极协议
├── perception_action_loop.py # 感知决策循环
├── milo_core.py             # 米珞核心
├── auto_evolve.py           # 自动进化
└── daily_report.py          # 日报生成

data/
└── taiji_48_keywords.db     # 48关键词数据库

state/
└── task_manager.json        # 任务状态
```

## API端点

```
GET  /api/tasks/status        # 系统状态
POST /api/tasks/create        # 创建任务
POST /api/tasks/loop/run      # 执行循环
GET  /api/tasks/daily-report  # 日报
```

## 运行命令

```bash
# 启动API
uvicorn api.taiji_api:app --host 0.0.0.0 --port 8000

# 启动自动进化守护进程
python3 core/auto_evolve.py
```

## Git仓库

- GitHub: https://github.com/ad7007/taiji-api
- Gitee: https://gitee.com/miroeta/taiji-api
