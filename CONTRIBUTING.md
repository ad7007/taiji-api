# 贡献指南

> **⚠️ 重要说明：社区共同维护项目**
>
> 这个项目**没有唯一维护者**，采用**社区共同治理**模式。
>
> 每个贡献者都是项目的主人，大家一起决策、一起开发、一起受益。

感谢你对太极 API 项目的兴趣！你的参与让这个项目变得更好。

---

## 🌟 为什么需要你的参与

**现状**：
- 创始人时间有限，无法单独维护
- 项目需要社区的力量才能持续发展
- 你的每个贡献都会让更多人受益

**你能获得**：
- 🏆 开源项目经验
- 🤝 社区影响力
- 📚 技术成长
- 🌟 官方认可（维护者身份）

---

## 🌟 如何贡献

### 1️⃣ 报告 Bug

发现 Bug？请创建 Issue：

- 使用 [Bug Report 模板](.github/ISSUE_TEMPLATE/bug_report.md)
- 提供详细的重现步骤
- 附上错误日志和截图
- 标注环境信息（OS、Python 版本等）

### 2️⃣ 提出新功能

有好点子？欢迎提议：

- 使用 [Feature Request 模板](.github/ISSUE_TEMPLATE/feature_request.md)
- 说明使用场景
- 描述预期行为
- 标注优先级

### 3️⃣ 提交代码

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

---

## 📋 代码规范

### Python 风格

- 遵循 [PEP 8](https://pep8.org/) 风格指南
- 使用 4 空格缩进
- 函数和变量使用小写 + 下划线
- 类名使用大驼峰

### 注释规范

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

### 提交信息规范

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

**示例**:
```
feat: 添加 3 宫模型分配功能
fix: 修复 5 宫负载计算错误
docs: 更新 README 安装说明
```

---

## 🔍 Code Review

所有 PR 都需要经过 Code Review：

### 审查标准

- ✅ 代码质量检查
- ✅ 功能完整性验证
- ✅ 向后兼容性确认
- ✅ 测试覆盖率检查
- ✅ 文档更新检查

### 审查流程

```
提交 PR → 自动 CI 测试 → 维护者审查 → 反馈修改 → 合并
```

### 审查时间

- 工作日：24-48 小时内响应
- 周末/节假日：48-72 小时内响应

---

## 🧪 测试

### 运行测试

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

### 编写测试

```python
def test_model_allocation():
    """测试模型分配功能"""
    allocator = Palace3ModelAllocator()
    result = allocator.allocate_model("video_process", priority=1)
    
    assert result.model is not None
    assert result.access_mode in ["api_token", "zero_token"]
```

---

## 📖 文档

### 文档类型

- **API 文档** - 自动生成（Swagger/OpenAPI）
- **用户文档** - README.md
- **开发文档** - CONTRIBUTING.md
- **架构文档** - docs/architecture.md

### 文档更新

如果 PR 包含以下变更，请更新文档：

- ✅ 新增 API 端点
- ✅ 修改配置项
- ✅ 变更使用方式
- ✅ 废弃旧功能

---

## 🏆 贡献者权益

| 贡献级别 | 权益 |
|---------|------|
| 提交 1 个 PR | ✅ 名字列入 CONTRIBUTORS.md |
| 提交 3 个 PR | ✅ + 社区认可徽章 |
| 提交 5 个 PR | ✅ + 优先 Review 权 |
| 提交 10 个 PR | ✅ + 维护者提名资格 |
| 成为维护者 | ✅ + 代码合并权 + 决策权 |

### 维护者申请 📢

**条件**：
- 提交过至少 10 个高质量 PR
- 积极参与社区讨论
- 认同社区共同维护理念
- 有时间投入项目维护

**申请方式**：
在 Issue 中留言说明你的意向和计划。

---

## ❓ 常见问题

### Q: 我没有时间维护，能贡献吗？

A: **当然可以！** 社区共同维护的核心就是：
- 有时间时贡献一点
- 没时间时旁观使用
- 有新版本了一起升级

**每个人按自己的能力参与，不强制、不压力。**

### Q: 我可以贡献什么？

A: 任何你感兴趣的方面：
- 新功能开发
- Bug 修复
- 文档改进
- 测试用例
- 性能优化
- 翻译本地化

### Q: 如何开始第一个贡献？

A: 推荐从以下开始：
1. 修复文档错别字
2. 改进注释
3. 添加测试用例
4. 修复简单的 Bug

### Q: PR 多久能被合并？

A: **社区审核模式**：
- 简单修复：1-3 天（任何维护者可合并）
- 新功能：3-7 天（需要 2 个维护者同意）
- 重大变更：7-14 天（社区讨论）

### Q: 如何成为维护者？

A: 参见上方的"维护者申请"部分。

### Q: 项目决策怎么做？

A: **社区民主决策**：
- 小改动：维护者直接决定
- 中等改动：2 个维护者同意
- 重大改动：社区投票（1 人 1 票）

---

## 🙏 感谢

感谢所有为太极 API 做出贡献的开发者！

**🌟 一起让太极 API 变得更好！**
