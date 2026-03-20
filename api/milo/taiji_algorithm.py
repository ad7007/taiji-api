"""
太极九宫组合算法

核心数学模型：
- 中宫(5): 阴阳同体，可与任何宫组队
- N宫组合：正反、三角、圆形循环
- 相生相克：动态平衡路径
"""

from enum import Enum
from typing import List, Tuple, Set, Dict
from itertools import combinations


# ==================== 基础定义 ====================

class Element(Enum):
    """五行"""
    WOOD = "木"
    FIRE = "火"
    EARTH = "土"
    METAL = "金"
    WATER = "水"


class Palaces(Enum):
    """九宫定义"""
    P1 = 1  # 坎·水·数据采集
    P2 = 2  # 坤·土·产品质量
    P3 = 3  # 震·木·技术团队
    P4 = 4  # 巽·木·品牌战略
    P5 = 5  # 中·土·中央控制（中宫）
    P6 = 6  # 乾·金·物联监控
    P7 = 7  # 兑·金·法务框架
    P8 = 8  # 艮·土·营销客服
    P9 = 9  # 离·火·行业生态


# 阴阳分类
YANG_PALACES = {6, 3, 1, 8}  # 阳卦: 乾震坎艮
YIN_PALACES = {2, 4, 9, 7}   # 阴卦: 坤巽离兑
CENTER_PALACE = 5            # 中宫：阴阳同体

# 五行对应
PALACE_ELEMENT = {
    1: Element.WATER,    # 坎·水
    2: Element.EARTH,    # 坤·土
    3: Element.WOOD,     # 震·木
    4: Element.WOOD,     # 巽·木
    5: Element.EARTH,    # 中·土
    6: Element.METAL,    # 乾·金
    7: Element.METAL,    # 兑·金
    8: Element.EARTH,    # 艮·土
    9: Element.FIRE,     # 离·火
}

# 后天八卦排序
BAGUA_ORDER = [
    [4, 9, 2],  # 第一行: 巽→离→坤
    [3, 5, 7],  # 第二行: 震→中→兑
    [8, 1, 6],  # 第三行: 艮→坎→乾
]


# ==================== N宫组合算法 ====================

def get_2_palace_relations() -> List[Tuple[int, int, str]]:
    """
    2宫组合：正反关系（阴阳生克）
    
    Returns:
        [(宫1, 宫2, 关系类型), ...]
    """
    relations = []
    
    # 阴阳配对
    for yang in YANG_PALACES:
        for yin in YIN_PALACES:
            relations.append((yang, yin, "阴阳"))
    
    # 五行相克配对
    克制关系 = [
        (3, 1),  # 木克土
        (1, 4),  # 土克水
        # ... 更多相克关系
    ]
    
    return relations


def get_3_palace_cycles() -> List[Tuple[int, int, int]]:
    """
    3宫组合：三角循环
    
    核心三角:
    - 159: 中轴（坎-中-离）
    - 258: 横向支撑（坤-中-艮）
    - 357: 技术闭环（震-中-兑）
    - 456: 策略闭环（巽-乾-中...）
    """
    return [
        (1, 5, 9),  # 纵向调控中轴
        (2, 5, 8),  # 横向支撑三角
        (3, 5, 7),  # 技术闭环三角
        (4, 5, 6),  # 监控闭环三角
    ]


def get_4_palace_relations() -> List[Tuple[int, int, int, int]]:
    """
    4宫组合：2组正反关系
    实质是 2×2宫
    """
    relations = []
    
    # 两个三角组合
    triangles = get_3_palace_cycles()
    for t1, t2 in combinations(triangles, 2):
        # 去掉重复的中宫
        palaces = set(t1) | set(t2)
        if len(palaces) == 4:
            relations.append(tuple(sorted(palaces)))
    
    return relations


def get_5_palace_circle() -> List[Tuple[int, ...]]:
    """
    5宫组合：圆形循环（小圆）
    中宫 + 4宫
    """
    circles = []
    
    # 中宫 + 每个三角去掉中宫
    for tri in get_3_palace_cycles():
        if 5 in tri:
            others = [p for p in tri if p != 5]
            # 中宫 + 4个其他宫
            for extra in combinations(YANG_PALACES | YIN_PALACES, 2):
                circle = (5,) + tuple(sorted(others + list(extra)))
                if len(set(circle)) == 5:
                    circles.append(circle)
    
    return circles[:10]  # 返回前10个代表性组合


