# L4 规则层集成文档

**版本**: v1.0  
**创建时间**: 2026-03-18  
**位置**: `/root/taiji-api-v2/core/l4_rule_engine.py`

---

## 一、架构概述

L4 规则层是太极 API 的**智能决策层**，集成：
- **5 宫指挥官机制**（感知→决策→调配→闭环）
- **7 宫 TDD 验收机制**（红灯→执行→绿灯→交付）

```
┌─────────────────────────────────────────────────┐
│              太极 API 架构                        │
├─────────────────────────────────────────────────┤
│  L1: HTTP 端点 (taiji_api.py)                    │
│  L2: 任务管理 (TaskManager)                      │
│  L3: 核心逻辑 (taiji_logic_engine)              │
│  L4: 规则引擎 (l4_rule_engine) ← 本层           │
│  L5: 数据采集 (palace_1_data_collection)        │
└─────────────────────────────────────────────────┘
```

---

## 二、核心规则

### 规则 1: 5 宫感知规则

#### 1.1 任务优先级检测
```python
# 关键词 → 优先级映射
CRITICAL: ["现在", "立刻", "马上", "紧急", "优先"]
HIGH:     ["今天", "尽快", "优先处理"]
MEDIUM:   普通指令
LOW:      ["有空", "不着急", "延后"]
```

#### 1.2 任务类型推断
```python
# 关键词 → 任务类型映射
video_process:   ["视频", "抖音", "摘要", "转录"]
file_download:   ["下载", "文件", "pdf"]
data_analysis:   ["分析", "数据", "报告"]
skill_install:   ["技能", "安装", "插件"]
...
```

#### 1.3 宫位可用性检测
```python
# 可用宫位 = 负载 < 0.7
available_palaces = [pid for pid, cap in capacities.items() 
                     if cap.current_load < 0.7]
```

#### 1.4 阴阳失衡检测
```python
# 平衡对: 4-5, 3-6, 2-1, 7-9
# 失衡 = 平衡度 < 0.6
balance = min(load1, load2) / max(load1, load2)
```

---

### 规则 2: 5 宫决策规则

#### 2.1 宫位分配
```python
TASK_PALACE_MAPPING = {
    "video_process":   [1, 7, 5],  # 采集→验收→交付
    "file_download":   [1, 7, 5],
    "data_analysis":   [1, 3, 7, 5],
    "skill_install":   [3, 7, 5],
    "content_create":  [4, 8, 7, 5],
    "monitoring":      [6, 9, 5],
    "legal_compliance":[7, 5],
    "general":         [5]
}
```

#### 2.2 任务创建
```python
task = TaskDefinition(
    task_id=f"task_{timestamp}",
    description=command,
    priority=detect_task_priority(command),
    assigned_palaces=assign_palaces(task_type)
)
```

---

### 规则 3: 7 宫 TDD 规则

#### 3.1 红灯确认
```python
def red_light_confirm(task):
    return {
        "confirmed": True,
        "message": f"红灯确认：任务未开始 - {task.description}",
        "task_status": TaskStatus.RED.value
    }
```

#### 3.2 定义验收标准
```python
TDD_STANDARDS_TEMPLATES = {
    "video_process": [
        TDDStandard("核心方法论", True, "必须提取视频核心观点"),
        TDDStandard("可行动建议", True, "必须有具体行动项"),
        TDDStandard("关键数据/案例", True, "必须引用数据或案例"),
        TDDStandard("结构清晰", True, "必须有清晰标题和分段")
    ],
    "file_download": [...],
    ...
}
```

#### 3.3 绿灯检查
```python
def green_light_check(task, output):
    for std in task.tdd_standards:
        # 基于关键词的简单规则检查
        if std.name == "结构清晰" and "##" in output:
            std.passed = True
        elif std.name == "核心方法论" and "核心" in output:
            std.passed = True
        ...
    
    return {
        "passed": all(s.passed for s in standards if s.required),
        "reasons": [f"{s.name}: {s.check}" for s in standards if not s.passed and s.required]
    }
```

---

### 规则 4: 闭环管理规则

