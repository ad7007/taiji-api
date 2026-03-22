# 5 宫 - 中央控制 · 中枢指挥模块

**模块路径**: `skills/taiji-nine-palaces/palace_5_commander.py`  
**创建时间**: 2026-03-18  
**状态**: 🟢 激活

---

## 一、核心职责

5 宫是太极系统的**中宫枢纽**，负责：

1. **与余总对话** - 感知意图、理解需求
2. **监控九宫状态** - 感知系统健康度
3. **任务优先级排序** - 决策资源分配
4. **按需调配宫位** - 指挥各宫参与
5. **任务闭环管理** - 红灯→执行→绿灯→交付

---

## 二、核心能力

### 2.1 感知层

```python
commander = Palace5Commander()

# 获取九宫状态
palaces = commander.get_palace_states()

# 获取阴阳平衡
balance = commander.get_balance_status()

# 检测失衡警告
warnings = commander.detect_imbalances()

# 获取可用宫位（负载<0.7）
available = commander.get_available_palaces()
```

### 2.2 决策层

```python
# 任务优先级判断
priority = commander.prioritize_task("余总指令")
# 返回：TaskPriority.CRITICAL / HIGH / MEDIUM / LOW

# 根据任务类型分配宫位
palaces = commander.assign_palaces("video_process")
# 返回：[1, 7, 5] - 数据采集 → TDD 验收 → 中宫交付
```

### 2.3 指挥层

```python
# 创建任务
task = commander.create_task(
    task_id="task_001",
    description="下载抖音视频并总结",
    priority=TaskPriority.HIGH,
    assigned_palaces=[1, 7, 5]
)

# 调用宫位执行
result = commander.invoke_palace(1, "download", {"url": "..."})
```

### 2.4 闭环管理（TDD 集成）

```python
# 完整闭环执行
execution = commander.execute_task_with_tdd("task_001")

# 绿灯交付
deliver_result = commander.green_light_deliver("task_001", output)
```

---

## 三、主入口函数

### handle_user_message(message: str) -> dict

**功能**: 余总消息的统一入口

```python
from skills.taiji-nine-palaces.palace_5_commander import handle_user_message

# 调用示例
result = handle_user_message("下载这个抖音视频并总结")

# 返回结构
{
    "task_id": "task_20260318094500",
    "priority": "HIGH",
    "assigned_palaces": [1, 7, 5],
    "system_status": {
        "palaces": {...},
        "balance": {...},
        "warnings": [...]
    },
    "execution": {
        "steps": [...]
    }
}
```

---

## 四、HTTP API 端点

```bash
# 九宫状态
GET http://localhost:8000/api/taiji/palaces

# 阴阳平衡
GET http://localhost:8000/api/taiji/balance

# 更新宫位负载
POST http://localhost:8000/api/taiji/update-palace-load
Body: {"palace_id": 7, "load": 0.8}

# 正转（推进任务）
POST http://localhost:8000/api/zhengzhuan
Body: {"node_id": "7-tdd", "value": 0.9}

# 反转（反思检查）
POST http://localhost:8000/api/fanzhuan
Body: {"node_id": "7-tdd"}
```

---

## 五、与 7 宫 TDD 的集成

```python
from skills.taiji-nine-palaces.palace_7_tdd import Palace7TDD

tdd = Palace7TDD()

# 时刻 1: 任务开始时 - 红灯确认
red_confirm = tdd.red_light_confirm(task_description)

# 时刻 2: 定义验收标准
standards = tdd.define_acceptance_criteria(task_type, requirements)

# 时刻 3: 任务完成后 - 绿灯检查
check_result = tdd.green_light_check(task_type, output, standards)
```

---

**5 宫指挥官已就绪，等待余总指令。**
