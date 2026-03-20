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

## 三、任务类型与宫位映射

| 任务类型 | 参与宫位 | 流程 |
|---------|---------|------|
| `video_process` | [1, 7, 5] | 数据采集 → TDD 验收 → 交付 |
| `file_download` | [1, 7, 5] | 下载 → 验收 → 交付 |
| `data_analysis` | [1, 3, 7, 5] | 采集 → 分析 → 验收 → 交付 |
| `skill_install` | [3, 7, 5] | 技术 → 验收 → 交付 |
| `content_create` | [4, 8, 7, 5] | 品牌 → 营销 → 验收 → 交付 |
| `monitoring` | [6, 9, 5] | 监控 → 生态 → 交付 |
| `legal_compliance` | [7, 5] | 法务 → 交付 |
| `general` | [5] | 中宫协调 |

---

## 四、任务优先级规则

| 优先级 | 触发条件 | 示例 |
|--------|---------|------|
| **CRITICAL** | 包含"现在"、"立刻"、"马上"、"紧急" | "现在处理这个" |
| **HIGH** | 包含"今天"、"尽快" | "今天内完成" |
| **MEDIUM** | 普通任务 | "帮我分析这个" |
| **LOW** | 可延后 | "有空时看看" |

---

## 五、TDD 闭环流程

```
┌─────────────────────────────────────────────────────────┐
│                  5 宫 TDD 任务闭环                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 收到余总指令                                         │
│     ↓                                                   │
│  2. 创建任务 → 状态=RED                                  │
│     ↓                                                   │
│  3. 调用 7 宫 → 红灯确认                                  │
│     ↓                                                   │
│  4. 调用 7 宫 → 定义验收标准                               │
│     ↓                                                   │
│  5. 指挥宫位执行 → 状态=RUNNING                          │
│     ↓                                                   │
│  6. 调用 7 宫 → 绿灯检查                                  │
│     ↓                                                   │
│  7. 通过 → 状态=GREEN → 交付                            │
│     ↓                                                   │
│  8. 失败 → 状态=RED → 返工                               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 六、与余总对话接口

### 主入口函数

```python
from skills.taiji-nine-palaces.palace_5_commander import handle_user_message

# 余总发送消息
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

## 七、系统监控

### 心跳监控（未来扩展）

```python
# 每 5 分钟检查一次
def heartbeat_check():
    commander = Palace5Commander()
    
    # 检查宫位负载
    palaces = commander.get_palace_states()
    for pid, pdata in palaces.items():
        if pdata["load"] > 0.9:
            send_alert(f"⚠️ {pid}宫负载过高：{pdata['load']}")
    
    # 检查阴阳平衡
    warnings = commander.detect_imbalances()
    if warnings:
        send_alert("\n".join(warnings))
```

### 任务报告

```python
report = commander.get_task_report()
# 返回：活跃任务数、完成任务数、最近 10 个任务
```

---

## 八、API 集成

### 调用太极 API

```python
# 更新宫位负载
requests.post(
    "http://localhost:8000/api/taiji/update-palace-load",
    json={"palace_id": 7, "load": 0.8}
)

# 正转（推进任务）
requests.post(
    "http://localhost:8000/api/zhengzhuan",
    json={"node_id": "7-tdd", "value": 0.9}
)

# 反转（反思检查）
requests.post(
    "http://localhost:8000/api/fanzhuan",
    json={"node_id": "7-tdd"}
)
```

---

## 九、升级历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v2.0 | 2026-03-18 | 新增 5 宫指挥官模块，集成 TDD 闭环 |
| v1.0 | - | 初始版本（API 查询） |

---

## 十、使用示例

### 示例 1：处理抖音视频任务

```python
from skills.taiji-nine-palaces.palace_5_commander import handle_user_message

result = handle_user_message("下载这个抖音链接并总结：https://v.douyin.com/xxx")

print(f"任务 ID: {result['task_id']}")
print(f"优先级：{result['priority']}")
print(f"参与宫位：{result['assigned_palaces']}")
```

### 示例 2：手动闭环管理

```python
from skills.taiji-nine-palaces.palace_5_commander import Palace5Commander
from skills.taiji-nine-palaces.palace_7_tdd import Palace7TDD

commander = Palace5Commander()
tdd = Palace7TDD()

# 1. 创建任务
task = commander.create_task(
    task_id="manual_001",
    description="分析数据",
    priority=TaskPriority.MEDIUM,
    assigned_palaces=[1, 3, 7]
)

# 2. 红灯确认
red = tdd.red_light_confirm("数据分析任务")

# 3. 定义标准
standards = tdd.define_acceptance_criteria("data_analysis")

# 4. 执行（调用各宫位）
# ... 实际执行逻辑 ...

# 5. 绿灯检查
output = "分析报告内容..."
result = tdd.green_light_check("data_analysis", output, standards)

if result["passed"]:
    commander.update_task_status("manual_001", TaskStatus.GREEN)
    print("✅ 绿灯通过，交付")
else:
    commander.update_task_status("manual_001", TaskStatus.RED)
    print(f"❌ 返工：{result['reasons']}")
```

---

## 十一、与 7 宫 TDD 的集成

```python
# 5 宫调用 7 宫的三个关键时刻

# 时刻 1: 任务开始时 - 红灯确认
red_confirm = tdd.red_light_confirm(task_description)

# 时刻 2: 定义验收标准
standards = tdd.define_acceptance_criteria(task_type, requirements)

# 时刻 3: 任务完成后 - 绿灯检查
check_result = tdd.green_light_check(task_type, output, standards)
```

---

**5 宫指挥官已就绪，等待余总指令。**
