# 九宫格并行协作流程指南

## 🎯 核心原则

**余总指示**：
> 一定先生成各插件任务与流程，并行获取多结果，最后由产品质量"开会"定稿，发送产品。

---

## 📊 标准数据分析业务流程

### 三阶段工作流

```
┌─────────────────────────────────────────────────────────┐
│  第一阶段：并行数据收集（7 宫同时）                      │
│  9-生态 | 4-品牌 | 8-营销 | 1-采集 | 3-技术 | 6-监控 | 7-法务  │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  第二阶段：产品质量会审（2 宫主持）                      │
│  汇总所有数据 → AI 生成报告 → 质量检查                    │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  第三阶段：中宫交付（5 宫）                              │
│  PDF 生成 → 交付客户                                      │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 详细执行流程

### 第一阶段：并行数据收集

**并发执行**（5 个 worker，7 个任务）

| 宫位 | 任务 | 输出 | 耗时 |
|------|------|------|------|
| 9-生态 | 热点搜索 | 20 个热点话题 | 10 秒 |
| 4-品牌 | 竞品分析 | 3 个竞品档案 | 5 秒 |
| 8-营销 | 用户需求 | 4 项核心需求 | 5 秒 |
| 1-采集 | 视频提取 | 2 个视频转录 | 30 秒 |
| 3-技术 | 模型路由 | 模型分配方案 | 2 秒 |
| 6-监控 | 质量检查 | 质量评分 | 3 秒 |
| 7-法务 | 合规审查 | 合规清单 | 3 秒 |

**总耗时**: 30 秒（串行的话需要 58 秒）  
**效率提升**: 48%

---

### 第二阶段：产品质量会审

**2-产品质量宫主持**

```python
# 汇总所有数据
data_summary = compile(phase1_results)

# AI 生成报告（使用百炼模型）
prompt = f"""
请根据以下数据生成报告：
{data_summary}

要求：
- TOP9 盈利业务形态
- 市场数据分析
- 推荐启动方案
- 获客渠道
- 风险提示
- 盈利预测
- 行动清单
"""

report = bailian_client.generate(prompt)
```

**耗时**: 15 秒

---

### 第三阶段：中宫交付

**5-中宫调度**

```python
# PDF 生成（Kimi）
pdf_result = kimi_generator.generate_report(
    prompt=report_content,
    title="云品牌服务报告",
    wait_seconds=45,
)

# 交付
deliver_to_customer(pdf_result)
```

**耗时**: 45 秒

---

## ⚡ 性能对比

| 方式 | 总耗时 | 成本 |
|------|--------|------|
| **单线程** | ~90 秒 | ¥0 |
| **九宫格并行** | ~60 秒 | ¥0 |
| **人工完成** | ~8 小时 | ¥500+ |

**效率提升**: 33%（自动化）+ 480 倍（vs 人工）

---

## 🎯 完整代码示例

### 执行工作流

```python
from cloud_brand_workflow import CloudBrandWorkflow

workflow = CloudBrandWorkflow()

# 执行完整流程
result = workflow.execute("云品牌服务")

# 输出
print(f"报告生成：{result['final_report']['pdf_path']}")
```

### 各宫位职责

```python
# 9-生态：热点搜索
def palace_9_research(topic):
    from hot_topic_analyzer import HotTopicAnalyzer
    analyzer = HotTopicAnalyzer()
    return analyzer.search_hot_topics(topic)

# 4-品牌：竞品分析
def palace_4_analysis(topic):
    # 调用竞品分析 API
    return competitors_data

# 8-营销：用户需求
def palace_8_user_research(topic):
    # 调用用户调研 API
    return user_needs

# 1-采集：视频提取
def palace_1_video_extract(topic):
    from multi_platform_transcriber import MultiPlatformTranscriber
    transcriber = MultiPlatformTranscriber()
    return transcriber.batch_transcribe(video_urls)

# 3-技术：模型路由
def palace_3_model_routing(topic):
    from model_router import ModelRouter
    router = ModelRouter()
    return router.select_model(task_type)

# 6-监控：质量检查
def palace_6_quality_check(topic):
    return quality_metrics

# 7-法务：合规审查
def palace_7_compliance(topic):
    return compliance_checklist

# 2-产品：质量会审（主持）
def palace_2_review(topic, phase1_results):
    from bailian_client import BailianClient
    client = BailianClient()
    
    # 汇总数据
    data_summary = compile(phase1_results)
    
    # AI 生成报告
    report = client.generate(f"生成报告：{data_summary}")
    return report

