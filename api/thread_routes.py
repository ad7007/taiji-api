"""
24线程API端点
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import json

from core.taiji_24_threads import (
    thread_system, Direction, THREAD_MATRIX,
    triangle_stability, n_palace_combinations, sheng_path,
    V_YANG, V_YIN, SHENG_CHAIN, KE, WUXING
)

router = APIRouter(prefix="/api/threads", tags=["24-threads"])


class TransformRequest(BaseModel):
    direction: str  # "YIN_TO_YANG" or "YANG_TO_YIN"
    alpha: float = 0.3


@router.get("/status")
async def get_threads_status():
    """获取24线程系统状态"""
    return {
        "thread_count": len(thread_system.threads),
        "balance": round(thread_system.get_balance(), 3),
        "rotation": thread_system.get_rotation(),
        "yang_endpoints": list(V_YANG),
        "yin_endpoints": list(V_YIN),
        "center": 5
    }


@router.post("/transform")
async def transform_threads(req: TransformRequest):
    """转换所有线程方向"""
    try:
        direction = Direction.YIN_TO_YANG if req.direction == "YIN_TO_YANG" else Direction.YANG_TO_YIN
    except:
        raise HTTPException(status_code=400, detail="Invalid direction")

    before = thread_system.get_balance()
    thread_system.transform_all(direction, req.alpha)
    after = thread_system.get_balance()

    return {
        "success": True,
        "direction": req.direction,
        "alpha": req.alpha,
        "balance_before": round(before, 3),
        "balance_after": round(after, 3),
        "rotation": thread_system.get_rotation()
    }


@router.get("/matrix")
async def get_thread_matrix():
    """获取线程连接矩阵"""
    matrix = THREAD_MATRIX[1:10, 1:10].tolist()
    connections = []

    for i in range(1, 10):
        for j in range(1, 10):
            if THREAD_MATRIX[i][j] != 0:
                rel = "相生" if THREAD_MATRIX[i][j] == 1 else "相克"
                connections.append({
                    "from": i,
                    "to": j,
                    "relation": rel
                })

    return {
        "matrix": matrix,
        "connections": connections,
        "yang_endpoints": list(V_YANG),
        "yin_endpoints": list(V_YIN)
    }


@router.get("/wuxing")
async def get_wuxing():
    """获取五行属性"""
    return {
        "wuxing": WUXING,
        "sheng_chain": SHENG_CHAIN,
        "ke_chain": KE
    }


@router.get("/sheng-path/{start}/{end}")
async def get_sheng_path(start: int, end: int):
    """获取相生路径"""
    if start < 1 or start > 9 or end < 1 or end > 9:
        raise HTTPException(status_code=400, detail="Palace must be 1-9")

    path = sheng_path(start, end)
    return {
        "start": start,
        "end": end,
        "path": path,
        "length": len(path)
    }


@router.get("/triangle-stability")
async def get_triangle_stability():
    """获取三角稳定性分析"""
    # 预定义三角
    triangles = [
        {"name": "159中轴", "palaces": [1, 5, 9]},
        {"name": "258横轴", "palaces": [2, 5, 8]},
        {"name": "357斜轴", "palaces": [3, 5, 7]},
        {"name": "456斜轴", "palaces": [4, 5, 6]},
    ]

    results = []
    for tri in triangles:
        stability = triangle_stability(set(tri["palaces"]))
        results.append({
            "name": tri["name"],
            "palaces": tri["palaces"],
            "stability": round(stability, 3),
            "status": "稳定" if stability > 0 else "不稳定" if stability < 0 else "中性"
        })

    return {"triangles": results}


@router.get("/combinations/{n}")
async def get_n_palace_combinations(n: int):
    """获取n宫组合"""
    if n < 1 or n > 9:
        raise HTTPException(status_code=400, detail="n must be 1-9")

    combinations = n_palace_combinations(n)
    return {
        "n": n,
        "count": len(combinations),
        "combinations": [list(c) for c in combinations[:20]]  # 只返回前20个
    }