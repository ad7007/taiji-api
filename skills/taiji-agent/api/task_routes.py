#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务管理 API 路由
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.task_manager import (
    get_task_manager, TaskStatus, TaskPriority, TaskSource
)
from core.daily_report import generate_daily_report, generate_daily_report_markdown
from core.perception_action_loop import get_loop

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


# ==================== 请求模型 ====================

class CreateTaskRequest(BaseModel):
    """创建任务请求"""
    title: str
    palace_id: int
    priority: str = "medium"
    source: str = "self"
    description: str = ""


class TaskActionRequest(BaseModel):
    """任务操作请求"""
    task_id: str
    result: str = ""


# ==================== 端点 ====================

@router.get("/status")
async def get_status():
    """获取任务系统状态"""
    tm = get_task_manager()
    return tm.get_system_status()


@router.get("/queues")
async def get_all_queues():
    """获取所有宫位任务队列状态"""
    tm = get_task_manager()
    return tm.get_all_queues_status()


@router.get("/next")
async def get_next_tasks():
    """获取所有宫位的下一个任务"""
    tm = get_task_manager()
    return tm.get_next_tasks()


@router.post("/create")
async def create_task(request: CreateTaskRequest):
    """创建任务"""
    tm = get_task_manager()
    
    priority_map = {
        "critical": TaskPriority.CRITICAL,
        "high": TaskPriority.HIGH,
        "medium": TaskPriority.MEDIUM,
        "low": TaskPriority.LOW,
    }
    source_map = {
        "yuzong": TaskSource.YUZONG,
        "taiji_md": TaskSource.TAIJI_MD,
        "explore": TaskSource.EXPLORE,
        "self": TaskSource.SELF,
        "auto": TaskSource.AUTO,
    }
    
    priority = priority_map.get(request.priority.lower(), TaskPriority.MEDIUM)
    source = source_map.get(request.source.lower(), TaskSource.SELF)
    
    if request.palace_id not in range(1, 10):
        raise HTTPException(status_code=400, detail="palace_id must be 1-9")
    
    task = tm.create_task(
        title=request.title,
        palace_id=request.palace_id,
        priority=priority,
        source=source,
        description=request.description
    )
    
    tm.save()
    
    return {
        "success": True,
        "task_id": task.task_id,
        "title": task.title,
        "palace_id": task.assigned_palace,
    }


@router.post("/start")
async def start_task(request: TaskActionRequest):
    """开始任务"""
    tm = get_task_manager()
    task = tm.start_task(request.task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    tm.save()
    
    return {
        "success": True,
        "task_id": task.task_id,
        "status": task.status.value,
    }


@router.post("/complete")
async def complete_task(request: TaskActionRequest):
    """完成任务"""
    tm = get_task_manager()
    task = tm.complete_task(request.task_id, request.result)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    tm.save()
    
    return {
        "success": True,
        "task_id": task.task_id,
        "status": task.status.value,
    }


@router.post("/ensure-alive")
async def ensure_all_alive():
    """确保所有宫位活着"""
    tm = get_task_manager()
    tm.ensure_all_alive()
    tm.save()
    
    return {
        "success": True,
        "status": tm.get_system_status(),
    }


# ==================== 日报端点 ====================

@router.get("/daily-report")
async def get_daily_report():
    """获取米珞日报（JSON格式）"""
    return generate_daily_report()


@router.get("/daily-report/markdown")
async def get_daily_report_markdown():
    """获取米珞日报（Markdown格式）"""
    return {"markdown": generate_daily_report_markdown()}


# ==================== 感知决策循环端点 ====================

@router.post("/loop/run")
async def run_perception_loop():
    """执行一次感知-决策-执行循环"""
    loop = get_loop()
    result = loop.run_once()
    return result


@router.get("/loop/status")
async def get_loop_status():
    """获取循环状态"""
    tm = get_task_manager()
    status = tm.get_system_status()
    
    import subprocess
    try:
        result = subprocess.run(['free', '-m'], capture_output=True, text=True, timeout=5)
        mem_line = [l for l in result.stdout.split('\n') if 'Mem:' in l][0]
        parts = mem_line.split()
        avail_mem = int(parts[6]) if len(parts) > 6 else int(parts[3])
    except:
        avail_mem = 0
    
    return {
        "tasks": status,
        "memory_available_mb": avail_mem,
        "status": "alive" if status["alive_palaces"] == 9 else "dead",
    }