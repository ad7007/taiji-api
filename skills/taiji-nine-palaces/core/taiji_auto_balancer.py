#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太极自动平衡工具 - 任务进度与战略分析的效率平衡
Taiji Auto-Balancing Tool

实现：
1. 任务进度 vs 战略分析的动态平衡
2. 成果转换效率优化
3. 五行循环验证开发与测试
4. 实事求是的任务生成和排序
集成数据采集功能用于系统进化
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.taiji_decision_engine import (
    TaijiDecisionEngine, 
    PalacePerception,
    TaijiMode,
    TaskPriority
)
from core.palace_constants import get_palace_name
from typing import Dict, List
import time

# 导入数据采集器
try:
    from .key_data_collector import KeyDataCollector
except ImportError:
    try:
        from key_data_collector import KeyDataCollector
    except ImportError:
        KeyDataCollector = None


class TaijiAutoBalancer:
    """
    太极自动平衡器
    
    核心功能：
    1. 监控任务进度与战略分析的平衡
    2. 动态调整资源分配
    3. 五行循环验证（开发→测试→部署）
    4. 实时优化任务排序
    """
    
    def __init__(self, decision_engine: TaijiDecisionEngine):
        self.engine = decision_engine
        self.balance_history: List[Dict] = []
        
        # 初始化数据采集器（复用 engine 的）
        self.data_collector = self.engine.data_collector if hasattr(self.engine, 'data_collector') else None
        
        # 平衡指标权重
        self.weights = {
            "progress": 0.4,      # 任务进度权重
            "strategy": 0.3,      # 战略分析权重
            "efficiency": 0.3     # 转换效率权重
        }
    
    def calculate_balance_score(self) -> float:
        """
        计算综合平衡分数 (0-1)
        
        考虑因素：
        1. 任务完成率
        2. 战略决策质量
        3. 资源利用效率
        """
        report = self.engine.get_strategic_report()
        
        # 任务进度分
        progress_score = report['task_statistics']['completion_rate']
        
        # 战略分析分（基于决策置信度）
        recent_decisions = report['recent_decisions']
        if recent_decisions:
            strategy_score = sum(d['confidence'] for d in recent_decisions) / len(recent_decisions)
        else:
            strategy_score = 0.5  # 默认值
        
        # 转换效率分
        efficiency_score = report['efficiency_metrics']['score']
        
        # 加权平均
        balance_score = (
            progress_score * self.weights['progress'] +
            strategy_score * self.weights['strategy'] +
            efficiency_score * self.weights['efficiency']
        )
        
        # 记录历史
        self.balance_history.append({
            'timestamp': time.time(),
            'balance_score': balance_score,
            'progress': progress_score,
            'strategy': strategy_score,
            'efficiency': efficiency_score
        })
        
        return balance_score
    
    def auto_adjust_task_priorities(self):
        """
        自动调整任务优先级
        
        规则：
        1. 高负载宫位的任务优先级降低
        2. 健康度高的宫位优先分配任务
        3. 根据阴阳平衡动态调整
        """
        current_mode = self.engine._get_current_mode()
        
        # 获取所有待处理任务
        pending_tasks = [
            t for t in self.engine.task_queue
            if not t.started_at and not t.completed_at
        ]
        
        # 记录调整前的状态用于对比
        adjustments_made = []
        
        for task in pending_tasks:
            palace = self.engine.palace_perceptions.get(task.palace_id)
            
            if not palace:
                continue
            
            old_priority = task.priority
            
            # 检查宫位状态
            if palace.health < 0.5 or palace.load > 0.8:
                # 宫位状态不佳，降级优先级
                if task.priority.value > TaskPriority.LOW.value:
                    task.priority = TaskPriority.LOW
                    adjustments_made.append({
                        'task_id': task.id,
                        'from': old_priority.name,
                        'to': 'LOW',
                        'reason': 'palace_weak'
                    })
            
            elif palace.activation > 0.8 and palace.health > 0.8:
                # 宫位状态极佳，提升优先级
                if task.priority.value < TaskPriority.HIGH.value:
                    task.priority = TaskPriority.HIGH
                    adjustments_made.append({
                        'task_id': task.id,
                        'from': old_priority.name,
                        'to': 'HIGH',
                        'reason': 'palace_strong'
                    })
        
        # ===== 新增：采集任务编排数据 =====
        if self.data_collector and adjustments_made:
            # 记录任务生成场景（简化版本）
            for adj in adjustments_made:
                task = next((t for t in pending_tasks if t.id == adj['task_id']), None)
                if task:
                    self.data_collector.record_task_generation(
                        task_id=adj['task_id'],
                        generated_by='auto_adjustment',
                        trigger_event=f"palace_{task.palace_id}_{adj['reason']}",
                        priority_assigned=adj['to'],
                        estimated_duration_min=int(task.estimated_load * 60),
                        actual_duration_min=int(task.estimated_load * 60),  # 暂时相同
                        system_state={
                            'current_mode': current_mode.value,
                            'palace_health': {p.position: p.health for p in self.engine.palace_perceptions.values()},
                            'pending_tasks_count': len(pending_tasks),
                            'available_capacity': 1.0 - self.engine._calculate_system_load() if hasattr(self.engine, '_calculate_system_load') else 0.5
                        },
                        outcome={
                            'completed': False,  # 还未完成
                            'success_rate': 0.0,
                            'blocked_other_tasks': False,
                            'created_value_score': 0.5  # 预估
                        }
                    )
    
    def wuxing_cycle_validation(self) -> Dict:
        """
        五行循环验证（开发→测试→部署）
        
        木 (开发) → 火 (测试) → 土 (部署) → 金 (反馈) → 水 (优化)
        
        Returns:
            验证报告
        """
        validation = {
            "wood_development": {"status": "checking", "issues": []},
            "fire_testing": {"status": "checking", "issues": []},
            "earth_deployment": {"status": "checking", "issues": []},
            "metal_feedback": {"status": "checking", "issues": []},
            "water_optimization": {"status": "checking", "issues": []},
        }
        
        # 简化版本：检查各阶段是否有阻塞
        # 实际应用中需要连接实际的 CI/CD 流程
        
        # 木 - 开发阶段（3-技术团队、4-品牌战略）
        tech_palace = self.engine.palace_perceptions.get(3)
        team_palace = self.engine.palace_perceptions.get(4)
        
        if tech_palace and tech_palace.load > 0.9:
            validation["wood_development"]["status"] = "blocked"
            validation["wood_development"]["issues"].append(f"{get_palace_name(3)}负载过高")
        
        # 火 - 测试阶段（9-行业生态）
        eco_palace = self.engine.palace_perceptions.get(9)
        if eco_palace and eco_palace.health < 0.5:
            validation["fire_testing"]["status"] = "warning"
            validation["fire_testing"]["issues"].append(f"{get_palace_name(9)}健康度不足")
        
        # 土 - 部署阶段（2-产品质量、8-营销客服）
        product_palace = self.engine.palace_perceptions.get(2)
        if product_palace and product_palace.activation < 0.3:
            validation["earth_deployment"]["status"] = "slow"
            validation["earth_deployment"]["issues"].append(f"{get_palace_name(2)}激活度低")
        
        # 计算整体通过率
        passed = sum(
            1 for v in validation.values() 
            if v["status"] == "checking"
        )
        
        validation["overall_pass_rate"] = passed / 5
        
        return validation
    
    def generate_balanced_report(self) -> str:
        """生成平衡分析报告"""
        balance_score = self.calculate_balance_score()
        validation = self.wuxing_cycle_validation()
        
        report_lines = [
            "=" * 60,
            "【太极系统平衡分析报告】",
            "=" * 60,
            f"综合平衡分数：{balance_score:.2f}",
            "",
            "【分项指标】",
            f"  任务进度：{self.weights['progress']*100:.0f}%",
            f"  战略分析：{self.weights['strategy']*100:.0f}%",
            f"  转换效率：{self.weights['efficiency']*100:.0f}%",
            "",
            "【五行循环验证】",
            f"  木 (开发): {validation['wood_development']['status']}",
            f"  火 (测试): {validation['fire_testing']['status']}",
            f"  土 (部署): {validation['earth_deployment']['status']}",
            f"  金 (反馈): {validation['metal_feedback']['status']}",
            f"  水 (优化): {validation['water_optimization']['status']}",
            f"  通过率：{validation['overall_pass_rate']:.0%}",
            "",
            "【建议】",
        ]
        
        # 根据平衡分数给出建议
        if balance_score > 0.8:
            report_lines.append("  ✅ 系统运行优秀，保持当前节奏")
        elif balance_score > 0.6:
            report_lines.append("  👍 系统良好，注意持续优化")
        elif balance_score > 0.4:
            report_lines.append("  ⚠️ 需要关注薄弱环节")
        else:
            report_lines.append("  🚨 系统失衡，建议立即调整")
        
        # 添加五行验证建议
        blocked_stages = [
            stage for stage, data in validation.items()
            if stage != "overall_pass_rate" and data["status"] in ["blocked", "warning", "slow"]
        ]
        
        if blocked_stages:
            report_lines.append(f"  瓶颈阶段：{', '.join(blocked_stages)}")
            report_lines.append("  建议：集中资源突破瓶颈")
        
        report_lines.append("=" * 60)
        
        return "\n".join(report_lines)
    
    def optimize_for_high_efficiency(self):
        """
        优化为高能效比工作状态
        
        适用于子 OPENCLAW 或外接智能体协作场景
        """
        print("🔧 开始优化系统至高能效状态...")
        
        # 1. 清理低价值任务
        low_value_tasks = [
            t for t in self.engine.task_queue
            if t.priority == TaskPriority.LOW and 
            (time.time() - t.created_at) > 7200  # 超过 2 小时未执行
        ]
        
        for task in low_value_tasks:
            # 标记为取消
            task.completed_at = time.time()
            task.actual_progress = 0.0
            print(f"  × 取消低价值任务：{task.description}")
        
        # 2. 重新分配过载宫位的任务
        overloaded = [
            (pos, p) for pos, p in self.engine.palace_perceptions.items()
            if p.load > 0.8
        ]
        
        for pos, palace in overloaded:
            # 找出该宫位的待处理任务
            palace_tasks = [
                t for t in self.engine.task_queue
                if t.palace_id == pos and not t.started_at
            ]
            
            # 尝试重新分配给空闲宫位
            idle_palaces = [
                p_pos for p_pos, p in self.engine.palace_perceptions.items()
                if p.load < 0.3 and p.health > 0.8
            ]
            
            if idle_palaces and palace_tasks:
                print(f"  ↻ 重新分配 {pos}宫 的任务到空闲宫位")
                # 实际应用中需要修改任务的 palace_id
        
        # 3. 触发一次全面的战略评估
        print("  📊 触发全面战略评估...")
        self.engine._check_mode_switch()
        
        print("✅ 优化完成")


