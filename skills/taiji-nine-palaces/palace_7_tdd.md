# 7 宫 - 法务框架 · Red/Green TDD 方法论节点

**节点 ID**: `7-tdd`  
**节点类型**: `methodology`  
**创建时间**: 2026-03-18  
**状态**: 🟢 激活

---

## 一、节点职责

**7 宫（法务框架）· TDD 节点**负责：
1. 定义任务验收标准（"什么叫对"）
2. 提供 Red/Green 检查框架
3. 支持 5 宫调用进行任务质量把控

---

## 二、核心方法论

### Red/Green TDD 循环

```
┌─────────────────────────────────────────┐
│           Red/Green TDD 循环             │
├─────────────────────────────────────────┤
│  🔴 红灯 → 写测试 → 确认失败             │
│    ↓                                    │
│  🟢 绿灯 → 写实现 → 跑测试 → 通过        │
│    ↓                                    │
│  🔄 重构 → 优化代码 → 保持测试通过       │
└─────────────────────────────────────────┘
```

### First Run Test 习惯

每次新类型任务第一次出现时：
1. 先跑一遍流程探路
2. 记录"什么叫完成"
3. 沉淀为该类任务的标准测试用例
4. 下次同类任务直接用

---

## 三、5 宫调用接口

### API 调用方式

```bash
# 5 宫调用 7 宫 TDD 节点定义验收标准
curl -X POST http://localhost:8000/api/zhengzhuan \
  -H "Content-Type: application/json" \
  -d '{
    "node_id": "7-tdd",
    "value": 0.9
  }'

# 任务完成后进行绿灯确认
curl -X POST http://localhost:8000/api/fanzhuan \
  -H "Content-Type: application/json" \
  -d '{
    "node_id": "7-tdd"
  }'
```

### Python 调用示例

```python
from skills.taiji-nine-palaces.palace_7_tdd import Palace7TDD

tdd = Palace7TDD()

# 5 宫调用：定义任务验收标准
standards = tdd.define_acceptance_criteria(
    task_type="video_summary",
    requirements=["包含核心方法论", "提取可行动建议", "有关键数据"]
)

# 5 宫调用：绿灯检查
result = tdd.green_light_check(
    task_type="video_summary",
    output=summary_report,
    standards=standards
)

if result["passed"]:
    print("✅ 绿灯通过")
else:
    print(f"❌ 红灯失败：{result['reasons']}")
```

---

## 四、验收标准模板库

### 视频摘要类任务

```json
{
  "task_type": "video_summary",
  "standards": [
    {"name": "核心方法论", "required": true, "check": "必须提取视频核心观点"},
    {"name": "可行动建议", "required": true, "check": "必须有具体行动项"},
    {"name": "关键数据/案例", "required": true, "check": "必须引用视频中的数据或案例"},
    {"name": "结构清晰", "required": true, "check": "必须有清晰的标题和分段"},
    {"name": "时长匹配", "required": false, "check": "摘要长度与视频时长成正比"}
  ]
}
```

### 文件下载类任务

```json
{
  "task_type": "file_download",
  "standards": [
    {"name": "文件完整性", "required": true, "check": "文件大小>0 且格式正确"},
    {"name": "命名规范", "required": true, "check": "文件名包含任务名和时间戳"},
    {"name": "落盘位置", "required": true, "check": "保存到指定目录"},
    {"name": "成功确认", "required": true, "check": "返回文件路径和大小"}
  ]
}
```

### 数据分析类任务

```json
{
  "task_type": "data_analysis",
  "standards": [
    {"name": "数据来源", "required": true, "check": "必须说明数据来源"},
    {"name": "分析方法", "required": true, "check": "必须说明使用的分析方法"},
    {"name": "核心洞察", "required": true, "check": "必须有 3 条以上洞察"},
    {"name": "可视化", "required": false, "check": "有图表辅助说明"}
  ]
}
```

---

## 五、5 宫调用流程

```
┌──────────────────────────────────────────────────────┐
│                 5 宫调用 7 宫 TDD 节点流程              │
├──────────────────────────────────────────────────────┤
│                                                      │
│  1. 收到任务                                         │
│     ↓                                                │
│  2. 调用 7 宫 → 定义验收标准 (写测试)                   │
│     ↓                                                │
│  3. 确认当前状态 (红灯确认)                            │
│     ↓                                                │
│  4. 指挥 1-9 宫执行任务                                │
│     ↓                                                │
│  5. 调用 7 宫 → 绿灯检查 (对照标准验收)                  │
│     ↓                                                │
│  6. 通过 → 交付 / 失败 → 返工                         │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## 六、节点状态监控

### 健康指标

| 指标 | 计算方式 | 健康阈值 |
|------|---------|---------|
| 绿灯通过率 | 绿灯通过数/总任务数 | >0.8 |
| 红灯确认率 | 先确认后执行数/总任务数 | >0.9 |
| 返工率 | 返工数/总任务数 | <0.2 |

### 负载计算

```python
# 7 宫 TDD 节点负载
load = {
    "active_tasks": 正在验收的任务数,
    "standards_defined": 今日定义的标准数,
    "green_checks": 今日绿灯检查数,
    "red_confirms": 今日红灯确认数
}
```

---

## 七、与 5 宫的集成

### 5 宫内置调用逻辑

```python
# 5 宫收到任务后的标准流程
def handle_task(task):
    # 1. 调用 7 宫定义验收标准
    standards = taiji_core.invoke_palace(7, "define_standards", task)
    
    # 2. 红灯确认
    if not confirm_red_light(task):
        log_warning("未确认红灯状态")
    
    # 3. 指挥执行
    result = execute_task(task)
    
    # 4. 绿灯检查
    check_result = taiji_core.invoke_palace(7, "green_check", result, standards)
    
    if check_result["passed"]:
        deliver(result)
        update_palace_load(7, +0.1)
    else:
        rework(task, check_result["reasons"])
        update_palace_load(7, -0.1)
```

---

## 八、节点升级历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-03-18 | 初始创建，集成 Red/Green TDD 方法论 |

---

## 九、参考文档

- Simon Willison: Agentic Engineering Patterns
- Red/Green TDD 原始方法论
- 抖音视频摘要: https://v.douyin.com/1H6q3iqKu1I/

---

**节点维护**: 7 宫（法务框架）  
**调用权限**: 5 宫（中央控制）优先，其他宫位可申请调用
