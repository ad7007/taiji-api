# 太极九宫任务管理系统 - OpenClaw 集成技能

## 快速开始

### 1. 检查 API 服务状态

```bash
# 健康检查
curl http://localhost:8000/health

# 或使用命令行工具
./taiji.sh status
```

### 2. 查看所有宫位状态

```bash
# 使用命令行工具
./taiji.sh palaces

# 或使用 Python 客户端
python3 taiji_client.py
```

### 3. 更新宫位负载

```bash
# 设置 5-中央控制 负载为 0.8
./taiji.sh load 5 0.8

# 批量更新
curl -X POST http://localhost:8000/api/taiji/batch-update-palaces \
  -H "Content-Type: application/json" \
  -d '{"palaces": [{"palace_id": 3, "load": 0.6}, {"palace_id": 5, "load": 0.9}]}'
```

### 4. 切换模式

```bash
# 切换到阳模式（任务推进）
./taiji.sh mode yang

# 切换到阴模式（Ask 模式）
./taiji.sh mode yin
```

## 九宫格布局

```
┌─────────┬─────────┬─────────┐
│ 4-品牌战略 │ 9-行业生态 │ 2-产品质量 │
│ (巽宫·木)  │ (离宫·土)  │ (坤宫·金)  │
├─────────┼─────────┼─────────┤
│ 3-技术团队 │ 5-中央控制 │ 7-法务框架 │
│ (震宫·木)  │ (中宫·土)  │ (兑宫·金)  │
├─────────┼─────────┼─────────┤
│ 8-营销客服 │ 1-数据采集 │ 6-物联监控 │
│ (艮宫·木)  │ (坎宫·土)  │ (乾宫·火)  │
└─────────┴─────────┴─────────┘
```

## 核心概念

### 两仪模式
- **阳_正转** - 任务推进模式，主动执行
- **阴_反转** - Ask 模式，智能体会议

### 四象阶段
- **阳_规划** - Planning，发散愿景 → 收敛承诺
- **阴_执行** - Daily，执行同步 → 障碍暴露
- **阳_展示** - Review，展示成果 → 收集反馈
- **阴_沉淀** - Retro，反思改进 → 文化沉淀

### 阴阳平衡对
| 平衡对 | 宫位 | 矛盾 |
|--------|------|------|
| team_process | 4 vs 5 | 灵活性 vs 标准化 |
| tech_quality | 3 vs 6 | 速度 vs 稳定 |
| product_data | 2 vs 1 | 需求 vs 数据 |
| monitor_eco | 7 vs 9 | 度量 vs 报告 |

### 五行循环
- **金** - 收敛：收集执行数据
- **水** - 流动：分析问题根因
- **木** - 生长：生成改进方案
- **火** - 发散：实施优化措施
- **土** - 承载：沉淀经验知识

## API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/state` | GET | 获取太极系统状态 |
| `/api/taiji/palaces` | GET | 获取所有宫位状态 |
| `/api/taiji/palace/{id}` | GET | 获取单个宫位状态 |
| `/api/taiji/update-palace-load` | POST | 更新宫位负载 |
| `/api/taiji/batch-update-palaces` | POST | 批量更新宫位 |
| `/api/taiji/balance` | GET | 获取阴阳平衡状态 |
| `/api/taiji/adjust-balance` | POST | 手动调整平衡 |
| `/api/taiji/switch-mode` | POST | 切换阳/阴模式 |
| `/api/taiji/advance-symbols` | POST | 推进四象阶段 |
| `/api/taiji/five-elements` | POST | 运行五行循环 |
| `/api/taiji/status` | GET | 获取引擎状态 |
| `/api/taiji/reset-engine` | POST | 重置引擎 |
| `/api/zhengzhuan` | POST | 正转操作 |
| `/api/fanzhuan` | POST | 反转操作 |

## Python 客户端使用

```python
from taiji_client import TaijiClient, display_palaces, display_balance

client = TaijiClient()

# 获取所有宫位
palaces = client.get_all_palaces()
print(display_palaces(palaces))

# 更新宫位负载
result = client.update_palace_load(5, 0.8)
print(result)

# 查看平衡状态
balance = client.get_balance_status()
print(display_balance(balance))

# 切换模式
client.switch_mode("yang")
```

## 文件结构

```
taiji-nine-palaces/
├── SKILL.md           # 技能定义
├── README.md          # 使用文档
├── taiji_client.py    # Python 客户端
├── taiji.sh           # 命令行工具
└── references/        # 参考资料
```

## 注意事项

1. API 服务必须运行在 `localhost:8000`
2. 负载值范围：0.0 - 1.0
3. 宫位 ID 范围：1 - 9
4. 模式选择：`yang` 或 `yin`
5. 平衡度 < 0.7 时会触发告警
