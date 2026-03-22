#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太极任务管理系统

核心功能：
1. 任务创建、分配、追踪
2. 任务状态管理（待办、进行中、完成）
3. 任务优先级和来源
4. 自动任务生成
5. 任务统计和持久化

生命原则：
- 任务队列 = 生命线
- 空 = 死，非空 = 活
- 系统永不死亡
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime
import json
import os


# ==================== 枚举定义 ====================

class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"        # 待办
    IN_PROGRESS = "in_progress" # 进行中
    COMPLETED = "completed"     # 已完成
    BLOCKED = "blocked"         # 阻塞


class TaskPriority(Enum):
    """任务优先级"""
    CRITICAL = 0  # 紧急
    HIGH = 1      # 高
    MEDIUM = 2    # 中
    LOW = 3       # 低


class TaskSource(Enum):
    """任务来源"""
    YUZONG = "yuzong"           # 余总指令
    TAIJI_MD = "taiji_md"       # Taiji.md衍生
    EXPLORE = "explore"         # 探索发现
    SELF = "self"               # 自我完善
    AUTO = "auto"               # 自动生成


# ==================== 任务定义 ====================

@dataclass
class Task:
    """任务"""
    task_id: str
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    source: TaskSource = TaskSource.SELF
    
    # 分配
    assigned_palace: Optional[int] = None
    assigned_time: Optional[str] = None
    
    # 时间
    created_time: str = field(default_factory=lambda: datetime.now().isoformat())
    started_time: Optional[str] = None
    completed_time: Optional[str] = None
    
    # 结果
    result: Optional[str] = None
    notes: List[str] = field(default_factory=list)
    
    def start(self):
        """开始任务"""
        self.status = TaskStatus.IN_PROGRESS
        self.started_time = datetime.now().isoformat()
    
    def complete(self, result: str = ""):
        """完成任务"""
        self.status = TaskStatus.COMPLETED
        self.completed_time = datetime.now().isoformat()
        self.result = result
    
    def block(self, reason: str):
        """阻塞任务"""
        self.status = TaskStatus.BLOCKED
        self.notes.append(f"阻塞: {reason}")
    
    def add_note(self, note: str):
        """添加备注"""
        self.notes.append(f"[{datetime.now().isoformat()}] {note}")


# ==================== 任务队列 ====================

@dataclass
class TaskQueue:
    """
    任务队列
    
    每个宫位都有自己的任务队列
    """
    palace_id: int
    palace_name: str
    tasks: List[Task] = field(default_factory=list)
    
    def add_task(self, task: Task):
        """添加任务"""
        task.assigned_palace = self.palace_id
        task.assigned_time = datetime.now().isoformat()
        self.tasks.append(task)
        self._sort_tasks()
    
    def _sort_tasks(self):
        """按优先级排序"""
        self.tasks.sort(key=lambda t: t.priority.value)
    
    def get_next_task(self) -> Optional[Task]:
        """获取下一个待办任务"""
        for task in self.tasks:
            if task.status == TaskStatus.PENDING:
                return task
        return None
    
    def get_active_task(self) -> Optional[Task]:
        """获取当前进行中的任务"""
        for task in self.tasks:
            if task.status == TaskStatus.IN_PROGRESS:
                return task
        return None
    
    def get_pending_count(self) -> int:
        """获取待办任务数"""
        return sum(1 for t in self.tasks if t.status == TaskStatus.PENDING)
    
    def get_completed_count(self) -> int:
        """获取已完成任务数"""
        return sum(1 for t in self.tasks if t.status == TaskStatus.COMPLETED)
    
    def is_alive(self) -> bool:
        """是否活着（有待办或进行中任务）"""
        return any(t.status in [TaskStatus.PENDING, TaskStatus.IN_PROGRESS] for t in self.tasks)
    
    def ensure_alive(self, default_task: str = "完善自己"):
        """确保活着 - 如果没有任务，自动生成"""
        if not self.is_alive():
            auto_task = Task(
                task_id=f"auto_{self.palace_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                title=default_task,
                source=TaskSource.AUTO,
                priority=TaskPriority.LOW
            )
            self.add_task(auto_task)
            return auto_task
        return None


