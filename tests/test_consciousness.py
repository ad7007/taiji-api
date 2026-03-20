#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太极意识系统测试
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.taiji_consciousness import (
    TaijiConsciousness, TaijiGoals, RotationDirection,
    EnergyLevel, SystemHealth, get_consciousness
)
from core.taiji_l0_protocol import get_l0_registry


def test_energy_levels():
    """测试能量等级"""
    consciousness = TaijiConsciousness()
    
    # CRITICAL
    consciousness.sense_energy(0.1, 0.1, 0.1, 0.1)
    assert consciousness.energy.level() == EnergyLevel.CRITICAL
    
    # HIGH
    consciousness.sense_energy(0.8, 0.7, 0.8, 0.7)
    assert consciousness.energy.level() == EnergyLevel.HIGH
    
    print("✅ 能量等级测试通过")


def test_rotation_decision():
    """测试旋转决策"""
    consciousness = TaijiConsciousness()
    
    # 场景1：有价值机会，能量充足，系统健康 → 正转
    consciousness.sense_energy(0.7, 0.6, 0.5, 0.5)
    consciousness.sense_value_flow(external_demand=0.5, pending_tasks=3, active_projects=1, revenue_potential=0.6)
    consciousness.sense_system(0.8, {5: 0.3}, bugs=0, improvements=0)
    
    rotation = consciousness.decide_rotation()
    assert rotation == RotationDirection.FORWARD
    
    # 场景2：无价值机会，有改进空间 → 反转
    consciousness.sense_value_flow(external_demand=0.1, pending_tasks=0, active_projects=0, revenue_potential=0.1)
    consciousness.sense_system(0.5, {5: 0.3}, bugs=0, improvements=3)
    rotation = consciousness.decide_rotation()
    assert rotation == RotationDirection.REVERSE
    
    # 场景3：能量严重不足 → 反转
    consciousness.sense_energy(0.1, 0.1, 0.1, 0.1)
    rotation = consciousness.decide_rotation()
    assert rotation == RotationDirection.REVERSE
    
    # 场景4：系统严重故障 → 反转
    consciousness.sense_energy(0.7, 0.6, 0.5, 0.5)
    consciousness.sense_system(0.3, {5: 0.3}, bugs=10, improvements=0)
    # 注意：bug=10 会让系统变成 BROKEN
    rotation = consciousness.decide_rotation()
    assert rotation == RotationDirection.REVERSE
    
    print("✅ 旋转决策测试通过")


def test_goals():
    """测试目标系统"""
    goals = TaijiGoals()
    
    assert "更大" in goals.ultimate_goal
    assert len(goals.medium_goals) == 3
    
    active = goals.get_active_goal("forward")
    assert "创造价值" in active
    
    active = goals.get_active_goal("reverse")
    assert "完善系统" in active
    
    print("✅ 目标系统测试通过")


def test_l0_protocol():
    """测试L0协议"""
    registry = get_l0_registry()
    
    # 测试任务路由
    handlers = registry.find_handler("download")
    assert 1 in handlers  # 1宫处理下载
    
    handlers = registry.find_handler("code")
    assert 3 in handlers  # 3宫处理代码
    
    handlers = registry.find_handler("content")
    assert 8 in handlers  # 8宫处理内容
    
    # 测试负载更新
    registry.update_load(1, 0.5)
    assert registry.palaces[1].load == 0.5
    assert registry.palaces[1].status == "busy"
    
    print("✅ L0协议测试通过")


def test_singleton():
    """测试单例"""
    c1 = get_consciousness()
    c2 = get_consciousness()
    
    assert c1 is c2
    
    print("✅ 单例测试通过")


if __name__ == "__main__":
    print("=== 太极意识系统测试 ===\n")
    
    test_energy_levels()
    test_rotation_decision()
    test_goals()
    test_l0_protocol()
    test_singleton()
    
    print("\n✅ 所有测试通过！")