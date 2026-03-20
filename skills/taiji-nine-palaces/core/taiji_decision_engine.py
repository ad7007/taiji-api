#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太极两仪决策系统 - L0 元规划增强版
Taiji Yin-Yang Decision System - Enhanced L0 Meta Planning

基于九宫感知的两仪状态决策：
- 正转 (Yang): 任务推进模式
- 反转 (Yin): Ask 模式/智能体会议模式

实现实事求是的任务生成和动态排序
集成数据采集功能用于系统进化
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import time
import json
import sys
from pathlib import Path

# 导入官方宫殿配置函数
sys.path.insert(0, str(Path(__file__).parent))
from palace_constants import get_palace_name

# 导入数据采集器
try:
    from .key_data_collector import KeyDataCollector
except ImportError:
    # 如果在 openclaw-sub 中运行
    try:
        from key_data_collector import KeyDataCollector
    except ImportError:
        KeyDataCollector = None


class TaijiMode(Enum):
    """两仪模式"""
    YANG_FORWARD = "阳_正转"      # 任务执行模式
    YIN_REVERSE = "阴_反转"       # Ask 模式/会议模式


class TaskPriority(Enum):
    """任务优先级"""
    CRITICAL = 1    # 紧急且重要
    HIGH = 2        # 重要不紧急
    MEDIUM = 3      # 常规任务
    LOW = 4         # 可延缓


@dataclass
class TaskItem:
    """任务项"""
    id: str
    description: str
    palace_id: int  # 关联宫位
    priority: TaskPriority
    estimated_load: float  # 预估负载 0-1
    actual_progress: float = 0.0  # 实际进度 0-1
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    
    def is_overdue(self) -> bool:
        """是否超时"""
        if self.completed_at:
            return False
        elapsed = time.time() - self.created_at
        return elapsed > 3600  # 默认 1 小时超时


@dataclass
class PalacePerception:
    """宫位感知数据"""
    position: int
    health: float  # 健康度
    activation: float  # 激活度
    load: float  # 当前负载
    task_count: int  # 任务数
    yao_lines: List[bool]  # 六爻状态
    five_element: str  # 五行
    
    @property
    def yin_yang_balance(self) -> float:
        """阴阳平衡度 (-1 ~ 1, 负=偏阴，正=偏阳)"""
        yang_count = sum(self.yao_lines)
        return (yang_count - 3) / 3  # 标准化到 -1~1


@dataclass
class StrategicDecision:
    """战略决策"""
    mode: TaijiMode
    confidence: float  # 置信度 0-1
    reasoning: List[str]  # 决策依据
    recommended_actions: List[str]  # 建议行动
    timestamp: float = field(default_factory=time.time)