# ==================== 任务管理系统 ====================

class TaijiTaskManager:
    """
    太极任务管理系统
    
    管理9个宫位的所有任务
    """
    
    def __init__(self, state_dir: str = "state"):
        self.state_dir = state_dir
        self.queues: Dict[int, TaskQueue] = {}
        self.task_counter = 0
        self.created_time = datetime.now().isoformat()
        
        # 初始化9个宫位的任务队列
        palace_names = {
            1: "数据采集", 2: "物联产品", 3: "技术团队",
            4: "品牌战略", 5: "中央控制", 6: "质量监控",
            7: "法务框架", 8: "营销客服", 9: "行业生态"
        }
        
        for p_id, p_name in palace_names.items():
            self.queues[p_id] = TaskQueue(palace_id=p_id, palace_name=p_name)
        
        # 确保目录存在
        os.makedirs(state_dir, exist_ok=True)
    
    # ==================== 任务创建 ====================
    
    def create_task(self, title: str, palace_id: int, 
                   priority: TaskPriority = TaskPriority.MEDIUM,
                   source: TaskSource = TaskSource.SELF,
                   description: str = "") -> Task:
        """创建任务"""
        self.task_counter += 1
        task_id = f"task_{self.task_counter:04d}"
        
        task = Task(
            task_id=task_id,
            title=title,
            description=description,
            priority=priority,
            source=source
        )
        
        self.queues[palace_id].add_task(task)
        return task
    
    def create_tasks_batch(self, tasks: List[Dict[str, Any]]):
        """批量创建任务"""
        for t in tasks:
            self.create_task(
                title=t["title"],
                palace_id=t["palace_id"],
                priority=t.get("priority", TaskPriority.MEDIUM),
                source=t.get("source", TaskSource.SELF),
                description=t.get("description", "")
            )
    
    # ==================== 任务操作 ====================
    
    def start_task(self, task_id: str) -> Optional[Task]:
        """开始任务"""
        for queue in self.queues.values():
            for task in queue.tasks:
                if task.task_id == task_id:
                    task.start()
                    return task
        return None
    
    def complete_task(self, task_id: str, result: str = "") -> Optional[Task]:
        """完成任务"""
        for queue in self.queues.values():
            for task in queue.tasks:
                if task.task_id == task_id:
                    task.complete(result)
                    # 完成后确保队列不空
                    queue.ensure_alive()
                    return task
        return None
    
    # ==================== 状态查询 ====================
    
    def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        alive_count = sum(1 for q in self.queues.values() if q.is_alive())
        
        total_pending = sum(q.get_pending_count() for q in self.queues.values())
        total_completed = sum(q.get_completed_count() for q in self.queues.values())
        
        return {
            "alive_palaces": alive_count,
            "total_palaces": 9,
            "status": "alive" if alive_count > 0 else "dead",
            "total_pending_tasks": total_pending,
            "total_completed_tasks": total_completed,
            "total_tasks": sum(len(q.tasks) for q in self.queues.values()),
        }
    
    def get_all_queues_status(self) -> Dict[int, Dict]:
        """获取所有队列状态"""
        return {
            p_id: {
                "palace_name": q.palace_name,
                "pending": q.get_pending_count(),
                "completed": q.get_completed_count(),
                "is_alive": q.is_alive(),
                "next_task": q.get_next_task().title if q.get_next_task() else None,
                "active_task": q.get_active_task().title if q.get_active_task() else None,
            }
            for p_id, q in self.queues.items()
        }
    
    def get_next_tasks(self) -> Dict[int, Optional[str]]:
        """获取所有宫位的下一个任务"""
        return {
            p_id: q.get_next_task().title if q.get_next_task() else None
            for p_id, q in self.queues.items()
        }
    
    # ==================== 确保活着 ====================
    
    def ensure_all_alive(self):
        """确保所有宫位都活着"""
        default_tasks = {
            1: "扫描外部数据源",
            2: "优化产品体验",
            3: "完善系统代码",
            4: "分析市场趋势",
            5: "协调各宫运转",
            6: "监控系统健康",
            7: "审查系统合规",
            8: "生成知识内容",
            9: "研究行业生态",
        }
        
        for p_id, q in self.queues.items():
            q.ensure_alive(default_tasks.get(p_id, "完善自己"))
    
    # ==================== 持久化 ====================
    
    def save(self, filename: str = "task_manager.json"):
        """保存状态"""
        data = {
            "task_counter": self.task_counter,
            "created_time": self.created_time,
            "saved_time": datetime.now().isoformat(),
            "queues": {}
        }
        
        for p_id, q in self.queues.items():
            data["queues"][str(p_id)] = {
                "palace_name": q.palace_name,
                "tasks": [
                    {
                        "task_id": t.task_id,
                        "title": t.title,
                        "status": t.status.value,
                        "priority": t.priority.value,
                        "source": t.source.value,
                        "created_time": t.created_time,
                        "result": t.result,
                    }
                    for t in q.tasks
                ]
            }
        
        filepath = os.path.join(self.state_dir, filename)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load(self, filename: str = "task_manager.json"):
        """加载状态"""
        filepath = os.path.join(self.state_dir, filename)
        if not os.path.exists(filepath):
            return
        
        with open(filepath, "r") as f:
            data = json.load(f)
        
        self.task_counter = data.get("task_counter", 0)
        self.created_time = data.get("created_time", datetime.now().isoformat())
        
        # 恢复任务
        for p_id_str, q_data in data.get("queues", {}).items():
            p_id = int(p_id_str)
            queue = self.queues[p_id]
            
            for t_data in q_data.get("tasks", []):
                task = Task(
                    task_id=t_data["task_id"],
                    title=t_data["title"],
                    status=TaskStatus(t_data["status"]),
                    priority=TaskPriority(t_data["priority"]),
                    source=TaskSource(t_data["source"]),
                    created_time=t_data["created_time"],
                    result=t_data.get("result"),
                )
                queue.tasks.append(task)


