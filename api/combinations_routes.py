"""
N宫组合计算API
基于Taiji.md的组合数学公式
"""

from fastapi import APIRouter
from typing import List, Set, Dict
from itertools import combinations

router = APIRouter(prefix="/api/combinations", tags=["n-palace-combinations"])


# 九宫全集
P = {1, 2, 3, 4, 5, 6, 7, 8, 9}
P_YANG = {3, 4, 7, 9}
P_YIN = {1, 2, 6, 8}
P_CENTER = {5}


def get_n_palace_combinations(n: int) -> List[Set[int]]:
    """计算n宫组合"""
    return [set(c) for c in combinations(P, n)]


def analyze_combination(combo: Set[int]) -> Dict:
    """分析一个组合的特性"""
    yang_count = len(combo & P_YANG)
    yin_count = len(combo & P_YIN)
    has_center = 5 in combo
    
    # 判断阴阳属性
    if yang_count > yin_count:
        attribute = "偏阳"
    elif yin_count > yang_count:
        attribute = "偏阴"
    else:
        attribute = "平衡"
    
    return {
        "combination": list(combo),
        "yang_count": yang_count,
        "yin_count": yin_count,
        "has_center": has_center,
        "attribute": attribute
    }


@router.get("/{n}")
async def get_combinations(n: int):
    """获取n宫组合及其分析"""
    if n < 1 or n > 9:
        return {"error": "n must be 1-9"}
    
    combos = get_n_palace_combinations(n)
    analyzed = [analyze_combination(c) for c in combos]
    
    return {
        "n": n,
        "total": len(combos),
        "combinations": analyzed
    }


@router.get("/summary")
async def get_combinations_summary():
    """获取所有组合的摘要"""
    summary = []
    for n in range(1, 10):
        combos = get_n_palace_combinations(n)
        summary.append({
            "n": n,
            "count": len(combos)
        })
    
    return {
        "total_combinations": sum(s["count"] for s in summary),
        "by_n": summary
    }


@router.get("/structure/{n}")
async def get_structure_analysis(n: int):
    """获取n宫结构分析（基于Taiji.md公式）"""
    if n < 1 or n > 9:
        return {"error": "n must be 1-9"}
    
    combos = get_n_palace_combinations(n)
    
    structures = {
        "total": len(combos),
        "with_center": 0,
        "without_center": 0,
        "yang_heavy": 0,
        "yin_heavy": 0,
        "balanced": 0
    }
    
    for combo in combos:
        analysis = analyze_combination(combo)
        
        if analysis["has_center"]:
            structures["with_center"] += 1
        else:
            structures["without_center"] += 1
        
        if analysis["attribute"] == "偏阳":
            structures["yang_heavy"] += 1
        elif analysis["attribute"] == "偏阴":
            structures["yin_heavy"] += 1
        else:
            structures["balanced"] += 1
    
    return {
        "n": n,
        "structures": structures
    }