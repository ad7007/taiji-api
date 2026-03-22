#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太极五行生克循环系统
Taiji Five Elements Cycle System - L0 Meta Planning

基于八卦五行相生相克关系的动态演化机制
实现各宫位之间的生克闭环和六爻动态演化
"""

from enum import Enum
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json
import sys
from pathlib import Path

# 导入官方宫殿配置函数
sys.path.insert(0, str(Path(__file__).parent))
from palace_constants import (
    get_palace_name,
    get_palace_trigram,
    get_palace_directory,
    get_palace_element,
    get_all_palaces
)


# ============================================================================
# L0 元数据定义
# ============================================================================

class FiveElements(Enum):
    """五行元素"""
    WOOD = "木"      # Wood
    FIRE = "火"      # Fire
    EARTH = "土"     # Earth
    METAL = "金"     # Metal
    WATER = "水"     # Water


class PalacePosition(Enum):
    """宫位（后天八卦）"""
    KAN_1 = 1       # 坎宫 - 水
    KUN_2 = 2       # 坤宫 - 土
    ZHEN_3 = 3      # 震宫 - 木
    XUN_4 = 4       # 巽宫 - 木
    CENTER_5 = 5    # 中宫 - 土
    QIAN_6 = 6      # 乾宫 - 金
    DUI_7 = 7       # 兑宫 - 金
    GEN_8 = 8       # 艮宫 - 土
    LI_9 = 9        # 离宫 - 火


# 宫位与五行的映射关系（使用官方函数）
PALACE_TO_ELEMENT: Dict[int, FiveElements] = {
    pos: FiveElements(get_palace_element(pos))  # 使用官方函数获取五行属性
    for pos in range(1, 10)
}


# 五行相生关系（生成、促进）
# 木生火，火生土，土生金，金生水，水生木
GENERATION_CYCLE: Dict[FiveElements, FiveElements] = {
    FiveElements.WOOD: FiveElements.FIRE,    # 木生火
    FiveElements.FIRE: FiveElements.EARTH,   # 火生土
    FiveElements.EARTH: FiveElements.METAL,  # 土生金
    FiveElements.METAL: FiveElements.WATER,  # 金生水
    FiveElements.WATER: FiveElements.WOOD,   # 水生木
}


# 五行相克关系（制约、抑制）
# 木克土，土克水，水克火，火克金，金克木
RESTRAINT_CYCLE: Dict[FiveElements, FiveElements] = {
    FiveElements.WOOD: FiveElements.EARTH,   # 木克土
    FiveElements.EARTH: FiveElements.WATER,  # 土克水
    FiveElements.WATER: FiveElements.FIRE,   # 水克火
    FiveElements.FIRE: FiveElements.METAL,   # 火克金
    FiveElements.METAL: FiveElements.WOOD,   # 金克木
}


@dataclass
class PalaceState:
    """宫位状态"""
    position: int
    element: FiveElements
    health: float = 1.0  # 健康度 0-1
    activation: float = 0.0  # 激活度 0-1
    yao_lines: List[bool] = None  # 6 个爻位的状态（True=阳爻，False=阴爻）
    
    def __post_init__(self):
        if self.yao_lines is None:
            # 默认初始状态：全为阳爻
            self.yao_lines = [True] * 6


@dataclass
class GenerationRelationship:
    """相生关系"""
    source: int  # 生者宫位
    target: int  # 被生者宫位
    strength: float  # 生力强度 0-1


@dataclass
class RestraintRelationship:
    """相克关系"""
    restrainer: int  # 克者宫位
    restrained: int  # 被克者宫位
    pressure: float  # 克制压力 0-1


# ============================================================================
# L0 元规划引擎
# ============================================================================

class TaijiMetaPlanner:
    """
    太极元规划器 - L0 层级
    
    负责：
    1. 计算各宫位之间的生克关系
    2. 触发生克闭环的动态演化
    3. 提供感知机制的权重依据
    """
    
    def __init__(self):
        self.palace_states: Dict[int, PalaceState] = {}
        self.generation_relations: List[GenerationRelationship] = []
        self.restraint_relations: List[RestraintRelationship] = []
        
        # 初始化 9 个宫位
        for pos in range(1, 10):
            element = PALACE_TO_ELEMENT[pos]
            self.palace_states[pos] = PalaceState(
                position=pos,
                element=element
            )
        
        # 构建生克关系网络
        self._build_generation_network()
        self._build_restraint_network()
    
    def _build_generation_network(self):
        """构建相生关系网络"""
        self.generation_relations.clear()
        
        # 遍历所有宫位，找出生我和我生的关系
        for pos, element in PALACE_TO_ELEMENT.items():
            # 找到生这个元素的元素
            for other_pos, other_element in PALACE_TO_ELEMENT.items():
                if GENERATION_CYCLE.get(other_element) == element:
                    # other_pos 生 pos
                    self.generation_relations.append(
                        GenerationRelationship(
                            source=other_pos,
                            target=pos,
                            strength=self._calculate_generation_strength(
                                other_pos, pos
                            )
                        )
                    )
    
    def _build_restraint_network(self):
        """构建相克关系网络"""
        self.restraint_relations.clear()
        
        # 遍历所有宫位，找出克我和我克的关系
        for pos, element in PALACE_TO_ELEMENT.items():
            # 找到克这个元素的元素
            for other_pos, other_element in PALACE_TO_ELEMENT.items():
                if RESTRAINT_CYCLE.get(other_element) == element:
                    # other_pos 克 pos
                    self.restraint_relations.append(
                        RestraintRelationship(
                            restrainer=other_pos,
                            restrained=pos,
                            pressure=self._calculate_restraint_pressure(
                                other_pos, pos
                            )
                        )
                    )
    
    def _calculate_generation_strength(self, source: int, target: int) -> float:
        """
        计算相生强度
        
        考虑因素：
        1. 基础生力（同属性更强）
        2. 宫位距离（相邻更强）
        3. 当前健康度
        """
        base_strength = 0.5
        
        # 同属性增强（如震木生离火，都是阳性）
        source_element = PALACE_TO_ELEMENT[source]
        target_element = PALACE_TO_ELEMENT[target]
        if source % 2 == target % 2:  # 同阴阳
            base_strength += 0.2
        
        # 相邻宫位增强
        if abs(source - target) == 1 or abs(source - target) == 8:
            base_strength += 0.2
        
        # 源宫位健康度影响
        source_health = self.palace_states[source].health
        base_strength *= source_health
        
        return min(1.0, base_strength)
    
    def _calculate_restraint_pressure(self, restrainer: int, restrained: int) -> float:
        """
        计算相克压力
        
        考虑因素：
        1. 基础克力
        2. 实力差距（健康度差异）
        3. 是否有救援（第三方调解）
        """
        base_pressure = 0.6
        
        # 健康度差异
        restrainer_health = self.palace_states[restrainer].health
        restrained_health = self.palace_states[restrained].health
        health_diff = restrainer_health - restrained_health
        
        if health_diff > 0:
            base_pressure += health_diff * 0.3
        else:
            base_pressure += health_diff * 0.5  # 弱势方克人，力不足
        
        # 检查是否有救援（被克者的生者）
        rescue_strength = self._get_rescue_strength(restrained)
        if rescue_strength > 0:
            base_pressure *= (1 - rescue_strength * 0.5)
        
        return max(0.1, min(1.0, base_pressure))
    
    def _get_rescue_strength(self, palace_pos: int) -> float:
        """获取救援力量（生我者的力量）"""
        rescue_power = 0.0
        
        for rel in self.generation_relations:
            if rel.target == palace_pos:
                rescue_power += rel.strength * self.palace_states[rel.source].health
        
        return min(1.0, rescue_power)
    
    def evolve_yao_lines(self, palace_pos: int) -> List[bool]:
        """
        演化指定宫位的六爻
        
        演化规则：
        1. 受生力影响：初爻、三爻、五爻（奇数位）易变阳
        2. 受克力影响：二爻、四爻、上爻（偶数位）易变阴
        3. 综合平衡后决定最终状态
        """
        state = self.palace_states[palace_pos]
        
        # 计算总生力
        total_generation = sum(
            rel.strength 
            for rel in self.generation_relations 
            if rel.target == palace_pos
        )
        
        # 计算总克力
        total_restraint = sum(
            rel.pressure 
            for rel in self.restraint_relations 
            if rel.restrained == palace_pos
        )
        
        # 净影响力
        net_influence = total_generation - total_restraint
        
        # 演化六爻
        new_yao_lines = state.yao_lines.copy()
        
        for i in range(6):
            # 基础概率
            yang_probability = 0.5 + net_influence * 0.3
            
            # 位置修正（奇数位偏阳，偶数位偏阴）
            if i % 2 == 0:  # 初、三、五爻
                yang_probability += 0.1
            else:  # 二、四、上爻
                yang_probability -= 0.1
            
            # 简单模拟：大于 0.5 则为阳
            new_yao_lines[i] = (yang_probability > 0.5)
        
        return new_yao_lines
    
    def get_balance_report(self) -> Dict:
        """获取整体平衡报告（使用官方名称）"""
        report = {
            "generation_cycle": [],
            "restraint_cycle": [],
            "palace_health": {},
            "overall_balance": 0.0
        }
        
        # 相生循环状态（使用官方名称）
        for rel in self.generation_relations:
            report["generation_cycle"].append({
                "source": f"{get_palace_name(rel.source)} ({PALACE_TO_ELEMENT[rel.source].value})",
                "target": f"{get_palace_name(rel.target)} ({PALACE_TO_ELEMENT[rel.target].value})",
                "strength": round(rel.strength, 3)
            })
        
        # 相克循环状态（使用官方名称）
        for rel in self.restraint_relations:
            report["restraint_cycle"].append({
                "restrainer": f"{get_palace_name(rel.restrainer)} ({PALACE_TO_ELEMENT[rel.restrainer].value})",
                "restrained": f"{get_palace_name(rel.restrained)} ({PALACE_TO_ELEMENT[rel.restrained].value})",
                "pressure": round(rel.pressure, 3)
            })
        
        # 各宫健康度（使用官方名称）
        for pos, state in self.palace_states.items():
            report["palace_health"][f"{get_palace_name(pos)}"] = round(state.health, 3)
        
        # 整体平衡度
        health_values = [state.health for state in self.palace_states.values()]
        report["overall_balance"] = round(sum(health_values) / len(health_values), 3)
        
        return report
    
    def update_palace_health(self, palace_pos: int, new_health: float):
        """更新宫位健康度"""
        if palace_pos in self.palace_states:
            self.palace_states[palace_pos].health = max(0.0, min(1.0, new_health))
            # 重新计算相关关系
            self._build_generation_network()
            self._build_restraint_network()
    
    def to_json(self) -> str:
        """导出为 JSON"""
        return json.dumps(self.get_balance_report(), ensure_ascii=False, indent=2)
    
    # ========== 四循环系统增强方法 ==========
    
    def get_central_axis_balance(self) -> float:
        """
        计算 159 中轴的平衡度
        
        Returns:
            float: 平衡度 0-1
        """
        try:
            from .nine_palaces_cycles import NinePalacesCycles
        except ImportError:
            from nine_palaces_cycles import NinePalacesCycles
        
        axis_palaces = NinePalacesCycles.get_central_axis_path()
        health_values = [
            self.palace_states[pos].health 
            for pos in axis_palaces 
            if pos in self.palace_states
        ]
        
        if not health_values:
            return 0.0
        
        return sum(health_values) / len(health_values)
    
    def get_triangle_support_balance(self) -> float:
        """
        计算 258 三角支撑的平衡度
        
        Returns:
            float: 平衡度 0-1
        """
        try:
            from .nine_palaces_cycles import NinePalacesCycles
        except ImportError:
            from nine_palaces_cycles import NinePalacesCycles
        
        triangle_palaces = NinePalacesCycles.get_triangle_support_path()
        health_values = [
            self.palace_states[pos].health 
            for pos in triangle_palaces 
            if pos in self.palace_states
        ]
        
        if not health_values:
            return 0.0
        
        return sum(health_values) / len(health_values)
    
    def get_core_palace_status(self) -> Dict:
        """
        获取核心宫位（5 中宫）的状态
        
        Returns:
            Dict: 核心宫位的详细状态
        """
        try:
            from .nine_palaces_cycles import NinePalacesCycles
        except ImportError:
            from nine_palaces_cycles import NinePalacesCycles
        
        if 5 not in self.palace_states:
            return {"error": "核心宫位不存在"}
        
        core_state = self.palace_states[5]
        return {
            "position": 5,
            "name": "5-中央控制",
            "health": core_state.health,
            "activation": core_state.activation,
            "is_healthy": core_state.health > 0.8,
            "role": NinePalacesCycles.get_cycle_role(5)
        }
    
    def get_four_cycles_report(self) -> Dict:
        """
        获取四循环系统的完整报告
        
        Returns:
            Dict: 四个循环的状态
        """
        try:
            from .nine_palaces_cycles import NinePalacesCycles
        except ImportError:
            from nine_palaces_cycles import NinePalacesCycles
        
        return {
            "generation_cycle": {
                "balance": self._calculate_cycle_balance(NinePalacesCycles.get_generation_path()),
                "status": "normal"
            },
            "restraint_cycle": {
                "balance": self._calculate_restraint_balance(),
                "status": "normal"
            },
            "central_axis_159": {
                "balance": self.get_central_axis_balance(),
                "core_health": self.palace_states.get(5, {}).health if 5 in self.palace_states else 0,
                "status": "critical" if self.get_central_axis_balance() < 0.6 else "normal"
            },
            "triangle_support_258": {
                "balance": self.get_triangle_support_balance(),
                "status": "normal"
            },
            "core_palace": self.get_core_palace_status()
        }
    
    def _calculate_cycle_balance(self, palace_positions: List[int]) -> float:
        """
        计算指定循环的平衡度
        
        Args:
            palace_positions: 宫位位置列表
        
        Returns:
            float: 平衡度 0-1
        """
        health_values = [
            self.palace_states[pos].health 
            for pos in palace_positions 
            if pos in self.palace_states
        ]
        
        if not health_values:
            return 0.0
        
        return sum(health_values) / len(health_values)
    
    def _calculate_restraint_balance(self) -> float:
        """
        计算相克循环的平衡度
        
        Returns:
            float: 平衡度 0-1
        """
        try:
            from .nine_palaces_cycles import NinePalacesCycles
        except ImportError:
            from nine_palaces_cycles import NinePalacesCycles
        
        pairs = NinePalacesCycles.get_restraint_pairs()
        balance_scores = []
        
        for restrainer, restrained in pairs:
            if restrainer in self.palace_states and restrained in self.palace_states:
                r_health = self.palace_states[restrainer].health
                e_health = self.palace_states[restrained].health
                
                # 平衡的理想状态：克制者略强
                ideal_diff = 0.2
                actual_diff = r_health - e_health
                balance = 1.0 - abs(actual_diff - ideal_diff)
                
                balance_scores.append(max(0, balance))
        
        return sum(balance_scores) / len(balance_scores) if balance_scores else 0.0


# ============================================================================
# 测试和演示
# ============================================================================

if __name__ == "__main__":
    print("=== 太极五行生克循环系统 L0 ===\n")
    
    planner = TaijiMetaPlanner()
    
    print("【九宫五行配置】（使用官方名称）")
    for pos in range(1, 10):
        element = PALACE_TO_ELEMENT[pos]
        print(f"  {get_palace_name(pos)}: {element.value}")
    
    print("\n【相生关系】")
    for rel in planner.generation_relations[:5]:  # 只显示前 5 个
        print(f"  {get_palace_name(rel.source)} → {get_palace_name(rel.target)} (强度：{rel.strength:.2f})")
    
    print("\n【相克关系】")
    for rel in planner.restraint_relations[:5]:  # 只显示前 5 个
        print(f"  {get_palace_name(rel.restrainer)} → {get_palace_name(rel.restrained)} (压力：{rel.pressure:.2f})")
    
    print("\n【整体平衡报告】")
    report = planner.get_balance_report()
    print(f"  整体平衡度：{report['overall_balance']}")
    print(f"  相生关系数：{len(report['generation_cycle'])}")
    print(f"  相克关系数：{len(report['restraint_cycle'])}")
    
    print("\n【六爻演化示例 - 1 数据采集】")
    initial_yao = planner.palace_states[1].yao_lines
    evolved_yao = planner.evolve_yao_lines(1)
    print(f"  初始：{initial_yao}")
    print(f"  演化：{evolved_yao}")
    
    print("\n【JSON 输出】")
    print(planner.to_json()[:500] + "...")
