#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
8-营销客服宫 - 客户管理、营销自动化、订阅收费、客服支持
Palace 8 - Marketing & Customer Service
"""

from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, '/root/.openclaw/workspace/skills/taiji-nine-palaces')

from palace_base import PalaceBase


class Palace8Marketing(PalaceBase):
    """
    8-营销客服宫
    
    职责:
    - 邮件营销
    - 订阅管理
    - 付费墙配置
    - 客服支持
    
    技能:
    - wechat-publisher: 微信发布
    - constant-contact: 邮件营销
    - chargebee: 订阅管理
    """
    
    def __init__(self):
        super().__init__(
            palace_id=8,
            palace_name="8-营销客服",
            element="木"
        )
        self.skills = ["wechat-publisher", "constant-contact", "chargebee"]
        self.capabilities = {
            "email_campaign": "邮件营销活动",
            "subscription管理": "订阅管理",
            "payment_wall": "付费墙配置",
            "customer_support": "客服支持",
        }
        self.customer_dir = Path("/root/.openclaw/workspace/customers")
        self.customer_dir.mkdir(parents=True, exist_ok=True)
        
        # 订阅计划
        self.subscription_plans = {
            "free": {"name": "免费版", "price": 0, "features": ["基础内容"]},
            "pro": {"name": "专业版", "price": 99, "features": ["全部内容", "模板下载"]},
            "enterprise": {"name": "企业版", "price": 2999, "features": ["全部内容", "1 小时咨询", "定制方案"]},
        }
    
    def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行宫位动作"""
        self._log(f"执行动作：{action}")
        
        action_map = {
            "email_campaign": self.email_campaign,
            "create_subscription": self.create_subscription,
            "setup_payment_wall": self.setup_payment_wall,
            "customer_support": self.customer_support,
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
    
    def email_campaign(self, campaign_name: str, recipients: List[str], content: str) -> Dict[str, Any]:
        """邮件营销活动"""
        self._log(f"邮件营销：{campaign_name}")
        
        # 调用 constant-contact
        campaign = {
            "name": campaign_name,
            "recipients_count": len(recipients),
            "content_preview": content[:100],
            "status": "pending",
            "message": "需要配置 constant-contact API",
        }
        
        return {"success": True, "data": campaign}
    
    def create_subscription(self, plan: str, customer_id: str) -> Dict[str, Any]:
        """创建订阅"""
        self._log(f"创建订阅：{plan}")
        
        if plan not in self.subscription_plans:
            return {"success": False, "error": f"未知订阅计划：{plan}"}
        
        plan_info = self.subscription_plans[plan]
        
        # 调用 chargebee
        subscription = {
            "customer_id": customer_id,
            "plan": plan_info["name"],
            "price": plan_info["price"],
            "features": plan_info["features"],
            "status": "pending",
            "message": "需要配置 chargebee API",
        }
        
        return {"success": True, "data": subscription}
    
    def setup_payment_wall(self, content_id: str, required_plan: str) -> Dict[str, Any]:
        """配置付费墙"""
        self._log(f"配置付费墙：{content_id}")
        
        if required_plan not in self.subscription_plans:
            return {"success": False, "error": f"未知订阅计划：{required_plan}"}
        
        payment_wall = {
            "content_id": content_id,
            "required_plan": self.subscription_plans[required_plan]["name"],
            "price": self.subscription_plans[required_plan]["price"],
            "status": "configured",
        }
        
        return {"success": True, "data": payment_wall}
    
    def customer_support(self, ticket_id: str, issue: str, priority: str = "normal") -> Dict[str, Any]:
        """客服支持"""
        self._log(f"客服工单：{ticket_id}")
        
        ticket = {
            "ticket_id": ticket_id,
            "issue": issue,
            "priority": priority,
            "status": "open",
            "created_at": datetime.now().isoformat(),
        }
        
        # 保存工单
        ticket_path = self.customer_dir / f"ticket_{ticket_id}.md"
        ticket_path.write_text(f"# 客服工单 {ticket_id}\n\n问题：{issue}\n\n优先级：{priority}\n", encoding="utf-8")
        
        return {"success": True, "data": ticket}
    
    def get_subscription_plans(self) -> Dict[str, Any]:
        """获取订阅计划"""
        return {
            "success": True,
            "plans": self.subscription_plans,
        }
    
    def initialize(self) -> bool:
        """初始化"""
        super().initialize()
        self._log(f"技能：{', '.join(self.skills)}")
        self._log(f"订阅计划：{len(self.subscription_plans)} 个")
        return True


if __name__ == "__main__":
    palace = Palace8Marketing()
    palace.initialize()
    
    print("\n=== 测试功能 ===")
    
    # 获取订阅计划
    result = palace.get_subscription_plans()
    print(f"订阅计划：{result}")
    
    # 配置付费墙
    result = palace.execute("setup_payment_wall", {
        "content_id": "report_v1",
        "required_plan": "pro",
    })
    print(f"付费墙：{result}")
    
    # 状态
    status = palace.get_status()
    print(f"\n状态：{status}")
