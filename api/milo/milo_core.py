"""
米珞核心能力：组队、分配任务、感知状态

基于太极九宫组合算法
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

# 导入太极算法
import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/taiji-nine-palaces/core')
from taiji_algorithm import (
    auto_group_by_mode,
    get_generation_path,
    get_control_relations,
    get_central_axis,
    get_support_triangle,
    YANG_PALACES,
    YIN_PALACES,
    PALACE_ELEMENT,
)


# ==================== 数据结构 ====================

class TaskComplexity(Enum):
    """任务复杂度"""
    SIMPLE = 2      # 2宫模式
    STANDARD = 3    # 3宫模式
    COMPLEX = 5     # 5宫模式
    FULL = 8        # 8宫模式


@dataclass
class Task:
    """任务定义"""
    task_id: str
    title: str
    description: str
    complexity: TaskComplexity
    scene: str
    assigned_palaces: List[int]
    current_flow_index: int = 0
    status: Dict[int, str] = None  # {宫位: 状态}
    
    def __post_init__(self):
        if self.status is None:
            self.status = {p: "pending" for p in self.assigned_palaces}


@dataclass
class PalaceState:
    """宫位状态"""
    palace_id: int
    name: str
    load: float
    status: str
    current_task: Optional[str]
    capabilities: List[str]


# ==================== 组队能力 ====================

class TeamBuilder:
    """组队引擎"""
    
    def __init__(self):
        self.palace_names = {
            1: "数据采集宫",
            2: "产品质量宫",
            3: "技术团队宫",
            4: "品牌战略宫",
            5: "中央控制宫",
            6: "物联监控宫",
            7: "法务框架宫",
            8: "营销客服宫",
            9: "行业生态宫",
        }
    
    def build_team(self, scene: str, complexity: TaskComplexity = TaskComplexity.STANDARD) -> List[int]:
        """
        根据场景和复杂度自动组队
        
        Args:
            scene: 场景标识
            complexity: 任务复杂度
        
        Returns:
            组队宫位列表
        """
        # 基于复杂度选择组队模式
        groups = auto_group_by_mode(complexity.value)
        
        # 基于场景选择最合适的组队
        best_group = self._select_best_group(scene, groups)
        
        return best_group
    
    def _select_best_group(self, scene: str, groups: List[List[int]]) -> List[int]:
        """选择最适合场景的组队"""
        
        # 场景关键词到宫位的映射
        scene_keywords = {
            "download": 1, "scrape": 1, "transcribe": 1,
            "quality": 2, "check": 2,
            "code": 3, "develop": 3, "debug": 3,
            "brand": 4, "strategy": 4, "competitive": 4,
            "monitor": 6, "backup": 6,
            "validate": 7, "approve": 7,
            "content": 8, "publish": 8,
            "research": 9, "trend": 9,
        }
        
        # 找到场景对应的核心宫位
        core_palace = 5  # 默认中宫
        for keyword, palace in scene_keywords.items():
            if keyword in scene.lower():
                core_palace = palace
                break
        
        # 找到包含核心宫位的组队
        for group in groups:
            if core_palace in group:
                return group
        
        # 默认返回第一个组队
        return groups[0] if groups else [5]
    
    def form_triangle(self, task_type: str) -> List[int]:
        """
        形成三角循环组队
        
        三角类型:
        - 159: 数据→控制→生态（信息流）
        - 258: 质量→控制→营销（产品流）
        - 357: 技术→控制→验收（开发流）
        - 456: 品牌→监控→中宫（监控流）
        """
        triangles = {
            "data_flow": [1, 5, 9],    # 信息流
            "product_flow": [2, 5, 8],  # 产品流
            "dev_flow": [3, 5, 7],      # 开发流
            "monitor_flow": [4, 5, 6],  # 监控流
        }
        
        return triangles.get(task_type, [1, 5, 9])
    
    def form_yin_yang_pair(self, task_type: str) -> List[int]:
        """
        形成阴阳配对
        
        阴阳互补:
        - (3, 4): 技术+品牌
        - (1, 8): 采集+营销
        - (6, 9): 监控+生态
        """
        pairs = {
            "tech_brand": [3, 4],
            "collect_marketing": [1, 8],
            "monitor_ecology": [6, 9],
            "quality_legal": [2, 7],
        }
        
        return pairs.get(task_type, [1, 9])


# ==================== 任务分配能力 ====================

class TaskDispatcher:
    """任务分配引擎"""
    
    def __init__(self):
        self.builder = TeamBuilder()
        self.generation_cycle = get_generation_path()
        self.control_relations = get_control_relations()
    
    def dispatch(self, task: Task) -> Dict[int, Any]:
        """
        分配任务到各宫位
        
        基于相生路径分配任务流转
        """
        assignments = {}
        
        # 获取组队
        team = task.assigned_palaces
        
        # 基于相生路径确定执行顺序
        ordered_team = self._order_by_generation(team)
        
        # 分配子任务
        for i, palace in enumerate(ordered_team):
            assignments[palace] = {
                "order": i + 1,
                "role": self._get_role(i, len(ordered_team)),
                "input_from": ordered_team[i-1] if i > 0 else None,
                "output_to": ordered_team[i+1] if i < len(ordered_team) - 1 else None,
            }
        
        return assignments
    
    def _order_by_generation(self, palaces: List[int]) -> List[int]:
        """
        按相生路径排序宫位
        
        相生路径: 3→6→9→7→4→8→3
        """
        # 中宫总是第一个
        if 5 in palaces:
            ordered = [5]
            others = [p for p in palaces if p != 5]
        else:
            ordered = []
            others = palaces.copy()
        
        # 按相生顺序排列其他宫位
        for p in self.generation_cycle:
            if p in others:
                ordered.append(p)
        
        # 添加未在相生路径中的宫位
        for p in others:
            if p not in ordered:
                ordered.append(p)
        
        return ordered
    
    def _get_role(self, index: int, total: int) -> str:
        """获取宫位在任务中的角色"""
        if total == 2:
            return ["执行", "验收"][index]
        elif total == 3:
            return ["启动", "执行", "验收"][index]
        else:
            roles = ["启动", "处理", "分析", "验收", "交付"]
            return roles[min(index, len(roles) - 1)]
    
    def create_balance_check(self, task: Task) -> Dict[int, str]:
        """
        创建制衡检查点
        
        基于相克关系
        """
        checks = {}
        
        for p1, p2, desc in self.control_relations:
            if p1 in task.assigned_palaces and p2 in task.assigned_palaces:
                checks[f"{p1}_{p2}"] = {
                    "type": desc,
                    "checker": p2,  # 被克方检查
                    "executor": p1,  # 执行方
                }
        
        return checks


# ==================== 状态感知能力 ====================

class StateSensor:
    """状态感知引擎"""
    
    def __init__(self):
        self.central_axis = get_central_axis()      # (1, 5, 9)
        self.support_triangle = get_support_triangle()  # (2, 5, 8)
    
    def sense_system_state(self, palace_states: Dict[int, PalaceState]) -> Dict[str, Any]:
        """
        感知整个系统状态
        
        Returns:
            {
                "balance": 阴阳平衡度,
                "axis_health": 中轴健康度,
                "support_strength": 支撑强度,
                "alerts": 告警列表
            }
        """
        # 计算阴阳平衡
        yang_load = sum(p.load for p in palace_states.values() if p.palace_id in YANG_PALACES)
        yin_load = sum(p.load for p in palace_states.values() if p.palace_id in YIN_PALACES)
        balance = self._calc_balance(yang_load, yin_load)
        
        # 中轴健康度（159中轴）
        axis_health = self._calc_axis_health(palace_states)
        
        # 支撑强度（258三角）
        support_strength = self._calc_support_strength(palace_states)
        
        # 告警
        alerts = self._detect_alerts(palace_states, balance)
        
        return {
            "balance": balance,
            "axis_health": axis_health,
            "support_strength": support_strength,
            "alerts": alerts,
        }
    
    def _calc_balance(self, yang_load: float, yin_load: float) -> float:
        """
        计算阴阳平衡度
        
        返回 0-1，越接近 1 越平衡
        """
        if yang_load + yin_load == 0:
            return 1.0
        
        ratio = min(yang_load, yin_load) / max(yang_load, yin_load)
        return ratio
    
    def _calc_axis_health(self, palace_states: Dict[int, PalaceState]) -> float:
        """
        计算中轴健康度
        
        159中轴: 数据采集→控制→生态
        """
        axis_palaces = list(self.central_axis)
        loads = [palace_states[p].load for p in axis_palaces if p in palace_states]
        
        if not loads:
            return 1.0
        
        # 中轴宫位负载应相对均衡
        avg_load = sum(loads) / len(loads)
        variance = sum((l - avg_load) ** 2 for l in loads) / len(loads)
        
        health = 1.0 - min(variance, 1.0)
        return health
    
    def _calc_support_strength(self, palace_states: Dict[int, PalaceState]) -> float:
        """
        计算支撑强度
        
        258三角: 质量→控制→营销
        """
        support_palaces = list(self.support_triangle)
        loads = [palace_states[p].load for p in support_palaces if p in palace_states]
        
        if not loads:
            return 0.0
        
        # 支撑强度 = 平均活跃度
        strength = sum(loads) / len(loads)
        return strength
    
    def _detect_alerts(self, palace_states: Dict[int, PalaceState], balance: float) -> List[str]:
        """检测告警"""
        alerts = []
        
        # 阴阳失衡告警
        if balance < 0.3:
            alerts.append("阴阳严重失衡")
        elif balance < 0.5:
            alerts.append("阴阳轻度失衡")
        
        # 宫位过载告警
        for p_id, state in palace_states.items():
            if state.load > 0.8:
                alerts.append(f"{p_id}宫({state.name})过载: {state.load:.1%}")
        
        # 宫位空闲告警
        idle_palaces = [p for p, s in palace_states.items() if s.load == 0 and p != 5]
        if len(idle_palaces) > 4:
            alerts.append(f"过多宫位闲置: {idle_palaces}")
        
        return alerts
    
    def sense_task_progress(self, task: Task) -> Dict[str, Any]:
        """
        感知任务进度
        """
        total = len(task.assigned_palaces)
        completed = sum(1 for s in task.status.values() if s == "completed")
        in_progress = sum(1 for s in task.status.values() if s == "in_progress")
        
        return {
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "pending": total - completed - in_progress,
            "progress": completed / total if total > 0 else 0,
            "current_stage": task.current_flow_index,
        }


# ==================== 米珞核心能力 ====================

class MiloCore:
    """米珞核心能力：组队、分配、感知"""
    
    def __init__(self):
        self.team_builder = TeamBuilder()
        self.dispatcher = TaskDispatcher()
        self.sensor = StateSensor()
    
    # === 组队能力 ===
    
    def create_team(self, scene: str, complexity: TaskComplexity = TaskComplexity.STANDARD) -> List[int]:
        """
        创建执行团队
        
        基于场景和复杂度自动组队
        """
        return self.team_builder.build_team(scene, complexity)
    
    def create_triangle_team(self, flow_type: str) -> List[int]:
        """
        创建三角循环团队
        
        用于标准任务的三角协作
        """
        return self.team_builder.form_triangle(flow_type)
    
    def create_pair_team(self, pair_type: str) -> List[int]:
        """
        创建阴阳配对团队
        
        用于简单任务的快速协作
        """
        return self.team_builder.form_yin_yang_pair(pair_type)
    
    # === 分配能力 ===
    
    def assign_task(self, task: Task) -> Dict[int, Any]:
        """
        分配任务到各宫位
        
        返回每个宫位的具体职责
        """
        return self.dispatcher.dispatch(task)
    
    def create_task(self, title: str, scene: str, complexity: TaskComplexity = TaskComplexity.STANDARD) -> Task:
        """
        创建任务并自动组队
        """
        team = self.create_team(scene, complexity)
        
        task = Task(
            task_id=f"task_{scene}_{len(team)}",
            title=title,
            description=f"场景: {scene}",
            complexity=complexity,
            scene=scene,
            assigned_palaces=team,
        )
        
        return task
    
    # === 感知能力 ===
    
    def get_system_status(self, palace_states: Dict[int, PalaceState]) -> Dict[str, Any]:
        """
        获取系统状态
        """
        return self.sensor.sense_system_state(palace_states)
    
    def get_task_progress(self, task: Task) -> Dict[str, Any]:
        """
        获取任务进度
        """
        return self.sensor.sense_task_progress(task)
    
    def check_balance(self, palace_states: Dict[int, PalaceState]) -> float:
        """
        检查阴阳平衡
        """
        status = self.get_system_status(palace_states)
        return status["balance"]
    
    # === 核心决策 ===
    
    def decide_next_action(self, task: Task, palace_states: Dict[int, PalaceState]) -> Dict[str, Any]:
        """
        决策下一步行动
        
        基于任务进度和系统状态
        """
        progress = self.get_task_progress(task)
        system = self.get_system_status(palace_states)
        
        decision = {
            "task_id": task.task_id,
            "current_stage": progress["current_stage"],
            "progress": progress["progress"],
            "system_balance": system["balance"],
            "alerts": system["alerts"],
            "recommendation": None,
        }
        
        # 决策逻辑
        if system["balance"] < 0.3:
            decision["recommendation"] = "系统失衡，暂停派发新任务，先平衡负载"
        elif progress["in_progress"] > 2:
            decision["recommendation"] = "多个宫位并行执行中，等待完成"
        elif progress["pending"] > 0:
            next_palace = task.assigned_palaces[progress["current_stage"]]
            decision["recommendation"] = f"派发给{next_palace}宫执行"
        else:
            decision["recommendation"] = "任务已完成，准备交付"
        
        return decision


# ==================== 示例用法 ====================

if __name__ == "__main__":
    milo = MiloCore()
    
    print("=== 米珞核心能力演示 ===\n")
    
    # 1. 组队
    print("- 组队")
    team = milo.create_team("download", TaskComplexity.STANDARD)
    print(f"  场景'download' → 组队: {team}")
    
    triangle = milo.create_triangle_team("data_flow")
    print(f"  数据流三角: {triangle}")
    
    pair = milo.create_pair_team("tech_brand")
    print(f"  技术+品牌配对: {pair}")
    
    # 2. 分配
    print("\n- 分配")
    task = milo.create_task("下载并分析视频", "transcribe", TaskComplexity.STANDARD)
    print(f"  创建任务: {task.title}")
    print(f"  分配宫位: {task.assigned_palaces}")
    
    assignments = milo.assign_task(task)
    for palace, info in assignments.items():
        print(f"  {palace}宫: 第{info['order']}步, 角色: {info['role']}")
    
    # 3. 感知
    print("\n- 感知")
    palace_states = {
        1: PalaceState(1, "数据采集", 0.5, "busy", "task_1", ["download", "scrape"]),
        2: PalaceState(2, "产品质量", 0.0, "idle", None, ["check", "score"]),
        3: PalaceState(3, "技术团队", 0.3, "busy", "task_1", ["code", "debug"]),
        4: PalaceState(4, "品牌战略", 0.0, "idle", None, ["brand", "strategy"]),
        5: PalaceState(5, "中央控制", 0.2, "coordinating", "task_1", ["dispatch", "coordinate"]),
        6: PalaceState(6, "物联监控", 0.8, "busy", None, ["monitor", "backup"]),
        7: PalaceState(7, "法务框架", 0.0, "idle", None, ["validate", "audit"]),
        8: PalaceState(8, "营销客服", 0.0, "idle", None, ["content", "publish"]),
        9: PalaceState(9, "行业生态", 0.0, "idle", None, ["research", "trend"]),
    }
    
    status = milo.get_system_status(palace_states)
    print(f"  阴阳平衡: {status['balance']:.2f}")
    print(f"  中轴健康: {status['axis_health']:.2f}")
    print(f"  支撑强度: {status['support_strength']:.2f}")
    print(f"  告警: {status['alerts']}")
    
    # 4. 决策
    print("\n- 决策")
    decision = milo.decide_next_action(task, palace_states)
    print(f"  任务进度: {decision['progress']:.0%}")
    print(f"  建议: {decision['recommendation']}")

# ==================== 完整核心结构感知 ====================

class FullStateSensor(StateSensor):
    """完整状态感知引擎 - 使用全部4个三角"""
    
    def __init__(self):
        from taiji_algorithm import get_all_triangles
        self.all_triangles = get_all_triangles()
        super().__init__()
    
    def sense_all_triangles(self, palace_states: Dict[int, PalaceState]) -> Dict[str, float]:
        """
        感知所有三角的健康度
        
        Returns:
            {
                "信息流(159)": 0.95,
                "产品流(258)": 0.8,
                "开发流(357)": 0.6,
                "监控流(456)": 0.7,
            }
        """
        results = {}
        
        names = ["信息流(159)", "产品流(258)", "开发流(357)", "监控流(456)"]
        
        for i, tri in enumerate(self.all_triangles):
            loads = [palace_states[p].load for p in tri if p in palace_states]
            if loads:
                avg = sum(loads) / len(loads)
                variance = sum((l - avg) ** 2 for l in loads) / len(loads)
                health = 1.0 - min(variance, 1.0)
            else:
                health = 1.0
            
            results[names[i]] = health
        
        return results
    
    def sense_system_state(self, palace_states: Dict[int, PalaceState]) -> Dict[str, Any]:
        """增强版系统状态感知"""
        base = super().sense_system_state(palace_states)
        triangles = self.sense_all_triangles(palace_states)
        
        return {
            **base,
            "triangles": triangles,
            "overall_health": sum(triangles.values()) / len(triangles),
        }


# 测试
if __name__ == "__main__":
    sensor = FullStateSensor()
    
    palace_states = {
        1: PalaceState(1, "数据采集", 0.9, "busy", "t1", ["download"]),
        2: PalaceState(2, "产品质量", 0.0, "idle", None, ["check"]),
        3: PalaceState(3, "技术团队", 0.7, "busy", "t1", ["code"]),
        4: PalaceState(4, "品牌战略", 0.0, "idle", None, ["brand"]),
        5: PalaceState(5, "中央控制", 0.3, "busy", "t1", ["dispatch"]),
        6: PalaceState(6, "物联监控", 0.95, "busy", None, ["monitor"]),
        7: PalaceState(7, "法务框架", 0.0, "idle", None, ["validate"]),
        8: PalaceState(8, "营销客服", 0.0, "idle", None, ["content"]),
        9: PalaceState(9, "行业生态", 0.1, "idle", None, ["research"]),
    }
    
    state = sensor.sense_system_state(palace_states)
    
    print("=== 完整核心结构感知 ===")
    print(f"阴阳平衡: {state['balance']:.2f}")
    print(f"中轴健康: {state['axis_health']:.2f}")
    print(f"支撑强度: {state['support_strength']:.2f}")
    print(f"整体健康: {state['overall_health']:.2f}")
    print()
    print("各三角健康度:")
    for name, health in state['triangles'].items():
        print(f"  {name}: {health:.2f}")
    print()
    print(f"告警: {state['alerts']}")
