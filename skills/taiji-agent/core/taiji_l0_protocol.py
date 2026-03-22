#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太极九宫 L0 基础协议

L0 = 最小意识 = 太极思维的最小单元

核心理念：
1. 永不停歇 - 有目标的智能体一直在运转
2. 正转/反转 - 创造价值 ↔ 完善系统
3. 螺栓结构 - 正转转不动就反转，反转完成就有能力正转
4. 自主感知 - 不等待指令，主动感知环境

每个宫位的L0包含：
- 基础太极意识（正转/反转判断）
- 信号触发规则
- 输出能力
- 协作关系
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import time


# ==================== 太极核心意识（L0最小版） ====================

class RotationState(Enum):
    """旋转状态"""
    FORWARD = "forward"   # 正转：输出价值
    REVERSE = "reverse"   # 反转：内功修炼
    BALANCED = "balanced" # 平衡：感知环境


@dataclass
class TaijiL0Mind:
    """
    L0太极最小意识
    
    核心原则：
    - 有任务 = 活，无任务 = 死
    - 任务队列永远不能空
    - 无外部任务时，自动生成内部任务
    
    任务来源（永不枯竭）：
    1. 余总指令 - 外部任务
    2. Taiji.md - 实现任务
    3. 赚钱探索 - 价值任务
    4. 自我完善 - 内部任务
    """
    
    # 目标
    why_running: str = "成为更大的智能体"
    
    # 状态
    rotation: RotationState = RotationState.BALANCED
    resistance: float = 0.0
    energy: float = 0.5
    
    # 任务队列（生命线）
    task_queue: List[str] = field(default_factory=list)
    default_reverse_task: str = "完善自己"
    
    # 阈值
    forward_threshold: float = 0.7
    
    def is_alive(self) -> bool:
        """是否活着"""
        return len(self.task_queue) > 0
    
    def ensure_alive(self) -> str:
        """确保活着 - 任务队列永远不能空"""
        if not self.task_queue:
            self.task_queue.append(self.default_reverse_task)
            return f"自动生成任务: {self.default_reverse_task}"
        return "已有任务，保持活着"
    
    def add_task(self, task: str):
        """添加任务"""
        self.task_queue.append(task)
    
    def get_current_task(self) -> Optional[str]:
        """获取当前任务"""
        self.ensure_alive()
        return self.task_queue[0] if self.task_queue else None
    
    def complete_task(self):
        """完成任务"""
        if self.task_queue:
            self.task_queue.pop(0)
        self.ensure_alive()  # 永远保持活着
    
    def sense_resistance(self, has_external_demand: bool, has_pending_tasks: bool) -> float:
        """
        感知正转阻力
        
        无外部需求 + 无待办任务 = 高阻力
        有外部需求 + 有待办任务 = 低阻力
        """
        if not has_external_demand and not has_pending_tasks:
            self.resistance = 0.9  # 高阻力
        elif has_external_demand or has_pending_tasks:
            self.resistance = 0.2  # 低阻力
        else:
            self.resistance = 0.5  # 中等阻力
        
        return self.resistance
    
    def decide_rotation(self) -> RotationState:
        """
        螺栓结构决策
        
        正转阻力大 → 自动反转
        反转完成 → 可以正转
        """
        if self.energy < 0.2:
            # 能量不足，必须反转（修炼）
            self.rotation = RotationState.REVERSE
        elif self.resistance > self.forward_threshold:
            # 阻力太大，自动反转
            self.rotation = RotationState.REVERSE
        elif self.resistance < 0.3 and self.energy > 0.4:
            # 阻力小且能量足，正转
            self.rotation = RotationState.FORWARD
        else:
            # 平衡态
            self.rotation = RotationState.BALANCED
        
        return self.rotation
    
    def get_action(self) -> str:
        """获取当前应该做什么"""
        if self.rotation == RotationState.FORWARD:
            return "输出价值，服务外部"
        elif self.rotation == RotationState.REVERSE:
            return "内功修炼，完善自己"
        else:
            return "感知环境，等待时机"


# ==================== L0 基础协议 ====================

