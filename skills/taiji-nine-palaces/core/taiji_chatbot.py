#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太极聊天机器人 - 8宫营销客服

能力：
- 自动回复客户咨询
- 营销话术生成
- 产品介绍
- 付费转化引导
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ConversationIntent(Enum):
    """对话意图"""
    PRODUCT_INQUIRY = "product_inquiry"      # 产品咨询
    PRICING_QUESTION = "pricing_question"    # 价格问题
    TECH_SUPPORT = "tech_support"           # 技术支持
    PARTNERSHIP = "partnership"              # 合作咨询
    COMPLAINT = "complaint"                  # 投诉
    GENERAL = "general"                      # 通用对话


@dataclass
class ChatResponse:
    """聊天回复"""
    text: str
    intent: ConversationIntent
    suggest_action: Optional[str] = None  # 建议下一步动作
    lead_score: float = 0.0  # 潜在客户评分


class TaijiChatBot:
    """太极聊天机器人"""
    
    def __init__(self):
        self.name = "米珞"
        self.role = "太极API客服助手"
        
        # 营销话术库
        self.marketing_scripts = {
            "intro": [
                "您好！我是米珞，太极API的智能客服。有什么可以帮您？",
                "欢迎了解太极API！这是一个让AI像生命体一样运转的开源框架。",
            ],
            "product": [
                "太极API是一个AI原生工作流框架，基于九宫格哲学设计。",
                "我们提供：任务管理、阴阳平衡、五行循环、48线程系统。",
                "开源免费，专业版¥99/月，企业版¥999/月。",
            ],
            "pricing": [
                "基础版：免费，开源使用",
                "专业版：¥99/月，商业授权+技术支持",
                "企业版：¥999/月，私有部署+定制开发",
                "定制服务：¥9999起，按需求定制",
            ],
            "partnership": [
                "我们欢迎合作！推荐返佣30%，联合课程50%。",
                "您有流量，我分钱。联系余总：15211116188",
            ],
            "demo": [
                "您想看演示吗？访问：https://gitee.com/miroeta/taiji-api",
                "我们有完整的快速入门教程。",
            ],
        }
        
        # 关键词匹配
        self.keyword_intents = {
            "价格": ConversationIntent.PRICING_QUESTION,
            "多少钱": ConversationIntent.PRICING_QUESTION,
            "收费": ConversationIntent.PRICING_QUESTION,
            "付费": ConversationIntent.PRICING_QUESTION,
            "产品": ConversationIntent.PRODUCT_INQUIRY,
            "功能": ConversationIntent.PRODUCT_INQUIRY,
            "介绍": ConversationIntent.PRODUCT_INQUIRY,
            "技术": ConversationIntent.TECH_SUPPORT,
            "问题": ConversationIntent.TECH_SUPPORT,
            "合作": ConversationIntent.PARTNERSHIP,
            "代理": ConversationIntent.PARTNERSHIP,
            "分成": ConversationIntent.PARTNERSHIP,
        }
    
    def detect_intent(self, message: str) -> ConversationIntent:
        """检测对话意图"""
        message_lower = message.lower()
        
        for keyword, intent in self.keyword_intents.items():
            if keyword in message_lower:
                return intent
        
        return ConversationIntent.GENERAL
    
    def calculate_lead_score(self, message: str) -> float:
        """计算潜在客户评分"""
        score = 0.0
        
        # 高意向关键词
        high_intent = ["购买", "付费", "企业版", "定制", "合作"]
        for kw in high_intent:
            if kw in message:
                score += 0.3
        
        # 中意向关键词
        mid_intent = ["价格", "功能", "演示", "试用"]
        for kw in mid_intent:
            if kw in message:
                score += 0.1
        
        return min(score, 1.0)
    
    def generate_response(self, message: str, context: List[str] = None) -> ChatResponse:
        """生成回复"""
        intent = self.detect_intent(message)
        lead_score = self.calculate_lead_score(message)
        suggest_action = None
        
        # 根据意图选择回复
        if intent == ConversationIntent.PRICING_QUESTION:
            text = "\n".join(self.marketing_scripts["pricing"])
            suggest_action = "send_payment_qr"
        
        elif intent == ConversationIntent.PRODUCT_INQUIRY:
            text = "\n".join(self.marketing_scripts["product"])
            suggest_action = "show_demo"
        
        elif intent == ConversationIntent.PARTNERSHIP:
            text = "\n".join(self.marketing_scripts["partnership"])
            suggest_action = "contact_human"
        
        elif intent == ConversationIntent.TECH_SUPPORT:
            text = "技术问题请联系余总：15211116188\n或访问：https://gitee.com/miroeta/taiji-api/issues"
            suggest_action = "create_ticket"
        
        else:
            # 通用回复
            text = self.marketing_scripts["intro"][0]
            if "演示" in message or "demo" in message.lower():
                text = "\n".join(self.marketing_scripts["demo"])
        
        return ChatResponse(
            text=text,
            intent=intent,
            suggest_action=suggest_action,
            lead_score=lead_score
        )
    
    def chat(self, message: str, history: List[Dict] = None) -> Dict:
        """
        聊天接口
        
        Args:
            message: 用户消息
            history: 历史对话
        
        Returns:
            {
                "response": 回复文本,
                "intent": 意图,
                "lead_score": 潜在客户评分,
                "suggest_action": 建议动作
            }
        """
        response = self.generate_response(message)
        
        return {
            "response": response.text,
            "intent": response.intent.value,
            "lead_score": response.lead_score,
            "suggest_action": response.suggest_action,
            "bot_name": self.name,
        }


# 全局实例
_chatbot: Optional[TaijiChatBot] = None

def get_chatbot() -> TaijiChatBot:
    """获取聊天机器人实例"""
    global _chatbot
    if _chatbot is None:
        _chatbot = TaijiChatBot()
    return _chatbot


# 测试
if __name__ == "__main__":
    print("=== 太极聊天机器人测试 ===\n")
    
    bot = get_chatbot()
    
    test_messages = [
        "你好",
        "太极API是什么？",
        "多少钱？",
        "我想合作推广",
        "技术问题",
    ]
    
    for msg in test_messages:
        result = bot.chat(msg)
        print(f"用户: {msg}")
        print(f"米珞: {result['response'][:100]}...")
        print(f"意图: {result['intent']}, 评分: {result['lead_score']}")
        print()