#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
6-物联监控宫 - 质量监控、评分系统
Palace 6 - Quality Monitoring & Scoring
"""

from typing import Dict, Any
from pathlib import Path
import sys

sys.path.insert(0, '/root/.openclaw/workspace/skills/taiji-nine-palaces')

from palace_base import PalaceBase
from quality_scorer import QualityScorer


class Palace6Monitor(PalaceBase):
    """
    6-物联监控宫
    
    职责:
    - PDF 质量评分
    - 视频质量评分
    - 视觉质量评分
    - 质量监控告警
    
    技能:
    - quality_scorer: 质量评分器
    """
    
    def __init__(self):
        super().__init__(
            palace_id=6,
            palace_name="6-物联监控",
            element="火"
        )
        self.skills = ["quality_scorer"]
        self.capabilities = {
            "pdf_scoring": "PDF 质量评分",
            "video_scoring": "视频质量评分",
            "visual_scoring": "视觉质量评分",
            "quality_alert": "质量告警",
        }
        self.scorer = QualityScorer()
    
    def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行宫位动作"""
        self._log(f"执行动作：{action}")
        
        action_map = {
            "score_pdf": self.score_pdf,
            "score_video": self.score_video,
            "score_visual": self.score_visual,
            "quality_check": self.quality_check,
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
    
    def score_pdf(self, pdf_path: str, content: str = None) -> Dict[str, Any]:
        """PDF 质量评分"""
        self._log(f"PDF 评分：{pdf_path}")
        return self.scorer.score_pdf(pdf_path, content)
    
    def score_video(self, video_url: str, transcript: str = None) -> Dict[str, Any]:
        """视频质量评分"""
        self._log(f"视频评分：{video_url}")
        return self.scorer.score_video(video_url, transcript)
    
    def score_visual(self, image_path: str = None, description: str = None) -> Dict[str, Any]:
        """视觉质量评分"""
        self._log(f"视觉评分")
        return self.scorer.score_visual(image_path, description)
    
    def quality_check(self, content_type: str, content_data: Dict) -> Dict[str, Any]:
        """质量检查（通用）"""
        self._log(f"质量检查：{content_type}")
        
        if content_type == "pdf":
            return self.score_pdf(**content_data)
        elif content_type == "video":
            return self.score_video(**content_data)
        elif content_type == "visual":
            return self.score_visual(**content_data)
        else:
            return {"success": False, "error": f"未知内容类型：{content_type}"}
    
    def initialize(self) -> bool:
        """初始化"""
        super().initialize()
        self._log(f"技能：{', '.join(self.skills)}")
        self._log(f"能力：{', '.join(self.capabilities.values())}")
        return True


if __name__ == "__main__":
    palace = Palace6Monitor()
    palace.initialize()
    
    print("\n=== 测试功能 ===")
    
    # PDF 评分
    result = palace.execute("score_pdf", {
        "pdf_path": "/root/.openclaw/workspace/content/pdfs/test.pdf",
        "content": "测试内容..."
    })
    print(f"PDF 评分：{result}")
    
    # 状态
    status = palace.get_status()
    print(f"\n状态：{status}")
