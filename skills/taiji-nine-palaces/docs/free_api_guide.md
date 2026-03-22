# 免费API Key申请指南

## 零成本方案

### 1. 智谱GLM（推荐）

**免费额度**: 每天100次调用  
**申请地址**: https://open.bigmodel.cn  
**申请步骤**:
1. 注册账号
2. 进入控制台
3. 创建API Key
4. 复制到环境变量：`export ZHIPU_API_KEY="your-key"`

---

### 2. DeepSeek

**免费额度**: 每月500万tokens  
**申请地址**: https://platform.deepseek.com  
**申请步骤**:
1. 注册账号
2. 创建API Key
3. 复制到环境变量：`export DEEPSEEK_API_KEY="your-key"`

---

### 3. 通义千问

**免费额度**: 100万tokens  
**申请地址**: https://dashscope.console.aliyun.com

---

### 4. Kimi Moonshot

**免费额度**: 有限免费  
**申请地址**: https://platform.moonshot.cn

---

## 配置方法

```bash
# 方法1: 环境变量（临时）
export ZHIPU_API_KEY="your-key"

# 方法2: 写入配置文件（永久）
mkdir -p ~/.openclaw/plugins
cat > ~/.openclaw/plugins/free_models.json << 'EOF'
{
  "zhipu_api_key": "your-key",
  "deepseek_api_key": "your-key",
  "default_model": "glm-4-flash"
}
EOF
```

---

## 已有的免费工具

| 工具 | 功能 | 成本 |
|------|------|------|
| ✅ Edge-TTS | 配音 | ¥0 |
| ✅ FFmpeg | 视频合成 | ¥0 |
| ⏳ 智谱GLM | 文本生成 | 需申请Key |
| ⏳ DeepSeek | 文本生成 | 需申请Key |

---

**余总：请提供智谱或DeepSeek的免费API Key，我立即开始生成内容！**