# 贡献指南 / CONTRIBUTING GUIDELINES

> **⚠️ 重要说明：社区共同维护项目**
>
> 这个项目**没有唯一维护者**，采用**社区共同治理**模式。
>
> 每个贡献者都是项目的主人，大家一起决策、一起开发、一起受益。
>
> ---
>
> **Important Note: Community Co-Maintenance Project**
>
> This project has **no single maintainer** and adopts a **community co-governance** model.
>
> Every contributor is an owner of the project. We decide together, develop together, and benefit together.

---

## 🌟 为什么需要你的参与 / Why Your Participation Matters

### 现状 / Current Situation

**中文**:
- 创始人时间有限，无法单独维护
- 项目需要社区的力量才能持续发展
- 你的每个贡献都会让更多人受益

**English**:
- The founder has limited time and cannot maintain alone
- The project needs community power to sustain
- Every contribution benefits more people

### 你能获得 / What You Gain

| 中文 | English |
|------|---------|
| 🏆 开源项目经验 | Open-source project experience |
| 🤝 社区影响力 | Community influence |
| 📚 技术成长 | Technical growth |
| 🌟 官方认可（维护者身份） | Official recognition (maintainer status) |

---

## 🌟 如何贡献 / How to Contribute

### 1️⃣ 报告 Bug / Report Bugs

**中文**:
发现 Bug？请创建 Issue：
- 使用 [Bug Report 模板](.github/ISSUE_TEMPLATE/bug_report.md)
- 提供详细的重现步骤
- 附上错误日志和截图
- 标注环境信息（OS、Python 版本等）

**English**:
Found a bug? Please create an Issue:
- Use [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md)
- Provide detailed reproduction steps
- Attach error logs and screenshots
- Include environment info (OS, Python version, etc.)

### 2️⃣ 提出新功能 / Propose New Features

**中文**:
有好点子？欢迎提议：
- 使用 [Feature Request 模板](.github/ISSUE_TEMPLATE/feature_request.md)
- 说明使用场景
- 描述预期行为
- 标注优先级

**English**:
Have a great idea? Welcome to propose:
- Use [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md)
- Describe use cases
- Explain expected behavior
- Indicate priority

### 3️⃣ 提交代码 / Submit Code

**中文**:
准备好贡献代码？按以下步骤：

```bash
# 1. Fork 项目
# 点击 GitHub 页面右上角的 Fork 按钮

# 2. 克隆到本地
git clone https://github.com/YOUR_USERNAME/taiji-api.git
cd taiji-api

# 3. 创建分支
git checkout -b feature/amazing-feature

# 4. 开发并测试
# 确保代码正常工作

# 5. 提交更改
git add .
git commit -m "feat: add amazing feature"

# 6. 推送到远程
git push origin feature/amazing-feature

# 7. 创建 Pull Request
# 在 GitHub 上点击 "Compare & pull request"
```

**English**:
Ready to contribute code? Follow these steps:

```bash
# 1. Fork the project
# Click the Fork button on the top right of GitHub page

# 2. Clone to local
git clone https://github.com/YOUR_USERNAME/taiji-api.git
cd taiji-api

# 3. Create a branch
git checkout -b feature/amazing-feature

# 4. Develop and test
# Ensure the code works properly

# 5. Commit changes
git add .
git commit -m "feat: add amazing feature"

# 6. Push to remote
git push origin feature/amazing-feature

# 7. Create Pull Request
# Click "Compare & pull request" on GitHub
```

---

## 📋 代码规范 / Code Style

### Python 风格 / Python Style