def get_6_palace_modes() -> Dict[str, List]:
    """
    6宫组合：中圆
    - 2宫模式
    - 三角循环
    - 圆形循环
    """
    return {
        "2_palace": get_2_palace_relations()[:6],
        "triangle": get_3_palace_cycles(),
        "circle": get_5_palace_circle()[:6],
    }


def get_7_palace_modes() -> Dict[str, List]:
    """
    7宫组合：大圆
    - 2宫模式
    - 三角循环
    - 圆形循环
    """
    all_palaces = set(range(1, 10)) - {5}
    
    return {
        "2_palace": get_2_palace_relations()[:7],
        "triangle": get_3_palace_cycles(),
        "circle": [tuple(all_palaces - {p, 5}) for p in [1, 2, 3]],
    }


def get_8_palace_full_mode(with_center: bool = True) -> Dict:
    """
    8宫组合
    
    Args:
        with_center: 是否包含中宫
    
    Returns:
        全模态 或 4组正反关系
    """
    if with_center:
        # 8宫 + 中宫 = 全模态
        return {
            "mode": "full",
            "palaces": list(range(1, 10)),
            "center": 5,
        }
    else:
        # 8宫不含中宫 = 4组正反关系
        pairs = []
        yang_list = list(YANG_PALACES)
        yin_list = list(YIN_PALACES)
        for i in range(4):
            pairs.append((yang_list[i], yin_list[i], "阴阳"))
        return {
            "mode": "pairs",
            "pairs": pairs,
        }


# ==================== 相生循环 ====================

GENERATION_CYCLE = [3, 6, 9, 7, 4, 8, 3]
"""
相生循环路径：
3(震·木) → 6(乾·金) → 9(离·火) → 7(兑·金) → 4(巽·木) → 8(艮·土) → 3
"""


def get_generation_path() -> List[int]:
    """获取相生循环路径"""
    return GENERATION_CYCLE


def find_generation_chain(start: int, length: int = 3) -> List[List[int]]:
    """
    找出生成长度为 length 的链
    
    Args:
        start: 起始宫位
        length: 链长度
    
    Returns:
        [[start, next, next...], ...]
    """
    chains = []
    cycle = GENERATION_CYCLE
    
    if start not in cycle:
        return chains
    
    idx = cycle.index(start)
    chain = []
    for i in range(length):
        chain.append(cycle[(idx + i) % len(cycle)])
    chains.append(chain)
    
    return chains


# ==================== 相克循环 ====================

CONTROL_RELATIONS = [
    (3, 6, "木克金"),  # 震(木) ⚔️ 乾(金)
    (6, 9, "金克火"),  # 乾(金) ⚔️ 离(火)
    (9, 7, "火克金"),  # 离(火) ⚔️ 兑(金)
    (7, 4, "金克木"),  # 兑(金) ⚔️ 巽(木)
    (4, 8, "木克土"),  # 巽(木) ⚔️ 艮(土)
    (8, 1, "土克水"),  # 艮(土) ⚔️ 坎(水)
    (1, 3, "水克木"),  # 坎(水) ⚔️ 震(木)
]
"""
相克循环：动态制衡路径
"""


def get_control_relations() -> List[Tuple[int, int, str]]:
    """获取相克关系"""
    return CONTROL_RELATIONS


def find_control_chain(palace: int) -> List[Tuple[int, str]]:
    """
    找出某宫被谁克、克谁
    
    Returns:
        [(宫位, "克我"/"我克"), ...]
    """
    relations = []
    
    for p1, p2, desc in CONTROL_RELATIONS:
        if p1 == palace:
            relations.append((p2, "我克"))
        if p2 == palace:
            relations.append((p1, "克我"))
    
    return relations


# ==================== 核心结构 ====================

def get_central_axis() -> Tuple[int, int, int]:
    """
    159中轴：纵向调控（坎-中-离）
    信息流：数据采集→中央控制→行业生态
    """
    return (1, 5, 9)


