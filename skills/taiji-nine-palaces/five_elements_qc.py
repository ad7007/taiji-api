#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
五行质检系统 - 7宫专用
Five Elements Quality Control System

基于五行生克关系的视频质量检验
"""

from enum import Enum
from typing import Dict, List, Tuple
from dataclasses import dataclass


class FiveElements(Enum):
    """五行元素"""
    WOOD = "木"   # 结构
    FIRE = "火"   # 创意
    EARTH = "土"  # 稳定性
    METAL = "金"  # 硬性标准
    WATER = "水"  # 流畅性


@dataclass
class QCResult:
    """质检结果"""
    element: FiveElements
    score: float  # 0-100
    passed: bool
    issues: List[str]
    suggestions: List[str]


class FiveElementsQC:
    """五行质检器"""
    
    def __init__(self):
        self.results: Dict[FiveElements, QCResult] = {}
    
    def check_all(self, video_path: str = None, content: str = "") -> Dict:
        """执行五行质检"""
        
        # 木：结构检查
        self._check_wood(content)
        
        # 火：创意检查
        self._check_fire(content)
        
        # 土：稳定性检查
        self._check_earth(content)
        
        # 金：硬性标准
        self._check_metal(content)
        
        # 水：流畅性检查
        self._check_water(content)
        
        return self._generate_report()
    
    def _check_wood(self, content: str):
        """木 - 结构检查"""
        issues = []
        score = 100
        
        # 检查是否有明确的开头、中间、结尾
        if "开场" not in content and "开始" not in content and "开头" not in content:
            issues.append("缺少明确的开场")
            score -= 20
        
        if "结尾" not in content and "结束" not in content and "待续" not in content:
            issues.append("缺少明确的结尾")
            score -= 20
        
        # 检查内容长度
        if len(content) < 100:
            issues.append("内容过短")
            score -= 30
        
        passed = score >= 60
        suggestions = ["增加开场白", "完善结尾"] if not passed else []
        
        self.results[FiveElements.WOOD] = QCResult(
            element=FiveElements.WOOD,
            score=score,
            passed=passed,
            issues=issues,
            suggestions=suggestions
        )
    
    def _check_fire(self, content: str):
        """火 - 创意检查"""
        issues = []
        score = 100
        
        # 检查创意元素
        creative_keywords = ["创新", "突破", "独特", "新颖", "有趣"]
        found = [kw for kw in creative_keywords if kw in content]
        
        if len(found) < 2:
            issues.append("创意元素不足")
            score -= 30
        
        # 检查是否有吸引力
        if "？" not in content and "！" not in content:
            issues.append("缺少吸引人的表达")
            score -= 20
        
        passed = score >= 60
        suggestions = ["加入更多创意表达", "使用感叹句增强感染力"] if not passed else []
        
        self.results[FiveElements.FIRE] = QCResult(
            element=FiveElements.FIRE,
            score=score,
            passed=passed,
            issues=issues,
            suggestions=suggestions
        )
    
    def _check_earth(self, content: str):
        """土 - 稳定性检查"""
        issues = []
        score = 100
        
        # 检查主题一致性
        if len(content.split("。")) > 5:
            # 检查是否围绕一个主题
            issues.append("内容可能过于分散")
            score -= 20
        
        # 检查逻辑连贯性
        connectors = ["因此", "所以", "但是", "然后", "接着"]
        found_connectors = [c for c in connectors if c in content]
        if len(found_connectors) < 2:
            issues.append("逻辑连接不够流畅")
            score -= 20
        
        passed = score >= 60
        suggestions = ["聚焦核心主题", "增加逻辑连接词"] if not passed else []
        
        self.results[FiveElements.EARTH] = QCResult(
            element=FiveElements.EARTH,
            score=score,
            passed=passed,
            issues=issues,
            suggestions=suggestions
        )
    
    def _check_metal(self, content: str):
        """金 - 硬性标准"""
        issues = []
        score = 100
        
        # 硬性标准检查
        standards = [
            ("时长合适", len(content) >= 50 and len(content) <= 5000),
            ("无敏感词", True),  # 简化处理
            ("格式规范", "。" in content or "！" in content),
            ("信息完整", len(content.split()) >= 10),
        ]
        
        for standard, passed in standards:
            if not passed:
                issues.append(f"不满足：{standard}")
                score -= 15
        
        passed = score >= 70  # 金的标准更高
        suggestions = ["确保满足所有硬性标准"] if not passed else []
        
        self.results[FiveElements.METAL] = QCResult(
            element=FiveElements.METAL,
            score=score,
            passed=passed,
            issues=issues,
            suggestions=suggestions
        )
    
    def _check_water(self, content: str):
        """水 - 流畅性检查"""
        issues = []
        score = 100
        
        # 检查句式变化
        sentences = content.replace("！", "。").replace("？", "。").split("。")
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) > 0:
            avg_length = sum(len(s) for s in sentences) / len(sentences)
            if avg_length > 50:
                issues.append("句子过长，影响流畅性")
                score -= 20
            if avg_length < 10:
                issues.append("句子过短，表达不完整")
                score -= 20
        
        # 检查重复
        if len(sentences) != len(set(sentences)):
            issues.append("存在重复表达")
            score -= 15
        
        passed = score >= 60
        suggestions = ["调整句式长度", "删除重复内容"] if not passed else []
        
        self.results[FiveElements.WATER] = QCResult(
            element=FiveElements.WATER,
            score=score,
            passed=passed,
            issues=issues,
            suggestions=suggestions
        )
    
    def _generate_report(self) -> Dict:
        """生成质检报告"""
        total_score = sum(r.score for r in self.results.values()) / 5
        all_passed = all(r.passed for r in self.results.values())
        
        return {
            "total_score": round(total_score, 1),
            "passed": all_passed,
            "details": {
                elem.value: {
                    "score": r.score,
                    "passed": r.passed,
                    "issues": r.issues,
                    "suggestions": r.suggestions
                }
                for elem, r in self.results.items()
            },
            "summary": self._generate_summary()
        }
    
    def _generate_summary(self) -> str:
        """生成摘要"""
        passed_count = sum(1 for r in self.results.values() if r.passed)
        total = len(self.results)
        
        if passed_count == total:
            return f"✅ 五行质检全部通过 ({passed_count}/{total})"
        else:
            return f"⚠️ 五行质检未通过 ({passed_count}/{total})"


def quick_qc(content: str) -> Dict:
    """快速质检函数"""
    qc = FiveElementsQC()
    return qc.check_all(content=content)


if __name__ == "__main__":
    # 测试
    test_content = """
    大家好，我是米珞，太极系统的五宫主控。今天我们来学习AI智能体。
    首先，我们要了解什么是AI智能体。
    AI智能体就是能够自主感知、决策、行动的AI系统。
    比如，我现在就是一个AI智能体，我能感知你的消息，理解你的意图，然后做出回应。
    AI智能体的核心是什么？是效率！
    好了，今天就到这里，下期再见！
    """
    
    result = quick_qc(test_content)
    print("=== 五行质检报告 ===")
    print(f"总分: {result['total_score']}/100")
    print(f"结果: {result['summary']}")
    print()
    for elem, detail in result['details'].items():
        status = "✅" if detail['passed'] else "❌"
        print(f"{status} {elem}: {detail['score']}分")
        if detail['issues']:
            for issue in detail['issues']:
                print(f"   - {issue}")