#### 4.1 启动任务
```python
def start_task(task_id):
    task.status = TaskStatus.RUNNING
    task.started_at = time.time()
    # 增加宫位负载
    for pid in task.assigned_palaces:
        _increase_palace_load(pid, 0.05)
```

#### 4.2 完成任务
```python
def complete_task(task_id, output):
    check_result = green_light_check(task, output)
    
    if check_result["passed"]:
        task.status = TaskStatus.GREEN
        task.completed_at = time.time()
        task.output = output
        return {"status": "delivered", ...}
    else:
        task.status = TaskStatus.RED
        task.rework_count += 1
        return {"status": "rework", "reasons": check_result["reasons"]}
```

---

### 规则 5: 自适应规则

#### 5.1 动态优先级调整
```python
def adjust_priority(task_id, elapsed_minutes):
    if elapsed_minutes > 60:
        return TaskPriority.CRITICAL  # 等待超 1 小时→紧急
    elif elapsed_minutes > 30:
        return TaskPriority(task.priority.value - 1)  # 提升一级
    return task.priority
```

#### 5.2 宫位负载平衡
```python
def balance_palace_loads():
    avg_load = sum(loads) / len(loads)
    overloaded = [pid for pid, load in loads.items() if load > 0.8]
    underloaded = [pid for pid, load in loads.items() if load < 0.4]
    
    return {
        "average_load": avg_load,
        "overloaded": overloaded,
        "underloaded": underloaded,
        "suggestion": f"考虑分配给宫位：{underloaded}"
    }
```

---

## 三、API 端点

### 3.1 5 宫指挥官入口

```bash
POST /api/l4/command
Content-Type: application/json

{
  "command": "下载这个抖音视频并总结"
}

Response:
{
  "task_id": "task_20260318100725",
  "priority": "MEDIUM",
  "task_type": "video_process",
  "assigned_palaces": [1, 7, 5],
  "tdd_standards": [...],
  "red_confirm": {...},
  "status": "ready_to_execute"
}
```

### 3.2 7 宫绿灯检查入口

```bash
POST /api/l4/complete
Content-Type: application/json

{
  "task_id": "task_20260318100725",
  "output": "# 视频摘要\n\n## 核心方法论\n..."
}

Response:
{
  "status": "delivered",
  "check_result": {
    "passed": true,
    "details": [...]
  }
}

或返工:
{
  "status": "rework",
  "reasons": ["关键数据/案例：必须引用视频中的数据或案例"],
  "rework_count": 1
}
```

### 3.3 状态查询入口

```bash
GET /api/l4/status

Response:
{
  "tasks": {
    "active_tasks": 2,
    "completed_tasks": 5,
    "recent_tasks": [...]
  },
  "palace_loads": {
    "1": 0.55,
    "5": 0.60,
    "7": 0.65,
    ...
  },
  "balance": {
    "average_load": 0.58,
    "overloaded": [],
    "underloaded": [],
    "suggestion": "负载均衡良好"
  }
}
```

---

## 四、使用示例

### 示例 1: 完整任务闭环

```python
import requests

# 1. 5 宫接收指令
response = requests.post(
    "http://localhost:8000/api/l4/command",
    json={"command": "今天内分析这份数据"}
)
task_id = response.json()["task_id"]
# 返回：priority=HIGH, assigned_palaces=[1,3,7,5]

# 2. 执行任务（调用各宫位）
# ... 实际执行逻辑 ...
output = "数据分析报告..."

# 3. 7 宫绿灯检查
response = requests.post(
    "http://localhost:8000/api/l4/complete",
    json={"task_id": task_id, "output": output}
)

if response.json()["status"] == "delivered":
    print("✅ 绿灯通过，交付")
else:
    print(f"❌ 返工：{response.json()['reasons']}")
```

### 示例 2: 查询系统状态

```python
# 查询 L4 状态
response = requests.get("http://localhost:8000/api/l4/status")
status = response.json()

print(f"活跃任务：{status['tasks']['active_tasks']}")
print(f"平均负载：{status['balance']['average_load']:.2f}")
print(f"建议：{status['balance']['suggestion']}")
```

---

## 五、TDD 验收标准模板

### video_process（视频处理）