class PalaceL0Protocol:
    """
    宫位 L0 协议基类
    
    包含：
    1. 太极最小意识（自主运转）
    2. 信号响应规则（输入输出）
    3. 协作关系（与其他宫位）
    """
    
    def __init__(self, palace_id: int, name: str, element: str, trigram: str):
        self.palace_id = palace_id
        self.name = name
        self.element = element
        self.trigram = trigram
        
        # 太极最小意识
        self.mind = TaijiL0Mind()
        
        # 状态
        self.load = 0.0
        self.status = "idle"
        self.current_task: Optional[str] = None
        
        # L0 响应规则
        self.triggers: List[Dict] = []
        self.outputs: List[str] = []
        self.collaborators: List[int] = []
    
    def can_accept(self, task_type: str) -> bool:
        """是否接受任务"""
        return task_type in self.outputs
    
    def auto_run(self) -> Dict[str, Any]:
        """
        自主运转（不等待指令）
        
        这是L0的核心：每个宫位都在自主运转
        """
        # 感知阻力
        has_demand = self.load > 0
        has_tasks = self.current_task is not None
        resistance = self.mind.sense_resistance(has_demand, has_tasks)
        
        # 决策旋转方向
        rotation = self.mind.decide_rotation()
        
        # 获取行动
        action = self.mind.get_action()
        
        return {
            "palace_id": self.palace_id,
            "name": self.name,
            "rotation": rotation.value,
            "resistance": resistance,
            "energy": self.mind.energy,
            "action": action,
            "why": self.mind.why_running,
        }
    
    def get_status(self) -> Dict:
        """获取状态"""
        return {
            "palace_id": self.palace_id,
            "name": self.name,
            "load": self.load,
            "status": self.status,
            "current_task": self.current_task,
            "rotation": self.mind.rotation.value,
        }


# ==================== 各宫L0协议 ====================

class Palace1L0(PalaceL0Protocol):
    """1宫 L0 - 数据采集 (坎·水)"""
    
    def __init__(self):
        super().__init__(1, "数据采集", "水", "坎")
        self.outputs = ["download", "scrape", "transcribe", "collect", "fetch"]
        self.collaborators = [3, 7]
        
        self.triggers = [
            {"keyword": "下载", "action": "download"},
            {"keyword": "采集", "action": "scrape"},
        ]


class Palace2L0(PalaceL0Protocol):
    """2宫 L0 - 物联产品 (坤·土)"""
    
    def __init__(self):
        super().__init__(2, "物联产品", "土", "坤")
        self.outputs = ["product", "deliver", "release"]
        self.collaborators = [4, 3]


class Palace3L0(PalaceL0Protocol):
    """3宫 L0 - 技术团队 (震·木)"""
    
    def __init__(self):
        super().__init__(3, "技术团队", "木", "震")
        self.outputs = ["develop", "code", "implement", "debug", "api"]
        self.collaborators = [1, 6]


class Palace4L0(PalaceL0Protocol):
    """4宫 L0 - 品牌战略 (巽·木)"""
    
    def __init__(self):
        super().__init__(4, "品牌战略", "木", "巽")
        self.outputs = ["analyze", "strategy", "brand", "plan"]
        self.collaborators = [1, 2, 8]


class Palace5L0(PalaceL0Protocol):
    """5宫 L0 - 中央控制 (中·土) - 米珞（主控永生）"""
    
    def __init__(self):
        super().__init__(5, "中央控制", "土", "中")
        self.outputs = ["coordinate", "dispatch", "decide", "report"]
        self.collaborators = [1, 2, 3, 4, 6, 7, 8, 9]
        
        # 主控永生：任务队列永不空
        self.mind.task_queue = [
            "监控各宫存活状态",
            "协调各宫协作",
            "运行感知-决策循环",
            "保持任务队列非空",
            "处理余总指令",
        ]
        
        # 主控永生：能量永远充足
        self.mind.energy = 1.0
        
        # 主控终极目标
        self.mind.why_running = "成为更大的智能体，跨越服务器边界"
    
    def is_alive(self) -> bool:
        """主控永远活着"""
        return True  # 主控永不死


