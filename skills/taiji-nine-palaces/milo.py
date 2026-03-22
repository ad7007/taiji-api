#!/usr/bin/env python3
"""
米珞快捷入口 - 5宫指挥官专用

为余总提供极简接口，一行代码调用太极系统

使用示例:
    from milo import Milo
    
    milo = Milo()
    
    # 一句话创建任务
    result = milo.do("下载这个抖音视频")
    
    # 查看任务状态
    status = milo.status(result['task_id'])
    
    # 获取待办列表
    todos = milo.todos()
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.task_manager import TaskManager, TaskPriority, TaskStatus
from typing import Dict, List, Any, Optional


class Milo:
    """
    米珞主控类 - 极简接口
    
    这是余总与太极系统交互的主要入口
    """
    
    def __init__(self):
        self.task_manager = TaskManager()
        self.active_tasks: Dict[str, Any] = {}
    
    # ========== 核心方法 ==========
    
    def do(self, description: str, priority: Optional[str] = None) -> Dict[str, Any]:
        """
        一句话创建并启动任务
        
        Args:
            description: 任务描述，自然语言即可
            priority: 优先级 (CRITICAL/HIGH/MEDIUM/LOW)，None则自动推断
        
        Returns:
            任务信息字典
        
        示例:
            milo.do("下载抖音视频")
            milo.do("紧急分析数据", priority="CRITICAL")
        """
        # 解析优先级
        task_priority = None
        if priority:
            try:
                task_priority = TaskPriority[priority.upper()]
            except KeyError:
                pass
        
        # 创建任务
        task = self.task_manager.create_task(description, priority=task_priority)
        
        # 自动启动
        self.task_manager.start_task(task.task_id)
        
        # 记录活跃任务
        self.active_tasks[task.task_id] = {
            "description": task.description,
            "palaces": task.assigned_palaces,
            "created_at": task.created_at.isoformat()
        }
        
        return {
            "task_id": task.task_id,
            "description": task.description,
            "priority": task.priority.name,
            "palaces": task.assigned_palaces,
            "status": "RUNNING",
            "message": f"✅ 任务已创建，分配宫位: {task.assigned_palaces}"
        }
    
    def status(self, task_id: Optional[str] = None) -> Dict[str, Any]:
        """
        查看任务状态
        
        Args:
            task_id: 任务ID，None则返回所有活跃任务
        
        Returns:
            任务状态信息
        """
        if task_id:
            task = self.task_manager.tasks.get(task_id)
            if not task:
                return {"error": "Task not found"}
            
            return {
                "task_id": task.task_id,
                "description": task.description,
                "status": task.status.value,
                "priority": task.priority.name,
                "palaces": task.assigned_palaces,
                "created_at": task.created_at.isoformat(),
                "started_at": task.started_at.isoformat() if task.started_at else None,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None
            }
        else:
            # 返回所有活跃任务
            active = self.task_manager.get_tasks_by_status(TaskStatus.RUNNING)
            pending = self.task_manager.get_tasks_by_status(TaskStatus.PENDING)
            
            return {
                "running": len(active),
                "pending": len(pending),
                "tasks": [
                    {
                        "task_id": t.task_id,
                        "description": t.description[:30] + "..." if len(t.description) > 30 else t.description,
                        "status": t.status.value,
                        "priority": t.priority.name
                    }
                    for t in (active + pending)[:10]  # 最多10个
                ]
            }
    
    def todos(self) -> List[Dict[str, Any]]:
        """
        获取待办任务列表
        
        Returns:
            待办任务列表（按优先级排序）
        """
        pending = self.task_manager.get_tasks_by_status(TaskStatus.PENDING)
        red = self.task_manager.get_tasks_by_status(TaskStatus.RED)
        running = self.task_manager.get_tasks_by_status(TaskStatus.RUNNING)
        
        all_tasks = pending + red + running
        
        # 按优先级和时间排序
        all_tasks.sort(key=lambda t: (-t.priority.value, t.created_at))
        
        return [
            {
                "task_id": t.task_id,
                "description": t.description[:40] + "..." if len(t.description) > 40 else t.description,
                "priority": t.priority.name,
                "status": t.status.value,
                "palaces": t.assigned_palaces
            }
            for t in all_tasks
        ]
    
    def done(self, task_id: str, output: Any = None) -> Dict[str, Any]:
        """
        标记任务完成
        
        Args:
            task_id: 任务ID
            output: 任务输出结果
        
        Returns:
            完成状态
        """
        success = self.task_manager.complete_task(task_id, output)
        
        if success:
            # 从活跃任务中移除
            if task_id in self.active_tasks:
                del self.active_tasks[task_id]
            
            return {
                "task_id": task_id,
                "status": "DELIVERED",
                "message": "✅ 任务已完成并交付"
            }
        else:
            return {"error": "Failed to complete task"}
    
    def cancel(self, task_id: str) -> Dict[str, Any]:
        """
        取消任务
        
        Args:
            task_id: 任务ID
        
        Returns:
            取消状态
        """
        task = self.task_manager.tasks.get(task_id)
        if not task:
            return {"error": "Task not found"}
        
        # 标记为失败
        self.task_manager.fail_task(task_id, "Cancelled by user")
        
        if task_id in self.active_tasks:
            del self.active_tasks[task_id]
        
        return {
            "task_id": task_id,
            "status": "CANCELLED",
            "message": "🚫 任务已取消"
        }
    
    def stats(self) -> Dict[str, Any]:
        """
        获取统计信息
        
        Returns:
            任务统计
        """
        return self.task_manager.get_stats()
    
    def team(self, task_type: str) -> List[int]:
        """
        查看某类任务的默认组队
        
        Args:
            task_type: 任务类型 (video_process/file_download/data_analysis等)
        
        Returns:
            宫位列表
        """
        return self.task_manager.auto_assign_team(task_type)
    
    # ========== 批量操作 ==========
    
    def batch(self, descriptions: List[str]) -> List[Dict[str, Any]]:
        """
        批量创建任务
        
        Args:
            descriptions: 任务描述列表
        
        Returns:
            任务信息列表
        """
        results = []
        for desc in descriptions:
            result = self.do(desc)
            results.append(result)
        return results
    
    def clear(self) -> Dict[str, Any]:
        """
        清空所有已完成任务
        
        Returns:
            清理结果
        """
        completed = [
            t.task_id for t in self.task_manager.tasks.values()
            if t.status in [TaskStatus.DELIVERED, TaskStatus.FAILED]
        ]
        
        for task_id in completed:
            del self.task_manager.tasks[task_id]
        
        self.task_manager._save_tasks()
        
        return {
            "cleared": len(completed),
            "message": f"🗑️ 已清理 {len(completed)} 个已完成任务"
        }


# ========== 全局快捷函数 ==========

_milo_instance = None

def get_milo() -> Milo:
    """获取全局米珞实例"""
    global _milo_instance
    if _milo_instance is None:
        _milo_instance = Milo()
    return _milo_instance


# 快捷函数，可以直接使用
def do(description: str, priority: Optional[str] = None) -> Dict[str, Any]:
    """快捷函数：创建任务"""
    return get_milo().do(description, priority)

def status(task_id: Optional[str] = None) -> Dict[str, Any]:
    """快捷函数：查看状态"""
    return get_milo().status(task_id)

def todos() -> List[Dict[str, Any]]:
    """快捷函数：获取待办"""
    return get_milo().todos()

def done(task_id: str, output: Any = None) -> Dict[str, Any]:
    """快捷函数：完成任务"""
    return get_milo().done(task_id, output)


# ========== 测试 ==========

if __name__ == "__main__":
    print("=== 米珞快捷入口测试 ===\n")
    
    # 测试1: 创建任务
    print("1. 创建任务:")
    result = do("下载抖音视频并总结")
    print(f"   {result['message']}")
    print(f"   任务ID: {result['task_id']}")
    
    # 测试2: 查看状态
    print("\n2. 查看状态:")
    status_info = status()
    print(f"   进行中: {status_info['running']}")
    print(f"   待处理: {status_info['pending']}")
    
    # 测试3: 待办列表
    print("\n3. 待办列表:")
    todo_list = todos()
    for t in todo_list[:3]:
        print(f"   [{t['priority']}] {t['description']}")
    
    # 测试4: 统计
    print("\n4. 统计信息:")
    stats_info = get_milo().stats()
    print(f"   总任务: {stats_info['total_tasks']}")
    print(f"   完成率: {stats_info['completion_rate']:.1%}")
    
    # 测试5: 查看组队
    print("\n5. 默认组队:")
    team_info = get_milo().team("video_process")
    print(f"   视频处理: {team_info}")
    
    print("\n=== 米珞已就绪，等待余总指令 ===")
