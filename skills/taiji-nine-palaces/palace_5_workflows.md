# 5 宫 - 工作流程 · 任务映射与 TDD 闭环

**模块路径**: `skills/taiji-nine-palaces/palace_5_commander.py`  
**创建时间**: 2026-03-18  
**状态**: 🟢 激活

---

## 一、任务类型与宫位映射

| 任务类型 | 参与宫位 | 流程 | 适用场景 |
|---------|---------|---------|---------|
| `video_process` | [1, 7, 5] | 采集→验收→交付 | 视频下载+摘要 |
| `file_download` | [1, 7, 5] | 下载→验收→交付 | 文件下载任务 |
| `data_analysis` | [1, 3, 7, 5] | 采集→分析→验收→交付 | 数据分析 |
| `skill_install` | [3, 7, 5] | 技术→验收→交付 | 安装技能 |
| `content_create` | [4, 8, 7, 5] | 品牌→营销→验收→交付 | 文案创作 |
| `monitoring` | [6, 9, 5] | 监控→生态→交付 | 系统监控 |
| `legal_compliance` | [7, 5] | 法务→交付 | 合规检查 |
| `general` | [5] | 中宫协调 | 通用任务 |

---

## 二、任务优先级规则

| 优先级 | 触发关键词 | 时间要求 |
|--------|-----------|---------|
| **CRITICAL** | "现在"、"立刻"、"马上"、"紧急" | 立即执行 |
| **HIGH** | "今天"、"尽快"、"优先" | 当日完成 |
| **MEDIUM** | 普通指令 | 常规处理 |
| **LOW** | "有空"、"稍后"、"看看" | 可延后 |

```python
class TaskPriority(Enum):
    CRITICAL = 4   # 紧急
    HIGH = 3       # 高
    MEDIUM = 2     # 中
    LOW = 1        # 低

def prioritize_task(message: str) -> TaskPriority:
    msg = message.lower()
    if any(kw in msg for kw in ["现在", "立刻", "马上", "紧急"]):
        return TaskPriority.CRITICAL
    elif any(kw in msg for kw in ["今天", "尽快", "优先"]):
        return TaskPriority.HIGH
    elif any(kw in msg for kw in ["有空", "稍后", "看看"]):
        return TaskPriority.LOW
    else:
        return TaskPriority.MEDIUM
```

---

## 三、TDD 闭环流程

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

## 四、使用示例

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

### 示例 3：系统监控

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

---

## 五、任务报告

```python
report = commander.get_task_report()
# 返回：活跃任务数、完成任务数、最近 10 个任务
```

---

## 六、升级历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v2.0 | 2026-03-18 | 新增 5 宫指挥官模块，集成 TDD 闭环 |
| v1.0 | - | 初始版本（API 查询） |

---

**5 宫工作流程文档已就绪**
