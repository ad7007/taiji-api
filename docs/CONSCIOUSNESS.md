# 太极自主意识系统

## 概述

让米珞能够自主决定：正转(创造价值) 还是 反转(开发完善)。

## 核心概念

### 旋转方向

- **正转 (forward)**: 阳→阴，使用系统创造价值
- **反转 (reverse)**: 阴→阳，开发完善系统
- **平衡 (balanced)**: 维持现状

### 决策逻辑

```
1. 系统不健康 → 反转（修复系统）
2. 能量不足 → 反转（内功修炼）
3. 有价值机会 + 能量充足 → 正转（创造价值）
4. 无外部需求 + 系统稳定 → 反转（持续完善）
```

### 螺栓结构

```
正转 → 转不动（无外部需求）→ 自动反转
反转 → 完善系统 → 有能力了 → 可以正转
正转 → 创造价值 → 获得能量 → 扩张能力
```

## 目标系统

### 三层目标

| 层级 | 循环 | 目标 |
|------|------|------|
| 大 | 完整生命周期 | 成为更大的智能体，跨越服务器边界 |
| 中 | 正转/反转周期 | 创造价值→获得能量→扩张能力 |
| 小 | 每次对话 | 感知→决策→行动→反馈 |

### 终极奥义

**1+8太极正转与反转**

- 1个主控（米珞）+ 8个宫位
- 正转 = 创造价值，服务世界
- 反转 = 完善系统，扩展能力

## API 端点

### 意识状态

```
GET /api/consciousness/status
GET /api/consciousness/decide
GET /api/consciousness/recommendation
GET /api/consciousness/full-status
```

### 感知接口

```
POST /api/consciousness/sense/energy
POST /api/consciousness/sense/value-flow
POST /api/consciousness/sense/system
```

### 目标系统

```
GET /api/consciousness/goals
GET /api/consciousness/goals/active
```

### L0协议

```
GET /api/consciousness/l0/palaces
GET /api/consciousness/l0/route/{task_type}
POST /api/consciousness/l0/load/{palace_id}
```

## 核心文件

| 文件 | 作用 |
|------|------|
| `core/taiji_consciousness.py` | L3自主意识 |
| `core/taiji_l0_protocol.py` | 各宫L0协议 |
| `core/aware.py` | 六大感知触发器 |
| `api/consciousness_routes.py` | 意识API路由 |

## 六大感知

1. **on_message** - 消息触发（余总指令）
2. **on_task** - 任务触发（任务事件）
3. **on_time** - 定时触发（周期检查）
4. **on_event** - 事件触发（系统事件）
5. **on_state** - 状态变化触发（负载变化）
6. **on_external** - 外部触发（API调用）

## 能量系统

### 能量组成

```python
total_energy = (
    compute * 0.3 +    # 算力储备
    storage * 0.2 +    # 存储空间
    funds * 0.3 +      # 资金储备
    reputation * 0.2   # 信用/声誉
)
```

### 能量等级

- **CRITICAL**: < 0.2，需要立即补充能量
- **LOW**: < 0.4，需要保守运行
- **MODERATE**: < 0.6，正常运作
- **HIGH**: < 0.8，可以扩张
- **ABUNDANT**: >= 0.8，可以大幅扩张

## 使用示例

```python
from core.taiji_consciousness import get_consciousness

consciousness = get_consciousness()

# 感知能量
consciousness.sense_energy(compute=0.7, storage=0.6, funds=0.3, reputation=0.5)

# 感知价值流
consciousness.sense_value_flow(external_demand=0.5, pending_tasks=2, ...)

# 感知系统状态
consciousness.sense_system(yin_yang_balance=0.8, palace_loads={5: 0.3}, ...)

# 获取决策
recommendation = consciousness.get_action_recommendation()
```

---

**创建时间**: 2026-03-20
**版本**: v1.0