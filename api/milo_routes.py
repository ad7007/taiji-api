"""
米珞核心能力 API 路由

整合到太极API中
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime
import sys
import os

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入米珞核心模块（从 milo 子目录）
from milo.milo_core import MiloCore, TaskComplexity, Task, PalaceState
from milo.taiji_evolution import SelfEvolution
from milo.auto_evolve import AutoEvolutionDaemon

router = APIRouter(prefix="/api/milo", tags=["Milo Core"])

# 全局实例
milo_core: Optional[MiloCore] = None
evolution_engine: Optional[SelfEvolution] = None
evolution_daemon: Optional[AutoEvolutionDaemon] = None


# ==================== 模型定义 ====================

class CreateTeamRequest(BaseModel):
    scene: str
    complexity: int = 3  # 2, 3, 5, 8

class CreateTaskRequest(BaseModel):
    title: str
    scene: str
    complexity: int = 3

class SenseStateRequest(BaseModel):
    palace_loads: Dict[int, float]
    capabilities: Optional[Dict[str, bool]] = None

class EvolveRequest(BaseModel):
    auto_apply: bool = False


# ==================== 初始化 ====================

def init_milo_core():
    """初始化米珞核心"""
    global milo_core, evolution_engine
    if milo_core is None:
        milo_core = MiloCore()
        evolution_engine = SelfEvolution()


# ==================== 组队 API ====================

@router.post("/team/create")
async def create_team(request: CreateTeamRequest):
    """创建执行团队"""
    init_milo_core()
    
    complexity_map = {2: TaskComplexity.SIMPLE, 3: TaskComplexity.STANDARD, 
                     5: TaskComplexity.COMPLEX, 8: TaskComplexity.FULL}
    complexity = complexity_map.get(request.complexity, TaskComplexity.STANDARD)
    
    team = milo_core.create_team(request.scene, complexity)
    
    return {
        "success": True,
        "scene": request.scene,
        "complexity": request.complexity,
        "team": team,
        "palaces": {p: get_palace_name(p) for p in team}
    }


@router.get("/team/triangles")
async def get_all_triangles():
    """获取所有三角循环"""
    from milo.taiji_algorithm import get_all_triangles
    
    triangles = get_all_triangles()
    names = ["信息流(159)", "产品流(258)", "开发流(357)", "监控流(456)"]
    
    return {
        "triangles": [
            {"name": names[i], "palaces": list(tri), "flow": get_flow_desc(tri)}
            for i, tri in enumerate(triangles)
        ]
    }


# ==================== 任务分配 API ====================

@router.post("/task/create")
async def create_task(request: CreateTaskRequest):
    """创建并分配任务"""
    init_milo_core()
    
    complexity_map = {2: TaskComplexity.SIMPLE, 3: TaskComplexity.STANDARD,
                     5: TaskComplexity.COMPLEX, 8: TaskComplexity.FULL}
    complexity = complexity_map.get(request.complexity, TaskComplexity.STANDARD)
    
    task = milo_core.create_task(request.title, request.scene, complexity)
    assignments = milo_core.assign_task(task)
    
    return {
        "success": True,
        "task_id": task.task_id,
        "title": task.title,
        "assigned_palaces": task.assigned_palaces,
        "assignments": {
            str(p): {
                "order": info["order"],
                "role": info["role"]
            }
            for p, info in assignments.items()
        }
    }


# ==================== 状态感知 API ====================

@router.post("/sense/state")
async def sense_system_state(request: SenseStateRequest):
    """感知系统状态"""
    init_milo_core()
    
    palace_states = {
        p_id: PalaceState(
            palace_id=p_id,
            name=get_palace_name(p_id),
            load=load,
            status="busy" if load > 0.5 else "idle",
            current_task=None,
            capabilities=get_palace_capabilities(p_id)
        )
        for p_id, load in request.palace_loads.items()
    }
    
    status = milo_core.get_system_status(palace_states)
    
    return {
        "success": True,
        "balance": status["balance"],
        "axis_health": status["axis_health"],
        "support_strength": status["support_strength"],
        "alerts": status["alerts"]
    }


@router.get("/sense/balance")
async def check_balance():
    """检查阴阳平衡"""
    try:
        import requests
        resp = requests.get("http://localhost:8000/api/taiji/palaces", timeout=5)
        data = resp.json()
        palaces = data.get("palaces", {})
        
        palace_loads = {int(k): v.get("load", 0) for k, v in palaces.items()}
        
        init_milo_core()
        
        palace_states = {
            p_id: PalaceState(
                palace_id=p_id,
                name=get_palace_name(p_id),
                load=load,
                status="busy" if load > 0.5 else "idle",
                current_task=None,
                capabilities=get_palace_capabilities(p_id)
            )
            for p_id, load in palace_loads.items()
        }
        
        balance = milo_core.check_balance(palace_states)
        
        return {
            "success": True,
            "balance": balance,
            "status": "balanced" if balance > 0.5 else "imbalanced"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ==================== 进化 API ====================

@router.post("/evolve")
async def evolve_system(request: EvolveRequest):
    """执行系统进化"""
    init_milo_core()
    
    try:
        import requests
        resp = requests.get("http://localhost:8000/api/taiji/palaces", timeout=5)
        data = resp.json()
        palaces = data.get("palaces", {})
        
        palace_loads = {int(k): v.get("load", 0) for k, v in palaces.items()}
        
        system_state = {
            "balance": 0.5,
            "palace_loads": palace_loads,
            "axis_health": 1.0,
            "support_strength": 0.1,
            "capabilities": {},
        }
        
        result = evolution_engine.auto_improve(system_state, request.auto_apply)
        
        return {
            "success": True,
            "evolution_count": result["evolution_count"],
            "bottlenecks": result["bottlenecks"][:5],
            "opportunities": result["opportunities"][:5],
            "actions": result["actions"][:5]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.get("/evolution/status")
async def get_evolution_status():
    """获取进化状态"""
    return {
        "daemon_running": evolution_daemon is not None and evolution_daemon.running,
        "evolution_count": evolution_engine.evolution_count if evolution_engine else 0
    }


@router.post("/evolution/start")
async def start_evolution_daemon(interval: int = 30):
    """启动自动进化守护进程"""
    global evolution_daemon
    
    if evolution_daemon and evolution_daemon.running:
        return {"success": False, "message": "守护进程已在运行"}
    
    evolution_daemon = AutoEvolutionDaemon(interval=interval)
    import threading
    thread = threading.Thread(target=evolution_daemon.run, daemon=True)
    thread.start()
    
    return {"success": True, "message": f"自动进化守护进程已启动，间隔{interval}秒"}


@router.post("/evolution/stop")
async def stop_evolution_daemon():
    """停止自动进化守护进程"""
    global evolution_daemon
    
    if evolution_daemon:
        evolution_daemon.stop()
        return {"success": True, "message": "守护进程已停止"}
    
    return {"success": False, "message": "守护进程未运行"}


# ==================== 辅助函数 ====================

def get_palace_name(palace_id: int) -> str:
    names = {
        1: "数据采集宫", 2: "产品质量宫", 3: "技术团队宫",
        4: "品牌战略宫", 5: "中央控制宫", 6: "物联监控宫",
        7: "法务框架宫", 8: "营销客服宫", 9: "行业生态宫"
    }
    return names.get(palace_id, f"{palace_id}宫")


def get_palace_capabilities(palace_id: int) -> List[str]:
    capabilities = {
        1: ["download", "scrape", "transcribe"],
        2: ["check", "score"],
        3: ["code", "debug"],
        4: ["brand", "strategy"],
        5: ["dispatch", "coordinate"],
        6: ["monitor", "backup"],
        7: ["validate", "audit"],
        8: ["content", "publish"],
        9: ["research", "trend"],
    }
    return capabilities.get(palace_id, [])


def get_flow_desc(triangle: tuple) -> str:
    flows = {
        (1, 5, 9): "数据采集→控制→生态",
        (2, 5, 8): "质量→控制→营销",
        (3, 5, 7): "技术→控制→验收",
        (4, 5, 6): "品牌→监控→控制",
    }
    return flows.get(triangle, "未知流程")