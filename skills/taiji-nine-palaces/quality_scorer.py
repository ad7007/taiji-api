#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
质量评分器 - PDF/视频/视觉质量评估
Quality Scorer - PDF/Video/Visual Quality Assessment

使用免费 API 和 AI 模型进行质量评分
"""

import subprocess
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class QualityScorer:
    """
    质量评分器
    
    评分维度：
    - PDF 质量（内容完整性、排版、可读性）
    - 视频质量（清晰度、内容价值、完播率）
    - 视觉质量（设计美感、专业性、品牌一致性）
    """
    
    def __init__(self):
        # 评分标准
        self.pdf_criteria = {
            "content_completeness": {"name": "内容完整性", "weight": 0.3},
            "readability": {"name": "可读性", "weight": 0.25},
            "formatting": {"name": "排版格式", "weight": 0.2},
            "visual_appeal": {"name": "视觉吸引力", "weight": 0.15},
            "actionability": {"name": "可执行性", "weight": 0.1},
        }
        
        self.video_criteria = {
            "clarity": {"name": "清晰度", "weight": 0.2},
            "content_value": {"name": "内容价值", "weight": 0.35},
            "engagement": {"name": "吸引力", "weight": 0.25},
            "production_quality": {"name": "制作质量", "weight": 0.2},
        }
        
        self.visual_criteria = {
            "design_quality": {"name": "设计质量", "weight": 0.3},
            "professionalism": {"name": "专业性", "weight": 0.25},
            "brand_consistency": {"name": "品牌一致性", "weight": 0.2},
            "color_harmony": {"name": "色彩和谐", "weight": 0.15},
            "typography": {"name": "字体排版", "weight": 0.1},
        }
    
    def score_pdf(self, pdf_path: str, content: str = None) -> Dict[str, Any]:
        """
        PDF 质量评分
        
        Args:
            pdf_path: PDF 文件路径
            content: PDF 内容（可选，用于 AI 分析）
        
        Returns:
            评分结果
        """
        scores = {}
        
        # 1. 文件基本信息
        pdf_file = Path(pdf_path)
        if not pdf_file.exists():
            return {"error": "PDF 文件不存在"}
        
        file_size_mb = pdf_file.stat().st_size / 1024 / 1024
        scores["file_size"] = min(1.0, file_size_mb / 10)  # 10MB 满分
        
        # 2. 页数（如果有 pdftk 或 pdfinfo）
        try:
            result = subprocess.run(
                f'pdfinfo "{pdf_path}" 2>/dev/null | grep Pages',
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                pages = int(result.stdout.split(":")[1].strip())
                scores["page_count"] = min(1.0, pages / 20)  # 20 页满分
        except:
            scores["page_count"] = 0.5
        
        # 3. AI 内容分析
        if content:
            ai_scores = self._ai_score_content(content, "pdf")
            scores.update(ai_scores)
        else:
            # 默认分数
            scores["content_completeness"] = 0.7
            scores["readability"] = 0.7
            scores["actionability"] = 0.7
        
        # 4. 计算加权总分
        total_score = self._calculate_weighted_score(scores, self.pdf_criteria)
        
        return {
            "type": "pdf",
            "file": str(pdf_path),
            "scores": scores,
            "criteria": self.pdf_criteria,
            "total_score": total_score,
            "level": self._score_to_level(total_score),
        }
    
    def score_video(self, video_url: str, transcript: str = None) -> Dict[str, Any]:
        """
        视频质量评分
        
        Args:
            video_url: 视频链接
            transcript: 视频转录文本（可选）
        
        Returns:
            评分结果
        """
        scores = {}
        
        # 1. 基础信息（如果有）
        scores["platform"] = self._detect_platform(video_url)
        
        # 2. AI 内容分析
        if transcript:
            ai_scores = self._ai_score_content(transcript, "video")
            scores.update(ai_scores)
        else:
            # 默认分数
            scores["content_value"] = 0.6
            scores["engagement"] = 0.6
            scores["clarity"] = 0.6
            scores["production_quality"] = 0.6
        
        # 3. 计算加权总分
        total_score = self._calculate_weighted_score(scores, self.video_criteria)
        
        return {
            "type": "video",
            "url": video_url,
            "scores": scores,
            "criteria": self.video_criteria,
            "total_score": total_score,
            "level": self._score_to_level(total_score),
        }
    
    def score_visual(self, image_path: str = None, description: str = None) -> Dict[str, Any]:
        """
        视觉质量评分
        
        Args:
            image_path: 图片文件路径（可选）
            description: 视觉内容描述（可选，用于 AI 分析）
        
        Returns:
            评分结果
        """
        scores = {}
        
        # 1. 文件信息
        if image_path:
            img_file = Path(image_path)
            if img_file.exists():
                file_size_mb = img_file.stat().st_size / 1024 / 1024
                scores["file_quality"] = min(1.0, file_size_mb / 5)  # 5MB 满分
        
        # 2. AI 视觉分析
        if description:
            ai_scores = self._ai_score_visual(description)
            scores.update(ai_scores)
        else:
            # 默认分数
            scores["design_quality"] = 0.7
            scores["professionalism"] = 0.7
            scores["brand_consistency"] = 0.7
        
        # 3. 计算加权总分
        total_score = self._calculate_weighted_score(scores, self.visual_criteria)
        
        return {
            "type": "visual",
            "file": image_path,
            "scores": scores,
            "criteria": self.visual_criteria,
            "total_score": total_score,
            "level": self._score_to_level(total_score),
        }
    
    def _ai_score_content(self, content: str, content_type: str) -> Dict[str, float]:
        """AI 内容评分"""
        from bailian_client import BailianClient
        
        client = BailianClient()
        
        # 检查是否配置 API Key
        if client.mock_mode:
            # 未配置 API Key 时返回默认分数
            if content_type == "pdf":
                return {
                    "content_completeness": 0.75,
                    "readability": 0.72,
                    "actionability": 0.78,
                }
            else:  # video
                return {
                    "content_value": 0.70,
                    "engagement": 0.68,
                    "clarity": 0.72,
                    "production_quality": 0.65,
                }
        
        if content_type == "pdf":
            prompt = f"""请评估以下内容的质量（0-1 分）：

