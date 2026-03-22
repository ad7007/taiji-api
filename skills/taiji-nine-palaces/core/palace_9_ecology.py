#!/usr/bin/env python3
"""
9 宫 - 行业生态核心

职责：
1. 行业洞察（趋势分析）
2. 生态合作（伙伴管理）
3. 资源整合（平台对接）
4. 商机发现（市场机会）
"""

from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Partner:
    """合作伙伴"""
    partner_id: str
    name: str
    type: str  # vendor/customer/platform/integrator
    status: str  # active/inactive/pending
    contact: str = ""
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Opportunity:
    """商机"""
    opp_id: str
    title: str
    source: str
    value: float
    status: str  # new/qualified/proposal/closed
    created_at: datetime = field(default_factory=datetime.now)


class Palace9Ecology:
    """9 宫 - 行业生态"""
    
    def __init__(self):
        self.palace_id = 9
        self.palace_name = "行业生态"
        
        self.partners: Dict[str, Partner] = {}
        self.opportunities: Dict[str, Opportunity] = {}
    
    def add_partner(self, name: str, type: str, contact: str = "") -> Partner:
        """添加合作伙伴"""
        partner_id = f"partner_{name.lower().replace(' ', '_')}"
        partner = Partner(
            partner_id=partner_id,
            name=name,
            type=type,
            status="active",
            contact=contact
        )
        self.partners[partner_id] = partner
        return partner
    
    def add_opportunity(self, title: str, source: str, value: float) -> Opportunity:
        """添加商机"""
        opp_id = f"opp_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        opp = Opportunity(
            opp_id=opp_id,
            title=title,
            source=source,
            value=value,
            status="new"
        )
        self.opportunities[opp_id] = opp
        return opp
    
    def list_partners(self, type: Optional[str] = None) -> List[Partner]:
        """列出合作伙伴"""
        partners = list(self.partners.values())
        if type:
            partners = [p for p in partners if p.type == type]
        return partners
    
    def list_opportunities(self, status: Optional[str] = None) -> List[Opportunity]:
        """列出商机"""
        opps = list(self.opportunities.values())
        if status:
            opps = [o for o in opps if o.status == status]
        return opps
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "partners": len(self.partners),
            "opportunities": len(self.opportunities),
            "pipeline_value": sum(o.value for o in self.opportunities.values())
        }


# 全局实例
_instance = None

def get_ecology() -> Palace9Ecology:
    global _instance
    if _instance is None:
        _instance = Palace9Ecology()
    return _instance


if __name__ == "__main__":
    e = Palace9Ecology()
    e.add_partner("ClawHub", "platform", "contact@clawhub.com")
    e.add_opportunity("企业版销售", "官网咨询", 999)
    print(f"统计数据: {e.get_stats()}")