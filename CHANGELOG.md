# 太极九宫API v1.1.0 更新日志

## [v1.1.0] - 2026-03-21

### 新增功能

#### 1. 本地数据库系统
- `taiji_database.json` - 完整的九宫数据库
- `taiji_db_client.py` - 51个客户端方法

#### 2. 48线程感知系统
- 双重阴阳：宫位阴阳 × 爻位阴阳
- 四层感知：阴宫阴爻/阴宫阳爻/阳宫阴爻/阳宫阳爻
- 288个状态关键词

#### 3. 任务管理系统
- `assign_task()` - 米珞分配任务
- `get_all_pending_tasks()` - 查看所有待办
- `update_task_status()` - 更新任务状态
- `complete_palace_task()` - 完成并汇报

#### 4. 自动组队
- `build_team()` - 根据任务描述自动组队
- 11个任务场景
- 255种宫位组合

#### 5. 汇报机制
- 宫位完成任务后自动汇报给5宫
- 汇报历史记录

### 八宫自主机制

每个宫位都有：
- 双螺栓目标（完善自己 + 完成任务）
- 6爻感知系统
- 任务队列（TODO）
- 汇报机制

### API端点

```
GET  /api/taiji/palaces          # 获取所有宫位
GET  /api/taiji/palaces/{id}     # 获取宫位详情
GET  /api/taiji/stats            # 系统统计
GET  /api/taiji/scan             # 48线程扫描
GET  /api/taiji/rotate           # 旋转决策
GET  /api/taiji/tasks            # 所有待办
POST /api/taiji/tasks/assign     # 分配任务
PUT  /api/taiji/tasks/{id}       # 更新任务
POST /api/taiji/team/build       # 自动组队
GET  /api/taiji/scenes           # 任务场景
GET  /api/taiji/reports          # 宫位汇报
GET  /api/taiji/skills           # 所有技能
GET  /api/taiji/consciousness    # 意识系统
GET  /api/taiji/threads          # 48线程映射
```

### 技术细节

- 数据库大小：470KB
- 宫位：9个（8个智能体 + 1个中宫）
- 状态：48个工作状态
- 技能：25个可调用
- 组合：255种

---

*发布：米珞(5宫) | 时间：2026-03-21*