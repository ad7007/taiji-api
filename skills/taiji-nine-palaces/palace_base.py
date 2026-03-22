#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
九宫格宫位基类
Palace Base Class - All palaces inherit from this
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
import sys

sys.path.insert(0, '/root/.openclaw/workspace/skills/taiji-nine-palaces')

from taiji_client import TaijiClient


class PalaceBase(ABC):
    """宫位基类"""
    
    def __init__(self, palace_id: int, palace_name: str, element: str):
        """
        初始化宫位
        
        Args:
            palace_id: 宫位 ID (1-9)
            palace_name: 宫位名称
            element: 五行属性
        """
        self.palace_id = palace_id
        self.palace_name = palace_name
        self.element = element
        self.client = TaijiClient()
        self.skills: List[str] = []
        self.capabilities: Dict[str, Any] = {}
        
    @abstractmethod
    def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行宫位核心动作
        
        Args:
            action: 动作名称
            params: 动作参数
            
        Returns:
            执行结果
        """
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """获取宫位状态"""
        palace_data = self.client.get_palace(self.palace_id)
        return {
            "palace_id": self.palace_id,
            "palace_name": self.palace_name,
            "element": self.element,
            "load": palace_data.get("load", 0) if palace_data else 0,
            "skills": self.skills,
            "capabilities": list(self.capabilities.keys()),
        }
    
    def update_load(self, load: float) -> Dict[str, Any]:
        """更新宫位负载"""
        if not 0 <= load <= 1:
            return {"success": False, "error": "负载值必须在 0-1 之间"}
        
        result = self.client.update_palace_load(self.palace_id, load)
        if result.get("success"):
            self._log(f"负载更新为 {load*100:.0f}%")
        return result
    
    def _log(self, message: str):
        """日志记录"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{self.palace_name}] {message}")
    
    def _check_balance(self) -> Optional[Dict[str, Any]]:
        """检查阴阳平衡"""
        balance = self.client.get_balance_status()
        return balance
    
    def initialize(self) -> bool:
        """初始化宫位（子类可重写）"""
        self._log("初始化宫位...")
        return True
    
    def shutdown(self) -> bool:
        """关闭宫位（子类可重写）"""
        self._log("关闭宫位...")
        return True
