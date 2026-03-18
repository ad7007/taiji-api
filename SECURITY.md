# 安全策略 (Security Policy)

太极 API 项目重视安全性，感谢帮助我们发现和修复安全问题。

---

## 📋 支持版本

| 版本 | 安全支持 | 状态 |
|------|---------|------|
| 2.x.x | ✅ | 当前版本 |
| 1.x.x | ✅ | 维护中 |
| 0.x.x | ❌ | 已弃用 |

---

## 🐛 报告漏洞

### 如何报告

**发现安全漏洞？** 请按以下方式报告：

1. **不要** 创建公开 Issue
2. 发送邮件至：[安全邮箱]
3. 或在 GitHub Security Advisory 中报告（私密）

### 报告内容

请提供以下信息：

- 漏洞类型描述
- 受影响版本
- 重现步骤
- 潜在影响
- 修复建议（如有）

### 响应时间

- **确认收到**: 48 小时内
- **初步评估**: 7 天内
- **修复计划**: 14 天内
- **补丁发布**: 30 天内（严重漏洞优先）

---

## 🔒 安全最佳实践

### 用户责任

#### API Key 管理

```bash
# ✅ 正确：使用环境变量
export GITHUB_TOKEN="ghp_xxx"
export FEISHU_APP_SECRET="xxx"

# ❌ 错误：硬编码在代码中
TOKEN = "ghp_xxx"  # 不要这样做！
```

#### 敏感信息

- ✅ 使用 `.env` 文件存储密钥
- ✅ 将 `.env` 加入 `.gitignore`
- ✅ 定期轮换密钥
- ❌ 不要提交密钥到 Git

#### 访问控制

- ✅ 使用最小权限原则
- ✅ 定期审查访问日志
- ✅ 限制 API 访问频率
- ❌ 不要公开敏感端点

---

### 开发者责任

#### 代码安全

```python
# ✅ 正确：输入验证
def update_palace_load(palace_id: int, load: float):
    if not 1 <= palace_id <= 9:
        raise ValueError("Invalid palace ID")
    if not 0 <= load <= 1:
        raise ValueError("Load must be between 0 and 1")

# ❌ 错误：无验证
def update_palace_load(palace_id, load):
    # 危险！
    pass
```

#### 依赖管理

```bash
# 定期检查依赖漏洞
pip install pip-audit
pip-audit

# 或使用 safety
pip install safety
safety check
```

#### 日志安全

```python
# ✅ 正确：不记录敏感信息
logger.info(f"User {user_id} logged in")

# ❌ 错误：记录敏感信息
logger.info(f"User logged in with token {token}")  # 不要这样做！
```

---

## 🛡️ 已知安全问题

### 已修复

| CVE | 描述 | 修复版本 | 日期 |
|-----|------|---------|------|
| - | 暂无公开 CVE | - | - |

### 进行中

- [ ] 无

---

## 🔐 加密措施

### 数据传输

- ✅ HTTPS/TLS 加密
- ✅ API Token 认证
- ✅ 敏感数据加密存储

### 数据存储

- ✅ 配置文件权限控制
- ✅ 密钥加密存储
- ✅ 定期备份

---

## 📢 安全公告

### 订阅方式

关注以下渠道获取安全更新：

- GitHub Security Advisories
- Release Notes
- Email Newsletter（计划中）

### 历史公告

| 日期 | 类型 | 描述 |
|------|------|------|
| - | - | 暂无公告 |

---

## 🙏 致谢

感谢以下安全研究者：

（待添加）

---

## 📞 联系方式

- **安全邮箱**: [待设置]
- **GitHub**: https://github.com/ad7007/taiji-api/security
- **Issues**: https://github.com/ad7007/taiji-api/issues（仅非安全问题）

---

**最后更新**: 2026-03-18

**版本**: v1.0
