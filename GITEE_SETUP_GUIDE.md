# Gitee 镜像配置指南

**版本 / Version**: v1.0  
**最后更新 / Last Updated**: 2026-03-18

---

## 📋 配置步骤 / Setup Steps

### 前提条件 / Prerequisites

- ✅ 已有 Gitee 账号
- ✅ 已有 Gitee SSH Key（您已确认有）
- ✅ GitHub 仓库已推送

---

## 🔧 快速配置（推荐）/ Quick Setup (Recommended)

### 方法 1: 使用配置脚本

```bash
# 进入项目目录
cd /root/taiji-api-v2

# 赋予脚本执行权限
chmod +x scripts/setup-gitee-mirror.sh

# 运行配置脚本
# 用法：./setup-gitee-mirror.sh <GITEE 用户名> <SSH 密钥路径>
./scripts/setup-gitee-mirror.sh ad7007 ~/.ssh/gitee_mirror
```

脚本会自动完成：
1. 检查 SSH 密钥
2. 验证 Gitee 仓库
3. 添加远程仓库
4. 测试 SSH 连接
5. 首次推送

---

## 📝 手动配置 / Manual Setup

### 步骤 1: 在 Gitee 创建仓库

访问：https://gitee.com/new

**配置**:
- 仓库路径：`taiji-api`
- 仓库名称：`太极 API`
- 介绍：`太极九宫任务管理系统 - Gitee 镜像`
- **不要勾选**"使用模板初始化仓库"
- 点击"创建"

---

### 步骤 2: 配置 SSH 密钥（如已有可跳过）

**检查现有密钥**:
```bash
ls -la ~/.ssh/gitee_mirror*
```

**如没有，生成新密钥**:
```bash
ssh-keygen -t ed25519 -C "gitee-mirror-key" -f ~/.ssh/gitee_mirror
```

**查看公钥**:
```bash
cat ~/.ssh/gitee_mirror.pub
```

**添加到 Gitee**:
1. 访问 https://gitee.com/profile/sshkeys
2. 点击"添加公钥"
3. 粘贴公钥内容
4. 标题：`taiji-api-mirror`
5. 点击"确定"

---

### 步骤 3: 添加 Gitee 远程仓库

```bash
cd /root/taiji-api-v2

# 添加 Gitee 远程仓库
git remote add gitee git@gitee.com:ad7007/taiji-api.git

# 验证远程仓库
git remote -v
```

**预期输出**:
```
gitee	git@gitee.com:ad7007/taiji-api.git (fetch)
gitee	git@gitee.com:ad7007/taiji-api.git (push)
origin	https://github.com/ad7007/taiji-api.git (fetch)
origin	https://github.com/ad7007/taiji-api.git (push)
```

---

### 步骤 4: 首次推送到 Gitee

```bash
# 推送到 Gitee
git push -u gitee main
```

**预期输出**:
```
Enumerating objects: XXX, done.
Counting objects: 100% (XXX/XXX), done.
Delta compression using up to X threads
Compressing objects: 100% (XXX/XXX), done.
Writing objects: 100% (XXX/XXX), XX.XX MiB | X.XX MiB/s, done.
Total XXX (delta XXX), reused XXX (delta XXX)
To gitee.com:ad7007/taiji-api.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'gitee'.
```

---

### 步骤 5: 配置 GitHub Actions 自动同步

**需要配置 GitHub Secret**:

1. 访问 https://github.com/ad7007/taiji-api/settings/secrets/actions
2. 点击"New repository secret"
3. 添加 Secret:
   - **Name**: `GITEE_SSH_PRIVATE_KEY`
   - **Value**: 粘贴私钥内容
     ```bash
     cat ~/.ssh/gitee_mirror
     # 复制全部内容（包括 BEGIN 和 END 行）
     ```
4. 点击"Add secret"

**验证工作流**:
- 访问 https://github.com/ad7007/taiji-api/actions
- 查看 "Sync to Gitee Mirror" 工作流
- 下次推送到 GitHub 时会自动同步

---

## 🧪 测试同步 / Test Sync

### 测试方法 1: 推送代码

```bash
# 推送到 GitHub（会自动同步到 Gitee）
git push origin main

# 检查 Gitee 是否更新
# 访问 https://gitee.com/ad7007/taiji-api/commits/main
```

### 测试方法 2: 手动触发

1. 访问 https://github.com/ad7007/taiji-api/actions/workflows/sync-to-gitee.yml
2. 点击 "Run workflow"
3. 选择分支（main）
4. 点击 "Run workflow"
5. 等待完成并查看日志

---

## ✅ 验证清单 / Verification Checklist

- [ ] Gitee 仓库已创建：https://gitee.com/ad7007/taiji-api
- [ ] SSH 公钥已添加到 Gitee
- [ ] Gitee 远程仓库已添加
- [ ] 首次推送成功
- [ ] GitHub Secret `GITEE_SSH_PRIVATE_KEY` 已配置
- [ ] GitHub Actions 工作流正常触发
- [ ] 同步后 Gitee 代码与 GitHub 一致

---

## 🔍 故障排查 / Troubleshooting

### 问题 1: SSH 连接失败

**错误**: `Permission denied (publickey)`

**解决**:
```bash
# 检查 SSH 密钥权限
chmod 600 ~/.ssh/gitee_mirror
chmod 644 ~/.ssh/gitee_mirror.pub

# 测试 SSH 连接
ssh -T git@gitee.com
```

### 问题 2: 推送失败

**错误**: `remote: Repository not found`

**解决**:
1. 确认 Gitee 仓库已创建
2. 确认仓库名正确（taiji-api）
3. 确认 SSH 公钥已添加

### 问题 3: GitHub Actions 失败

**检查**:
1. GitHub Secret 是否正确配置
2. Gitee SSH 公钥是否有效
3. 查看 Actions 日志获取详细错误

---

## 📞 需要帮助？

**文档**:
- [GITEE_MIRROR.md](GITEE_MIRROR.md) - 详细说明
- [GITEE_MIRROR.en.md](GITEE_MIRROR.en.md) - English version

**联系方式**:
- GitHub Issues: https://github.com/ad7007/taiji-api/issues

---

## 🎯 下一步

配置完成后：

1. ✅ 每次推送到 GitHub 会自动同步到 Gitee
2. ✅ 国内用户可使用 Gitee 镜像获得更快访问
3. ✅ 更新 README 中的 Gitee 链接

**验证 Gitee 镜像**:
- 访问：https://gitee.com/ad7007/taiji-api
- 确认代码已同步
- 确认 README 显示正常

---

**最后更新**: 2026-03-18  
**维护者**: Taiji API Community
