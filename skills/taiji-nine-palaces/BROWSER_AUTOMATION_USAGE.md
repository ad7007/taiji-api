# 浏览器自动化模块使用指南

## ✅ 测试成功

**测试时间**: 2026-03-18 00:46  
**生成文件**:
- PDF: `/root/.openclaw/workspace/content/pdfs/九宫格管理方法实战报告_20260318_004548.pdf`
- 截图：`/root/.openclaw/workspace/content/pdfs/九宫格管理方法实战报告_20260318_004548.png`

---

## 🚀 快速开始

### 基础用法

```python
from browser_automation import KimiPDFGenerator

generator = KimiPDFGenerator()

# 生成单个 PDF 报告
result = generator.generate_report(
    prompt="请生成一份关于 AI 助手的行业报告",
    title="AI 助手行业报告",
    wait_seconds=30,  # 等待内容生成时间
)

if result["success"]:
    print(f"PDF 已生成：{result['pdf_path']}")
    print(f"截图：{result['screenshot_path']}")
```

### 批量生成

```python
# 批量生成多个报告
prompts = [
    "九宫格管理方法详解",
    "AI 助手市场分析",
    "企业数字化转型指南",
]

titles = [
    "九宫格管理报告",
    "AI 助手市场报告",
    "数字化转型报告",
]

results = generator.batch_generate(prompts, titles, delay_seconds=10)

for i, result in enumerate(results):
    print(f"报告{i+1}: {result['pdf_path']} - {'成功' if result['success'] else '失败'}")
```

---

## ⚠️ 注意事项

### 1. Kimi 登录问题

当前 Kimi 需要**手机号 + 验证码登录**，有两种解决方案：

**方案 A：手动登录后保持会话**
```bash
# 1. 手动打开浏览器登录
agent-browser open https://kimi.moonshot.cn/
# 2. 扫码/验证码登录
# 3. 保持浏览器打开，Cookie 会保存

# 然后用自动化脚本时带上 Cookie（需要实现）
```

**方案 B：使用 API 而非浏览器**
```python
# 使用百炼 API 直接生成内容
from bailian_client import BailianClient

client = BailianClient()
result = client.generate("请生成九宫格管理报告...")

# 然后用其他工具转 PDF
```

### 2. 等待时间调整

不同内容生成时间不同，建议：
- 简短回答：10-20 秒
- 详细报告：30-60 秒
- 超长内容：60-120 秒

### 3. 文件命名

文件名自动使用时间戳，避免冲突：
```
九宫格管理方法实战报告_20260318_004548.pdf
                              ↓
                         日期_时分秒
```

---

## 🔧 集成到九宫格

### 2-产品质量宫

```python
# palace_2_product.py
from browser_automation import KimiPDFGenerator

class Palace2Product(PalaceBase):
    def __init__(self):
        super().__init__(...)
        self.pdf_generator = KimiPDFGenerator()
    
    def generate_whitepaper(self, title: str, outline: List[str]):
        prompt = f"请生成产品白皮书：{title}\n\n大纲：\n" + "\n".join(outline)
        
        result = self.pdf_generator.generate_report(
            prompt=prompt,
            title=title,
            wait_seconds=45,
        )
        
        return result
```

### 8-营销客服宫

```python
# palace_8_marketing.py
class Palace8Marketing(PalaceBase):
    def deliver_paid_content(self, customer_id: str, content_type: str):
        # 1. 生成 PDF
        # 2. 上传到云存储
        # 3. 发送下载链接
        pass
```

---

## 📊 成本估算

### 使用 Kimi（浏览器自动化）

| 项目 | 成本 |
|------|------|
| Kimi 使用费 | 免费（有额度限制） |
| 浏览器自动化 | 免费 |
| 时间成本 | 30-60 秒/报告 |

### 使用百炼 API

| 模型 | 2000 字成本 | 速度 |
|------|-------------|------|
| qwen-turbo | ¥0.03 | 5 秒 |
| qwen-plus | ¥0.12 | 8 秒 |
| qwen-max | ¥0.60 | 12 秒 |
| kimi2.5 | ¥0.24 | 10 秒 |

---

## 💡 最佳实践

### 1. 付费报告生成流程

```
用户付费 → 生成 PDF → 交付
   ↓
1. 收到付费通知
2. 调用 KimiPDFGenerator 生成
3. 质量检查（可选）
4. 上传到云存储
5. 发送下载链接给用户
```

### 2. 质量控制

```python
from content_sop import ContentSOP

sop = ContentSOP()

# 生成 PDF
result = generator.generate_report(prompt, title)

# 质量检查
pdf_content = Path(result["pdf_path"]).read_text()
quality = sop.quality_check(pdf_content)

if quality["overall"]["passed"]:
    # 交付给用户
    pass
else:
    # 重新生成或人工审核
    pass
```

### 3. 错误处理

```python
try:
    result = generator.generate_report(prompt, title)
    if not result["success"]:
        print(f"生成失败：{result.get('error')}")
        # 重试或降级方案
except Exception as e:
    print(f"异常：{e}")
```

---

## 📁 输出目录

**默认位置**: `/root/.openclaw/workspace/content/pdfs/`

可以自定义：
```python
generator = KimiPDFGenerator(output_dir="/path/to/custom/dir")
```

---

## 🔗 相关文件

- 模块代码：`/root/.openclaw/workspace/skills/taiji-nine-palaces/browser_automation.py`
- 测试报告：`/root/.openclaw/workspace/tests/BROWSER_TEST_REPORT.md`
- 内容 SOP: `/root/.openclaw/workspace/skills/taiji-nine-palaces/content_sop.py`

---

**Kimi PDF 生成器已就绪！可以开始生成付费报告了！** 🚀