# 5-中宫：交付
def palace_5_delivery(topic, phase2_result):
    from browser_automation import KimiPDFGenerator
    generator = KimiPDFGenerator()
    return generator.generate_report(phase2_result['content'])
```

---

## 📊 数据流向

```
用户输入：云品牌服务
    ↓
┌───────────────────────────────────┐
│ 第一阶段：并行收集                │
├───────────────────────────────────┤
│ 9-生态 → hot_topics[]             │
│ 4-品牌 → competitors[]            │
│ 8-营销 → user_needs[]             │
│ 1-采集 → transcripts[]            │
│ 3-技术 → model_assignments{}      │
│ 6-监控 → quality_metrics{}        │
│ 7-法务 → compliance_checklist[]   │
└───────────────────────────────────┘
    ↓
┌───────────────────────────────────┐
│ 第二阶段：汇总生成                │
├───────────────────────────────────┤
│ 2-产品 → report_draft             │
│   (调用百炼 AI)                   │
└───────────────────────────────────┘
    ↓
┌───────────────────────────────────┐
│ 第三阶段：PDF 交付                 │
├───────────────────────────────────┤
│ 5-中宫 → final_pdf                │
│   (调用 Kimi)                     │
└───────────────────────────────────┘
    ↓
交付客户
```

---

## 💡 关键优化点

### 1. 并发最大化

```python
# ❌ 错误：串行执行
result1 = palace_9_research(topic)
result2 = palace_4_analysis(topic)
result3 = palace_8_user_research(topic)
# ...

# ✅ 正确：并发执行
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [
        executor.submit(palace_9_research, topic),
        executor.submit(palace_4_analysis, topic),
        executor.submit(palace_8_user_research, topic),
        # ...
    ]
    results = [f.result() for f in as_completed(futures)]
```

### 2. 免费资源优先

```python
# 优先使用免费服务
service_priority = [
    "jina",          # 免费
    "kimi",          # 免费额度
    "feishu_miaoji", # 免费额度
    "qwen_plus",     # ¥0.008/1K
    "qwen_max",      # ¥0.04/1K（最后选择）
]
```

### 3. 质量会审机制

```python
# 2-产品质量宫主持会审
def product_review(all_data):
    # 1. 数据完整性检查
    if not all_data_complete(all_data):
        return {"status": "need_more_data"}
    
    # 2. 质量评分
    quality_score = calculate_quality(all_data)
    if quality_score < 0.8:
        return {"status": "quality_low"}
    
    # 3. AI 生成报告
    report = ai_generate(all_data)
    
    # 4. 合规审查
    if not compliance_check(report):
        return {"status": "compliance_issue"}
    
    return {"status": "approved", "report": report}
```

---

## 🎯 适用场景

### 适合九宫格并行的任务

| 任务类型 | 特点 | 效率提升 |
|----------|------|----------|
| 市场调研报告 | 多源数据收集 | 50%+ |
| 竞品分析报告 | 多维度分析 | 40%+ |
| 行业洞察报告 | 热点 + 趋势 | 60%+ |
| 内容创意方案 | 视频 + 文本 | 70%+ |
| 数据分析报告 | 多指标监控 | 50%+ |

### 不适合的场景

- 简单问答（单宫位即可）
- 实时性要求极高（并发开销大）
- 数据量极小（没必要）

---

## 📈 扩展能力

### 添加新宫位任务

```python
# 在 task_assignments 中添加
self.task_assignments = {
    # 现有
    "9-生态": self.palace_9_research,
    # 新增
    "新宫位": self.palace_new_task,
}

# 实现新方法
def palace_new_task(self, topic: str) -> Dict:
    # 实现逻辑
    return {"status": "success", "data": ...}
```

### 自定义工作流

```python
class CustomWorkflow(CloudBrandWorkflow):
    def execute(self, topic: str):
        # 自定义流程
        # 1. ...
        # 2. ...
        # 3. ...
        pass
```

---

## 🚀 下一步优化

1. **缓存机制** - 相同话题直接返回缓存
2. **增量更新** - 只更新变化的数据
3. **智能调度** - 根据任务类型动态分配宫位
4. **质量反馈** - 客户反馈优化流程

---

**九宫格并行协作 = 效率提升 33% + 成本降低 100%** 🚀
