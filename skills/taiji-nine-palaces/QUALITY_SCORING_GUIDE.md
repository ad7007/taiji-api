# 质量评分系统使用指南

## 🎯 功能说明

**为 PDF、视频、视觉内容提供专业质量评分**

支持：
- PDF 文档质量评分
- 视频内容质量评分
- 视觉设计质量评分

---

## 📊 评分维度

### PDF 质量评分

| 维度 | 权重 | 说明 |
|------|------|------|
| 内容完整性 | 30% | 是否全面、有深度 |
| 可读性 | 25% | 是否清晰、易懂 |
| 排版格式 | 20% | 格式是否规范、美观 |
| 视觉吸引力 | 15% | 设计是否吸引人 |
| 可执行性 | 10% | 是否有 actionable 建议 |

### 视频质量评分

| 维度 | 权重 | 说明 |
|------|------|------|
| 内容价值 | 35% | 信息密度、实用性 |
| 吸引力 | 25% | 是否引人入胜 |
| 清晰度 | 20% | 逻辑是否清晰 |
| 制作质量 | 20% | 脚本、剪辑质量 |

### 视觉质量评分

| 维度 | 权重 | 说明 |
|------|------|------|
| 设计质量 | 30% | 美感、创意 |
| 专业性 | 25% | 是否专业、精致 |
| 品牌一致性 | 20% | 是否符合品牌调性 |
| 色彩和谐 | 15% | 配色是否协调 |
| 字体排版 | 10% | 字体选择是否合适 |

---

## 🚀 快速开始

### PDF 质量评分

```python
from quality_scorer import QualityScorer

scorer = QualityScorer()

# 评分
result = scorer.score_pdf(
    pdf_path="/path/to/report.pdf",
    content="报告内容文本..."  # 用于 AI 分析
)

print(f"总分：{result['total_score']:.2f}")
print(f"等级：{result['level']}")
print(f"各维度评分：{result['scores']}")
```

### 视频质量评分

```python
result = scorer.score_video(
    video_url="https://www.bilibili.com/video/BV1xx",
    transcript="视频转录文本..."  # 用于 AI 分析
)

print(f"总分：{result['total_score']:.2f}")
print(f"等级：{result['level']}")
```

### 视觉质量评分

```python
result = scorer.score_visual(
    image_path="/path/to/design.png",
    description="专业的商业报告封面设计，蓝色主色调，简洁现代风格"
)

print(f"总分：{result['total_score']:.2f}")
print(f"等级：{result['level']}")
```

---

## 🎯 评分等级

| 分数范围 | 等级 | 说明 |
|----------|------|------|
| 0.9-1.0 | S - 卓越 | 行业标杆水平 |
| 0.8-0.9 | A - 优秀 | 高质量，可直接交付 |
| 0.7-0.8 | B - 良好 | 合格，小改进即可 |
| 0.6-0.7 | C - 合格 | 勉强合格，需改进 |
| 0.0-0.6 | D - 需改进 | 不合格，需重做 |

---

## 💡 集成到九宫格

### 6-物联监控宫

```python
from palace_6_monitor import Palace6Monitor

palace = Palace6Monitor()

# PDF 评分
result = palace.execute("score_pdf", {
    "pdf_path": "/path/to/report.pdf",
    "content": "报告内容..."
})

# 质量检查（通用）
result = palace.execute("quality_check", {
    "content_type": "pdf",
    "content_data": {
        "pdf_path": "/path/to/report.pdf",
        "content": "报告内容..."
    }
})
```

### 工作流集成

```python
# 在云品牌工作流中添加质量检查
class CloudBrandWorkflow:
    def _phase2_product_review(self, topic, phase1_results):
        # ... 生成报告
        
        # 质量检查（6-监控宫）
        quality_result = palace_6.score_pdf(
            pdf_path=draft_pdf,
            content=report_content
        )
        
        if quality_result['total_score'] < 0.7:
            # 质量不达标，需要改进
            return {"status": "need_improvement", "quality": quality_result}
        
        return {"status": "approved", "quality": quality_result}
```

---

## 📊 批量评分

```python
# 批量 PDF 评分
pdf_files = [
    "/path/to/report1.pdf",
    "/path/to/report2.pdf",
    "/path/to/report3.pdf",
]

results = []
for pdf_path in pdf_files:
    result = scorer.score_pdf(pdf_path)
    results.append(result)

# 统计
avg_score = sum(r['total_score'] for r in results) / len(results)
print(f"平均分数：{avg_score:.2f}")
print(f"S 级：{sum(1 for r in results if r['total_score'] >= 0.9)} 个")
print(f"A 级：{sum(1 for r in results if 0.8 <= r['total_score'] < 0.9)} 个")
```

---

## ⚠️ 注意事项

### 1. AI 评分依赖

- 需要配置百炼 API Key
- 未配置时使用默认分数
- 建议配置后使用

### 2. 内容长度限制

- AI 分析限制 3000 字符
- 长内容需要截断或分段
- 建议提供关键章节

### 3. 评分标准调整

```python
# 自定义评分标准
scorer.pdf_criteria = {
    "content_completeness": {"name": "内容完整性", "weight": 0.4},
    "readability": {"name": "可读性", "weight": 0.3},
    "actionability": {"name": "可执行性", "weight": 0.3},
}
```

---

## 💰 变现应用

### 质量评估服务

```
客户：帮我评估这份报告质量
流程：
1. 上传 PDF/视频
2. AI 质量评分
3. 生成评估报告
4. 改进建议

定价：¥199-599/份
```

### 内容优化服务

```
客户：帮我优化内容质量
流程：
1. 初始评分
2. 问题诊断
3. 优化建议
4. 复评确认

定价：¥599-1999/份
```

---

## 📁 输出示例

### PDF 评分结果

```json
{
  "type": "pdf",
  "file": "/path/to/report.pdf",
  "scores": {
    "content_completeness": 0.85,
    "readability": 0.78,
    "formatting": 0.82,
    "visual_appeal": 0.75,
    "actionability": 0.88
  },
  "total_score": 0.82,
  "level": "A - 优秀"
}
```

### 视频评分结果

```json
{
  "type": "video",
  "url": "https://www.bilibili.com/video/BV1xx",
  "scores": {
    "content_value": 0.92,
    "engagement": 0.85,
    "clarity": 0.88,
    "production_quality": 0.80
  },
  "total_score": 0.87,
  "level": "A - 优秀"
}
```

---

**质量评分系统已就绪！可以为 PDF、视频、视觉内容提供专业评分！** 🚀
