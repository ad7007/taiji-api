#!/usr/bin/env python3
"""
4 宫 - 品牌战略核心

职责：
1. 品牌定位（差异化、价值主张）
2. 竞品分析（市场调研、对比分析）
3. 内容策略（话题规划、发布计划）
4. 品牌资产管理（视觉、调性、slogan）

自动组队：1宫采集 → 4宫分析 → 7宫验收 → 5宫交付
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field


@dataclass
class Brand:
    """品牌数据类"""
    brand_id: str
    name: str
    positioning: str  # 定位
    value_proposition: str  # 价值主张
    target_audience: str  # 目标受众
    tone: str  # 品牌调性
    slogan: Optional[str] = None
    competitors: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)


@dataclass
class Competitor:
    """竞品数据类"""
    name: str
    url: Optional[str] = None
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    pricing: Optional[str] = None
    features: List[str] = field(default_factory=list)
    market_share: Optional[float] = None


@dataclass
class ContentPlan:
    """内容计划"""
    plan_id: str
    topic: str
    content_type: str  # article/video/post/ad
    platform: str
    scheduled_date: datetime
    status: str = "planned"  # planned/published/completed
    keywords: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)


class Palace4Brand:
    """
    4 宫 - 品牌战略
    
    使用示例:
        brand = Palace4Brand()
        
        # 品牌定位
        positioning = brand.define_positioning(
            name="太极系统",
            target="创业者",
            differentiation="1+8智能体协作"
        )
        
        # 竞品分析
        analysis = brand.analyze_competitor("竞品A", ...)
        
        # 内容规划
        plan = brand.create_content_plan(...)
    """
    
    def __init__(self):
        self.palace_id = 4
        self.palace_name = "品牌战略"
        
        # 品牌库
        self.brands: Dict[str, Brand] = {}
        self.competitors: Dict[str, Competitor] = {}
        self.content_plans: Dict[str, ContentPlan] = {}
        
        # 分析历史
        self.analysis_history: List[Dict] = []
    
    # ========== 品牌定位 ==========
    
    def define_positioning(self,
                          name: str,
                          target: str,
                          differentiation: str,
                          value: str = None,
                          tone: str = "professional") -> Brand:
        """
        定义品牌定位
        
        Args:
            name: 品牌名称
            target: 目标受众
            differentiation: 差异化卖点
            value: 价值主张
            tone: 品牌调性
        
        Returns:
            Brand 对象
        """
        brand_id = f"brand_{name.lower().replace(' ', '_')}"
        
        # 自动生成价值主张
        if not value:
            value = f"为{target}提供{differentiation}解决方案"
        
        # 自动生成 slogan
        slogan = self._generate_slogan(name, differentiation)
        
        brand = Brand(
            brand_id=brand_id,
            name=name,
            positioning=f"面向{target}的{differentiation}专家",
            value_proposition=value,
            target_audience=target,
            tone=tone,
            slogan=slogan,
            keywords=[name, differentiation, target]
        )
        
        self.brands[brand_id] = brand
        return brand
    
    def _generate_slogan(self, name: str, differentiation: str) -> str:
        """生成品牌标语"""
        templates = [
            f"{name}，让{differentiation}更简单",
            f"选择{name}，选择{differentiation}",
            f"{name}，{differentiation}领航者",
            f"专注{differentiation}，信赖{name}"
        ]
        
        import random
        return random.choice(templates)
    
    def get_brand_identity(self, brand_id: str) -> Dict[str, Any]:
        """获取品牌身份信息"""
        brand = self.brands.get(brand_id)
        if not brand:
            return {"error": "Brand not found"}
        
        return {
            "name": brand.name,
            "positioning": brand.positioning,
            "value_proposition": brand.value_proposition,
            "target_audience": brand.target_audience,
            "tone": brand.tone,
            "slogan": brand.slogan,
            "keywords": brand.keywords
        }
    
    # ========== 竞品分析 ==========
    
    def analyze_competitor(self,
                          name: str,
                          url: Optional[str] = None,
                          strengths: Optional[List[str]] = None,
                          weaknesses: Optional[List[str]] = None,
                          pricing: Optional[str] = None,
                          features: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        分析竞品
        
        Args:
            name: 竞品名称
            url: 竞品网址
            strengths: 优势列表
            weaknesses: 劣势列表
            pricing: 定价
            features: 功能列表
        
        Returns:
            分析报告
        """
        competitor = Competitor(
            name=name,
            url=url,
            strengths=strengths or [],
            weaknesses=weaknesses or [],
            pricing=pricing,
            features=features or []
        )
        
        self.competitors[name] = competitor
        
        # 生成分析报告
        report = {
            "competitor": name,
            "analyzed_at": datetime.now().isoformat(),
            "summary": self._generate_competitor_summary(competitor),
            "strengths": strengths or ["待调研"],
            "weaknesses": weaknesses or ["待调研"],
            "pricing": pricing or "待调研",
            "features": features or ["待调研"],
            "recommendation": self._generate_recommendation(competitor)
        }
        
        self.analysis_history.append(report)
        return report
    
    def _generate_competitor_summary(self, competitor: Competitor) -> str:
        """生成竞品摘要"""
        parts = [f"{competitor.name} 是市场主要竞品之一。"]
        
        if competitor.strengths:
            parts.append(f"其优势在于：{', '.join(competitor.strengths[:3])}。")
        
        if competitor.weaknesses:
            parts.append(f"但其存在：{', '.join(competitor.weaknesses[:3])}等不足。")
        
        return " ".join(parts)
    
    def _generate_recommendation(self, competitor: Competitor) -> str:
        """生成竞争策略建议"""
        if competitor.weaknesses:
            return f"建议针对其{competitor.weaknesses[0]}的弱点，强化我们在这方面的优势。"
        return "建议进一步调研其产品和市场策略，找到差异化竞争点。"
    
    def compare_competitors(self, 
                           competitors: List[str],
                           criteria: List[str] = None) -> Dict[str, Any]:
        """
        对比多个竞品
        
        Args:
            competitors: 竞品名称列表
            criteria: 对比维度
        
        Returns:
            对比矩阵
        """
        if not criteria:
            criteria = ["价格", "功能", "用户体验", "品牌知名度", "售后服务"]
        
        comparison = {
            "criteria": criteria,
            "competitors": {}
        }
        
        for name in competitors:
            comp = self.competitors.get(name)
            if comp:
                # 模拟评分（实际应该基于真实数据）
                scores = {}
                for criterion in criteria:
                    import random
                    scores[criterion] = random.randint(60, 95)
                
                comparison["competitors"][name] = {
                    "scores": scores,
                    "avg_score": sum(scores.values()) / len(scores)
                }
        
        return comparison
    
    # ========== 内容策略 ==========
    
    def create_content_plan(self,
                           topic: str,
                           content_type: str = "article",
                           platform: str = "wechat",
                           keywords: Optional[List[str]] = None,
                           days_from_now: int = 1) -> ContentPlan:
        """
        创建内容计划
        
        Args:
            topic: 主题
            content_type: 内容类型
            platform: 发布平台
            keywords: 关键词
            days_from_now: 几天后发布
        
        Returns:
            ContentPlan 对象
        """
        plan_id = f"plan_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        plan = ContentPlan(
            plan_id=plan_id,
            topic=topic,
            content_type=content_type,
            platform=platform,
            scheduled_date=datetime.now() + timedelta(days=days_from_now),
            keywords=keywords or []
        )
        
        self.content_plans[plan_id] = plan
        return plan
    
    def get_content_calendar(self, 
                            days: int = 7) -> List[Dict[str, Any]]:
        """
        获取内容日历
        
        Args:
            days: 未来几天
        
        Returns:
            内容计划列表
        """
        end_date = datetime.now() + timedelta(days=days)
        
        calendar = []
        for plan in self.content_plans.values():
            if plan.scheduled_date <= end_date:
                calendar.append({
                    "plan_id": plan.plan_id,
                    "topic": plan.topic,
                    "type": plan.content_type,
                    "platform": plan.platform,
                    "scheduled_date": plan.scheduled_date.isoformat(),
                    "status": plan.status
                })
        
        # 按日期排序
        calendar.sort(key=lambda x: x["scheduled_date"])
        return calendar
    
    def suggest_topics(self, 
                      brand_id: str,
                      count: int = 5) -> List[Dict[str, str]]:
        """
        建议内容话题
        
        Args:
            brand_id: 品牌ID
            count: 数量
        
        Returns:
            话题建议列表
        """
        brand = self.brands.get(brand_id)
        if not brand:
            return []
        
        # 基于品牌关键词生成话题
        topic_templates = [
            f"{brand.keywords[0] if brand.keywords else '产品'}如何帮助{brand.target_audience}解决问题",
            f"为什么{brand.keywords[0] if brand.keywords else '我们'}是{brand.target_audience}的最佳选择",
            f"{brand.target_audience}必看：{brand.keywords[1] if len(brand.keywords) > 1 else '行业'}最新趋势",
            f"如何用{brand.keywords[0] if brand.keywords else '工具'}提升效率",
            f"案例分享：{brand.target_audience}的成功故事"
        ]
        
        topics = []
        for i, template in enumerate(topic_templates[:count]):
            topics.append({
                "topic": template,
                "type": "article" if i % 2 == 0 else "post",
                "reason": "基于品牌定位和目标受众生成"
            })
        
        return topics
    
    # ========== 统计 ==========
    
    def get_stats(self) -> Dict[str, Any]:
        """获取战略统计"""
        return {
            "brands": len(self.brands),
            "competitors": len(self.competitors),
            "content_plans": len(self.content_plans),
            "analysis_count": len(self.analysis_history)
        }


