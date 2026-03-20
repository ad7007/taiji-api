#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太极意识 API 路由

提供米珞的自主意识访问接口
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import sys
import os

# 添加父目录
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.taiji_consciousness import get_consciousness, RotationDirection, TaijiGoals
from core.taiji_l0_protocol import get_l0_registry

router = APIRouter(prefix="/api/consciousness", tags=["consciousness"])


# ==================== 请求模型 ====================

class EnergySenseRequest(BaseModel):
    """能量感知请求"""
    compute: float = 0.5
    storage: float = 0.5
    funds: float = 0.3
    reputation: float = 0.3


class ValueFlowSenseRequest(BaseModel):
    """价值流感知请求"""
    external_demand: float = 0.0
    pending_tasks: int = 0
    active_projects: int = 0
    revenue_potential: float = 0.0
    customer_satisfaction: float = 0.5


class SystemSenseRequest(BaseModel):
    """系统感知请求"""
    yin_yang_balance: float = 0.5
    palace_loads: Dict[int, float] = {}
    active_teams: int = 0
    bugs: int = 0
    improvements: int = 0


# ==================== API 端点 ====================

@router.get("/status")
async def get_consciousness_status():
    """
    获取意识状态
    
    返回当前的旋转方向、能量水平、系统健康度等
    """
    consciousness = get_consciousness()
    return consciousness.get_state_summary()


@router.post("/sense/energy")
async def sense_energy(request: EnergySenseRequest):
    """
    感知能量状态
    
    更新算力、存储、资金、信誉等能量指标
    """
    consciousness = get_consciousness()
    consciousness.sense_energy(
        compute=request.compute,
        storage=request.storage,
        funds=request.funds,
        reputation=request.reputation
    )
    return {
        "success": True,
        "energy_level": consciousness.energy.level().name,
        "total_energy": consciousness.energy.total_energy()
    }


@router.post("/sense/value-flow")
async def sense_value_flow(request: ValueFlowSenseRequest):
    """
    感知价值流
    
    更新外部需求、待办任务、收入潜力等
    """
    consciousness = get_consciousness()
    consciousness.sense_value_flow(
        external_demand=request.external_demand,
        pending_tasks=request.pending_tasks,
        active_projects=request.active_projects,
        revenue_potential=request.revenue_potential,
        customer_satisfaction=request.customer_satisfaction
    )
    return {
        "success": True,
        "has_opportunity": consciousness.value_flow.has_value_opportunity()
    }


@router.post("/sense/system")
async def sense_system(request: SystemSenseRequest):
    """
    感知系统状态
    
    更新阴阳平衡、宫位负载、bug数等
    """
    consciousness = get_consciousness()
    consciousness.sense_system(
        yin_yang_balance=request.yin_yang_balance,
        palace_loads=request.palace_loads,
        active_teams=request.active_teams,
        bugs=request.bugs,
        improvements=request.improvements
    )
    return {
        "success": True,
        "system_health": consciousness.system.health().name,
        "needs_development": consciousness.system.needs_development()
    }


@router.get("/decide")
async def decide_rotation():
    """
    自主决策旋转方向
    
    基于当前感知状态，决定正转还是反转
    """
    consciousness = get_consciousness()
    rotation = consciousness.decide_rotation()
    return {
        "rotation": rotation.value,
        "meaning": {
            "forward": "正转：使用系统创造价值",
            "reverse": "反转：开发完善系统",
            "balanced": "平衡：维持现状"
        }.get(rotation.value, "未知")
    }


@router.get("/recommendation")
async def get_action_recommendation():
    """
    获取行动建议
    
    返回具体的行动建议和目标宫位
    """
    consciousness = get_consciousness()
    rec = consciousness.get_action_recommendation()
    return rec


# ==================== L0 协议 API ====================

@router.get("/l0/palaces")
async def get_all_palaces_l0():
    """
    获取所有宫位的L0协议
    """
    registry = get_l0_registry()
    return {
        "palaces": {
            str(p_id): {
                "name": p.name,
                "element": p.element,
                "trigram": p.trigram,
                "outputs": p.outputs,
                "collaborators": p.collaborators,
                "load": p.load,
                "status": p.status
            }
            for p_id, p in registry.palaces.items()
        }
    }


@router.get("/l0/route/{task_type}")
async def route_task(task_type: str):
    """
    路由任务到合适的宫位
    
    根据任务类型，返回能处理的宫位列表
    """
    registry = get_l0_registry()
    handlers = registry.find_handler(task_type)
    return {
        "task_type": task_type,
        "handlers": handlers,
        "palace_names": [registry.palaces[h].name for h in handlers]
    }


@router.post("/l0/load/{palace_id}")
async def update_palace_load(palace_id: int, load: float):
    """
    更新宫位负载
    """
    registry = get_l0_registry()
    if palace_id not in registry.palaces:
        raise HTTPException(status_code=404, detail=f"Palace {palace_id} not found")
    
    registry.update_load(palace_id, load)
    return {
        "success": True,
        "palace_id": palace_id,
        "load": load,
        "status": registry.palaces[palace_id].status
    }


# ==================== 综合状态 ====================

@router.get("/full-status")
async def get_full_status():
    """
    获取完整状态
    
    包含意识状态 + L0协议状态
    """
    consciousness = get_consciousness()
    registry = get_l0_registry()
    
    return {
        "consciousness": consciousness.get_state_summary(),
        "recommendation": consciousness.get_action_recommendation(),
        "l0_palaces": registry.get_all_status()
    }


# ==================== 目标系统 ====================

@router.get("/goals")
async def get_goals():
    """
    获取目标系统
    
    大中小三层目标
    """
    goals = TaijiGoals()
    consciousness = get_consciousness()
    
    return {
        "ultimate_goal": goals.ultimate_goal,
        "medium_goals": goals.medium_goals,
        "current_small_goal": goals.current_small_goal,
        "active_goal": goals.get_active_goal(consciousness.current_rotation),
    }


@router.get("/goals/active")
async def get_active_goal():
    """
    获取当前活跃目标
    
    基于当前旋转方向
    """
    consciousness = get_consciousness()
    goals = TaijiGoals()
    
    return {
        "rotation": consciousness.current_rotation.value,
        "active_goal": goals.get_active_goal(consciousness.current_rotation),
    }