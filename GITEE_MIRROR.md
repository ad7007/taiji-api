# Gitee 镜像仓库说明

**Gitee Mirror Repository Documentation**

---

## 📦 仓库地址 / Repository URLs

| 平台 / Platform | 地址 / URL | 状态 / Status |
|----------------|-----------|---------------|
| **GitHub (主仓库)** | https://github.com/ad7007/taiji-api | ✅ 主仓库 / Main |
| **Gitee (镜像)** | https://gitee.com/miroeta/taiji-api | ✅ 已同步 / Synced |

---

## 🔄 自动同步机制 / Auto-Sync Mechanism

### 同步方式 / Sync Method

- **触发条件**: GitHub 主仓库推送时自动触发
- **Trigger**: Automatically triggered when pushing to GitHub main repository
- **同步方向**: GitHub → Gitee（单向）
- **Sync Direction**: GitHub → Gitee (one-way)
- **同步内容**: 所有分支和标签
- **Sync Content**: All branches and tags

### GitHub Actions 工作流 / GitHub Actions Workflow

```yaml
name: Sync to Gitee Mirror

on:
  push:
    branches: [main, develop]
  workflow_dispatch:  # 允许手动触发 / Allow manual trigger

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - uses: pixta-dev/repository-mirroring-action@v1
        with:
          target_repo_url:
            https://gitee.com/ad7007/taiji-api.git
          ssh_private_key:
            ${{ secrets.GITEE_SSH_PRIVATE_KEY }}
```

---

## ⚙️ 配置步骤 / Configuration Steps

### 1. 在 Gitee 创建空仓库 / Create Empty Repository on Gitee

```
1. 访问 https://gitee.com
2. 登录 Gitee 账号
3. 点击 "+" → "新建仓库"
4. 仓库名：taiji-api
5. 初始化为空仓库（不要勾选"使用模板初始化"）
6. 点击"创建"
```

### 2. 生成 SSH 密钥 / Generate SSH Key

**在本地执行 / Run Locally**:
```bash
# 生成 SSH 密钥
ssh-keygen -t ed25519 -C "gitee-mirror-key" -f ~/.ssh/gitee_mirror

# 查看公钥
cat ~/.ssh/gitee_mirror.pub
```

### 3. 配置 Gitee SSH 公钥 / Configure Gitee SSH Public Key

```
1. 访问 https://gitee.com/profile/sshkeys
2. 点击"添加公钥"
3. 粘贴公钥内容（~/.ssh/gitee_mirror.pub）
4. 点击"确定"
```

### 4. 配置 GitHub Secrets / Configure GitHub Secrets

```
1. 访问 GitHub 仓库 → Settings → Secrets and variables → Actions
2. 点击"New repository secret"
3. 添加以下 Secret:
   - Name: GITEE_SSH_PRIVATE_KEY
   - Value: 粘贴私钥内容（~/.ssh/gitee_mirror）
4. 点击"Add secret"
```

### 5. 测试同步 / Test Sync

```bash
# 推送代码到 GitHub
git push origin main

# GitHub Actions 会自动触发同步
# 查看 Actions 标签页确认同步状态
```

---

## 📋 注意事项 / Notes

### 单向同步 / One-Way Sync

- ✅ **GitHub → Gitee**: 自动同步
- ❌ **Gitee → GitHub**: 不同步

**重要**: 所有开发在 GitHub 进行，Gitee 仅作为镜像。

**Important**: All development should be done on GitHub. Gitee is mirror-only.

---

### Issues 和 Pull Requests

- 📍 **GitHub**: 主 Issues 和 PRs 讨论区
- 📍 **Gitee**: 可关闭或重定向到 GitHub

**建议**: 在 Gitee README 中说明 Issues 请到 GitHub 提交。

---

### 标签同步 / Tags Sync

- ✅ 所有 Git 标签会自动同步
- ✅ Release 发布后手动在 Gitee 创建对应 Release

---

## 🇨🇳 国内用户指南 / For Chinese Users

### 访问 Gitee 镜像

**克隆仓库 / Clone Repository**:
```bash
# 使用 Gitee 镜像（国内更快）
git clone https://gitee.com/ad7007/taiji-api.git

# 或使用 GitHub（国际用户）
git clone https://github.com/ad7007/taiji-api.git
```

### 贡献代码 / Contribute Code

**推荐方式**:
1. 在 GitHub Fork 项目
2. 提交 PR 到 GitHub
3. Issues/Discussions 在 GitHub

**原因**:
- 社区集中在 GitHub
- 维护者主要在 GitHub 活跃
- 国际贡献者也能参与

---

## 📊 同步状态 / Sync Status

### 查看同步历史

1. 访问 GitHub 仓库 → Actions 标签页
2. 查看 "Sync to Gitee Mirror" 工作流
3. 点击具体运行查看日志

### 手动触发同步

1. 访问 Actions → Sync to Gitee Mirror
2. 点击 "Run workflow"
3. 选择分支
4. 点击 "Run workflow"

---

## 🔧 故障排查 / Troubleshooting

### 同步失败 / Sync Failed

**检查项 / Checklist**:
- [ ] Gitee SSH 密钥配置正确
- [ ] GitHub Secret 已正确配置
- [ ] Gitee 仓库存在且为空或已配置远程
- [ ] 网络连接正常

### 常见问题 / Common Issues

**Q: 同步显示成功但 Gitee 没有更新？**
A: 检查 Gitee 仓库权限设置，确保 SSH 密钥有写入权限。

**Q: 第一次同步失败？**
A: 确保 Gitee 仓库是空的，或已正确配置远程。

---

## 📞 联系方式 / Contact

**问题反馈**: 
- GitHub Issues: https://github.com/ad7007/taiji-api/issues
- Gitee Issues: https://gitee.com/ad7007/taiji-api/issues (重定向到 GitHub)

---

**最后更新 / Last Updated**: 2026-03-18

**维护者 / Maintainers**: Taiji API Community

---

**Languages**: 
- [中文](GITEE_MIRROR.md) | [English](GITEE_MIRROR.en.md)
