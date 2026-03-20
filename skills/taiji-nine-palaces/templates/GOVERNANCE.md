# 太极管控体系（Governance）

---
version: 1.0.0
description: 管控能力 + 权限控制
***

## 管控架构

```
┌─────────────────────────────────────────────────────────────┐
│                    太极管控体系                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  管控能力（7宫-法务框架）                                      │
│  ├── RBAC（角色权限）                                        │
│  ├── 审批（红灯确认）                                         │
│  └── 审计（操作日志）                                         │
│                                                             │
│  权限控制（5宫-中央控制）                                      │
│  ├── L0 完全禁止（限制级）                                    │
│  ├── L1 人工审批（限制级）                                    │
│  ├── L2 通知确认（限制级）                                    │
│  ├── L3 米珞自主（5宫）                                       │
│  └── L4 8宫智能体自主                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

***

## 一、管控能力（7宫-法务框架）

### 1. RBAC（基于角色的访问控制）

```yaml
roles:
  commander:
    name: 主控
    palace: 5宫
    permissions: [dispatch, coordinate, monitor, report]
    
  worker:
    name: 执行者
    palaces: [1, 2, 3, 4, 6, 8, 9]
    permissions: [execute, report]
    
  validator:
    name: 验收者
    palace: 7宫
    permissions: [validate, audit, approve]
```

### 2. 审批流程（红灯确认）

```
任务到达
    ↓
7宫红灯检查
    ├── 风险评估
    ├── 标准定义
    └── 审批决策
    ↓
├── L0任务 → 拒绝，需余总审批
├── L1任务 → 等待人工确认
├── L2任务 → 执行后通知
└── L3+任务 → 自动执行
```

### 3. 审计日志

```yaml
audit_log:
  - timestamp: "2026-03-19T21:11:00"
    palace: 5
    action: dispatch
    target: palace-1
    task: "download_video"
    permission_level: L3
    result: success
    
  - timestamp: "2026-03-19T21:11:05"
    palace: 7
    action: validate
    task: "download_video"
    result: green_light
```

***

## 二、权限控制（L0-L4）

### 权限等级定义

| 等级 | 名称 | 执行者 | 行为 | 触发条件 |
|------|------|--------|------|----------|
| **L0** | 完全禁止 | - | 不执行，等待人工指令 | 敏感操作、首次任务、高风险 |
| **L1** | 人工审批 | - | 执行前必须人工确认 | 高风险操作、关键决策 |
| **L2** | 通知确认 | - | 执行后通知，可撤销 | 中等风险、重要任务 |
| **L3** | 自动执行 | **米珞（5宫）** | 自主执行，事后汇报 | **默认级别** |
| **L4** | 完全自主 | **8宫智能体** | 自主决策，无需汇报 | 低风险、重复任务 |

### 权限分布

```
┌─────────────────────────────────────────────────────────────┐
│                    权限等级分布                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  L0 完全禁止                                                 │
│     └─ 敏感操作：删除数据、外部发送、财务操作                   │
│                                                             │
│  L1 人工审批                                                 │
│     └─ 高风险：发布内容、修改配置、安装技能                     │
│                                                             │
│  L2 通知确认                                                 │
│     └─ 中等风险：代码提交、质量报告、竞品分析                   │
│                                                             │
│  L3 米珞自主 ━━━ 📍 5宫默认级别                               │
│     └─ 日常任务：数据采集、监控检查、任务调度                   │
│                                                             │
│  L4 8宫自主 ━━━ 各宫智能体                                    │
│     └─ 常规操作：监控运行、数据同步、日志记录                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 宫位权限表

| 宫位 | 默认权限 | 最高权限 | L0操作 | L1操作 | L2操作 | L3操作 | L4操作 |
|------|----------|----------|--------|--------|--------|--------|--------|
| 1宫 | L3 | L4 | - | 修改采集规则 | 批量下载 | 单次下载 | 自动抓取 |
| 2宫 | L2 | L3 | - | 修改评分标准 | 执行质检 | - | - |
| 3宫 | L2 | L3 | 删除文件 | 修改配置 | 提交代码 | 创建文件 | - |
| 4宫 | L2 | L3 | - | 发布战略 | 分析报告 | 采集竞品 | - |
| **5宫** | **L3** | **L4** | 删除宫位 | 调整架构 | 派发任务 | **默认** | 日常调度 |
| 6宫 | L4 | L4 | - | - | - | 调整阈值 | 监控运行 |
| 7宫 | L1 | L2 | - | 修改验收标准 | 执行验收 | - | - |
| 8宫 | L2 | L3 | - | 发布内容 | 创建内容 | 采集素材 | - |
| 9宫 | L3 | L4 | - | 修改研究范围 | 分析报告 | 数据采集 | 自动监控 |