def get_support_triangle() -> Tuple[int, int, int]:
    """
    258三角：横向支撑（坤-中-艮）
    产品流：产品质量→中央控制→营销客服
    """
    return (2, 5, 8)


def get_tech_triangle() -> Tuple[int, int, int]:
    """
    357三角：技术闭环（震-中-兑）
    开发流：技术团队→中央控制→法务验收
    """
    return (3, 5, 7)


def get_monitor_triangle() -> Tuple[int, int, int]:
    """
    456三角：监控闭环（巽-乾-中）
    监控流：品牌战略→物联监控→中央控制
    """
    return (4, 5, 6)


def get_all_triangles() -> List[Tuple[int, int, int]]:
    """
    获取所有三角循环
    
    4个核心三角：
    - 159: 信息流（数据→控制→生态）
    - 258: 产品流（质量→控制→营销）
    - 357: 开发流（技术→控制→验收）
    - 456: 监控流（品牌→监控→控制）
    """
    return [
        (1, 5, 9),  # 信息流
        (2, 5, 8),  # 产品流
        (3, 5, 7),  # 开发流
        (4, 5, 6),  # 监控流
    ]


def get_absolute_core() -> int:
    """
    绝对核心：5-中央控制（双循环交点）
    """
    return 5


# ==================== 组队算法 ====================

def auto_group_by_mode(mode: int, exclude_center: bool = False) -> List[List[int]]:
    """
    按模式自动生成组队
    
    Args:
        mode: 2-8宫组合模式
        exclude_center: 是否排除中宫
    
    Returns:
        组队列表
    """
    if mode == 2:
        relations = get_2_palace_relations()
        return [[r[0], r[1]] for r in relations[:5]]
    
    elif mode == 3:
        return [list(tri) for tri in get_3_palace_cycles()]
    
    elif mode == 4:
        return [list(rel) for rel in get_4_palace_relations()[:5]]
    
    elif mode == 5:
        return [list(c) for c in get_5_palace_circle()[:5]]
    
    elif mode == 6:
        modes = get_6_palace_modes()
        return modes["triangle"] + modes["circle"][:3]
    
    elif mode == 7:
        modes = get_7_palace_modes()
        return modes["triangle"] + modes["circle"][:4]
    
    elif mode == 8:
        full = get_8_palace_full_mode(with_center=not exclude_center)
        if full["mode"] == "full":
            return [full["palaces"]]
        else:
            return [[p[0], p[1]] for p in full["pairs"]]
    
    return []


# ==================== 工具函数 ====================

def is_yang(palace: int) -> bool:
    """判断是否为阳卦"""
    return palace in YANG_PALACES


def is_yin(palace: int) -> bool:
    """判断是否为阴卦"""
    return palace in YIN_PALACES


def get_element(palace: int) -> Element:
    """获取宫位的五行属性"""
    return PALACE_ELEMENT.get(palace, Element.EARTH)


def get_position(palace: int) -> Tuple[int, int]:
    """
    获取宫位在九宫格中的位置
    
    Returns:
        (row, col) 从0开始
    """
    for row, cols in enumerate(BAGUA_ORDER):
        if palace in cols:
            return (row, cols.index(palace))
    return (-1, -1)


# ==================== 示例用法 ====================

if __name__ == "__main__":
    print("=== 太极九宫组合算法 ===\n")
    
    print("- 2宫组合（正反关系）")
    for r in get_2_palace_relations()[:5]:
        print(f"  {r}")
    
    print("\n- 3宫组合（三角循环）")
    for tri in get_3_palace_cycles():
        print(f"  {tri}")
    
    print("\n- 相生循环")
    print(f"  {' → '.join(map(str, GENERATION_CYCLE))}")
    
    print("\n- 相克关系")
    for p1, p2, desc in CONTROL_RELATIONS:
        print(f"  {p1}宫 {desc} {p2}宫")
    
    print("\n- 核心结构")
    print(f"  159中轴: {get_central_axis()}")
    print(f"  258三角: {get_support_triangle()}")
    print(f"  绝对核心: {get_absolute_core()}宫")
    
    print("\n- 按模式组队")
    for mode in [2, 3, 5, 8]:
        groups = auto_group_by_mode(mode)[:3]
        print(f"  {mode}宫模式: {groups}")