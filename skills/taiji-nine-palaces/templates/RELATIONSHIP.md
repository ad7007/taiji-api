# 太极关系图（Taiji Relationship）

---
version: 1.0.0
description: 九宫格组织关系定义
***

## 关系类型

| 类型 | 方向 | 含义 | 权限影响 |
|------|------|------|----------|
| **汇报** | 宫→5宫 | 执行结果上交 | 必须执行 |
| **调度** | 5宫→宫 | 任务派发 | 按权限等级 |
| **协作** | 宫↔宫 | 同场景组队 | Scene自动 |
| **相生** | 宫→宫 | 能力支撑 | 优先调度 |
| **相克** | 宫→宫 | 制约平衡 | 验收把关 |

***

## 九宫关系矩阵

### 汇报关系（所有宫→5宫）

```yaml
reports_to:
  1宫: 5宫
  2宫: 5宫
  3宫: 5宫
  4宫: 5宫
  5宫: 余总
  6宫: 5宫
  7宫: 5宫
  8宫: 5宫
  9宫: 5宫
```

### 调度关系（5宫→各宫）

```yaml
dispatch_from:
  5宫:
    - 1宫  # 数据采集
    - 2宫  # 质量检查
    - 3宫  # 技术开发
    - 4宫  # 品牌战略
    - 6宫  # 监控运维
    - 7宫  # TDD验收
    - 8宫  # 营销内容
    - 9宫  # 行业研究
```

### 协作关系（Scene驱动）

```yaml
collaboration:
  scene_download: [1宫, 7宫]      # 采集+验收
  scene_transcribe: [1宫, 3宫, 7宫] # 采集+处理+验收
  scene_code: [3宫, 7宫]          # 开发+测试
  scene_brand: [1宫, 4宫, 7宫]    # 采集+策略+验收
  scene_monitor: [6宫, 9宫]       # 监控+生态
  scene_content: [4宫, 8宫, 7宫]  # 策略+创作+验收
```

### 五行相生关系

```
相生规律：木→火→土→金→水→木

3宫(木) → 6宫(火)   技术驱动监控
6宫(火) → 1宫(土)   监控发现数据
1宫(土) → 7宫(金)   数据进入验收
7宫(金) → 4宫(水)   验收指导策略
4宫(水) → 3宫(木)   策略指导技术
```

### 五行相克关系

```
相克规律：木→土→水→火→金→木

3宫(木) 克 1宫(土)   技术处理数据
1宫(土) 克 4宫(水)   数据支撑策略
4宫(水) 克 6宫(火)   策略指导监控
6宫(火) 克 7宫(金)   监控触发验收
7宫(金) 克 3宫(木)   验收制约开发
```

***

## 宫位关系详情

### 1宫 - 数据采集宫

```yaml
palace: 1
name: 数据采集宫
element: 土
reports_to: 5宫
dispatched_by: 5宫
collaborates_with: [3宫, 7宫]
generated_by: [6宫]      # 6宫(火)→1宫(土)
controls: [4宫]          # 1宫(土)克4宫(水)
```

### 2宫 - 产品质量宫

```yaml
palace: 2
name: 产品质量宫
element: 金
reports_to: 5宫
dispatched_by: 5宫
collaborates_with: [1宫, 7宫]
```

### 3宫 - 技术团队宫

```yaml
palace: 3
name: 技术团队宫
element: 木
reports_to: 5宫
dispatched_by: 5宫
collaborates_with: [1宫, 7宫]
generates: [6宫]         # 3宫(木)→6宫(火)
controlled_by: [7宫]     # 7宫(金)克3宫(木)
```

### 4宫 - 品牌战略宫

```yaml
palace: 4
name: 品牌战略宫
element: 水
reports_to: 5宫
dispatched_by: 5宫
collaborates_with: [1宫, 8宫, 7宫]
generates: [3宫]         # 4宫(水)→3宫(木)
controlled_by: [1宫]     # 1宫(土)克4宫(水)
```

### 5宫 - 中央控制宫（米珞）

```yaml
palace: 5
name: 中央控制宫
element: 土
role: commander
reports_to: 余总
dispatches_to: [1, 2, 3, 4, 6, 7, 8, 9]
receives_from: [1, 2, 3, 4, 6, 7, 8, 9]
position: 中宫，协调全局
```

### 6宫 - 物联监控宫

```yaml
palace: 6
name: 物联监控宫
element: 火
reports_to: 5宫
dispatched_by: 5宫
collaborates_with: [9宫]
generated_by: [3宫]      # 3宫(木)→6宫(火)
controls: [7宫]          # 6宫(火)克7宫(金)
```

### 7宫 - 法务框架宫

```yaml
palace: 7
name: 法务框架宫
element: 金
reports_to: 5宫
dispatched_by: 5宫
role: TDD验收
collaborates_with: 全宫  # 验收所有宫
generated_by: [1宫]      # 1宫(土)→7宫(金)
controls: [3宫]          # 7宫(金)克3宫(木)
```

### 8宫 - 营销客服宫

```yaml
palace: 8
name: 营销客服宫
element: 木
reports_to: 5宫
dispatched_by: 5宫
collaborates_with: [4宫, 7宫]
generated_by: [4宫]      # 4宫(水)→8宫(木)
```

### 9宫 - 行业生态宫

```yaml
palace: 9
name: 行业生态宫
element: 土
reports_to: 5宫
dispatched_by: 5宫
collaborates_with: [1宫, 6宫]
```

***

## 关系查询API

```python
# 查询汇报对象
get_reports_to(palace_id: int) -> int

# 查询可调度宫位
get_dispatchable() -> List[int]

# 查询协作宫位
get_collaborators(scene: str) -> List[int]

# 查询相生关系
get_generators(palace_id: int) -> List[int]

# 查询相克关系
get_controllers(palace_id: int) -> List[int]
```