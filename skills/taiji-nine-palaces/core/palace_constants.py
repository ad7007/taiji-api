#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
九宫格系统常量定义
Palace System Constants - Unified Definition
"""

from typing import Dict, List
from config.palace_config import palace_config

# ============================================================================
# 官方九宫格配置表（所有字段都带数字前缀）
# ============================================================================

# 后天八卦九宫格标准布局（已锁定）⭐
# ┌─────┬─────┬─────┐
# │ 4 巽 │ 9 离 │ 2 坤 │
# ├─────┼─────┼─────┤
# │ 3 震 │ 5 中 │ 7 兑 │
# ├─────┼─────┼─────┤
# │ 8 艮 │ 1 坎 │ 6 乾 │
# └─────┴─────┴─────┘

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

# 宫位配置（补充配置信息）
PALACES_CONFIG: Dict[int, Dict[str, str]] = {
    1: {"name": "1-数据采集", "trigram": "1-坎", "directory": "palace_1_data", "element": "土"},
    2: {"name": "2-产品质量", "trigram": "2-坤", "directory": "palace_2_product", "element": "金"},
    3: {"name": "3-技术团队", "trigram": "3-震", "directory": "palace_3_tech", "element": "木"},
    4: {"name": "4-品牌战略", "trigram": "4-巽", "directory": "palace_4_team", "element": "水"},
    5: {"name": "5-中央控制", "trigram": "5-中", "directory": "palace_5_master", "element": "土"},
    6: {"name": "6-物联监控", "trigram": "6-乾", "directory": "palace_6_iot", "element": "火"},
    7: {"name": "7-法务框架", "trigram": "7-兑", "directory": "palace_7_monitor", "element": "金"},
    8: {"name": "8-营销客服", "trigram": "8-艮", "directory": "palace_8_marketing", "element": "木"},
    9: {"name": "9-行业生态", "trigram": "9-离", "directory": "palace_9_ecology", "element": "土"}
}

# ============================================================================
# 核心 Getter 函数
# ============================================================================

def get_palace_name(position: int) -> str:
    """获取宫位名称（带数字前缀）"""
    return PALACES_CONFIG.get(position, {}).get("name", f"{position}宫")

def get_palace_trigram(position: int) -> str:
    """获取宫位卦象（带数字前缀）"""
    return PALACES_CONFIG.get(position, {}).get("trigram", "未知")

def get_palace_directory(position: int) -> str:
    """获取宫位目录名"""
    return PALACES_CONFIG.get(position, {}).get("directory", f"palace_{position}")

def get_palace_element(position: int) -> str:
    """获取宫位五行属性"""
    return PALACES_CONFIG.get(position, {}).get("element", "未知")

def get_custom_name(position: int, custom: str = None) -> str:
    """
    获取宫位显示名称（支持用户自定义）
    
    Args:
        position: 宫位数字 (1-9)
        custom: 用户自定义名称（可选）
    
    Returns:
        格式："1-数据采集 (用户自定义)" 或 "1-数据采集"
    """
    official = get_palace_name(position)
    if custom:
        return f"{official} ({custom})"
    return official

def get_all_palaces() -> List[Dict]:
    """获取所有宫位的完整信息"""
    return [
        {
            "position": pos,
            "name": config["name"],
            "trigram": config["trigram"],
            "directory": config["directory"],
            "element": config["element"]
        }
        for pos, config in PALACES_CONFIG.items()
    ]

def get_standard_layout() -> Dict[tuple, int]:
    """获取标准后天八卦九宫格布局（坐标映射）"""
    return STANDARD_LAYOUT_COORDS.copy()

def display_bagua_layout() -> str:
    """显示标准后天八卦九宫格布局"""
    return BAGUA_LAYOUT

# ============================================================================
# 调试输出
# ============================================================================

if __name__ == "__main__":
    print("=== 九宫格系统配置 ===\n")
    print("📊 标准后天八卦布局（已锁定）⭐:")
    print(BAGUA_LAYOUT)
    print("\n" + "="*55)
    print(f"{'宫位':<4} {'官方全称':<12} {'卦象':<8} {'目录名':<20} {'五行':<4}")
    print("-" * 55)
    for pos in range(1, 10):
        config = PALACES_CONFIG[pos]
        print(f"{pos:<4} {config['name']:<12} {config['trigram']:<8} {config['directory']:<20} {config['element']:<4}")
    
    print("\n=== 函数测试 ===")
    print(f"get_palace_name(1) = {get_palace_name(1)}")
    print(f"get_palace_trigram(1) = {get_palace_trigram(1)}")
    print(f"get_palace_directory(1) = {get_palace_directory(1)}")
    print(f"get_palace_element(1) = {get_palace_element(1)}")
    print(f"get_custom_name(1, '我的数据') = {get_custom_name(1, '我的数据')}")
    
    print("\n=== 标准布局坐标映射 ===")
    layout = get_standard_layout()
    for coord, palace_num in sorted(layout.items()):
        print(f"坐标 {coord}: {get_palace_name(palace_num)}")
    
    print("\n=== 配置系统测试 ===")
    print(f"palace_config.get_palace_name(1) = {palace_config.get_palace_name(1)}")
    print(f"palace_config.get_palace_element(1) = {palace_config.get_palace_element(1)}")