内容：{content[:3000]}...

请评分：
1. 内容完整性（是否全面、有深度）
2. 可读性（是否清晰、易懂）
3. 可执行性（是否有 actionable 建议）

返回 JSON 格式：
{{"content_completeness": 0.8, "readability": 0.7, "actionability": 0.9}}
"""
        else:  # video
            prompt = f"""请评估以下视频转录内容的质量（0-1 分）：

内容：{content[:3000]}...

请评分：
1. 内容价值（信息密度、实用性）
2. 吸引力（是否引人入胜）
3. 清晰度（逻辑是否清晰）
4. 制作质量（脚本质量）

返回 JSON 格式：
{{"content_value": 0.8, "engagement": 0.7, "clarity": 0.9, "production_quality": 0.8}}
"""
        
        try:
            result = client.generate(prompt)
            # 解析 JSON 响应
            content_text = result.get("content", "{}")
            start_idx = content_text.find("{")
            end_idx = content_text.rfind("}") + 1
            if start_idx >= 0 and end_idx > start_idx:
                scores = json.loads(content_text[start_idx:end_idx])
                return {k: float(v) for k, v in scores.items()}
        except:
            pass
        
        # 失败时返回默认分数
        if content_type == "pdf":
            return {"content_completeness": 0.7, "readability": 0.7, "actionability": 0.7}
        else:
            return {"content_value": 0.65, "engagement": 0.65, "clarity": 0.7, "production_quality": 0.65}
    
    def _ai_score_visual(self, description: str) -> Dict[str, float]:
        """AI 视觉评分"""
        from bailian_client import BailianClient
        
        client = BailianClient()
        
        # 检查是否配置 API Key
        if client.mock_mode:
            return {
                "design_quality": 0.72,
                "professionalism": 0.75,
                "brand_consistency": 0.70,
                "color_harmony": 0.73,
                "typography": 0.70,
            }
        
        prompt = f"""请评估以下视觉设计的质量（0-1 分）：

描述：{description}

请评分：
1. 设计质量（美感、创意）
2. 专业性（是否专业、精致）
3. 品牌一致性（是否符合品牌调性）
4. 色彩和谐（配色是否协调）
5. 字体排版（字体选择是否合适）

返回 JSON 格式：
{{"design_quality": 0.8, "professionalism": 0.7, "brand_consistency": 0.9, "color_harmony": 0.8, "typography": 0.7}}
"""
        
        try:
            result = client.generate(prompt)
            content_text = result.get("content", "{}")
            start_idx = content_text.find("{")
            end_idx = content_text.rfind("}") + 1
            if start_idx >= 0 and end_idx > start_idx:
                scores = json.loads(content_text[start_idx:end_idx])
                return {k: float(v) for k, v in scores.items()}
        except:
            pass
        
        return {
            "design_quality": 0.7,
            "professionalism": 0.7,
            "brand_consistency": 0.7,
            "color_harmony": 0.7,
            "typography": 0.7,
        }
    
    def _calculate_weighted_score(self, scores: Dict[str, float], criteria: Dict[str, Dict]) -> float:
        """计算加权总分"""
        total = 0.0
        weight_sum = 0.0
        
        for criterion, config in criteria.items():
            if criterion in scores:
                total += scores[criterion] * config["weight"]
                weight_sum += config["weight"]
        
        return total / weight_sum if weight_sum > 0 else 0.0
    
    def _score_to_level(self, score: float) -> str:
        """分数转等级"""
        if score >= 0.9:
            return "S - 卓越"
        elif score >= 0.8:
            return "A - 优秀"
        elif score >= 0.7:
            return "B - 良好"
        elif score >= 0.6:
            return "C - 合格"
        else:
            return "D - 需改进"
    
    def _detect_platform(self, url: str) -> str:
        """检测视频平台"""
        if "douyin.com" in url:
            return "抖音"
        elif "xiaohongshu.com" in url:
            return "小红书"
        elif "bilibili.com" in url:
            return "B 站"
        elif "youtube.com" in url:
            return "YouTube"
        else:
            return "未知"


def demo():
    """演示"""
    print("="*60)
    print("        质量评分器演示")
    print("="*60)
    
    scorer = QualityScorer()
    
    # PDF 评分
    print("\n【PDF 质量评分】")
    pdf_result = scorer.score_pdf(
        pdf_path="/root/.openclaw/workspace/content/pdfs/云品牌服务_最强_9_种盈利业务形态与流程_20260318_010942.pdf",
        content="云品牌服务报告内容..."
    )
    print(f"总分：{pdf_result.get('total_score', 0):.2f} - {pdf_result.get('level', 'N/A')}")
    
    # 视频评分
    print("\n【视频质量评分】")
    video_result = scorer.score_video(
        video_url="https://www.bilibili.com/video/BV1xx411c7mD",
        transcript="视频内容转录..."
    )
    print(f"总分：{video_result.get('total_score', 0):.2f} - {video_result.get('level', 'N/A')}")
    
    # 视觉评分
    print("\n【视觉质量评分】")
    visual_result = scorer.score_visual(
        description="专业的商业报告封面设计，蓝色主色调，简洁现代风格"
    )
    print(f"总分：{visual_result.get('total_score', 0):.2f} - {visual_result.get('level', 'N/A')}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    demo()
