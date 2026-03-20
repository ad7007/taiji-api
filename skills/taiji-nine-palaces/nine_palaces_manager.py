#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
九宫格调度器
Nine Palaces Manager - Orchestrates all 9 palaces
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import sys

sys.path.insert(0, '/root/.openclaw/workspace/skills/taiji-nine-palaces')

from taiji_client import TaijiClient, display_palaces, display_balance
from palace_base import PalaceBase


class NinePalacesManager:
    """
    九宫格调度器
    
    职责:
    - 管理所有 9 个宫位
    - 协调跨宫位任务
    - 监控阴阳平衡
    - 调度资源分配
    """
    
    def __init__(self):
        self.client = TaijiClient()
        self.palaces: Dict[int, PalaceBase] = {}
        self._load_palaces()
    
    def _load_palaces(self):
        """加载所有宫位"""
        # 延迟导入避免循环依赖
        from palace_1_data_collection import Palace1DataCollection
        from palace_2_product import Palace2Product
        from palace_3_tech import Palace3Tech
        from palace_4_brand import Palace4Brand
        from palace_7_legal import Palace7Legal
        from palace_8_marketing import Palace8Marketing
        from palace_9_ecology import Palace9Ecology
        
        # 已实现的宫位
        self.palaces = {
            1: Palace1DataCollection(),
            2: Palace2Product(),
            3: Palace3Tech(),  # ✅ 技术团队（智能模型路由）
            4: Palace4Brand(),
            5: self._create_palace_5(),  # 中宫（调度器自身）
            7: Palace7Legal(),
            8: Palace8Marketing(),
            9: Palace9Ecology(),
        }
        
        # 待实现的宫位
        self._pending_palaces = {
            6: "6-物联监控 (tencentcloud-lighthouse)",
        }
    
    def _create_palace_5(self) -> PalaceBase:
        """创建中宫（调度器自身）"""
        class Palace5Master(PalaceBase):
            def __init__(self):
                super().__init__(5, "5-中央控制", "土")
                self.skills = ["taiji-nine-palaces"]
                self.capabilities = {
                    "orchestrate": "调度协调",
                    "balance_monitor": "平衡监控",
                    "resource_alloc": "资源分配",
                }
            
            def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
                return {"success": True, "message": "中宫调度完成"}
        
        return Palace5Master()
    
    def initialize_all(self) -> Dict[str, Any]:
        """初始化所有宫位"""
        results = {}
        
        for palace_id, palace in self.palaces.items():
            try:
                palace.initialize()
                results[palace_id] = {"status": "initialized", "name": palace.palace_name}
            except Exception as e:
                results[palace_id] = {"status": "failed", "error": str(e)}
        
        return {
            "success": True,
            "initialized": len([r for r in results.values() if r["status"] == "initialized"]),
            "failed": len([r for r in results.values() if r["status"] == "failed"]),
            "details": results,
        }
    
    def get_status(self) -> Dict[str, Any]:
        """获取九宫格整体状态"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "palaces": {},
            "balance": None,
            "pending": self._pending_palaces,
        }
        
        # 获取各宫位状态
        for palace_id, palace in self.palaces.items():
            status["palaces"][palace_id] = palace.get_status()
        
        # 获取阴阳平衡
        try:
            balance = self.client.get_balance_status()
            status["balance"] = balance
        except Exception as e:
            status["balance"] = {"error": str(e)}
        
        return status
    
    def execute(self, palace_id: int, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行宫位动作"""
        if palace_id not in self.palaces:
            return {"success": False, "error": f"宫位 {palace_id} 不存在或未实现"}
        
        palace = self.palaces[palace_id]
        return palace.execute(action, params)
    
    def check_balance(self) -> Dict[str, Any]:
        """检查阴阳平衡"""
        try:
            balance_data = self.client.get_balance_status()
            imbalanced = self.client.get_balance_status()  # 获取失衡对
            
            result = {
                "status": "balanced",
                "balance": balance_data,
                "imbalanced_pairs": [],
                "recommendations": [],
            }
            
            # 检查失衡
            if "balance" in balance_data:
                for pair, value in balance_data["balance"].items():
                    if value < 0.7:
                        result["status"] = "imbalanced"
                        result["imbalanced_pairs"].append({
                            "pair": pair,
                            "value": value,
                        })
                        result["recommendations"].append(f"调整 {pair} 宫位负载")
            
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def display_status(self):
        """显示九宫格状态（可视化）"""
        print("\n" + "="*60)
        print("           九宫格系统状态")
        print("="*60)
        
        # 获取所有宫位
        palaces_data = self.client.get_all_palaces()
        if palaces_data:
            print(display_palaces(palaces_data))
        
        # 获取平衡状态
        balance_data = self.client.get_balance_status()
        if balance_data:
            print("\n" + display_balance({"balance": balance_data}))
        
        # 显示待实现宫位
        if self._pending_palaces:
            print("\n【待实现宫位】")
            for palace_id, desc in self._pending_palaces.items():
                print(f"  ⏳ {palace_id}: {desc}")
        
        print("="*60)


def demo():
    """演示"""
    print("=== 九宫格调度器演示 ===\n")
    
    manager = NinePalacesManager()
    
    # 初始化所有宫位
    print("【1. 初始化宫位】")
    result = manager.initialize_all()
    print(f"初始化完成：{result['initialized']}/{len(manager.palaces)} 宫位\n")
    
    # 显示状态
    print("【2. 九宫格状态】")
    manager.display_status()
    
    # 检查平衡
    print("\n【3. 阴阳平衡检查】")
    balance = manager.check_balance()
    print(f"状态：{balance.get('status', 'unknown')}")
    if balance.get("imbalanced_pairs"):
        print(f"失衡对：{balance['imbalanced_pairs']}")
    
    # 测试执行
    print("\n【4. 执行测试】")
    
    # 2-产品质量
    result = manager.execute(2, "quality_checklist", {"product_type": "content"})
    print(f"2-产品质量：{result.get('message', '')}")
    
    # 4-品牌战略
    result = manager.execute(4, "content_strategy", {
        "target_audience": "中小企业管理者",
        "goals": ["品牌曝光"],
    })
    print(f"4-品牌战略：{result.get('data', {}).get('recommendations', [])}")
    
    # 8-营销客服
    result = manager.execute(8, "setup_payment_wall", {
        "content_id": "report_v1",
        "required_plan": "pro",
    })
    print(f"8-营销客服：付费墙配置 {result.get('data', {}).get('status', '')}")
    
    # 9-行业生态
    result = manager.execute(9, "keyword_research", {
        "topic": "九宫格管理",
        "target_audience": "企业管理者",
    })
    print(f"9-行业生态：关键词 {len(result.get('data', {}).get('keywords', []))} 个")


if __name__ == "__main__":
    demo()
