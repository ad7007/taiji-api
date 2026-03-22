# 视频内容提取器使用指南

## 🎯 支持平台

| 平台 | 域名 | 支持度 |
|------|------|--------|
| 抖音 | douyin.com, iesdouyin.com | ✅ |
| 视频号 | channels.weixin.qq.com | ✅ |
| 小红书 | xiaohongshu.com, xhslink.com | ✅ |
| B 站 | bilibili.com, b23.tv | ✅ |
| YouTube | youtube.com, youtu.be | ✅ |

---

## 🔧 三种提取方法

### 方法 1：Jina Reader（推荐）

**优点**: 快速、免费、无需登录  
**缺点**: 部分平台可能无法提取

```python
from video_transcriber import VideoTranscriber

transcriber = VideoTranscriber()

# 单个视频
result = transcriber.transcribe_video(
    video_url="https://www.bilibili.com/video/BV1xx411c7mD",
    method="jina"  # 使用 Jina Reader
)

if result["success"]:
    print(f"转录成功：{result['output_files']}")
    print(f"内容预览：{result['transcript'][:200]}...")
```

**原理**: 使用 `https://r.jina.ai/URL` 提取网页内容

---

### 方法 2：Kimi 总结

**优点**: AI 智能总结、质量高  
**缺点**: 需要等待生成、Kimi 可能无法访问某些链接

```python
result = transcriber.transcribe_video(
    video_url="https://www.xiaohongshu.com/explore/xxx",
    method="browser"  # 使用 Kimi
)
```

---

### 方法 3：百度 AI 笔记

**优点**: 专业视频转录工具  
**缺点**: 需要 API 密钥

```python
result = transcriber.transcribe_video(
    video_url="https://www.youtube.com/watch?v=xxx",
    method="baidu_ai_notes"
)
```

---

## 📊 批量处理

```python
# 批量转录多个视频
video_urls = [
    "https://www.douyin.com/video/123",
    "https://www.xiaohongshu.com/explore/456",
    "https://www.bilibili.com/video/789",
]

results = transcriber.batch_transcribe(
    video_urls=video_urls,
    method="jina",
    delay_seconds=2  # 每个视频间隔 2 秒
)

# 处理结果
for i, result in enumerate(results):
    if result["success"]:
        print(f"视频{i+1}: ✅ {result['output_files']}")
    else:
        print(f"视频{i+1}: ❌ {result.get('error')}")
```

---

## 💡 完整工作流

### 1. 收集视频链接

```python
# 从九宫格 9-行业生态收集竞品视频
video_urls = [
    # 抖音竞品视频
    "https://www.douyin.com/video/7xxx",
    # 小红书种草视频
    "https://www.xiaohongshu.com/explore/6xxx",
    # B 站教程视频
    "https://www.bilibili.com/video/BV1xx",
]
```

### 2. 提取内容

```python
from video_transcriber import VideoTranscriber

transcriber = VideoTranscriber()
results = transcriber.batch_transcribe(video_urls, method="jina")
```

### 3. AI 总结分析

```python
from bailian_client import BailianClient

client = BailianClient()

# 汇总所有转录内容
all_content = "\n\n".join([r["transcript"] for r in results if r["success"]])

# AI 分析
prompt = f"""请分析这些竞品视频内容：

{all_content}

请提供：
1. 共同主题和趋势
2. 各视频的差异化亮点
3. 可借鉴的内容创意
4. 目标受众分析
"""

analysis = client.generate(prompt)
print(analysis["content"])
```

### 4. 生成报告

```python
from browser_automation import KimiPDFGenerator

generator = KimiPDFGenerator()

report = generator.generate_report(
    prompt=f"请生成竞品视频分析报告：\n{analysis['content']}",
    title="竞品视频分析报告",
    wait_seconds=30,
)

print(f"报告已生成：{report['pdf_path']}")
```

---

## 📁 输出文件

**默认目录**: `/root/.openclaw/workspace/content/videos/`

**文件命名**:
```
transcript_20260318_004800.md    # 转录稿
jina_20260318_004800.md          # Jina 提取
video_summary_20260318_004800.pdf # Kimi 总结
```

---

## ⚠️ 注意事项

### 1. 平台限制

| 平台 | 限制 | 解决方案 |
|------|------|----------|
| 抖音 | 需要登录 | 使用浏览器自动化 |
| 视频号 | 微信生态封闭 | 手动复制链接 + Kimi 总结 |
| 小红书 | 部分需要登录 | Jina Reader 可用 |
| B 站 | 部分视频有字幕 | 优先使用 B 站 API |
| YouTube | 需要网络 | 使用 YouTube API |

### 2. 内容质量

- **Jina Reader**: 提取网页文字，可能不完整
- **Kimi 总结**: 质量高，但依赖 AI 理解
- **百度 AI 笔记**: 专业但需要 API

### 3. 速率限制

- Jina Reader: 免费，有速率限制
- Kimi: 有使用额度限制
- 建议批量处理时添加延迟（2-5 秒）

---

## 🔗 第三方服务

### 推荐服务列表

| 服务 | URL | 功能 | 价格 |
|------|-----|------|------|
| Jina Reader | https://r.jina.ai/ | 网页提取 | 免费 |
| 百度 AI 笔记 | https://note.baidu.com/ | 视频转录 | 免费额度 |
| 飞书妙记 | https://www.feishu.cn/product/mingji | 语音转文字 | 免费额度 |
| 通义听悟 | https://tingwu.aliyun.com/ | 音视频转写 | 免费额度 |
| 网易见外 | http://jianwai.netease.com/ | 视频转写 | 付费 |

---

## 💰 变现应用

### 1. 竞品分析报告

```
收集竞品视频 → 提取内容 → AI 分析 → 生成报告 → 付费交付
```

**定价**: ¥299-999/份

### 2. 内容创意服务

```
客户产品 → 收集相关视频 → 提取亮点 → 创意方案 → 付费交付
```

**定价**: ¥599-2999/方案

### 3. 培训课程

```
行业教程视频 → 提取内容 → 整理成文 → 制作课程 → 售卖
```

**定价**: ¥199-1999/课程

---

## 📋 完整示例

```python
from video_transcriber import VideoTranscriber
from bailian_client import BailianClient
from browser_automation import KimiPDFGenerator

# 1. 初始化
transcriber = VideoTranscriber()
client = BailianClient()
generator = KimiPDFGenerator()

# 2. 收集竞品视频
video_urls = [
    "https://www.xiaohongshu.com/explore/xxx1",
    "https://www.xiaohongshu.com/explore/xxx2",
    "https://www.douyin.com/video/xxx",
]

# 3. 提取内容
results = transcriber.batch_transcribe(video_urls, method="jina")

# 4. AI 分析
all_content = "\n\n".join([r["transcript"] for r in results if r["success"]])

analysis = client.generate(f"""
请分析这些竞品视频的共同点和差异化：

{all_content}

输出：
1. 共同主题
2. 差异化亮点
3. 可借鉴的创意
4. 目标受众画像
""")

# 5. 生成报告
report = generator.generate_report(
    prompt=f"请生成详细的竞品分析报告：\n{analysis['content']}",
    title="竞品分析报告",
    wait_seconds=45,
)

print(f"报告已生成：{report['pdf_path']}")
```

---

**视频内容提取器已就绪！可以开始处理竞品分析了！** 🚀
