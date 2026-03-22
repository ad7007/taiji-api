"""
太极任务管理系统

遵循 Agent Skills 规范的渐进式披露设计
"""

import os
import json
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from enum import Enum


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    VALIDATING = "validating"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    """任务定义"""
    task_id: str
    title: str
    description: str
    scene: str
    flow: List[int]
    priority: str
    status: str
    permission_level: str
    created_at: str
    updated_at: str
    source: str
    payload: Dict[str, Any]
    current_palace: Optional[int] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class TaskManager:
    """任务管理器"""
    
    def __init__(self, base_path: str = "~/.openclaw/workspace/tasks"):
        self.base_path = os.path.expanduser(base_path)
        self.active_path = os.path.join(self.base_path, "active")
        self.completed_path = os.path.join(self.base_path, "completed")
        
        os.makedirs(self.active_path, exist_ok=True)
        os.makedirs(self.completed_path, exist_ok=True)
    
    def create_task(self, title: str, description: str, scene: str,
                    flow: List[int], source: str = "yuzong",
                    priority: str = "medium", payload: Dict = None) -> Task:
        """创建新任务"""
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        now = datetime.now().isoformat()
        
        task = Task(
            task_id=task_id, title=title, description=description,
            scene=scene, flow=flow, priority=priority,
            status=TaskStatus.PENDING.value, permission_level="L3",
            created_at=now, updated_at=now, source=source,
            payload=payload or {}
        )
        self._save_task(task)
        return task
    
    def _save_task(self, task: Task):
        task_path = os.path.join(self.active_path, task.task_id)
        os.makedirs(task_path, exist_ok=True)
        
        with open(os.path.join(task_path, "status.json"), 'w') as f:
            json.dump(asdict(task), f, indent=2, ensure_ascii=False)
    
    def list_active_tasks(self) -> List[Task]:
        tasks = []
        for tid in os.listdir(self.active_path):
            path = os.path.join(self.active_path, tid, "status.json")
            if os.path.exists(path):
                with open(path) as f:
                    tasks.append(Task(**json.load(f)))
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)


if __name__ == "__main__":
    mgr = TaskManager()
    task = mgr.create_task("测试任务", "这是一个测试", "scene:download", [1, 7, 5])
    print(f"创建任务: {task.task_id}")