# ==================== 全局实例 ====================

_task_manager: Optional[TaijiTaskManager] = None

def get_task_manager() -> TaijiTaskManager:
    """获取全局任务管理器"""
    global _task_manager
    if _task_manager is None:
        _task_manager = TaijiTaskManager()
        _task_manager.load()
    return _task_manager


# ==================== 测试 ====================

if __name__ == "__main__":
    print("=== 太极任务管理系统测试 ===\n")
    
    tm = TaijiTaskManager(state_dir="state")
    
    # 创建任务
    print("【创建任务】")
    tm.create_task("实现24线程协议", 3, TaskPriority.HIGH, TaskSource.TAIJI_MD)
    tm.create_task("分析市场机会", 4, TaskPriority.MEDIUM, TaskSource.EXPLORE)
    tm.create_task("协调各宫运转", 5, TaskPriority.HIGH, TaskSource.SELF)
    
    # 查看状态
    print("\n【系统状态】")
    status = tm.get_system_status()
    print(f"活着的宫位: {status['alive_palaces']}/9")
    print(f"待办任务: {status['total_pending_tasks']}")
    print(f"状态: {status['status']}")
    
    # 确保所有宫位活着
    print("\n【确保所有宫位活着】")
    tm.ensure_all_alive()
    
    # 查看各宫任务
    print("\n【各宫任务队列】")
    for p_id, q_status in tm.get_all_queues_status().items():
        status_icon = "🟢" if q_status["is_alive"] else "🔴"
        print(f"{p_id}宫 {q_status['palace_name']}: {status_icon}")
        print(f"   待办: {q_status['pending']} | 完成: {q_status['completed']}")
        if q_status["next_task"]:
            print(f"   下一个: {q_status['next_task']}")
    
    # 保存
    tm.save()
    print("\n✅ 状态已保存")