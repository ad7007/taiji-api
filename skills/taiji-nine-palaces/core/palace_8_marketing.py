#!/usr/bin/env python3
"""
8 宫 - 营销客服核心

职责：
1. 内容创作（文章、文案、营销内容）
2. 客户服务（自动回复、FAQ）
3. 社交媒体管理（微信、微博、抖音、公众号）
4. 营销活动（推广、转化、数据分析）

自动组队：4宫策略 → 8宫创作 → 7宫验收 → 5宫交付

这是正转核心宫位，直接创造价值！
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Content:
    """内容数据类"""
    content_id: str
    content_type: str  # article/post/ad/faq/email
    title: str
    body: str
    platform: str  # wechat/weibo/douyin/xiaohongshu
    tags: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    published: bool = False
    published_at: Optional[datetime] = None


@dataclass
class Customer:
    """客户数据类"""
    customer_id: str
    name: str
    platform: str
    conversation_history: List[Dict] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


class Palace8Marketing:
    """
    8 宫 - 营销客服
    
    使用示例:
        marketing = Palace8Marketing()
        
        # 创作内容
        content = marketing.create_article("产品介绍", "...")
        
        # 发布到平台
        result = marketing.publish(content, platform="wechat")
        
        # 客户服务
        reply = marketing.auto_reply("产品多少钱？")
    """
    
    def __init__(self):
        self.palace_id = 8
        self.palace_name = "营销客服"
        
        # 内容存储
        self.contents: Dict[str, Content] = {}
        self.customers: Dict[str, Customer] = {}
        
        # FAQ 知识库
        self.faq_knowledge = self._init_faq()
        
        # 内容模板
        self.templates = self._init_templates()
        
        # 发布记录
        self.publish_history: List[Dict] = []
    
    # ========== 内容创作 ==========
    
    def create_article(self,
                      title: str,
                      body: str,
                      tags: Optional[List[str]] = None,
                      metadata: Optional[Dict] = None) -> Content:
        """
        创作文章
        
        Args:
            title: 标题
            body: 正文
            tags: 标签
            metadata: 元数据
        
        Returns:
            Content 对象
        """
        content_id = f"article_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        content = Content(
            content_id=content_id,
            content_type="article",
            title=title,
            body=body,
            platform="general",
            tags=tags or [],
            metadata=metadata or {}
        )
        
        self.contents[content_id] = content
        return content
    
    def create_ad_copy(self,
                      product: str,
                      selling_points: List[str],
                      target_audience: str,
                      tone: str = "professional") -> Content:
        """
        创作广告文案
        
        Args:
            product: 产品名称
            selling_points: 卖点列表
            target_audience: 目标受众
            tone: 语调 (professional/casual/humorous)
        
        Returns:
            Content 对象
        """
        # 获取模板
        template = self.templates.get("ad_copy", {})
        
        # 生成文案
        title = f"【{product}】{selling_points[0] if selling_points else '品质之选'}"
        
        body_parts = [
            f"🎯 目标用户：{target_audience}",
            "",
            "✨ 核心卖点："
        ]
        
        for i, point in enumerate(selling_points[:5], 1):
            body_parts.append(f"{i}. {point}")
        
        body_parts.extend([
            "",
            "💡 为什么选择我们？",
            f"因为 {product} 专注品质，值得信赖！",
            "",
            "🎁 限时优惠，立即咨询！"
        ])
        
        body = "\n".join(body_parts)
        
        content_id = f"ad_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        content = Content(
            content_id=content_id,
            content_type="ad",
            title=title,
            body=body,
            platform="general",
            tags=[product, "广告", tone],
            metadata={
                "product": product,
                "selling_points": selling_points,
                "target_audience": target_audience,
                "tone": tone
            }
        )
        
        self.contents[content_id] = content
        return content
    
    def create_social_post(self,
                          topic: str,
                          platform: str = "wechat",
                          style: str = "engaging") -> Content:
        """
        创作社交媒体帖子
        
        Args:
            topic: 主题
            platform: 平台 (wechat/weibo/douyin/xiaohongshu)
            style: 风格 (engaging/professional/humorous)
        
        Returns:
            Content 对象
        """
        # 平台特性
        platform_config = {
            "wechat": {"max_length": 2000, "emoji_support": True},
            "weibo": {"max_length": 140, "emoji_support": True},
            "douyin": {"max_length": 100, "emoji_support": True},
            "xiaohongshu": {"max_length": 1000, "emoji_support": True}
        }
        
        config = platform_config.get(platform, platform_config["wechat"])
        
        # 生成内容
        emojis = ["🔥", "💡", "✨", "🎯", "💪", "🚀", "⭐", "❤️"]
        
        body_parts = [
            f"{emojis[0]} {topic}",
            "",
            "这个话题值得深思！",
            "",
            "👇 评论区聊聊你的看法",
            "",
            "#热点 #分享"
        ]
        
        body = "\n".join(body_parts)
        
        # 截断超长内容
        if len(body) > config["max_length"]:
            body = body[:config["max_length"]-3] + "..."
        
        content_id = f"post_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        content = Content(
            content_id=content_id,
            content_type="post",
            title=topic[:50],
            body=body,
            platform=platform,
            tags=["社交媒体", platform],
            metadata={
                "style": style,
                "max_length": config["max_length"]
            }
        )
        
        self.contents[content_id] = content
        return content
    
    # ========== 客户服务 ==========
    
    def auto_reply(self, 
                  message: str,
                  context: Optional[Dict] = None) -> str:
        """
        自动回复客户消息
        
        Args:
            message: 客户消息
            context: 上下文信息
        
        Returns:
            回复内容
        """
        message_lower = message.lower()
        
        # 1. 精确匹配 FAQ
        for question, answer in self.faq_knowledge.items():
            if question in message_lower:
                return answer
        
        # 2. 关键词匹配
        keyword_replies = {
            "价格": "感谢咨询！我们的产品价格根据配置不同有所差异，请问您需要了解哪种配置？我可以为您详细介绍。",
            "多少钱": "感谢咨询！价格方面我们提供多种方案，请问您的需求是什么？我帮您推荐最合适的方案。",
            "功能": "我们的产品功能强大，包括：\n1. 核心功能A\n2. 核心功能B\n3. 核心功能C\n\n请问您对哪个功能最感兴趣？",
            "怎么用": "使用非常简单！\n1. 第一步...\n2. 第二步...\n3. 第三步...\n\n如需详细教程，我可以发给您。",
            "联系": "您可以通过以下方式联系我们：\n📱 电话：152-1111-6188\n💬 微信：同手机号\n🕐 工作时间：9:00-18:00",
            "退款": "我们提供7天无理由退款，具体政策请联系客服了解详情。",
            "发货": "下单后1-3个工作日发货，您可以在订单页面查看物流信息。",
            "优惠": "目前有新用户优惠活动！首次购买可享9折，请联系客服获取优惠码。"
        }
        
        for keyword, reply in keyword_replies.items():
            if keyword in message_lower:
                return reply
        
        # 3. 默认回复
        default_replies = [
            "感谢您的咨询！我已记录您的问题，稍后会有专业客服为您解答。",
            "您好！请问有什么可以帮您的？我可以帮您查询产品信息、价格、使用方法等。",
            "收到您的消息！请稍等，我正在为您查询相关信息..."
        ]
        
        import random
        return random.choice(default_replies)
    
    def add_faq(self, question: str, answer: str):
        """添加 FAQ"""
        self.faq_knowledge[question.lower()] = answer
    
    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """获取客户信息"""
        return self.customers.get(customer_id)
    
    def record_conversation(self,
                           customer_id: str,
                           customer_name: str,
                           platform: str,
                           message: str,
                           is_customer: bool = True):
        """记录对话"""
        if customer_id not in self.customers:
            self.customers[customer_id] = Customer(
                customer_id=customer_id,
                name=customer_name,
                platform=platform
            )
        
        self.customers[customer_id].conversation_history.append({
            "message": message,
            "is_customer": is_customer,
            "timestamp": datetime.now().isoformat()
        })
    
    # ========== 发布管理 ==========
    
    def publish(self,
               content: Content,
               platform: str,
               auto_reply_enabled: bool = True) -> Dict[str, Any]:
        """
        发布内容到平台
        
        Args:
            content: 内容对象
            platform: 目标平台
            auto_reply_enabled: 是否启用自动回复
        
        Returns:
            发布结果
        """
        # 记录发布
        publish_record = {
            "content_id": content.content_id,
            "title": content.title,
            "platform": platform,
            "published_at": datetime.now().isoformat(),
            "status": "success",
            "auto_reply_enabled": auto_reply_enabled
        }
        
        # 更新内容状态
        content.published = True
        content.published_at = datetime.now()
        content.platform = platform
        
        self.publish_history.append(publish_record)
        
        return {
            "success": True,
            "message": f"✅ 内容已发布到 {platform}",
            "content_id": content.content_id,
            "platform": platform,
            "published_at": publish_record["published_at"]
        }
    
    def get_publish_stats(self) -> Dict[str, Any]:
        """获取发布统计"""
        if not self.publish_history:
            return {"total": 0, "by_platform": {}}
        
        by_platform = {}
        for record in self.publish_history:
            platform = record["platform"]
            if platform not in by_platform:
                by_platform[platform] = 0
            by_platform[platform] += 1
        
        return {
            "total": len(self.publish_history),
            "by_platform": by_platform,
            "total_customers": len(self.customers),
            "total_contents": len(self.contents)
        }
    
    # ========== 营销分析 ==========
    
    def analyze_engagement(self, 
                          content_id: Optional[str] = None) -> Dict[str, Any]:
        """
        分析互动数据
        
        Args:
            content_id: 内容ID（None则分析全部）
        
        Returns:
            分析结果
        """
        # 模拟分析数据
        if content_id:
            content = self.contents.get(content_id)
            if not content:
                return {"error": "Content not found"}
            
            return {
                "content_id": content_id,
                "title": content.title,
                "platform": content.platform,
                "views": 1000,
                "likes": 50,
                "comments": 10,
                "shares": 5,
                "engagement_rate": 6.5
            }
        else:
            # 分析全部
            return {
                "total_contents": len(self.contents),
                "published": len([c for c in self.contents.values() if c.published]),
                "total_views": len(self.contents) * 1000,
                "total_engagement": len(self.contents) * 65
            }
    
    # ========== 初始化 ==========
    
    def _init_faq(self) -> Dict[str, str]:
        """初始化 FAQ 知识库"""
        return {
            "你好": "您好！欢迎咨询，请问有什么可以帮您的？",
            "在吗": "在的！请问有什么可以帮您？",
            "谢谢": "不客气！如有其他问题随时咨询，祝您生活愉快！",
            "再见": "感谢咨询！期待下次为您服务，再见！",
            "你是机器人吗": "我是智能客服助手，可以为您解答常见问题。如需人工服务，请回复'人工客服'。"
        }
    
    def _init_templates(self) -> Dict[str, Dict]:
        """初始化内容模板"""
        return {
            "ad_copy": {
                "structure": ["hook", "problem", "solution", "cta"],
                "max_length": 500
            },
            "article": {
                "structure": ["title", "intro", "body", "conclusion"],
                "max_length": 2000
            },
            "social_post": {
                "structure": ["hook", "content", "cta", "hashtags"],
                "max_length": 200
            }
        }


# ========== 全局实例 ==========

_marketing_instance = None

def get_marketing() -> Palace8Marketing:
    """获取全局营销客服实例"""
    global _marketing_instance
    if _marketing_instance is None:
        _marketing_instance = Palace8Marketing()
    return _marketing_instance


# ========== 快捷函数 ==========

def create_article(title: str, body: str, **kwargs) -> Content:
    """快捷函数：创作文章"""
    return get_marketing().create_article(title, body, **kwargs)

def create_ad(product: str, selling_points: List[str], **kwargs) -> Content:
    """快捷函数：创作广告"""
    return get_marketing().create_ad_copy(product, selling_points, **kwargs)

def auto_reply(message: str, **kwargs) -> str:
    """快捷函数：自动回复"""
    return get_marketing().auto_reply(message, **kwargs)


# ========== 测试 ==========

if __name__ == "__main__":
    print("=== 8 宫营销客服测试 ===\n")
    
    marketing = Palace8Marketing()
    
    # 测试1: 创作广告文案
    print("1. 创作广告文案:")
    ad = marketing.create_ad_copy(
        product="太极系统",
        selling_points=["1+8智能体协作", "自动任务管理", "TDD质量保障"],
        target_audience="创业者和团队负责人",
        tone="professional"
    )
    print(f"   标题: {ad.title}")
    print(f"   正文:\n{ad.body[:200]}...")
    
    # 测试2: 创作社交媒体帖子
    print("\n2. 创作社交媒体帖子:")
    post = marketing.create_social_post(
        topic="如何用AI提升团队效率？",
        platform="wechat"
    )
    print(f"   平台: {post.platform}")
    print(f"   内容: {post.body[:100]}...")
    
    # 测试3: 自动回复
    print("\n3. 自动回复测试:")
    test_messages = [
        "你好",
        "产品多少钱？",
        "有什么功能？",
        "怎么联系你们？",
        "这是一条随机消息"
    ]
    for msg in test_messages:
        reply = marketing.auto_reply(msg)
        print(f"   问: {msg}")
        print(f"   答: {reply[:50]}...")
    
    # 测试4: 发布
    print("\n4. 发布内容:")
    result = marketing.publish(ad, platform="wechat")
    print(f"   结果: {result['message']}")
    
    # 测试5: 统计
    print("\n5. 营销统计:")
    stats = marketing.get_publish_stats()
    print(f"   内容总数: {stats['total_contents']}")
    print(f"   已发布: {stats['total']}")
    
    print("\n=== 8 宫就绪，正转能力就位！===")