# ========== 全局实例 ==========

_brand_instance = None

def get_brand() -> Palace4Brand:
    """获取全局品牌战略实例"""
    global _brand_instance
    if _brand_instance is None:
        _brand_instance = Palace4Brand()
    return _brand_instance


# ========== 快捷函数 ==========

def define_positioning(name: str, target: str, differentiation: str, **kwargs) -> Brand:
    """快捷函数：定义品牌定位"""
    return get_brand().define_positioning(name, target, differentiation, **kwargs)

def analyze_competitor(name: str, **kwargs) -> Dict[str, Any]:
    """快捷函数：分析竞品"""
    return get_brand().analyze_competitor(name, **kwargs)

def create_content_plan(topic: str, **kwargs) -> ContentPlan:
    """快捷函数：创建内容计划"""
    return get_brand().create_content_plan(topic, **kwargs)


# ========== 测试 ==========

if __name__ == "__main__":
    print("=== 4 宫品牌战略测试 ===\n")
    
    brand = Palace4Brand()
    
    # 测试1: 品牌定位
    print("1. 品牌定位:")
    result = brand.define_positioning(
        name="太极系统",
        target="创业者和团队负责人",
        differentiation="1+8智能体协作",
        tone="professional"
    )
    print(f"   品牌名: {result.name}")
    print(f"   定位: {result.positioning}")
    print(f"   Slogan: {result.slogan}")
    
    # 测试2: 竞品分析
    print("\n2. 竞品分析:")
    analysis = brand.analyze_competitor(
        name="竞品A",
        strengths=["功能全面", "价格低"],
        weaknesses=["学习曲线陡", "售后差"],
        pricing="¥99/月"
    )
    print(f"   竞品: {analysis['competitor']}")
    print(f"   摘要: {analysis['summary']}")
    print(f"   建议: {analysis['recommendation']}")
    
    # 测试3: 内容计划
    print("\n3. 内容计划:")
    plan = brand.create_content_plan(
        topic="如何用AI提升团队效率",
        content_type="article",
        platform="wechat",
        keywords=["AI", "效率", "团队"]
    )
    print(f"   主题: {plan.topic}")
    print(f"   平台: {plan.platform}")
    print(f"   发布日期: {plan.scheduled_date.strftime('%Y-%m-%d')}")
    
    # 测试4: 话题建议
    print("\n4. 话题建议:")
    topics = brand.suggest_topics("brand_太极系统")
    for i, topic in enumerate(topics[:3], 1):
        print(f"   {i}. {topic['topic']}")
    
    # 测试5: 统计
    print("\n5. 战略统计:")
    stats = brand.get_stats()
    print(f"   品牌数: {stats['brands']}")
    print(f"   竞品数: {stats['competitors']}")
    print(f"   内容计划: {stats['content_plans']}")
    
    print("\n=== 4 宫就绪 ===")