***

## 三、权限与操作类型映射

### 操作风险等级

```yaml
operations:
  # L0 级别（完全禁止）
  delete_palace:
    risk: critical
    level: L0
    description: 删除宫位智能体
    
  external_send:
    risk: critical
    level: L0
    description: 发送数据到外部系统
    
  financial_operation:
    risk: critical
    level: L0
    description: 财务相关操作
    
  # L1 级别（人工审批）
  publish_content:
    risk: high
    level: L1
    description: 发布内容到外部平台
    
  install_skill:
    risk: high
    level: L1
    description: 安装新技能
    
  modify_config:
    risk: high
    level: L1
    description: 修改系统配置
    
  # L2 级别（通知确认）
  commit_code:
    risk: medium
    level: L2
    description: 提交代码
    
  quality_report:
    risk: medium
    level: L2
    description: 生成质量报告
    
  competitor_analysis:
    risk: medium
    level: L2
    description: 竞品分析
    
  # L3 级别（米珞自主）
  data_collection:
    risk: low
    level: L3
    description: 数据采集
    
  task_dispatch:
    risk: low
    level: L3
    description: 任务派发
    
  status_report:
    risk: low
    level: L3
    description: 状态汇报
    
  # L4 级别（8宫自主）
  monitoring:
    risk: minimal
    level: L4
    description: 监控运行
    
  log_sync:
    risk: minimal
    level: L4
    description: 日志同步
    
  auto_backup:
    risk: minimal
    level: L4
    description: 自动备份
```

***

## 四、审批流程

### L1 审批流程

```
任务到达 → 7宫风险评估 → 等待审批 → 人工确认 → 执行 → 记录审计
```

### L2 通知流程

```
任务到达 → 7宫风险评估 → 自动执行 → 通知余总 → 可撤销(5分钟内)
```

### L3 自动流程

```
任务到达 → Scene匹配 → 自动组队 → 执行 → 7宫验收 → 交付 → 审计记录
```

### L4 自主流程

```
触发器激活 → 宫位自主执行 → 记录日志 → 定期汇总汇报
```

***

## 五、审计能力

### 审计日志格式

```json
{
  "timestamp": "2026-03-19T21:11:00Z",
  "session_id": "agent:main:feishu:direct:xxx",
  "palace": 5,
  "action": "dispatch",
  "target_palace": 1,
  "task_type": "video_transcribe",
  "permission_level": "L3",
  "risk_level": "low",
  "result": "success",
  "duration_ms": 1234,
  "user_instruction": "下载这个视频"
}
```

### 审计查询

```bash
# 查询某宫操作记录
curl http://localhost:8000/api/audit?palace=1&days=7

# 查询高风险操作
curl http://localhost:8000/api/audit?level=L1,L0

# 查询失败操作
curl http://localhost:8000/api/audit?result=failed
```

***

## 六、权限升级与降级

### 升级条件

| 当前 | 目标 | 条件 |
|------|------|------|
| L0 | L1 | 余总手动授权 |
| L1 | L2 | 连续10次成功+无投诉 |
| L2 | L3 | 连续50次成功+验收通过率>95% |
| L3 | L4 | 连续100次成功+无错误+余总批准 |

### 降级触发

| 触发条件 | 降级结果 |
|----------|----------|
| 执行失败 | L3→L2 |
| 验收不通过 | L3→L2 |
| 重大错误 | L3→L1 |
| 数据泄露 | L4→L0 |

***

## 七、Clawith vs 太极 管控对比

| 维度 | Clawith | 太极 |
|------|---------|------|
| RBAC | 角色权限 | **7宫法务框架** |
| 审批 | 流程审批 | **红灯确认** |
| 审计 | 操作日志 | **宫位操作全记录** |
| 权限分级 | 3级 | **5级（L0-L4）** |
| 自主主体 | 无明确区分 | **L3米珞 + L4 8宫** |
| 升降级 | 无 | **动态调整机制** |