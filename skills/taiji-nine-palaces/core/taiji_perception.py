#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太极感知机制 - 动态演化监控系统
Taiji Perception Mechanism

基于五行生克关系的实时感知和响应系统
监控各宫位状态变化，触发六爻动态演化
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.taiji_wuxing_loop import (
    TaijiMetaPlanner, 
    PalacePosition,
    FiveElements,
    PALACE_TO_ELEMENT
)
from core.palace_constants import get_palace_name
from typing import Dict, List, Callable
import time


class TaijiPerception:
    """
    太极感知器
    
    功能：
    1. 实时监控各宫位健康度
    2. 检测生克关系变化
    3. 触发六爻演化
    4. 提供感知回调机制
    """
    
    def __init__(self):
        self.planner = TaijiMetaPlanner()
        self.callbacks: List[Callable] = []
        self.evolution_history: List[Dict] = []
        
        # 感知阈值
        self.health_change_threshold = 0.1  # 健康度变化超过 10% 触发感知
        self.balance_threshold = 0.7  # 平衡度低于 70% 触发警报
        
        # 初始感知
        self.last_report = self.planner.get_balance_report()
    
    def register_callback(self, callback: Callable):
        """注册感知回调函数"""
        self.callbacks.append(callback)
    
    def update_palace_state(self, palace_pos: int, health: float, activation: float = None):
        """
        更新宫位状态（外部输入）
        
        Args:
            palace_pos: 宫位数字 1-9
            health: 健康度 0-1
            activation: 激活度 0-1
        """
        old_health = self.planner.palace_states[palace_pos].health
        
        # 更新状态
        self.planner.update_palace_health(palace_pos, health)
        
        if activation is not None:
            self.planner.palace_states[palace_pos].activation = activation
        
        # 检测是否触发感知
        health_change = abs(health - old_health)
        if health_change >= self.health_change_threshold:
            palace_name = get_palace_name(palace_pos)
            self._trigger_perception(f"{palace_name}健康度变化：{old_health:.2f} → {health:.2f}")
        
        # 触发六爻演化
        self._evolve_palace_yao_lines(palace_pos)
    
    def _evolve_palace_yao_lines(self, palace_pos: int):
        """演化指定宫位的六爻"""
        new_yao_lines = self.planner.evolve_yao_lines(palace_pos)
        self.planner.palace_states[palace_pos].yao_lines = new_yao_lines
        
        # 记录演化历史
        self.evolution_history.append({
            "timestamp": time.time(),
            "palace": palace_pos,
            "yao_lines": new_yao_lines,
            "yang_count": sum(new_yao_lines),
            "yin_count": 6 - sum(new_yao_lines)
        })
        
        # 通知回调
        yin_yang_str = "".join(["⚊" if y else "⚋" for y in new_yao_lines])
        self._notify_callbacks({
            "type": "yao_evolution",
            "palace": palace_pos,
            "yao_lines": yin_yang_str,
            "yang_ratio": sum(new_yao_lines) / 6
        })
    
    def _trigger_perception(self, message: str):
        """触发全局感知"""
        current_report = self.planner.get_balance_report()
        
        # 检查整体平衡
        if current_report["overall_balance"] < self.balance_threshold:
            self._notify_callbacks({
                "type": "balance_alert",
                "message": f"系统失衡警告！平衡度：{current_report['overall_balance']:.2f}",
                "severity": "high" if current_report["overall_balance"] < 0.5 else "medium"
            })
        
        # 检测生克关系剧变
        self._detect_relationship_changes(current_report)
        
        self.last_report = current_report
    
    def _detect_relationship_changes(self, current_report: Dict):
        """检测生克关系的重大变化"""
        # 简化版本：检查相生相克数量变化
        gen_count = len(current_report["generation_cycle"])
        rst_count = len(current_report["restraint_cycle"])
        
        # 如果生克关系严重失衡
        if gen_count < 5 or rst_count < 5:
            self._notify_callbacks({
                "type": "relationship_imbalance",
                "message": f"生克关系失衡！相生:{gen_count}, 相克:{rst_count}",
                "severity": "medium"
            })
    
    def _notify_callbacks(self, data: Dict):
        """通知所有注册的回调"""
        for callback in self.callbacks:
            try:
                callback(data)
            except Exception as e:
                print(f"回调执行失败：{e}")
    
    def get_system_status(self) -> Dict:
        """获取系统完整状态"""
        report = self.planner.get_balance_report()
        
        # 添加六爻状态
        yao_states = {}
        for pos, state in self.planner.palace_states.items():
            yao_states[f"{pos}宫"] = {
                "yao_lines": "".join(["⚊" if y else "⚋" for y in state.yao_lines]),
                "yang_count": sum(state.yao_lines),
                "health": state.health,
                "element": state.element.value
            }
        
        report["yao_states"] = yao_states
        report["evolution_count"] = len(self.evolution_history)
        
        return report
    
    def manual_adjustment(self, source_palace: int, target_palace: int, 
                         adjustment_type: str, strength: float):
        """
        手动调整生克关系（用于调试或特殊干预）
        
        Args:
            source_palace: 源宫位
            target_palace: 目标宫位
            adjustment_type: "generation" 或 "restraint"
            strength: 调整强度 0-1
        """
        if adjustment_type == "generation":
            # 增强相生
            for rel in self.planner.generation_relations:
                if rel.source == source_palace and rel.target == target_palace:
                    rel.strength = strength
                    break
        elif adjustment_type == "restraint":
            # 增强相克
            for rel in self.planner.restraint_relations:
                if rel.restrainer == source_palace and rel.restrained == target_palace:
                    rel.pressure = strength
                    break
        
        self._trigger_perception(f"手动调整：{source_palace}宫 → {target_palace}宫 ({adjustment_type})")


# ============================================================================
# 使用示例
# ============================================================================

if __name__ == "__main__":
    print("=== 太极感知机制演示 ===\n")
    
    perception = TaijiPerception()
    
    # 注册回调
    def on_event(data):
        print(f"\n【事件】{data['type']}")
        if data['type'] == 'yao_evolution':
            print(f"  {data['palace']}宫六爻：{data['yao_lines']}")
            print(f"  阴阳比：{data['yang_ratio']:.1%}")
        elif data['type'] == 'balance_alert':
            print(f"  {data['message']} (等级：{data['severity']})")
    
    perception.register_callback(on_event)
    
    # 模拟场景：1 宫（数据宫）健康度下降
    print("【场景 1】数据宫健康度下降到 0.6")
    perception.update_palace_state(1, 0.6, 0.8)
    
    time.sleep(0.5)
    
    # 模拟场景：9 宫（生态宫）激活
    print("\n【场景 2】生态宫激活度提升")
    perception.update_palace_state(9, 0.9, 0.95)
    
    time.sleep(0.5)
    
    # 模拟场景：连锁反应
    print("\n【场景 3】多个宫位连续变化")
    for pos in [3, 4, 6]:
        perception.update_palace_state(pos, 0.7 + pos * 0.05, 0.6)
        time.sleep(0.3)
    
    # 显示最终状态
    print("\n\n【最终系统状态】")
    status = perception.get_system_status()
    print(f"整体平衡度：{status['overall_balance']}")
    print(f"演化次数：{status['evolution_count']}")
    
    print("\n各宫六爻状态:")
    for palace_name, yao_info in status['yao_states'].items():
        print(f"  {palace_name}: {yao_info['yao_lines']} (阳爻：{yao_info['yang_count']}, 健康：{yao_info['health']:.2f})")