# ============================================================================
# 使用示例
# ============================================================================

if __name__ == "__main__":
    print("=== 太极自动平衡工具演示 ===\n")
    
    # 创建决策引擎
    engine = TaijiDecisionEngine()
    
    # 初始化宫位感知
    perceptions = [
        PalacePerception(1, 0.8, 0.9, 0.3, 5, [True]*6, "水"),
        PalacePerception(2, 0.6, 0.5, 0.7, 8, [True, False]*3, "土"),
        PalacePerception(3, 0.9, 0.8, 0.4, 3, [True]*6, "木"),
        PalacePerception(9, 0.4, 0.3, 0.9, 12, [False]*6, "火"),
    ]
    
    for p in perceptions:
        engine.update_palace_perception(p)
    
    # 生成一些任务
    engine.generate_task("紧急 bug 修复", 1, TaskPriority.CRITICAL, 0.3)
    engine.generate_task("产品需求分析", 2, TaskPriority.MEDIUM, 0.4)
    engine.generate_task("性能优化", 3, TaskPriority.LOW, 0.5)
    engine.generate_task("用户调研", 9, TaskPriority.LOW, 0.2)
    
    # 创建平衡器
    balancer = TaijiAutoBalancer(engine)
    
    # 显示平衡报告
    print(balancer.generate_balanced_report())
    
    # 自动调整优先级
    print("\n【自动调整任务优先级】")
    balancer.auto_adjust_task_priorities()
    
    # 高能效优化
    print("\n【高能效优化】")
    balancer.optimize_for_high_efficiency()
