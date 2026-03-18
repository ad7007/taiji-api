#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
九宫格四循环系统
Nine Palaces Four-Cycle System
"""

from typing import Dict, List, Tuple
from enum import Enum


class CycleType(Enum):
    """循环类型"""
    GENERATION = "相生循环"
    RESTRAINT = "相克循环"
    CENTRAL_AXIS = "159 中轴"
    TRIANGLE_SUPPORT = "258 三角"


class NinePalacesCycles:
    """九宫格四循环系统"""
    
    # 后天八卦九宫格标准布局（已锁定）⭐
    BAGUA_LAYOUT = """
┌─────────┬─────────┬─────────┐
│ 4-品牌战略  │ 9-行业生态  │ 2-产品质量  │
│ (巽宫·木)  │ (离宫·土)  │ (坤宫·金)  │
├─────────┼─────────┼─────────┤
│ 3-技术团队  │ 5-中央控制  │ 7-法务框架  │
│ (震宫·木)  │ (中宫·土)  │ (兑宫·金)  │
├─────────┼─────────┼─────────┤
│ 8-营销客服  │ 1-数据采集  │ 6-物联监控  │
│ (艮宫·木)  │ (坎宫·土)  │ (乾宫·火)  │
└─────────┴─────────┴─────────┘
"""
    
    # 标准坐标映射（用于程序化访问）
    STANDARD_LAYOUT_COORDS: Dict[tuple, int] = {
        (0, 0): 4,  # 左上：巽宫
        (0, 1): 9,  # 上中：离宫
        (0, 2): 2,  # 右上：坤宫
        (1, 0): 3,  # 左中：震宫
        (1, 1): 5,  # 正中：中宫
        (1, 2): 7,  # 右中：兑宫
        (2, 0): 8,  # 左下：艮宫
        (2, 1): 1,  # 下中：坎宫
        (2, 2): 6,  # 右下：乾宫
    }
    
    # 基础配置
    GENERATION_CYCLE: Dict[str, str] = {
        "木": "火",
        "火": "土",
        "土": "金",
        "金": "水",
        "水": "木",
    }
    
    RESTRAINT_CYCLE: Dict[str, str] = {
        "木": "土",
        "土": "水",
        "水": "火",
        "火": "金",
        "金": "木",
    }
    
    CENTRAL_AXIS: List[int] = [1, 5, 9]
    TRIANGLE_SUPPORT: List[int] = [2, 5, 8]
    CORE_PALACE = 5
    
    @classmethod
    def get_generation_path(cls) -> List[int]:
        return [3, 6, 9, 7, 4, 8]
    
    @classmethod
    def get_restraint_pairs(cls) -> List[Tuple[int, int]]:
        return [
            (3, 1), (8, 5), (4, 6), (6, 2), (6, 7), (2, 3), (7, 8),
        ]
    
    @classmethod
    def get_central_axis_path(cls) -> List[int]:
        return cls.CENTRAL_AXIS
    
    @classmethod
    def get_triangle_support_path(cls) -> List[int]:
        return cls.TRIANGLE_SUPPORT
    
    @classmethod
    def is_core_palace(cls, position: int) -> bool:
        return position == cls.CORE_PALACE
    
    @classmethod
    def is_central_axis(cls, position: int) -> bool:
        return position in cls.CENTRAL_AXIS
    
    @classmethod
    def is_triangle_support(cls, position: int) -> bool:
        return position in cls.TRIANGLE_SUPPORT
    
    @classmethod
    def is_dual_cycle_palace(cls, position: int) -> bool:
        return position in cls.CENTRAL_AXIS and position in cls.TRIANGLE_SUPPORT
    
    @classmethod
    def get_cycle_role(cls, position: int) -> str:
        if cls.is_core_palace(position):
            return "绝对核心 - 中央枢纽"
        elif position == 1:
            return "北土 - 数据基础"
        elif position == 9:
            return "南土 - 战略升级"
        elif position == 2:
            return "西金 - 产品约束"
        elif position == 8:
            return "东木 - 营销创新"
        else:
            return "外围宫位"
    
    @classmethod
    def get_standard_layout(cls) -> Dict[tuple, int]:
        """获取标准后天八卦九宫格布局（坐标映射）"""
        return cls.STANDARD_LAYOUT_COORDS.copy()
    
    @classmethod
    def display_bagua_layout(cls) -> str:
        """显示标准后天八卦九宫格布局"""
        return cls.BAGUA_LAYOUT
    
    @classmethod
    def visualize_four_cycles(cls) -> str:
        visual = """
╔══════════════════════════════════════════╗
║      九宫格四循环系统全景图                  ║
╠══════════════════════════════════════════╣
║  【循环 1: 相生】3→6→9→7→4→8              ║
║  【循环 2: 相克】木制土，土制水...           ║
║  【循环 3: 159 中轴】1↔5↔9 ⭐纵向调控       ║
║  【循环 4: 258 三角】2↔5↔8 ⭐横向支撑       ║
║                                          ║
║  核心：5-中央控制 (唯一双循环交点)          ║
╚══════════════════════════════════════════╝
        """
        return visual.strip()
    
    @classmethod
    def get_statistics(cls) -> Dict:
        return {
            "total_cycles": 4,
            "generation_cycle_length": len(cls.get_generation_path()),
            "restraint_pairs_count": len(cls.get_restraint_pairs()),
            "central_axis_count": len(cls.CENTRAL_AXIS),
            "triangle_support_count": len(cls.TRIANGLE_SUPPORT),
            "core_palace": cls.CORE_PALACE,
            "dual_cycle_palaces": [p for p in range(1, 10) if cls.is_dual_cycle_palace(p)],
            "earth_palaces": cls.CENTRAL_AXIS,
        }
