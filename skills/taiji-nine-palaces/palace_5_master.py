#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
5-中央控制宫 - 调度协调、资源分配、平衡监控
Palace 5 - Central Control & Orchestration

职责：
- 九宫格调度器
- 资源分配
- 阴阳平衡监控
- 任务交付
"""

from typing import Dict, Any, List
from datetime import datetime
import sys

sys.path.insert(0, '/root/.openclaw/workspace/skills/taiji-nine-palaces')

from palace_base import PalaceBase


class Palace5Master(PalaceBase):
    """
    5-中央控制宫（中宫）
    
    职责:
    - 九宫格调度协调
    - 资源分配优化
    - 阴阳平衡监控
    - 最终交付
    
    技能:
    - taiji-nine-palaces: 九宫格调度
    - n8n-workflow: 并发工作流（备用）
    - research-assistant: 多方案优选（备用）
    """
    
    def __init__(self):
        super().__init__(
            palace_id=5,
            palace_name="5-中央控制",
            element="土"
        )
        self.skills = ["taiji-nine-palaces", "n8n-workflow", "research-assistant"]
        self.capabilities = {
            "orchestrate": "九宫格调度",
            "allocate_resources": "资源分配",
            "monitor_balance": "平衡监控",
            "deliver": "任务交付",
            "compare_plans": "多方案对比",
        }
    
    def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行宫位动作"""
        self._log(f"执行动作：{action}")
        
        action_map = {
            "orchestrate": self.orchestrate,
            "allocate_resources": self.allocate_resources,
            "monitor_balance": self.monitor_balance,
            "deliver": self.deliver,
            "compare_plans": self.compare_plans,
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
    
    def orchestrate(self, task: str, palaces: List[int] = None) -> Dict[str, Any]:
        """九宫格调度"""
        self._log(f"调度任务：{task}")
        
        # 从九宫格调度器导入
        from nine_palaces_manager import NinePalacesManager
        
        manager = NinePalacesManager()
        result = manager.execute(task, palaces)
        
        return {
            "success": True,
            "message": f"任务已调度：{task}",
            "result": result,
        }
    
    def allocate_resources(self, resources: Dict[str, Any]) -> Dict[str, Any]:
        """资源分配"""
        self._log(f"分配资源：{resources}")
        
        # 资源分配逻辑
        allocation = {
            "cpu": resources.get("cpu", 100),
            "memory": resources.get("memory", 100),
            "concurrency": resources.get("concurrency", 5),
        }
        
        return {
            "success": True,
            "message": "资源已分配",
            "allocation": allocation,
        }
    
    def monitor_balance(self) -> Dict[str, Any]:
        """阴阳平衡监控"""
        self._log("监控阴阳平衡")
        
        from taiji_client import TaijiClient
        
        client = TaijiClient()
        balance = client.get_balance_status()
        
        return {
            "success": True,
            "balance": balance,
            "status": "balanced" if all(v >= 0.7 for v in balance.values()) else "imbalanced",
        }
    
    def deliver(self, content: str, title: str, format: str = "pdf") -> Dict[str, Any]:
        """任务交付"""
        self._log(f"交付：{title}")
        
        from browser_automation import KimiPDFGenerator
        
        generator = KimiPDFGenerator()
        result = generator.generate_report(
            prompt=content[:5000],
            title=title,
            wait_seconds=45,
        )
        
        return {
            "success": result.get("success", False),
            "pdf_path": result.get("pdf_path", ""),
            "message": f"已交付：{title}",
        }
    
    def compare_plans(self, plans: List[Dict[str, Any]]) -> Dict[str, Any]:
        """多方案对比（使用 research-assistant）"""
        self._log(f"对比 {len(plans)} 个方案")
        
        # 使用 research-assistant 存储和对比
        from research_assistant import ResearchAssistant
        
        research = ResearchAssistant()
        
        # 添加方案
        for i, plan in enumerate(plans):
            research.add_note(
                topic="方案对比",
                content=str(plan),
                tags=[f"方案{i+1}", plan.get("name", "")]
            )
        
        # 导出对比报告
        comparison = research.export_to_markdown()
        
        return {
            "success": True,
            "comparison": comparison,
            "best_plan": plans[0] if plans else None,  # 简化处理
        }
    
    def initialize(self) -> bool:
        """初始化"""
        super().initialize()
        self._log(f"技能：{', '.join(self.skills)}")
        self._log(f"能力：{', '.join(self.capabilities.values())}")
        self._log(f"角色：中宫调度器")
        return True


if __name__ == "__main__":
    palace = Palace5Master()
    palace.initialize()
    
    print("\n=== 测试功能 ===")
    
    # 调度任务
    result = palace.execute("orchestrate", {
        "task": "云品牌报告",
        "palaces": [1, 3, 4, 7, 8, 9]
    })
    print(f"调度：{result}")
    
    # 状态
    status = palace.get_status()
    print(f"\n状态：{status}")