| 标准名 | 必需 | 检查规则 |
|--------|------|---------|
| 核心方法论 | ✅ | 包含"核心"、"方法"、"关键"、"TDD"、"测试" |
| 可行动建议 | ✅ | 包含"建议"、"行动"、"步骤"、"先"、"然后" |
| 关键数据/案例 | ✅ | 包含"数据"、"案例"、"美元"、"$"、"一周"、"工程师" |
| 结构清晰 | ✅ | 包含"##"或换行符 |

### file_download（文件下载）

| 标准名 | 必需 | 检查规则 |
|--------|------|---------|
| 文件完整性 | ✅ | 输出长度>100 |
| 命名规范 | ✅ | 包含时间戳格式 |
| 落盘位置 | ✅ | 包含路径信息 |

### data_analysis（数据分析）

| 标准名 | 必需 | 检查规则 |
|--------|------|---------|
| 数据来源 | ✅ | 包含"来源"、"来自" |
| 分析方法 | ✅ | 包含"方法"、"分析"、"使用" |
| 核心洞察 | ✅ | 包含"洞察"、"发现"、"结论"且数量≥3 |

### skill_install（技能安装）

| 标准名 | 必需 | 检查规则 |
|--------|------|---------|
| 技能来源 | ✅ | 包含"skillhub"或"clawhub" |
| 版本信息 | ✅ | 包含版本号格式 (vX.X.X) |
| 依赖检查 | ✅ | 包含"依赖"、"安装" |
| 功能验证 | ✅ | 包含"测试"、"验证" |

---

## 六、与 OpenClaw 集成

### 5 宫指挥官 Python 调用

```python
from skills.taiji-nine-palaces.palace_5_commander import Palace5Commander

commander = Palace5Commander()

# 调用 L4 API
result = commander.handle_user_message("下载这个 PDF 并分析")

# 返回结构与 API 一致
print(f"任务 ID: {result['task_id']}")
print(f"参与宫位：{result['assigned_palaces']}")
```

### 7 宫 TDD Python 调用

```python
from skills.taiji-nine-palaces.palace_7_tdd import Palace7TDD

tdd = Palace7TDD()

# 定义标准
standards = tdd.define_acceptance_criteria("video_process")

# 绿灯检查
result = tdd.green_light_check("video_process", output, standards)

if result["passed"]:
    print("✅ 交付")
else:
    print(f"❌ 返工：{result['reasons']}")
```

---

## 七、监控与调试

### 日志查看

```bash
# API 日志
tail -f /root/taiji-api-v2/taiji_api.log

# L4 引擎日志（集成在 API 日志中）
grep "L4" /root/taiji-api-v2/taiji_api.log
```

### 状态检查

```bash
# 检查 L4 引擎状态
curl http://localhost:8000/api/l4/status | jq

# 检查任务报告
curl http://localhost:8000/api/l4/status | jq '.tasks'
```

### 重启服务

```bash
# 重启太极 API（加载 L4 规则）
cd /root/taiji-api-v2
pkill -f "uvicorn.*taiji_api"
nohup venv/bin/python -m uvicorn api.taiji_api:app --host 0.0.0.0 --port 8000 >> taiji_api.log 2>&1 &
```

---

## 八、扩展指南

### 添加新任务类型

1. 在 `TASK_TYPE_KEYWORDS` 中添加关键词
2. 在 `TASK_PALACE_MAPPING` 中定义宫位分配
3. 在 `TDD_STANDARDS_TEMPLATES` 中定义验收标准

```python
# 示例：添加"report_generate"任务类型
TASK_TYPE_KEYWORDS["report_generate"] = ["报告", "report", "生成"]
TASK_PALACE_MAPPING["report_generate"] = [1, 3, 7, 5]
TDD_STANDARDS_TEMPLATES["report_generate"] = [
    TDDStandard("数据准确", True, "必须引用准确数据"),
    TDDStandard("结论清晰", True, "必须有明确结论"),
    ...
]
```

### 自定义验收规则

修改 `green_light_check` 方法中的规则逻辑：

```python
# 添加自定义检查
if std.name == "自定义标准":
    passed = custom_check_function(output)
```

---

## 九、版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-03-18 | 初始版本，集成 5 宫指挥官和 7 宫 TDD |

---

**L4 规则层已就绪，5 宫指挥官可调用。**
