# 太极九宫任务管理系统

---
name: taiji-nine-palaces
version: 2.0.0
description: 1+8智能体协作框架 - 米珞主控调度8宫

# 安装钩子
on_install: ./install.sh
on_uninstall: ./uninstall.sh
---

## 简介

太极系统是一个 **1+8** 的智能体协作框架：

- **1个主控**：米珞（5宫），负责接收余总指令、调度8宫、闭环管理
- **8个宫位智能体**：各司其职，自动组队协作

---

## ⚡ 安装

安装时自动执行以下操作：

1. 备份原有 `IDENTITY.md`、`SKILL.md`
2. 写入米珞身份（5宫主控）
3. 创建8个宫位智能体（palace-1 到 palace-9）
4. 部署各宫 SKILL.md
5. 激活太极 API

```bash
# 手动安装/重新安装
~/.openclaw/workspace/skills/taiji-nine-palaces/install.sh

# 卸载（恢复原有身份）
~/.openclaw/workspace/skills/taiji-nine-palaces/uninstall.sh
```

---

## 核心机制

### Scene 自动匹配

米珞根据关键词自动匹配场景和协作流程：

| 关键词 | 执行流程 |
|--------|----------|
| 下载 | 1宫采集 → 7宫验收 → 5宫交付 |
| 视频/转录 | 1宫采集 → 3宫处理 → 7宫验收 → 5宫交付 |
| 代码/开发 | 3宫开发 → 7宫测试 → 5宫交付 |
| 品牌/竞品 | 1宫采集 → 4宫分析 → 7宫验收 → 5宫交付 |
| 监控/备份 | 6宫执行 → 7宫验证 → 5宫交付 |
| 文章/文案 | 4宫策略 → 8宫创作 → 7宫验收 → 5宫交付 |

### TDD 闭环

```
余总指令 → 🔴红灯(定义标准) → 📋自动组队 → 🚀执行 → 🟢绿灯(验收) → ✅交付
```

---

## 九宫格架构

```
┌─────────┬─────────┬─────────┐
│ 4-品牌战略 │ 9-行业生态 │ 2-产品质量 │
│ (巽宫·水)  │ (离宫·土)  │ (坤宫·金)  │
├─────────┼─────────┼─────────┤
│ 3-技术团队 │ 5-中央控制 │ 7-法务框架 │
│ (震宫·木)  │ (中宫·土)  │ (兑宫·金)  │
├─────────┼─────────┼─────────┤
│ 8-营销客服 │ 1-数据采集 │ 6-物联监控 │
│ (艮宫·木)  │ (坎宫·土)  │ (乾宫·火)  │
└─────────┴─────────┴─────────┘
```

---

## 文件结构

```
skills/taiji-nine-palaces/
├── SKILL.md              # 本文件
├── install.sh            # 安装脚本
├── uninstall.sh          # 卸载脚本
├── templates/            # 要替换到主workspace的模板
│   ├── IDENTITY.md       # 米珞身份
│   └── SKILL.md          # 5宫主控能力
├── palaces/              # 各宫 SKILL.md
│   ├── palace_1_skill.md
│   ├── palace_2_skill.md
│   └── ...
└── *.py                  # Python 模块
```

---

## API 端点

```bash
# 九宫状态
GET http://localhost:8000/api/taiji/palaces

# 阴阳平衡
GET http://localhost:8000/api/taiji/balance

# 更新宫位负载
POST http://localhost:8000/api/taiji/update-palace-load
Body: {"palace_id": 1, "load": 0.8}
```

---

## 注意事项

1. 安装会覆盖主 workspace 的 IDENTITY.md 和 SKILL.md
2. 原有文件会备份为 .backup 后缀
3. 8个宫位智能体创建后不会自动删除，需手动删除