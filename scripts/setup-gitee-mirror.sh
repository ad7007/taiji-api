#!/bin/bash
# Gitee Mirror Setup Script
# 配置 Gitee 自动镜像脚本

set -e

echo "======================================"
echo "Gitee Mirror Setup / Gitee 镜像配置"
echo "======================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查参数
if [ $# -lt 2 ]; then
    echo -e "${RED}用法 / Usage:${NC}"
    echo "  ./setup-gitee-mirror.sh <GITEE_USERNAME> <GITEE_SSH_KEY_PATH>"
    echo ""
    echo "示例 / Example:"
    echo "  ./setup-gitee-mirror.sh ad7007 ~/.ssh/gitee_mirror"
    echo ""
    exit 1
fi

GITEE_USERNAME=$1
SSH_KEY_PATH=$2
GITEE_REPO_URL="https://gitee.com/${GITEE_USERNAME}/taiji-api.git"

echo -e "${GREEN}配置信息 / Configuration:${NC}"
echo "  Gitee 用户名 / Username: ${GITEE_USERNAME}"
echo "  SSH 密钥路径 / SSH Key Path: ${SSH_KEY_PATH}"
echo "  Gitee 仓库 / Repository: ${GITEE_REPO_URL}"
echo ""

# 步骤 1: 检查 SSH 密钥
echo -e "${YELLOW}步骤 1/5: 检查 SSH 密钥${NC}"
if [ -f "${SSH_KEY_PATH}" ]; then
    echo -e "${GREEN}✓ SSH 私钥存在${NC}"
else
    echo -e "${RED}✗ SSH 私钥不存在：${SSH_KEY_PATH}${NC}"
    echo "请生成 SSH 密钥："
    echo "  ssh-keygen -t ed25519 -C 'gitee-mirror-key' -f ${SSH_KEY_PATH}"
    exit 1
fi

if [ -f "${SSH_KEY_PATH}.pub" ]; then
    echo -e "${GREEN}✓ SSH 公钥存在${NC}"
    echo ""
    echo -e "${YELLOW}公钥内容 / Public Key:${NC}"
    cat ${SSH_KEY_PATH}.pub
    echo ""
    echo "请将以上公钥添加到 Gitee:"
    echo "  1. 访问 https://gitee.com/profile/sshkeys"
    echo "  2. 点击'添加公钥'"
    echo "  3. 粘贴公钥内容"
    echo "  4. 点击'确定'"
    echo ""
    read -p "已完成 Gitee SSH 公钥配置？(y/n): " confirm
    if [ "$confirm" != "y" ]; then
        echo "请先配置 Gitee SSH 公钥"
        exit 1
    fi
else
    echo -e "${RED}✗ SSH 公钥不存在：${SSH_KEY_PATH}.pub${NC}"
    exit 1
fi

# 步骤 2: 检查 Gitee 仓库
echo -e "${YELLOW}步骤 2/5: 检查 Gitee 仓库${NC}"
echo "请确认已在 Gitee 创建空仓库："
echo "  1. 访问 https://gitee.com/new"
echo "  2. 仓库名：taiji-api"
echo "  3. 不要勾选'使用模板初始化'"
echo "  4. 点击'创建'"
echo ""
read -p "已创建 Gitee 仓库？(y/n): " confirm
if [ "$confirm" != "y" ]; then
    echo "请先创建 Gitee 仓库"
    exit 1
fi

# 步骤 3: 添加 Gitee 远程仓库
echo -e "${YELLOW}步骤 3/5: 添加 Gitee 远程仓库${NC}"
if git remote | grep -q "gitee"; then
    echo -e "${YELLOW}⚠ Gitee 远程仓库已存在，将更新${NC}"
    git remote set-url gitee git@gitee.com:${GITEE_USERNAME}/taiji-api.git
else
    echo -e "${GREEN}添加 Gitee 远程仓库${NC}"
    git remote add gitee git@gitee.com:${GITEE_USERNAME}/taiji-api.git
fi
echo -e "${GREEN}✓ Gitee 远程仓库已配置${NC}"
echo ""

# 步骤 4: 测试 SSH 连接
echo -e "${YELLOW}步骤 4/5: 测试 SSH 连接${NC}"
ssh -T -o StrictHostKeyChecking=no git@gitee.com <<EOF
if [ \$? -eq 0 ]; then
    echo -e "${GREEN}✓ SSH 连接成功${NC}"
else
    echo -e "${RED}✗ SSH 连接失败${NC}"
    echo "请检查："
    echo "  1. SSH 密钥是否正确配置"
    echo "  2. Gitee SSH 公钥是否已添加"
    echo "  3. 网络连接是否正常"
    exit 1
fi
EOF
echo ""

# 步骤 5: 首次手动推送
echo -e "${YELLOW}步骤 5/5: 首次手动推送到 Gitee${NC}"
echo "将推送到 Gitee 仓库..."
git push -u gitee main

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}======================================"
    echo "✓ Gitee 镜像配置完成！"
    echo "======================================${NC}"
    echo ""
    echo "Gitee 仓库地址："
    echo "  https://gitee.com/${GITEE_USERNAME}/taiji-api"
    echo ""
    echo "自动同步已配置："
    echo "  - 每次推送到 GitHub 会自动同步到 Gitee"
    echo "  - GitHub Actions 工作流：.github/workflows/sync-to-gitee.yml"
    echo ""
    echo "下次推送："
    echo "  git push origin main  # 会自动同步到 Gitee"
    echo ""
else
    echo ""
    echo -e "${RED}✗ 推送失败${NC}"
    echo "请检查："
    echo "  1. Gitee 仓库是否存在"
    echo "  2. SSH 密钥是否有权限"
    echo "  3. 网络连接是否正常"
    exit 1
fi
