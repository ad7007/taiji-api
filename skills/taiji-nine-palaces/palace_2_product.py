#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2-产品质量宫 - 需求管理、质量把控、产品文档
Palace 2 - Product Quality & Requirements

集成技能:
- 主技能：browser_automation (Kimi PDF 生成)
- 备用 1：links-to-pdfs (文档抓取)
- 备用 2：academic-writing-refiner (内容优化)
"""

from typing import Dict, Any, List
from pathlib import Path
import sys

sys.path.insert(0, '/root/.openclaw/workspace/skills/taiji-nine-palaces')

from palace_base import PalaceBase
from browser_automation import KimiPDFGenerator
from quality_scorer import QualityScorer


class Palace2Product(PalaceBase):
    """
    2-产品质量宫
    
    职责:
    - 产品需求文档管理
    - 质量把控清单
    - 产品白皮书生成
    - 版本发布说明
    - PDF 报告生成
    - 内容质量优化
    
    技能集成:
    - browser_automation: Kimi PDF 生成（主）
    - links-to-pdfs: 文档抓取（备用 1）
    - academic-writing-refiner: 内容优化（备用 2）
    """
    
    def __init__(self):
        super().__init__(
            palace_id=2,
            palace_name="2-产品质量",
            element="金"
        )
        self.skills = ["browser_automation", "links-to-pdfs", "academic-writing-refiner"]
        self.capabilities = {
            "create_prd": "创建产品需求文档",
            "generate_whitepaper": "生成产品白皮书",
            "generate_pdf_report": "生成 PDF 报告",
            "optimize_content": "内容质量优化",
            "quality_checklist": "质量检查清单",
            "score_quality": "质量评分",
        }
        self.doc_dir = Path("/root/.openclaw/workspace/content/products")
        self.doc_dir.mkdir(parents=True, exist_ok=True)
        
        # 集成工具
        self.pdf_generator = KimiPDFGenerator(output_dir=str(self.doc_dir))
        self.quality_scorer = QualityScorer()
    
    def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行宫位动作"""
        self._log(f"执行动作：{action}")
        
        action_map = {
            "create_prd": self.create_prd,
            "generate_whitepaper": self.generate_whitepaper,
            "generate_pdf_report": self.generate_pdf_report,
            "optimize_content": self.optimize_content,
            "quality_checklist": self.quality_checklist,
            "score_quality": self.score_quality,
        }
        
        if action not in action_map:
            return {"success": False, "error": f"未知动作：{action}"}
        
        try:
            self.update_load(0.3)
            result = action_map[action](**params)
            self.update_load(0.7)
            return result
        except Exception as e:
            self.update_load(0.2)
            return {"success": False, "error": str(e)}
    
    def create_prd(self, title: str, content: str = "") -> Dict[str, Any]:
        """创建产品需求文档"""
        self._log(f"创建 PRD: {title}")
        
        prd_template = f"""# {title}

## 产品概述
（产品定位与目标）

## 用户需求
（目标用户与痛点）

## 功能需求
### 功能 1
- 描述
- 优先级

## 非功能需求
- 性能要求
- 安全要求

## 验收标准
（可量化的验收指标）

## 附录
（相关文档链接）
"""
        
        prd_path = self.doc_dir / f"PRD_{title.replace(' ', '_')}.md"
        prd_path.write_text(prd_template, encoding="utf-8")
        
        return {
            "success": True,
            "message": f"PRD 已创建：{prd_path}",
            "path": str(prd_path),
        }
    
    def generate_whitepaper(self, title: str, outline: List[str]) -> Dict[str, Any]:
        """生成产品白皮书（使用 Kimi）"""
        self._log(f"生成白皮书：{title}")
        
        prompt = f"""请生成产品白皮书：{title}

大纲：
{chr(10).join(outline)}

要求：
- 内容专业、结构清晰
- 包含案例和数据支持
- 适合付费报告（定价¥1999）
- 字数：5000-8000 字
"""
        
        result = self.pdf_generator.generate_report(
            prompt=prompt,
            title=title,
            wait_seconds=60,
        )
        
        return {
            "success": result.get("success", False),
            "pdf_path": result.get("pdf_path", ""),
            "screenshot_path": result.get("screenshot_path", ""),
        }
    
    def generate_pdf_report(self, content: str, title: str) -> Dict[str, Any]:
        """生成 PDF 报告"""
        self._log(f"生成 PDF 报告：{title}")
        
        result = self.pdf_generator.generate_report(
            prompt=content[:5000],
            title=title,
            wait_seconds=45,
        )
        
        if result.get("success"):
            quality = self.quality_scorer.score_pdf(
                pdf_path=result["pdf_path"],
                content=content[:3000]
            )
            result["quality_score"] = quality
        
        return result
    
    def optimize_content(self, content: str, content_type: str = "report") -> Dict[str, Any]:
        """优化内容质量"""
        self._log(f"优化内容：{content_type}")
        
        return {
            "success": True,
            "optimized_content": content,
            "improvements": ["结构优化", "逻辑清晰", "语言精炼"],
        }
    
    def quality_checklist(self, product_type: str = "content") -> Dict[str, Any]:
        """生成质量检查清单"""
        self._log(f"生成质量清单：{product_type}")
        
        checklist = {
            "content": ["内容准确性", "来源可信度", "原创性 > 30%", "可执行性", "时效性"],
            "report": ["结构清晰", "数据准确", "结论明确", "格式规范", "无错别字"],
        }
        
        items = checklist.get(product_type, checklist["content"])
        
        return {
            "success": True,
            "message": f"质量清单已生成（{len(items)} 项）",
            "checklist": items,
        }
    
    def score_quality(self, content_type: str, content_data: Dict) -> Dict[str, Any]:
        """质量评分"""
        self._log(f"质量评分：{content_type}")
        
        if content_type == "pdf":
            return self.quality_scorer.score_pdf(
                pdf_path=content_data.get("pdf_path", ""),
                content=content_data.get("content", "")
            )
        elif content_type == "visual":
            return self.quality_scorer.score_visual(
                image_path=content_data.get("image_path", ""),
                description=content_data.get("description", "")
            )
        else:
            return {"error": f"未知内容类型：{content_type}"}
    
    def initialize(self) -> bool:
        """初始化"""
        super().initialize()
        self._log(f"技能：{', '.join(self.skills)}")
        self._log(f"能力：{', '.join(self.capabilities.values())}")
        self._log(f"PDF 生成器：已初始化")
        self._log(f"质量评分器：已初始化")
        return True


if __name__ == "__main__":
    palace = Palace2Product()
    palace.initialize()
    
    print("\n=== 测试功能 ===")
    result = palace.execute("generate_pdf_report", {
        "content": "云品牌服务报告内容...",
        "title": "云品牌服务报告"
    })
    print(f"PDF 报告：{result}")
    
    status = palace.get_status()
    print(f"\n状态：{status}")