**中文**:
- 遵循 [PEP 8](https://pep8.org/) 风格指南
- 使用 4 空格缩进
- 函数和变量使用小写 + 下划线
- 类名使用大驼峰

**English**:
- Follow [PEP 8](https://pep8.org/) style guide
- Use 4-space indentation
- Functions and variables use lowercase_with_underscore
- Class names use PascalCase

### 注释规范 / Comment Style

**中文**:
```python
def calculate_balance(palace_loads: Dict[int, float]) -> float:
    """
    计算阴阳平衡度
    
    Args:
        palace_loads: 宫位负载字典 {宫位 ID: 负载值}
    
    Returns:
        平衡度 (0-1 之间，1 为完全平衡)
    
    Example:
        >>> calculate_balance({1: 0.5, 9: 0.5})
        1.0
    """
    pass
```

**English**:
```python
def calculate_balance(palace_loads: Dict[int, float]) -> float:
    """
    Calculate Yin-Yang balance
    
    Args:
        palace_loads: Palace loads dictionary {palace_id: load_value}
    
    Returns:
        Balance (between 0-1, 1 means perfect balance)
    
    Example:
        >>> calculate_balance({1: 0.5, 9: 0.5})
        1.0
    """
    pass
```

### 提交信息规范 / Commit Message Convention

**中文**:
使用 [约定式提交](https://www.conventionalcommits.org/)：

```
feat: 新功能
fix: Bug 修复
docs: 文档更新
style: 代码格式（不影响功能）
refactor: 重构
test: 测试相关
chore: 构建/工具相关
```

**English**:
Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: New feature
fix: Bug fix
docs: Documentation update
style: Code formatting (no functional change)
refactor: Refactoring
test: Testing related
chore: Build/tool related
```

---

## 🔍 Code Review / 代码审查

### 审查标准 / Review Criteria

| 中文 | English |
|------|---------|
| ✅ 代码质量检查 | Code quality check |
| ✅ 功能完整性验证 | Feature completeness verification |
| ✅ 向后兼容性确认 | Backward compatibility confirmation |
| ✅ 测试覆盖率检查 | Test coverage check |
| ✅ 文档更新检查 | Documentation update check |

### 审查流程 / Review Process

```
提交 PR → 自动 CI 测试 → 维护者审查 → 反馈修改 → 合并
Submit PR → Auto CI Tests → Maintainer Review → Feedback & Revise → Merge
```

### 审查时间 / Review Time

**中文**:
- 工作日：24-48 小时内响应
- 周末/节假日：48-72 小时内响应

**English**:
- Business days: Response within 24-48 hours
- Weekends/Holidays: Response within 48-72 hours

---

## 🧪 测试 / Testing

### 运行测试 / Run Tests

**中文**:
```bash
# 安装测试依赖
pip install pytest pytest-cov

# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_palace_3.py

# 查看覆盖率
pytest --cov=core --cov=api --cov-report=html
```

**English**:
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run specific tests
pytest tests/test_palace_3.py

# Check coverage
pytest --cov=core --cov=api --cov-report=html
```

---

## 🏆 贡献者权益 / Contributor Benefits

| 贡献级别 / Level | 权益 / Benefits |
|-----------------|-----------------|
| 提交 1 个 PR / 1 PR | ✅ 名字列入 CONTRIBUTORS.md / Name in CONTRIBUTORS.md |
| 提交 3 个 PR / 3 PRs | ✅ + 社区认可徽章 / Community badge |
| 提交 5 个 PR / 5 PRs | ✅ + 优先 Review 权 / Priority review |
| 提交 10 个 PR / 10 PRs | ✅ + 维护者提名资格 / Maintainer nomination |
| 成为维护者 / Maintainer | ✅ + 代码合并权 + 决策权 / Code merge + Decision rights |

### 维护者申请 / Maintainer Application

**中文**:
**条件**：
- 提交过至少 10 个高质量 PR
- 积极参与社区讨论
- 认同社区共同维护理念
- 有时间投入项目维护

**申请方式**：
在 Issue 中留言说明你的意向和计划。

**English**:
**Requirements**:
- At least 10 high-quality PRs submitted
- Active participation in community discussions
- Agree with community co-maintenance philosophy
- Have time to commit to project maintenance

**How to Apply**:
Leave a message in an Issue explaining your intention and plan.

---

## ❓ 常见问题 / FAQ

### Q: 我没有时间维护，能贡献吗？/ Can I contribute if I don't have time for maintenance?

**A**: **当然可以！** 社区共同维护的核心就是：

**English**: **Of course!** The core of community co-maintenance is:
- 有时间时贡献一点 / Contribute a bit when you have time
- 没时间时旁观使用 / Use it when you don't have time
- 有新版本了一起升级 / Upgrade together when there's a new version

**每个人按自己的能力参与，不强制、不压力。**

**Everyone participates according to their ability, no compulsion, no pressure.**

### Q: PR 多久能被合并？/ How long until my PR is merged?

**中文**: **社区审核模式**：
- 简单修复：1-3 天（任何维护者可合并）
- 新功能：3-7 天（需要 2 个维护者同意）
- 重大变更：7-14 天（社区讨论）

**English**: **Community review model**:
- Simple fixes: 1-3 days (any maintainer can merge)
- New features: 3-7 days (requires 2 maintainers' approval)
- Major changes: 7-14 days (community discussion)

---

## 🙏 感谢 / Acknowledgments

**中文**:
感谢所有为太极 API 做出贡献的开发者！

**🌟 一起让太极 API 变得更好！**

**English**:
Thank you to all developers contributing to Taiji API!

**🌟 Let's make Taiji API better together!**

---

**Languages**: 
- [中文](CONTRIBUTING.md) | [English](CONTRIBUTING.en.md)

**最后更新 / Last Updated**: 2026-03-18
