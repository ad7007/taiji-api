# 国际化指南 / Internationalization Guide

**版本 / Version**: v1.0  
**最后更新 / Last Updated**: 2026-03-18

---

## 🌍 多语言支持 / Multi-language Support

太极 API 项目支持多语言文档，方便全球贡献者参与。

Taiji API project supports multi-language documentation to facilitate global contributor participation.

### 可用语言 / Available Languages

| 语言 / Language | 代码 / Code | 状态 / Status |
|----------------|-------------|---------------|
| 简体中文 / Simplified Chinese | zh-CN | ✅ 默认 / Default |
| 英语 / English | en-US | ✅ 完整 / Complete |
| 日本語 / Japanese | ja-JP | 📅 计划中 / Planned |

---

## 📁 文档结构 / Documentation Structure

### 核心文档 / Core Documents

```
taiji-api/
├── README.md                    # 中文主文档
├── README.en.md                 # English main document
├── CONTRIBUTING.md              # 中文贡献指南
├── CONTRIBUTING.en.md           # English contribution guide
├── GOVERNANCE.md                # 中文治理模式
├── GOVERNANCE.en.md             # English governance model
├── FOUNDER_STATEMENT.md         # 中文创始人声明
├── FOUNDER_STATEMENT.en.md      # English founder statement
├── CODE_OF_CONDUCT.md           # 行为准则（中英对照）
├── LICENSE                      # 许可证（英文）
└── docs/
    ├── INTERNATIONALIZATION.md  # 国际化指南（本文件）
    └── API_EXAMPLES.md          # API 示例（中文，英文计划中）
```

### 文件命名规范 / File Naming Convention

**中文**: `FILENAME.md`  
**英文**: `FILENAME.en.md`

**示例 / Examples**:
- `README.md` → `README.en.md`
- `CONTRIBUTING.md` → `CONTRIBUTING.en.md`
- `GOVERNANCE.md` → `GOVERNANCE.en.md`

---

## 📝 翻译指南 / Translation Guidelines

### 翻译原则 / Translation Principles

1. **准确性 / Accuracy**
   - 忠实于原文含义
   - 技术术语使用标准翻译
   - Faithful to original meaning
   - Use standard translations for technical terms

2. **一致性 / Consistency**
   - 术语翻译保持一致
   - 格式和风格保持一致
   - Consistent terminology translation
   - Consistent format and style

3. **可读性 / Readability**
   - 符合目标语言习惯
   - 避免直译造成的歧义
   - Follow target language conventions
   - Avoid ambiguity from literal translation

### 技术术语翻译 / Technical Terms

| 中文 | English | 备注 / Notes |
|------|---------|-------------|
| 九宫格 | Nine Palaces | 太极哲学术语 / Taiji philosophy term |
| 阴阳 | Yin-Yang | 保留拼音 / Keep Pinyin |
| 五行 | Five Elements | 金木水火土 / Metal Wood Water Fire Earth |
| 六爻 | Six Lines (Liu Yao) | 保留拼音 / Keep Pinyin |
| 卦 | Hexagram | 易经术语 / I Ching term |
| 爻 | Line | 卦的组成单位 / Component of hexagram |
| 变爻 | Changing Line | 动爻 / Moving line |
| 贡献者 | Contributor | 开源社区通用 / Open-source community term |
| 维护者 | Maintainer | 开源社区通用 / Open-source community term |
| 合并请求 | Pull Request (PR) | GitHub 术语 / GitHub term |

---

## 🔧 翻译流程 / Translation Process

### 添加新语言 / Adding New Language

1. **创建翻译文件 / Create Translation File**
   ```bash
   # 复制原文档
   cp README.md README.ja.md
   
   # 翻译内容
   nano README.ja.md
   ```

2. **更新语言列表 / Update Language List**
   - 在 README.md 中添加语言链接
   - Add language link in README.md

3. **提交 PR / Submit PR**
   ```bash
   git add README.ja.md
   git commit -m "docs: add Japanese translation"
   git push origin main
   ```

### 更新翻译 / Updating Translation

**当原文档更新时 / When original document is updated**:

1. **记录变更 / Record Changes**
   ```markdown
   <!-- Translation Status -->
   <!-- Last synced with original: 2026-03-18 -->
   ```

2. **同步更新 / Sync Update**
   - 对比原文档变更
   - 更新翻译文件
   - Compare changes with original
   - Update translation file

3. **标记版本 / Mark Version**
   ```markdown
   **翻译版本 / Translation Version**: v1.0 (基于 / Based on original v1.0)
   ```

