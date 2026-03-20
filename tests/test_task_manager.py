#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务管理系统测试
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.task_manager import (
    get_task_manager, TaskStatus, TaskPriority, TaskSource
)


def test_create_task():
    """测试创建任务"""
    tm = get_task_manager()
    
    task = tm.create_task(
        title="测试任务",
        palace_id=3,
        priority=TaskPriority.HIGH,
        source=TaskSource.SELF
    )
    
    assert task.task_id.startswith("task_")
    assert task.title == "测试任务"
    assert task.assigned_palace == 3
    assert task.status == TaskStatus.PENDING
    
    print("✅ 创建任务测试通过")


def test_task_lifecycle():
    """测试任务生命周期"""
    tm = get_task_manager()
    
    # 创建
    task = tm.create_task("生命周期测试", 5)
    assert task.status == TaskStatus.PENDING
    
    # 开始
    started = tm.start_task(task.task_id)
    assert started.status == TaskStatus.IN_PROGRESS
    assert started.started_time is not None
    
    # 完成
    completed = tm.complete_task(task.task_id, "完成")
    assert completed.status == TaskStatus.COMPLETED
    assert completed.completed_time is not None
    
    print("✅ 任务生命周期测试通过")


def test_queue_alive():
    """测试队列存活"""
    tm = get_task_manager()
    
    # 确保所有宫位活着
    tm.ensure_all_alive()
    
    for p_id, queue in tm.queues.items():
        assert queue.is_alive(), f"{p_id}宫应该活着"
    
    print("✅ 队列存活测试通过")


def test_system_status():
    """测试系统状态"""
    tm = get_task_manager()
    tm.ensure_all_alive()
    
    status = tm.get_system_status()
    
    assert status["alive_palaces"] == 9
    assert status["status"] == "alive"
    assert status["total_pending_tasks"] > 0
    
    print("✅ 系统状态测试通过")


def test_persistence():
    """测试持久化"""
    tm = get_task_manager()
    
    # 创建任务
    task = tm.create_task("持久化测试", 1)
    
    # 保存
    tm.save()
    
    # 重新加载
    tm2 = get_task_manager()
    tm2.load()
    
    # 验证
    status = tm2.get_system_status()
    assert status["total_pending_tasks"] > 0
    
    print("✅ 持久化测试通过")


if __name__ == "__main__":
    print("=== 任务管理系统测试 ===\n")
    
    test_create_task()
    test_task_lifecycle()
    test_queue_alive()
    test_system_status()
    test_persistence()
    
    print("\n✅ 所有测试通过！")