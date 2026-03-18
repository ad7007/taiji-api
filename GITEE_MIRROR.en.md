# Gitee Mirror Repository Documentation

---

## 📦 Repository URLs

| Platform | URL | Status |
|----------|-----|--------|
| **GitHub (Main)** | https://github.com/ad7007/taiji-api | ✅ Main Repository |
| **Gitee (Mirror)** | https://gitee.com/miroeta/taiji-api | ✅ Synced |

---

## 🔄 Auto-Sync Mechanism

### Sync Method

- **Trigger**: Automatically triggered when pushing to GitHub main repository
- **Sync Direction**: GitHub → Gitee (one-way)
- **Sync Content**: All branches and tags

### GitHub Actions Workflow

```yaml
name: Sync to Gitee Mirror

on:
  push:
    branches: [main, develop]
  workflow_dispatch:  # Allow manual trigger

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

## ⚙️ Configuration Steps

### 1. Create Empty Repository on Gitee

```
1. Visit https://gitee.com
2. Login to Gitee account
3. Click "+" → "New Repository"
4. Repository name: taiji-api
5. Initialize as empty (do NOT check "Initialize with template")
6. Click "Create"
```

### 2. Generate SSH Key

**Run Locally**:
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "gitee-mirror-key" -f ~/.ssh/gitee_mirror

# View public key
cat ~/.ssh/gitee_mirror.pub
```

### 3. Configure Gitee SSH Public Key

```
1. Visit https://gitee.com/profile/sshkeys
2. Click "Add Public Key"
3. Paste public key content (~/.ssh/gitee_mirror.pub)
4. Click "OK"
```

### 4. Configure GitHub Secrets

```
1. Visit GitHub repo → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add secret:
   - Name: GITEE_SSH_PRIVATE_KEY
   - Value: Paste private key content (~/.ssh/gitee_mirror)
4. Click "Add secret"
```

### 5. Test Sync

```bash
# Push code to GitHub
git push origin main

# GitHub Actions will automatically trigger sync
# Check Actions tab to confirm sync status
```

---

## 📋 Notes

### One-Way Sync

- ✅ **GitHub → Gitee**: Auto-sync
- ❌ **Gitee → GitHub**: Not synced

**Important**: All development should be done on GitHub. Gitee is mirror-only.

---

### Issues and Pull Requests

- 📍 **GitHub**: Main Issues and PRs discussion
- 📍 **Gitee**: Can be closed or redirected to GitHub

**Recommendation**: State in Gitee README that Issues should be submitted to GitHub.

---

### Tags Sync

- ✅ All Git tags will auto-sync
- ✅ Manually create corresponding Release on Gitee after GitHub release

---

## 🇨🇳 For Chinese Users

### Access Gitee Mirror

**Clone Repository**:
```bash
# Use Gitee mirror (faster in China)
git clone https://gitee.com/ad7007/taiji-api.git

# Or use GitHub (international users)
git clone https://github.com/ad7007/taiji-api.git
```

### Contribute Code

**Recommended**:
1. Fork project on GitHub
2. Submit PR to GitHub
3. Issues/Discussions on GitHub

**Reasons**:
- Community concentrated on GitHub
- Maintainers mainly active on GitHub
- International contributors can participate

---

## 📊 Sync Status

### View Sync History

1. Visit GitHub repo → Actions tab
2. View "Sync to Gitee Mirror" workflow
3. Click specific run to view logs

### Manual Sync Trigger

1. Visit Actions → Sync to Gitee Mirror
2. Click "Run workflow"
3. Select branch
4. Click "Run workflow"

---

## 🔧 Troubleshooting

### Sync Failed

**Checklist**:
- [ ] Gitee SSH key configured correctly
- [ ] GitHub Secret configured correctly
- [ ] Gitee repository exists and is empty or remote configured
- [ ] Network connection is normal

### Common Issues

**Q: Sync shows success but Gitee not updated?**
A: Check Gitee repository permission settings, ensure SSH key has write access.

**Q: First sync failed?**
A: Ensure Gitee repository is empty, or remote is properly configured.

---

## 📞 Contact

**Issue Reports**: 
- GitHub Issues: https://github.com/ad7007/taiji-api/issues
- Gitee Issues: https://gitee.com/ad7007/taiji-api/issues (Redirect to GitHub)

---

**Last Updated**: 2026-03-18

**Maintainers**: Taiji API Community

---

**Languages**: 
- [中文](GITEE_MIRROR.md) | [English](GITEE_MIRROR.en.md)
