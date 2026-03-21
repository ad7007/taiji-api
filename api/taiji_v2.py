"""
太极九宫API v1.1.0
基于本地数据库的完整太极系统

功能：
- 九宫状态查询
- 48线程感知扫描
- 任务分配与管理
- 自动组队
- 四层感知决策
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
import sys
sys.path.insert(0, '/root/taiji-api-v2/core/local')
from taiji_db_client import TaijiDatabase

router = APIRouter(prefix="/api/taiji", tags=["太极九宫"])

# 初始化数据库
db = TaijiDatabase('/root/taiji-api-v2/data/taiji_database.json')


# ==================== 响应模型 ====================

class TaskAssignRequest(BaseModel):
    palace_id: int
    task_type: str
    description: str
    priority: str = "medium"


# ==================== 九宫状态 ====================

@router.get("/palaces")
async def get_all_palaces():
    """获取所有宫位状态"""
    return {
        "success": True,
        "data": db.get_all_palaces()
    }


@router.get("/palaces/{palace_id}")
async def get_palace(palace_id: int):
    """获取指定宫位详情"""
    palace = db.get_palace(palace_id)
    if not palace:
        raise HTTPException(status_code=404, detail=f"宫位 {palace_id} 不存在")
    return {
        "success": True,
        "data": palace
    }


# ==================== 统计信息 ====================

@router.get("/stats")
async def get_statistics():
    """获取系统统计"""
    return {
        "success": True,
        "data": db.get_statistics()
    }


# ==================== 48线程感知 ====================

@router.get("/scan")
async def scan_all_threads(text: Optional[str] = ""):
    """扫描48线程状态"""
    return {
        "success": True,
        "data": db.scan_all_threads(text)
    }


@router.get("/palaces/{palace_id}/scan")
async def scan_palace_yao(palace_id: int, text: Optional[str] = ""):
    """扫描某宫6爻状态"""
    return {
        "success": True,
        "data": db.scan_palace_yao(palace_id, text)
    }


# ==================== 旋转决策 ====================

@router.get("/rotate")
async def get_rotation_decision(text: Optional[str] = ""):
    """获取旋转决策"""
    return {
        "success": True,
        "data": db.get_rotation_decision(text)
    }


# ==================== 任务管理 ====================

@router.get("/tasks")
async def get_all_pending_tasks():
    """获取所有待办任务"""
    return {
        "success": True,
        "data": db.get_all_pending_tasks()
    }


@router.post("/tasks/assign")
async def assign_task(request: TaskAssignRequest):
    """分配任务给宫位"""
    result = db.assign_task(
        palace_id=request.palace_id,
        task_type=request.task_type,
        description=request.description,
        priority=request.priority
    )
    return {
        "success": True,
        "data": result
    }


@router.put("/tasks/{palace_id}/{task_id}")
async def update_task_status(palace_id: int, task_id: str, status: str, note: str = ""):
    """更新任务状态"""
    db.update_task_status(palace_id, task_id, status, note)
    return {
        "success": True,
        "message": f"任务 {task_id} 已更新为 {status}"
    }


# ==================== 自动组队 ====================

@router.post("/team/build")
async def build_team(text: str):
    """根据任务描述自动组队"""
    return {
        "success": True,
        "data": db.build_team(text)
    }


@router.get("/scenes")
async def get_task_scenes():
    """获取所有任务场景"""
    return {
        "success": True,
        "data": db.get_task_scenes()
    }


# ==================== 汇报系统 ====================

@router.get("/reports")
async def get_palace_reports(palace_id: Optional[int] = None, limit: int = 20):
    """获取宫位汇报"""
    return {
        "success": True,
        "data": db.get_palace_reports(palace_id, limit)
    }


# ==================== 技能查询 ====================

@router.get("/skills")
async def list_all_skills():
    """列出所有技能"""
    return {
        "success": True,
        "data": db.list_all_skills()
    }


@router.get("/skills/{skill_name}")
async def get_skill_info(skill_name: str):
    """获取技能详情"""
    info = db.get_skill_info(skill_name)
    if not info:
        raise HTTPException(status_code=404, detail=f"技能 {skill_name} 不存在")
    return {
        "success": True,
        "data": info
    }


# ==================== 意识系统 ====================

@router.get("/consciousness")
async def get_consciousness_system():
    """获取意识系统配置"""
    return {
        "success": True,
        "data": db.get_consciousness_system()
    }


@router.get("/threads")
async def get_thread_mapping():
    """获取48线程映射"""
    return {
        "success": True,
        "data": db.get_thread_mapping()
    }