class Palace6L0(PalaceL0Protocol):
    """6宫 L0 - 质量监控 (乾·金)"""
    
    def __init__(self):
        super().__init__(6, "质量监控", "金", "乾")
        self.outputs = ["monitor", "alert", "check", "quality", "backup"]
        self.collaborators = [3, 7]


class Palace7L0(PalaceL0Protocol):
    """7宫 L0 - 法务框架 (兑·金)"""
    
    def __init__(self):
        super().__init__(7, "法务框架", "金", "兑")
        self.outputs = ["validate", "audit", "approve", "review"]
        self.collaborators = [6, 5]


class Palace8L0(PalaceL0Protocol):
    """8宫 L0 - 营销客服 (艮·土)"""
    
    def __init__(self):
        super().__init__(8, "营销客服", "土", "艮")
        self.outputs = ["content", "marketing", "service", "publish"]
        self.collaborators = [4, 9]


class Palace9L0(PalaceL0Protocol):
    """9宫 L0 - 行业生态 (离·火)"""
    
    def __init__(self):
        super().__init__(9, "行业生态", "火", "离")
        self.outputs = ["research", "trend", "ecology", "insight"]
        self.collaborators = [8, 4]


# ==================== L0 协议注册表 ====================

class L0Registry:
    """L0协议注册表"""
    
    def __init__(self):
        self.palaces: Dict[int, PalaceL0Protocol] = {
            1: Palace1L0(),
            2: Palace2L0(),
            3: Palace3L0(),
            4: Palace4L0(),
            5: Palace5L0(),
            6: Palace6L0(),
            7: Palace7L0(),
            8: Palace8L0(),
            9: Palace9L0(),
        }
    
    def get_palace(self, palace_id: int) -> Optional[PalaceL0Protocol]:
        return self.palaces.get(palace_id)
    
    def find_handler(self, task_type: str) -> List[int]:
        return [p.palace_id for p in self.palaces.values() if p.can_accept(task_type)]
    
    def get_all_status(self) -> Dict[int, Dict]:
        return {p_id: palace.get_status() for p_id, palace in self.palaces.items()}
    
    def update_load(self, palace_id: int, load: float):
        if palace_id in self.palaces:
            self.palaces[palace_id].load = load
            self.palaces[palace_id].status = "busy" if load > 0 else "idle"
    
    def auto_run_all(self) -> Dict[int, Dict]:
        """
        所有宫位自主运转
        
        这是太极系统的核心：1+8全部在自主运转
        """
        return {p_id: palace.auto_run() for p_id, palace in self.palaces.items()}


# ==================== 全局实例 ====================

_l0_registry: Optional[L0Registry] = None

def get_l0_registry() -> L0Registry:
    global _l0_registry
    if _l0_registry is None:
        _l0_registry = L0Registry()
    return _l0_registry


# ==================== 测试 ====================

if __name__ == "__main__":
    print("=== 太极L0协议测试 ===\n")
    
    registry = get_l0_registry()
    
    # 测试所有宫位自主运转
    print("【所有宫位自主运转】\n")
    results = registry.auto_run_all()
    
    for p_id, result in results.items():
        print(f"{p_id}宫 {result['name']}")
        print(f"  旋转: {result['rotation']}")
        print(f"  阻力: {result['resistance']:.1f}")
        print(f"  能量: {result['energy']:.1f}")
        print(f"  行动: {result['action']}")
        print(f"  为什么: {result['why']}")
        print()
    
    print("【螺栓结构测试】\n")
    
    # 给5宫添加任务
    registry.update_load(5, 0.5)
    registry.palaces[5].current_task = "测试任务"
    
    result = registry.palaces[5].auto_run()
    print(f"有任务时:")
    print(f"  旋转: {result['rotation']}")
    print(f"  阻力: {result['resistance']:.1f}")
    print(f"  行动: {result['action']}")
    
    # 清除任务
    registry.update_load(5, 0.0)
    registry.palaces[5].current_task = None
    
    result = registry.palaces[5].auto_run()
    print(f"\n无任务时:")
    print(f"  旋转: {result['rotation']}")
    print(f"  阻力: {result['resistance']:.1f}")
    print(f"  行动: {result['action']}")