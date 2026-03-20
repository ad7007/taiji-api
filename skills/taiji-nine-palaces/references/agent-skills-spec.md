# Agent Skills 规范（Anthropic 标准）

---
version: 1.0.0
source: Anthropic Agent Skills Documentation
---

- 核心概念

Agent Skills 是一种通过结构化文件夹为 AI Agent 注入领域知识、操作流程与可执行代码的新范式。

---

- 目录结构

```
skill-name/
├── SKILL.md           # 必需：元数据 + 指令
├── scripts/           # 可选：可执行脚本
├── references/        # 可选：参考资料（扁平化）
└── assets/            # 可选：模板和资源
```

---

- SKILL.md 规范

-- 元数据（YAML）

```yaml
---
name: skill-name
version: 1.0.0
description: 简短描述
triggers:
  - 触发词1
  - 触发词2
---
```

-- 内容层级

| 标记 | 用途 |
|------|------|
| `-` | 一级标题 |
| `--` | 二级标题 |
| `---` | 分隔线 |
| `----` | 四级标题 |

-- 内容结构

```
- 概述
-- 什么是这个技能

- 触发条件
-- 何时使用

- 核心功能
-- 主要能力

- 使用示例
-- 代码示例

- 注意事项
-- 警告和限制
```

---

- 渐进式披露

-- 三层加载

| 层级 | 加载内容 | 用途 |
|------|---------|------|
| L1 发现 | name + description | 判断是否相关 |
| L2 激活 | 完整 SKILL.md | 执行任务 |
| L3 深度 | scripts/references/assets | 详细资料 |

-- 为什么渐进式

- 上下文窗口有限
- 避免一次性加载所有信息
- 按需加载，Token 经济

---

- 子目录规范

-- scripts/

```
scripts/
├── main.py        # 主脚本
├── helper.sh      # 辅助脚本
└── utils.py       # 工具函数
```

-- references/

```
references/
├── api-docs.md    # API 文档
├── cheatsheet.md  # 速查表
└── examples.md    # 示例
```

**注意**：references/ 必须扁平化，禁止子目录。

-- assets/

```
assets/
├── templates/
│   └── report.md
└── diagrams/
    └── flow.png
```

---

- 最佳实践

-- SKILL.md 行数

- 建议 < 500 行
- 详细内容放 references/
- 可执行逻辑放 scripts/

-- 文档结构

- 清晰的层级（`-` `--` `---`）
- 元数据在前
- 指令在后
- 示例最后

-- 可复用性

- 一个 Skill 做一件事
- 避免过度耦合
- 支持参数化

---

- 太极系统应用

-- 已实现

- ✅ 目录结构符合规范
- ✅ SKILL.md 使用 `-` `--` 层级
- ✅ templates/ 目录
- ✅ scripts/ 目录
- ✅ references/ 目录
- ✅ core/ 核心模块

-- 待优化

- SKILL.md 内容精简到 500 行以内
- references/ 文档完善
- 更多任务模板