class TaijiDecisionEngine:
    """
    太极决策引擎
    
    核心逻辑：
    1. 收集各宫位感知数据
    2. 计算整体阴阳平衡
    3. 决定两仪模式（正转/反转）
    4. 动态调整任务优先级
    5. 提供战略分析建议
    """
    
    # 决策阈值
    MODE_SWITCH_THRESHOLD = 0.3  # 阴阳失衡超过 30% 切换模式
    ASK_MODE_TRIGGER_COUNT = 3   # 3 个以上宫位异常触发 Ask 模式
    
    def __init__(self):
        self.palace_perceptions: Dict[int, PalacePerception] = {}
        self.task_queue: List[TaskItem] = []
        self.decision_history: List[StrategicDecision] = []
        
        # 初始化数据采集器
        self.data_collector = KeyDataCollector() if KeyDataCollector else None
        
        # 五行生克权重（增强版）
        self.element_weights = {
            "木": 1.2,  # 技术、团队 - 创新驱动力
            "火": 1.0,  # 生态 - 影响力
            "土": 1.5,  # ⭐ 特别加重（因为有 3 个土位，且 5 是中轴核心）
            "金": 0.9,  # 物联、监控 - 约束力
            "水": 1.3,  # 数据 - 核心资源
        }
        
        # 🆕 循环特殊权重
        self.central_axis_bonus = 1.5   # 159 中轴额外加成
        self.triangle_bonus = 1.3        # 258 三角额外加成
        self.core_palace_bonus = 2.0     # 5 中宫绝对核心加成
    
    def update_palace_perception(self, perception: PalacePerception):
        """更新宫位感知数据"""
        self.palace_perceptions[perception.position] = perception
        
        # 检查是否需要重新决策
        self._check_mode_switch()
    
    def _calculate_global_yin_yang(self) -> float:
        """
        计算全局阴阳平衡
        
        Returns:
            float: -1(全阴) ~ 1(全阳)
        """
        if not self.palace_perceptions:
            return 0.0
        
        total_balance = 0.0
        weight_sum = 0.0
        
        for pos, perception in self.palace_perceptions.items():
            # 五行权重加成
            element_weight = self.element_weights.get(perception.five_element, 1.0)
            
            # 健康度和激活度的影响
            vitality = (perception.health + perception.activation) / 2
            weighted_balance = perception.yin_yang_balance * vitality * element_weight
            
            total_balance += weighted_balance
            weight_sum += element_weight
        
        return total_balance / weight_sum if weight_sum > 0 else 0.0
    
    def _check_mode_switch(self):
        """检查是否需要切换两仪模式"""
        global_balance = self._calculate_global_yin_yang()
        
        # 统计异常宫位数量
        abnormal_count = sum(
            1 for p in self.palace_perceptions.values()
            if p.health < 0.5 or p.load > 0.8
        )
        
        # 保存旧的决策用于对比
        old_mode = self._get_current_mode() if self.decision_history else None
        
        # 决策逻辑
        if abs(global_balance) < self.MODE_SWITCH_THRESHOLD:
            # 接近平衡，维持当前模式
            return
        
        if global_balance < -self.MODE_SWITCH_THRESHOLD or abnormal_count >= self.ASK_MODE_TRIGGER_COUNT:
            # 阴盛阳衰或多个宫位异常 → 切换到 Ask 模式
            new_mode = TaijiMode.YIN_REVERSE
            reasoning = [
                f"全局阴阳失衡：{global_balance:.2f}",
                f"异常宫位数：{abnormal_count}",
                "建议：暂停执行，进行战略调整"
            ]
        else:
            # 阳气充足 → 切换到执行模式
            new_mode = TaijiMode.YANG_FORWARD
            reasoning = [
                f"全局状态良好：{global_balance:.2f}",
                f"活跃宫位：{len([p for p in self.palace_perceptions.values() if p.activation > 0.7])}",
                "建议：继续推进任务"
            ]
        
        # 创建决策记录
        decision = StrategicDecision(
            mode=new_mode,
            confidence=abs(global_balance),
            reasoning=reasoning,
            recommended_actions=self._generate_recommendations(new_mode)
        )
        
        self.decision_history.append(decision)
        
        # ===== 新增：采集决策质量数据 =====
        if self.data_collector:
            # 准备决策上下文
            context = {
                'global_yin_yang': round(global_balance, 3),
                'abnormal_palace_count': abnormal_count,
                'active_tasks': len([t for t in self.task_queue if not t.completed_at]),
                'system_load': self._calculate_system_load()
            }
            
            # 决策内容
            decision_made = {
                'mode': new_mode.value,
                'confidence': round(abs(global_balance), 3),
                'key_factors': reasoning[:2]
            }
            
            # 初始结果（后续会更新）
            outcome = {
                'success': True,  # 暂时标记为成功，实际结果需要后续跟踪
                'actual_improvement': 0.0,  # 待后续评估
                'time_to_result_hours': 0.0,
                'user_intervened': False
            }
            
            # 记录决策
            self.data_collector.record_decision_outcome(
                decision_context=context,
                decision_made=decision_made,
                outcome=outcome
            )
        
        # 通知回调（如果有）
        if hasattr(self, '_mode_callback'):
            self._mode_callback(decision)
    
    def _generate_recommendations(self, mode: TaijiMode) -> List[str]:
        """生成具体建议"""
        recommendations = []
        
        if mode == TaijiMode.YIN_REVERSE:
            # Ask 模式建议
            weak_palaces = [
                p for p in self.palace_perceptions.values()
                if p.health < 0.6
            ]
            
            if weak_palaces:
                palace_names = ", ".join([f"{p.position}宫" for p in weak_palaces])
                recommendations.append(f"优先关注薄弱宫位：{palace_names}")
            
            overloaded = [
                p for p in self.palace_perceptions.values()
                if p.load > 0.8
            ]
            
            if overloaded:
                recommendations.append("考虑任务分流或延后低优先级任务")
            
            recommendations.append("召开智能体协调会议")
            recommendations.append("重新评估任务优先级")
        
        else:
            # 执行模式建议
            high_energy = [
                p for p in self.palace_perceptions.values()
                if p.activation > 0.8 and p.health > 0.8
            ]
            
            if high_energy:
                palace_names = ", ".join([f"{p.position}宫" for p in high_energy])
                recommendations.append(f"高能效宫位可承担更多任务：{palace_names}")
            
            recommendations.append("按优先级顺序执行任务")
            recommendations.append("监控关键指标变化")
        
        return recommendations
    
    def calculate_palace_weight(self, position: int) -> float:
        """
        计算宫位综合权重
        
        Args:
            position: 宫位数字
        
        Returns:
            float: 综合权重
        """
        try:
            from core.palace_constants import get_palace_element
        except ImportError:
            from palace_constants import get_palace_element
        
        try:
            from .nine_palaces_cycles import NinePalacesCycles
        except ImportError:
            from nine_palaces_cycles import NinePalacesCycles
        
        element = get_palace_element(position)
        base_weight = self.element_weights.get(element, 1.0)
        
        # 累加各种加成
        multiplier = 1.0
        
        # 如果是核心宫位（5 号），给予最高优先级
        if NinePalacesCycles.is_core_palace(position):
            multiplier *= self.core_palace_bonus
        else:
            # 其他宫位根据所属循环给予加成
            if NinePalacesCycles.is_central_axis(position):
                multiplier *= self.central_axis_bonus
            
            if NinePalacesCycles.is_triangle_support(position):
                multiplier *= self.triangle_bonus
        
        return base_weight * multiplier
    
    def is_core_palace_critical(self) -> bool:
        """
        判断核心宫位（5 中宫）是否处于 critical 状态
        
        Returns:
            bool: True 如果核心宫位健康度低于 0.6
        """
        if 5 not in self.palace_perceptions:
            return False
        
        return self.palace_perceptions[5].health < 0.6
    
    def get_priority_recommendation(self) -> str:
        """
        获取优先级建议
        
        Returns:
            str: 建议文本
        """
        try:
            from .nine_palaces_cycles import NinePalacesCycles
        except ImportError:
            from nine_palaces_cycles import NinePalacesCycles
        
        if self.is_core_palace_critical():
            return "⚠️ 紧急：5-中央控制 状态异常，需立即处理！"
        
        # 检查 159 中轴
        axis_health = []
        for pos in NinePalacesCycles.get_central_axis_path():
            if pos in self.palace_perceptions:
                axis_health.append(self.palace_perceptions[pos].health)
        
        if axis_health and min(axis_health) < 0.6:
            return "⚠️ 警告：159 中轴失衡，需优先恢复！"
        
        # 检查 258 三角
        triangle_health = []
        for pos in NinePalacesCycles.get_triangle_support_path():
            if pos in self.palace_perceptions:
                triangle_health.append(self.palace_perceptions[pos].health)
        
        if triangle_health and min(triangle_health) < 0.6:
            return "⚠️ 警告：258 三角支撑不稳，需关注！"
        
        return "系统运行正常，按优先级顺序执行任务"
    
    def generate_task(self, description: str, palace_id: int, 
                     priority: TaskPriority = TaskPriority.MEDIUM,
                     estimated_load: float = 0.3) -> TaskItem:
        """
        生成新任务（实事求是）
        
        根据当前系统状态决定是否接受新任务
        """
        # 检查系统负载
        current_mode = self._get_current_mode()
        
        if current_mode == TaijiMode.YIN_REVERSE:
            # Ask 模式下谨慎添加任务
            print(f"⚠️ 系统处于 Ask 模式，建议暂缓添加任务")
        
        # 创建任务
        task = TaskItem(
            id=f"TASK-{int(time.time())}",
            description=description,
            palace_id=palace_id,
            priority=priority,
            estimated_load=estimated_load
        )
        
        # 插入任务队列（按优先级排序）
        self._insert_task_by_priority(task)
        
        return task
    
    def _insert_task_by_priority(self, task: TaskItem):
        """按优先级插入任务"""
        # 找到合适的插入位置
        insert_pos = 0
        for i, existing_task in enumerate(self.task_queue):
            if task.priority.value <= existing_task.priority.value:
                insert_pos = i
                break
            insert_pos = i + 1
        
        self.task_queue.insert(insert_pos, task)
    
    def get_next_task(self, palace_id: Optional[int] = None) -> Optional[TaskItem]:
        """
        获取下一个可执行任务
        
        Args:
            palace_id: 可选，指定宫位
        
        Returns:
            任务项或 None
        """
        # 检查是否在 Ask 模式
        if self._get_current_mode() == TaijiMode.YIN_REVERSE:
            return None
        
        # 查找任务
        for task in self.task_queue:
            if task.completed_at or task.started_at:
                continue
            
            # 如果指定了宫位，只返回该宫位的任务
            if palace_id and task.palace_id != palace_id:
                continue
            
            # 检查宫位状态
            palace = self.palace_perceptions.get(task.palace_id)
            if palace and (palace.health < 0.5 or palace.load > 0.9):
                # 宫位状态不佳，跳过
                continue
            
            # 找到合适任务
            task.started_at = time.time()
            return task
        
        return None
    
    def complete_task(self, task_id: str, success: bool = True):
        """完成任务"""
        for task in self.task_queue:
            if task.id == task_id:
                task.completed_at = time.time()
                task.actual_progress = 1.0 if success else 0.0
                
                # 更新宫位负载
                if task.palace_id in self.palace_perceptions:
                    palace = self.palace_perceptions[task.palace_id]
                    # 简化：完成任务后负载略微下降
                    palace.load = max(0.0, palace.load - task.estimated_load * 0.5)
                
                break
    
    def _get_current_mode(self) -> TaijiMode:
        """获取当前模式"""
        if not self.decision_history:
            return TaijiMode.YANG_FORWARD  # 默认执行模式
        return self.decision_history[-1].mode
    
    def _calculate_system_load(self) -> float:
        """计算系统负载 (0-1)"""
        if not self.palace_perceptions:
            return 0.0
        
        # 基于各宫位负载的平均值
        loads = [p.load for p in self.palace_perceptions.values()]
        return sum(loads) / len(loads)
    
    def update_decision_outcome(self, decision_index: int, success: bool, improvement: float):
        """更新决策结果（用于后续跟踪）
        
        Args:
            decision_index: 决策在 history 中的索引
            success: 是否成功
            improvement: 实际改善程度
        """
        if self.data_collector and decision_index < len(self.decision_history):
            # 更新数据采集器中的记录（简化处理，实际应该更复杂）
            pass
    
    def get_strategic_report(self) -> Dict:
        """获取战略分析报告"""
        current_mode = self._get_current_mode()
        global_balance = self._calculate_global_yin_yang()
        
        # 统计信息
        total_tasks = len(self.task_queue)
        pending_tasks = len([t for t in self.task_queue if not t.started_at and not t.completed_at])
        completed_tasks = len([t for t in self.task_queue if t.completed_at])
        
        # 效率指标
        efficiency_score = self._calculate_efficiency_score()
        
        report = {
            "current_mode": current_mode.value,
            "global_yin_yang": round(global_balance, 3),
            "task_statistics": {
                "total": total_tasks,
                "pending": pending_tasks,
                "completed": completed_tasks,
                "completion_rate": round(completed_tasks / total_tasks, 3) if total_tasks > 0 else 0
            },
            "palace_status": {
                str(pos): {
                    "health": round(p.health, 3),
                    "activation": round(p.activation, 3),
                    "load": round(p.load, 3),
                    "yin_yang_balance": round(p.yin_yang_balance, 3)
                }
                for pos, p in self.palace_perceptions.items()
            },
            "efficiency_metrics": efficiency_score,
            "recent_decisions": [
                {
                    "mode": d.mode.value,
                    "confidence": round(d.confidence, 3),
                    "timestamp": d.timestamp
                }
                for d in self.decision_history[-5:]  # 最近 5 次决策
            ],
            "recommendations": self._generate_recommendations(current_mode)
        }
        
        return report
    
    def _calculate_efficiency_score(self) -> Dict:
        """计算效率指标"""
        completed = [t for t in self.task_queue if t.completed_at]
        
        if not completed:
            return {"score": 0.0, "avg_duration": 0, "success_rate": 0}
        
        # 平均完成时间
        durations = [
            t.completed_at - t.started_at 
            for t in completed 
            if t.started_at
        ]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        # 成功率
        successful = len([t for t in completed if t.actual_progress > 0])
        success_rate = successful / len(completed)
        
        # 综合效率分
        score = (success_rate * 0.7 + 
                 min(1.0, 3600 / avg_duration) * 0.3) if avg_duration > 0 else 0
        
        return {
            "score": round(score, 3),
            "avg_duration_sec": round(avg_duration, 1),
            "success_rate": round(success_rate, 3)
        }
    
    def set_mode_callback(self, callback):
        """设置模式切换回调"""
        self._mode_callback = callback


