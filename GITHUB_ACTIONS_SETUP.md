# GitHub Actions 自动同步配置指南

**版本**: v1.0  
**最后更新**: 2026-03-18

---

## 📋 配置步骤

### 步骤 1: 添加 GitHub Secrets

访问：https://github.com/ad7007/taiji-api/settings/secrets/actions

添加以下 2 个 Secret：

#### 1. GITEE_USERNAME

- **Name**: `GITEE_USERNAME`
- **Value**: `miroeta`

#### 2. GITEE_TOKEN

- **Name**: `GITEE_TOKEN`
- **Value**: `7ffd01bcc35c4cf651c7c10f0541ff19`

### 步骤 2: 验证配置

添加完成后，推送代码到 GitHub：

```bash
cd /root/taiji-api-v2
git push origin main
```

GitHub Actions 会自动触发同步工作流。

### 步骤 3: 查看同步状态

访问：https://github.com/ad7007/taiji-api/actions

查看 "Sync to Gitee Mirror" 工作流运行状态。

---

## 🔍 手动触发同步

如需手动触发同步：

1. 访问 https://github.com/ad7007/taiji-api/actions/workflows/sync-to-gitee.yml
2. 点击 "Run workflow"
3. 选择分支（main）
4. 点击 "Run workflow"

---

## 📊 同步日志

同步成功后，日志会显示：

```
✓ Synced to Gitee: https://gitee.com/miroeta/taiji-api
```

---

## ❓ 故障排查

### 同步失败

**检查项**:
- [ ] GITEE_USERNAME 是否正确（miroeta）
- [ ] GITEE_TOKEN 是否正确
- [ ] Gitee 仓库是否存在
- [ ] Token 是否有推送权限

### 查看错误日志

1. 访问 GitHub Actions
2. 点击失败的运行
3. 查看详细错误信息

---

**配置完成后，每次推送到 GitHub 都会自动同步到 Gitee！** 🚀
