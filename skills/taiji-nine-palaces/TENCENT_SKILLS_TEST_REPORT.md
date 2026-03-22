# 腾讯系技能测试报告

## 测试时间
2026-03-18 02:15 GMT+8

---

## 1️⃣ tencent-docs（腾讯文档）

### 技能信息

| 项目 | 详情 |
|------|------|
| **位置** | `/root/.openclaw/workspace/skills/tencent-docs` |
| **版本** | 1.0.0 |
| **状态** | ✅ 已安装 |
| **依赖** | TENCENT_DOCS_TOKEN |

### 支持功能

#### 文档类型

| 类型 | doc_type | 推荐度 | 说明 |
|------|----------|--------|------|
| 智能文档 | smartcanvas | ⭐⭐⭐ | 首选，排版美观 |
| Excel | excel | ⭐⭐⭐ | 数据表格 |
| 幻灯片 | slide | ⭐⭐⭐ | 演示文稿 |
| 思维导图 | mind | ⭐⭐⭐ | 知识图谱 |
| 流程图 | flowchart | ⭐⭐⭐ | 流程图 |
| Word | word | ⭐⭐ | 传统格式 |
| 智能表格 | smartsheet | ⭐⭐⭐ | 高级表格 |

#### 核心能力

- ✅ 创建智能文档（Markdown → 腾讯文档）
- ✅ 查询/搜索文档空间
- ✅ 管理文件夹结构
- ✅ 读取文档内容
- ✅ 编辑智能表
- ✅ 编辑智能文档

### 使用示例

```python
# 创建智能文档
feishu_doc action=create title="云品牌报告" doc_type=smartcanvas

# 读取文档
feishu_doc action=read doc_token="xxx"

# 更新内容
feishu_doc action=append doc_token="xxx" content="新内容"
```

### 集成到九宫格

**4-品牌战略宫** 可以使用：
- 创建品牌文档
- 管理营销方案
- 协作编辑

**2-产品质量宫** 可以使用：
- 产品需求文档
- 质量检查清单
- 版本发布说明

### 测试状态

- [ ] 需要 TENCENT_DOCS_TOKEN
- [ ] 等待配置后测试

---

## 2️⃣ tencentcloud-lighthouse-skill（腾讯云轻量服务器）

### 技能信息

| 项目 | 详情 |
|------|------|
| **位置** | `/root/.openclaw/workspace/skills/tencentcloud-lighthouse-skill` |
| **版本** | 1.0.0 |
| **状态** | ⚠️ 需要配置 |
| **依赖** | mcporter, SecretId, SecretKey |

### 核心功能

- ✅ 自动安装 mcporter + MCP
- ✅ 查询轻量服务器实例
- ✅ 监控与告警
- ✅ 自诊断
- ✅ 防火墙管理
- ✅ 快照管理
- ✅ 远程命令执行（TAT）

### 安装流程

#### 步骤 1：检查状态

```bash
bash scripts/setup.sh --check-only
```

**当前状态**:
```
[MISSING] mcporter not installed
[MISSING] Config file not found: /root/.mcporter/mcporter.json
```

#### 步骤 2：安装 mcporter

```bash
npm install -g mcporter
```

#### 步骤 3：配置腾讯云密钥

需要用户提供：
1. **SecretId** - 腾讯云 API 密钥 ID
2. **SecretKey** - 腾讯云 API 密钥 Key

获取地址：https://console.cloud.tencent.com/cam/capi

#### 步骤 4：运行自动配置

```bash
bash scripts/setup.sh
```

### 集成到九宫格

**6-物联监控宫** 可以使用：
- 服务器监控
- 自动告警
- 远程命令执行

**3-技术团队宫** 可以使用：
- 代码部署
- 服务器管理
- 自动化运维

### 测试状态

- [ ] 需要安装 mcporter
- [ ] 需要腾讯云密钥
- [ ] 等待配置后测试

---

## 📊 对比总结

| 维度 | tencent-docs | tencentcloud-lighthouse |
|------|--------------|------------------------|
| **安装状态** | ✅ 已安装 | ⚠️ 需配置 |
| **依赖** | TENCENT_DOCS_TOKEN | mcporter + 腾讯云密钥 |
| **复杂度** | ⭐⭐ | ⭐⭐⭐ |
| **使用场景** | 文档协作 | 服务器运维 |
| **推荐宫位** | 2-产品、4-品牌 | 3-技术、6-监控 |

---

## 🚀 下一步

### tencent-docs

1. 获取 TENCENT_DOCS_TOKEN
2. 测试创建文档
3. 集成到工作流

### tencentcloud-lighthouse

1. 安装 mcporter
2. 配置腾讯云密钥
3. 测试服务器查询
4. 集成到监控系统

---

## 💡 建议

### 优先级

1. **tencent-docs** - 简单，立即能用
   - 用于报告协作编辑
   - 集成到 2-产品质量宫

2. **tencentcloud-lighthouse** - 需要配置
   - 用于服务器监控
   - 集成到 6-物联监控宫

### 使用场景

**tencent-docs**:
- 团队协作编辑报告
- 客户实时查看进度
- 多版本管理

**tencentcloud-lighthouse**:
- 监控服务器状态
- 自动部署脚本
- 故障告警

---

**测试完成！两个技能都需要配置密钥后才能使用。** 📝