---

## 📋 翻译检查清单 / Translation Checklist

### 翻译前 / Before Translation

- [ ] 确认原文档是最新版本
- [ ] Confirm original document is latest version
- [ ] 准备术语表
- [ ] Prepare terminology glossary
- [ ] 了解项目背景
- [ ] Understand project background

### 翻译中 / During Translation

- [ ] 保持格式一致
- [ ] Keep format consistent
- [ ] 翻译所有文本（包括注释）
- [ ] Translate all text (including comments)
- [ ] 检查链接是否有效
- [ ] Check if links are valid
- [ ] 保留代码示例不变
- [ ] Keep code examples unchanged

### 翻译后 / After Translation

- [ ] 校对拼写和语法
- [ ] Proofread spelling and grammar
- [ ] 检查术语一致性
- [ ] Check terminology consistency
- [ ] 添加翻译者信息
- [ ] Add translator information
- [ ] 更新语言链接
- [ ] Update language links

---

## 🌐 网站国际化 / Website Internationalization

### 多语言切换 / Multi-language Switcher

**计划实现 / Planned Implementation**:

```html
<!-- 语言选择器 / Language Selector -->
<div class="language-selector">
  <a href="/zh-CN/">🇨🇳 中文</a> |
  <a href="/en-US/">🇺🇸 English</a> |
  <a href="/ja-JP/">🇯🇵 日本語</a>
</div>
```

### URL 结构 / URL Structure

```
# 中文
https://taiji-api.dev/zh-CN/docs/

# English
https://taiji-api.dev/en-US/docs/

# 默认（中文）
https://taiji-api.dev/docs/
```

---

## 🤝 翻译贡献 / Translation Contribution

### 成为翻译志愿者 / Become a Translation Volunteer

**要求 / Requirements**:
- ✅ 精通中文和目标语言
- ✅ Fluent in Chinese and target language
- ✅ 了解开源文化
- ✅ Understand open-source culture
- ✅ 有时间投入（每月 2-4 小时）
- ✅ Have time to commit (2-4 hours/month)

### 翻译任务 / Translation Tasks

| 任务 / Task | 预计时间 / Est. Time | 难度 / Difficulty |
|------------|---------------------|------------------|
| README 翻译 | 2-3 小时 | ⭐ |
| CONTRIBUTING 翻译 | 3-4 小时 | ⭐⭐ |
| GOVERNANCE 翻译 | 4-5 小时 | ⭐⭐⭐ |
| API 文档翻译 | 6-8 小时 | ⭐⭐⭐ |
| 网站翻译 | 4-6 小时 | ⭐⭐ |

### 翻译贡献认可 / Translation Contribution Recognition

- ✅ 名字列入 CONTRIBUTORS.md
- ✅ Name in CONTRIBUTORS.md
- ✅ 翻译贡献徽章
- ✅ Translation contribution badge
- ✅ 社区感谢
- ✅ Community appreciation

---

## 📊 翻译状态 / Translation Status

### 文档翻译进度 / Documentation Translation Progress

| 文档 / Document | 中文 | English | 日本語 |
|----------------|------|---------|--------|
| README | ✅ | ✅ | 📅 |
| CONTRIBUTING | ✅ | ✅ | 📅 |
| GOVERNANCE | ✅ | ✅ | 📅 |
| FOUNDER_STATEMENT | ✅ | ✅ | 📅 |
| CODE_OF_CONDUCT | ✅ | ✅ | 📅 |
| ROADMAP | ✅ | 📅 | 📅 |
| CHANGELOG | ✅ | 📅 | 📅 |
| API_EXAMPLES | ✅ | 📅 | 📅 |

**图例 / Legend**:
- ✅ 完成 / Complete
- 📅 计划中 / Planned
- ❌ 未开始 / Not started

---

## 📞 联系方式 / Contact

**翻译问题？**

- 在 Issue 中提问：https://github.com/ad7007/taiji-api/issues
- 或在 Discussions 中交流：https://github.com/ad7007/taiji-api/discussions

**Translation Questions?**

- Ask in Issues: https://github.com/ad7007/taiji-api/issues
- Or discuss in Discussions: https://github.com/ad7007/taiji-api/discussions

---

**最后更新 / Last Updated**: 2026-03-18

**维护者 / Maintainers**: Taiji API Community

**Languages**: 
- [中文](INTERNATIONALIZATION.md) | [English](INTERNATIONALIZATION.en.md)