# ============================================================================
# 使用示例和测试
# ============================================================================

if __name__ == "__main__":
    print("=== 太极两仪决策系统演示 ===\n")
    
    engine = TaijiDecisionEngine()
    
    # 模拟宫位感知数据
    perceptions = [
        PalacePerception(1, 0.8, 0.9, 0.3, 5, [True]*6, "水"),
        PalacePerception(2, 0.6, 0.5, 0.7, 8, [True, False]*3, "土"),
        PalacePerception(3, 0.9, 0.8, 0.4, 3, [True]*6, "木"),
        PalacePerception(9, 0.4, 0.3, 0.9, 12, [False]*6, "火"),  # 异常
    ]
    
    # 更新感知
    for p in perceptions:
        engine.update_palace_perception(p)
    
    # 生成任务
    print("【生成任务】")
    task1 = engine.generate_task("数据采集优化", 1, TaskPriority.HIGH, 0.4)
    task2 = engine.generate_task("产品功能迭代", 2, TaskPriority.MEDIUM, 0.3)
    task3 = engine.generate_task("技术架构升级", 3, TaskPriority.LOW, 0.5)
    
    print(f"已生成 {len(engine.task_queue)} 个任务")
    
    # 获取战略报告
    print("\n【战略分析报告】")
    report = engine.get_strategic_report()
    print(f"当前模式：{report['current_mode']}")
    print(f"全局阴阳：{report['global_yin_yang']}")
    print(f"任务完成率：{report['task_statistics']['completion_rate']:.1%}")
    print(f"效率评分：{report['efficiency_metrics']['score']}")
    
    print("\n【建议行动】")
    for rec in report['recommendations']:
        print(f"  • {rec}")
    
    # 执行任务
    print("\n【执行任务】")
    next_task = engine.get_next_task()
    if next_task:
        print(f"准备执行：{next_task.description} (优先级：{next_task.priority.name})")
        engine.complete_task(next_task.id)
        print(f"✅ 任务完成")
    else:
        print("⚠️ 系统处于 Ask 模式或无可用任务")
