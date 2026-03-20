"""
太极九宫核心模块

包含:
- governance: 管控体系（RBAC + L0-L4权限）
- aware: 感知系统（6种触发器）
- relationship: 九宫关系图
- taiji_algorithm: 太极算法（相生相克、N宫组合）
- milo_core: 米珞核心能力（组队、分配、感知）
- taiji_evolution: 自我进化引擎
- auto_evolve: 自动进化守护进程
"""

from .governance import (
    PermissionLevel, PermissionChecker,
    ApprovalManager, AuditManager, check_permission
)
from .aware import AwareSystem, setup_default_triggers
from .relationship import RelationshipGraph, PALACES, SCENE_COLLABORATION
from .taiji_algorithm import (
    get_central_axis, get_support_triangle, get_tech_triangle,
    get_monitor_triangle, get_all_triangles, get_generation_path,
    get_control_relations, auto_group_by_mode
)
from .milo_core import MiloCore, TaskComplexity
from .taiji_evolution import SelfEvolution
from .auto_evolve import AutoEvolutionDaemon

__all__ = [
    'PermissionLevel', 'PermissionChecker', 'check_permission',
    'AwareSystem', 'setup_default_triggers',
    'RelationshipGraph', 'PALACES', 'SCENE_COLLABORATION',
    'get_central_axis', 'get_support_triangle', 'get_tech_triangle',
    'get_monitor_triangle', 'get_all_triangles',
    'get_generation_path', 'get_control_relations', 'auto_group_by_mode',
    'MiloCore', 'TaskComplexity',
    'SelfEvolution', 'AutoEvolutionDaemon',
    # 意识系统
    'TaijiConsciousness', 'get_consciousness',
    'TaijiGoals', 'GoalLevel', 'RotationDirection',
    'EnergyLevel', 'SystemHealth',
    # 任务管理
    'TaijiTaskManager', 'get_task_manager', 'Task', 'TaskStatus', 'TaskPriority', 'TaskSource',
]
