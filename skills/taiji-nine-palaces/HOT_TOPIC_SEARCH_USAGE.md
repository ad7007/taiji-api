# 热点搜索与分析使用指南

## 🎯 功能说明

**输入关键词 → 生成 9 个热点标题排名 + 数据分析**

支持平台：
- 抖音热榜
- 小红书热榜
- B 站热榜
- 微博热搜
- 知乎热榜
- 微信视频号

---

## 🚀 快速开始

### 基础用法

```python
from hot_topic_analyzer import HotTopicAnalyzer

analyzer = HotTopicAnalyzer()

# 搜索热点
result = analyzer.search_hot_topics(
    keyword="AI 助手",
    platforms=["douyin", "xiaohongshu", "bilibili"],
    top_n=9
)

if result["success"]:
    print(f"找到 {len(result['top_topics'])} 个热点")
    print(f"报告：{result['output_files'][0]}")
    
    # 显示 TOP9
    for i, topic in enumerate(result["top_topics"], 1):
        print(f"{i}. {topic['title']}")
```

---

## 📊 输出示例

### TOP9 热点标题排名

```markdown
# 热点数据分析报告

**关键词**: AI 助手
**时间**: 2026-03-18_010113
**平台**: 抖音，小红书，B 站

---

## 🔥 TOP9 热点标题排名

**1. AI 助手如何改变工作方式**
- 平台：抖音
- 排名：3
- 热度：1,234,567
- 相关性：2.85

**2. 我用 AI 助手提升了 10 倍效率**
- 平台：小红书
- 排名：7
- 热度：567,890
- 相关性：2.65

**3. B 站 UP 主都在用的 AI 工具**
- 平台：B 站
- 排名：12
- 热度：345,678
- 相关性：2.45

...

## 📊 数据分析

- **相关热点总数**: 45
- **平均相关性**: 2.15
- **热度趋势**: rising 🔥
- **最热平台**: 抖音

### 平台分布
- 抖音：15 个
- 小红书：12 个
- B 站：10 个
- 微博：5 个
- 知乎：3 个

## 💡 建议

- 关键词'AI 助手'热度很高，建议快速跟进
- 相关内容与关键词高度相关，适合深度创作
```

---

## 💰 变现应用

### 1. 竞品监控服务

```
客户：帮我监控竞品动态
流程：
1. 输入竞品品牌名
2. 搜索各平台热点
3. 生成监控报告
4. 每日/周推送

定价：¥999/月
```

### 2. 内容创意服务

```
客户：我需要内容创意
流程：
1. 输入行业关键词
2. 搜索热门话题
3. 分析热点趋势
4. 生成创意方案

定价：¥599/份
```

### 3. 市场洞察报告

```
客户：想了解行业趋势
流程：
1. 输入行业名称
2. 搜索相关热点
3. 数据分析
4. 生成洞察报告

定价：¥1999-4999/份
```

---

## 🔧 完整工作流

### 1. 收集热点

```python
from hot_topic_analyzer import HotTopicAnalyzer

analyzer = HotTopicAnalyzer()

# 搜索多个关键词
keywords = ["AI 助手", "数字化转型", "九宫格管理"]

all_results = []
for keyword in keywords:
    result = analyzer.search_hot_topics(keyword, top_n=9)
    all_results.append(result)
```

### 2. AI 分析趋势

```python
from bailian_client import BailianClient

client = BailianClient()

# 汇总热点
all_topics = "\n\n".join([
    f"{r['keyword']}:\n" + "\n".join([t['title'] for t in r['top_topics']])
    for r in all_results if r['success']
])

# AI 分析
prompt = f"""请分析这些热点话题的趋势：

{all_topics}

请提供：
1. 共同主题
2. 热门关键词
3. 内容创作方向建议
4. 目标受众分析
"""

analysis = client.generate(prompt)
print(analysis["content"])
```

### 3. 生成报告

```python
from browser_automation import KimiPDFGenerator

generator = KimiPDFGenerator()

report = generator.generate_report(
    prompt=f"请生成市场热点分析报告：\n{analysis['content']}",
    title="市场热点分析报告",
    wait_seconds=45,
)

print(f"报告已生成：{report['pdf_path']}")
```

---

## ⚠️ 注意事项

### 1. API 限流问题

**问题**: Jina Reader 对抖音/小红书限流

**解决方案**:
- 使用备用 API（vvhan、uapis）
- 使用 Kimi 搜索
- 浏览器自动化

### 2. 数据更新频率

| 平台 | 更新频率 | 建议查询间隔 |
|------|----------|--------------|
| 抖音 | 实时 | 5 分钟+ |
| 微博 | 实时 | 5 分钟+ |
| B 站 | 每小时 | 30 分钟+ |
| 知乎 | 实时 | 10 分钟+ |
| 小红书 | 每小时 | 30 分钟+ |

### 3. 批量处理

```python
# 避免频繁请求
import time

keywords = ["关键词 1", "关键词 2", "关键词 3"]
for kw in keywords:
    result = analyzer.search_hot_topics(kw)
    time.sleep(2)  # 间隔 2 秒
```

---

## 📁 输出文件

**默认目录**: `/root/.openclaw/workspace/content/hot_topics/`

**文件命名**:
```
hot_topics_AI_助手_20260318_010113.md
hot_topics_九宫格_20260318_010129.md
```

---

## 🎯 最佳实践

### 1. 监控竞品

```python
# 竞品品牌列表
competitors = ["竞品 A", "竞品 B", "竞品 C"]

for competitor in competitors:
    result = analyzer.search_hot_topics(competitor)
    # 保存结果
```

### 2. 发现趋势

```python
# 行业关键词
industry_keywords = ["AI", "数字化", "自动化", "SaaS"]

# 批量搜索
results = []
for kw in industry_keywords:
    result = analyzer.search_hot_topics(kw, top_n=20)
    results.append(result)

# 分析共同趋势
```

### 3. 内容规划

```python
# 每月搜索一次
monthly_keywords = [
    "春节营销",
    "情人节活动",
    "五一促销",
]

for kw in monthly_keywords:
    result = analyzer.search_hot_topics(kw)
    # 生成内容创意
```

---

## 💡 高级用法

### 自定义平台

```python
# 只搜索特定平台
result = analyzer.search_hot_topics(
    keyword="AI 助手",
    platforms=["douyin", "xiaohongshu"],  # 只搜索抖音和小红书
    top_n=9
)
```

### 导出数据

```python
import json

result = analyzer.search_hot_topics("AI 助手")

# 导出 JSON
json_file = analyzer.output_dir / f"hot_topics_{result['timestamp']}.json"
json_file.write_text(json.dumps(result, ensure_ascii=False, indent=2))
```

---

**热点搜索器已就绪！输入关键词即可生成 9 个热点标题排名和数据分析！** 🚀
