# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your`re` specifics — the stuff that's unique to your setup.

---

## 太极九宫任务管理系统

**执行模式**: 本地直接执行（不依赖API）

**Skill位置**: `/root/.openclaw/workspace/skills/taiji-nine-palaces/`

### 快速开始

```python
import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/taiji-nine-palaces')
from local_client import get_client

client = get_client()

# 九宫状态
palaces = client.get_all_palaces()

# 六爻探测
result = client.detect_yao("API延迟很高，连接超时")

# 场景组队
team = client.build_team("download")
```

---

### 核心模块 (core/)

| 模块 | 功能 | 状态 |
|------|------|------|
| `taiji_algorithm.py` | N宫组合算法 | ✅ |
| `milo_core.py` | 米珞组队能力 | ✅ |
| `taiji_consciousness.py` | 自主意识系统 | ✅ |
| `taiji_heartbeat.py` | 心跳机制 | ✅ |
| `taiji_l0_protocol.py` | L0协议 | ✅ |
| `l4_rule_engine.py` | L4规则层 | ✅ |
| `task_manager.py` | 任务管理 | ✅ |
| `task_dispatch.py` | 任务分发 | ✅ |
| `six_yao_engine.py` | 六爻引擎 | ✅ |
| `yao_learning_db.py` | 六爻学习 | ✅ |
| `yao_state_persistence.py` | 爻位持久化 | ✅ |
| `palace_hexagrams.py` | 宫位卦象 | ✅ |
| `taiji_decision_engine.py` | 决策引擎 | ✅ |
| `taiji_perception.py` | 感知系统 | ✅ |
| `idle_detector.py` | 空闲检测 | ✅ |
| `ralph_wiggum_loop.py` | AI循环 | ✅ |
| `taiji_wuxing_loop.py` | 五行循环 | ✅ |
| `perception_action_loop.py` | 感知-行动循环 | ✅ |
| `taiji_24_threads.py` | 24线程系统 | ✅ |
| `thread_24_system.py` | 线程系统 | ✅ |
| `daily_report.py` | 日报 | ✅ |
| `taiji_chatbot.py` | 聊天机器人 | ✅ |
| `taiji_evolution.py` | 演化系统 | ✅ |
| `auto_evolve.py` | 自动演化 | ✅ |

---

### 宫位模块

| 宫位 | 文件 | 功能 |
|------|------|------|
| 1宫 | `palace_1_data_collection.py` | 数据采集 |
| 2宫 | `palace_2_product.py` | 产品质量 |
| 3宫 | `palace_3_tech.py` | 技术团队 |
| 4宫 | `palace_4_brand.py` | 品牌战略 |
| 5宫 | `palace_5_commander.py` | 中央控制 |
| 6宫 | `palace_6_monitor.py` | 物联监控 |
| 7宫 | `palace_7_tdd.py` | 法务框架 |
| 8宫 | `palace_8_marketing.py` | 营销客服 |
| 9宫 | `palace_9_ecology.py` | 行业生态 |

---

### 六爻关键词

**统计**: 358 个关键词，覆盖 9宫 × 6爻

**5宫 (OpenClaw本体) 六爻**:
| 爻位 | 阴阳 | 功能域 | 关键词数 |
|------|------|--------|----------|
| 1爻 | 阴 | 会话管理 | 7 |
| 2爻 | 阳 | 工具调用 | 8 |
| 3爻 | 阴 | 模型推理 | 7 |
| 4爻 | 阳 | 记忆系统 | 6 |
| 5爻 | 阴 | 技能系统 | 6 |
| 6爻 | 阳 | 服务状态 | 7 |

---

### 插件系统 (plugins/)

| 插件 | 功能 |
|------|------|
| `free_models_plugin.py` | 智谱/DeepSeek免费模型 |

---

### 场景映射

| 关键词 | 场景 | 默认组队 |
|--------|------|----------|
| 下载 | download | 1→5→9 |
| 代码/开发 | code | 3→5→7 |
| 品牌/竞品 | brand | 4→5→6 |
| 抓取/采集 | scrape | 1→5→9 |
| 转录 | transcribe | 1→5→9 |
| 质量/检查 | quality | 2→5→7 |

---

### 太极API（对外接口）

**地址**: `http://localhost:8000`

- 仅供外部系统调用
- 米珞内部使用本地客户端

---

## GitHub 配置（3 宫）

GITHUB_TOKEN="" # 已移除敏感信息

---

## 定时备份配置（6 宫）

BACKUP_SCHEDULE_NOON="0 12 * * *"
BACKUP_SCHEDULE_NIGHT="0 23 * * *"
RCLONE_CONFIG="gdrive"
BACKUP_RETENTION_DAYS=30
BACKUP_LOCAL_KEEP=7