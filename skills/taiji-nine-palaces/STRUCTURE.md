# 太极系统目录规范

---
version: 2.0.0
updated: 2026-03-19
standard: Agent Skills (Anthropic)
---

## 一、根目录结构

```
~/.openclaw/workspace/
├── IDENTITY.md           # 主控身份（米珞）
├── SKILL.md              # 主控能力定义
├── RELATIONSHIP.md       # 太极关系图
├── GOVERNANCE.md         # 管控体系
├── SOUL.md               # 行为准则
├── USER.md               # 用户信息（余总）
├── AGENTS.md             # 系统说明（本文件）
├── MEMORY.md             # 长期记忆
├── TOOLS.md              # 工具配置
├── HEARTBEAT.md          # 心跳任务
├── memory/               # 日常记忆
│   └── YYYY-MM-DD.md
└── skills/               # 技能目录
    └── taiji-nine-palaces/
```

---

## 二、技能目录结构

遵循 Agent Skills 标准：

```
skills/taiji-nine-palaces/
├── SKILL.md                    # 必需：技能入口
├── install.sh                  # 安装脚本
├── uninstall.sh                # 卸载脚本
│
├── templates/                  # 模板文件（安装时复制）
│   ├── IDENTITY.md
│   ├── SKILL.md
│   ├── RELATIONSHIP.md
│   └── GOVERNANCE.md
│
├── palaces/                    # 各宫 SKILL.md
│   ├── palace_1_skill.md
│   ├── palace_2_skill.md
│   ├── palace_3_skill.md
│   ├── palace_4_skill.md
│   ├── palace_6_skill.md
│   ├── palace_7_skill.md
│   ├── palace_8_skill.md
│   ├── palace_9_skill.md
│   └── SCENE_REGISTRY.md
│
├── scripts/                    # 可执行脚本
│   ├── taiji.sh                # CLI 入口
│   ├── init_task.py            # 任务初始化
│   └── balance_check.py        # 平衡检查
│
├── references/                 # 参考资料（扁平化）
│   ├── api-docs.md             # API 文档
│   ├── scene-guide.md          # Scene 使用指南
│   ├── permission-matrix.md    # 权限矩阵
│   └── wuxing-rules.md         # 五行规则
│
├── assets/                     # 静态资源
│   ├── templates/              # 任务模板
│   │   ├── task-report.md
│   │   └── audit-log.json
│   └── diagrams/               # 架构图
│       └── relationship.png
│
├── core/                       # 核心模块
│   ├── governance.py           # 管控体系
│   ├── aware.py                # 感知系统
│   └── relationship.py         # 关系图
│
└── archive/                    # 历史版本
    └── v1.0/
```

---

## 三、SKILL.md 规范

### 3.1 元数据（YAML）

```yaml
---
name: skill-name
version: 1.0.0
description: 简短描述（用于发现阶段）
author: 作者
triggers:                       # 触发词
  - 关键词1
  - 关键词2
on_install: ./install.sh        # 安装钩子
on_uninstall: ./uninstall.sh    # 卸载钩子
---
```

### 3.2 内容结构

```markdown
# 标题

## 描述（用于激活判断）

## 触发条件

## 核心功能

## 使用示例

## 接口规范

## 注意事项
```

### 3.3 行数限制

- SKILL.md < 500 行
- 详细内容放 references/
- 可执行逻辑放 scripts/

---

## 四、渐进式披露

```
┌─────────────────────────────────────────────────────────────┐
│                    渐进式披露层级                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  L1 发现阶段（启动时）                                        │
│     └─ 只加载：name + description                           │
│     └─ 目的：判断是否相关                                    │
│                                                             │
│  L2 激活阶段（匹配时）                                        │
│     └─ 加载：完整 SKILL.md                                   │
│     └─ 目的：执行任务                                        │
│                                                             │
│  L3 深度阶段（需要时）                                        │
│     └─ 加载：scripts/ + references/ + assets/               │
│     └─ 目的：获取详细资料或执行脚本                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 五、任务管理结构（规划）

```
tasks/
├── active/                    # 活跃任务
│   └── task_YYYYMMDD_HHMMSS/
│       ├── task.md            # 任务定义
│       ├── status.json        # 状态追踪
│       ├── logs/              # 执行日志
│       └── outputs/           # 输出文件
│
├── completed/                 # 已完成任务
│   └── task_XXX/
│
└── templates/                 # 任务模板
    ├── video-transcribe.md
    ├── data-analysis.md
    └── report-generation.md
```

---

## 六、命名规范

### 文件命名

| 类型 | 规范 | 示例 |
|------|------|------|
| SKILL | 大写 + .md | `SKILL.md` |
| 宫位 | palace_N_小写 | `palace_1_skill.md` |
| 脚本 | 小写 + 扩展名 | `init_task.py` |
| 文档 | 小写 + 连字符 | `api-docs.md` |
| 模板 | 小写 + 连字符 | `task-report.md` |

### 目录命名

| 类型 | 规范 | 示例 |
|------|------|------|
| 技能 | 小写 + 连字符 | `taiji-nine-palaces` |
| 子目录 | 小写 | `scripts/`, `references/` |
| 宫位 | palace-N | `palace-1/` |

---

## 七、版本控制

```
archive/
├── v1.0/
│   ├── SKILL.md
│   └── core/
├── v1.1/
└── CHANGELOG.md
```

---

## 八、检查清单

### 新建技能时

- [ ] SKILL.md < 500 行
- [ ] 元数据完整（name, version, description）
- [ ] references/ 扁平化（无子目录）
- [ ] scripts/ 可执行
- [ ] assets/ 静态资源

### 安装时

- [ ] 备份原有文件
- [ ] 创建必要的目录
- [ ] 设置权限
- [ ] 验证安装