#!/usr/bin/env python3
"""
太极系统完整闭环测试

验证：红灯 → 执行 → 绿灯 → 交付 的完整流程
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.task_manager import TaskManager, TaskPriority, TaskStatus
from palace_7_tdd import Palace7TDD
import json


def test_tdd_loop():
    """测试完整 TDD 闭环"""
    print("=" * 60)
    print("太极系统 TDD 闭环测试")
    print("=" * 60)

    # 初始化
    task_manager = TaskManager()
    tdd = Palace7TDD()

    # ========== Step 1: 创建任务 ==========
    print("\n📋 Step 1: 创建任务")
    task = task_manager.create_task(
        description="分析竞品数据并生成报告",
        priority=TaskPriority.HIGH
    )
    print(f"   任务ID: {task.task_id}")
    print(f"   优先级: {task.priority.name}")
    print(f"   分配宫位: {task.assigned_palaces}")
    print(f"   任务类型: {task.metadata.get('task_type')}")

    # ========== Step 2: 红灯确认 ==========
    print("\n🔴 Step 2: 红灯确认")
    red_confirm = tdd.red_light_confirm(task.description)
    print(f"   确认状态: {red_confirm['confirmed']}")
    print(f"   消息: {red_confirm['message']}")

    # ========== Step 3: 定义验收标准 ==========
    print("\n📐 Step 3: 定义验收标准")
    task_type = task.metadata.get("task_type", "data_analysis")
    standards = tdd.define_acceptance_criteria(
        task_type=task_type,
        requirements=["必须有竞品对比表格"]
    )
    task_manager.set_tdd_standards(task.task_id, standards)
    print(f"   标准数量: {len(standards['standards'])}")
    for std in standards['standards'][:3]:
        print(f"   - {std['name']}: {'✅' if std['required'] else '⭕'}")

    # ========== Step 4: 开始执行 ==========
    print("\n🚀 Step 4: 开始执行")
    task_manager.start_task(task.task_id)
    print(f"   状态: {task_manager.tasks[task.task_id].status.value}")

    # ========== Step 5: 模拟执行输出 ==========
    print("\n⚙️ Step 5: 模拟执行")
    sample_output = """
# 竞品数据分析报告

## 数据来源
数据采集自 A、B、C 三家竞品官网，时间范围 2024-01 至 2024-03

## 分析方法
采用对比分析法，从功能、价格、用户评价三个维度进行评估

## 核心洞察
1. A产品功能最全面，但价格偏高
2. B产品性价比最高，适合中小企业
3. C产品用户体验最好，但功能较少

## 竞品对比表格
| 产品 | 功能数 | 价格 | 评分 |
|------|--------|------|------|
| A    | 50+    | ¥999 | 4.2  |
| B    | 30+    | ¥499 | 4.5  |
| C    | 20+    | ¥299 | 4.8  |

## 建议行动
1. 重点关注 B 产品的定价策略
2. 借鉴 C 产品的用户体验设计
"""
    print("   执行完成，生成输出...")

    # ========== Step 6: 绿灯检查 ==========
    print("\n🟢 Step 6: 绿灯检查")
    check_result = tdd.green_light_check(
        task_type=task_type,
        output=sample_output,
        standards=standards
    )
    print(f"   通过状态: {'✅ 通过' if check_result['passed'] else '❌ 未通过'}")
    if check_result['reasons']:
        print(f"   未通过原因: {check_result['reasons']}")
    print(f"   检查项数: {len(check_result['details'])}")
    for detail in check_result['details'][:3]:
        status = "✅" if detail['passed'] else "❌"
        print(f"   - {detail['name']}: {status}")

    # ========== Step 7: 交付 ==========
    print("\n📦 Step 7: 交付")
    if check_result['passed']:
        task_manager.complete_task(task.task_id, sample_output)
        print(f"   状态: ✅ 已交付")
        print(f"   完成时间: {task_manager.tasks[task.task_id].completed_at}")
    else:
        print(f"   状态: ❌ 需要返工")

    # ========== Step 8: 统计报告 ==========
    print("\n📊 Step 8: 统计报告")
    stats = task_manager.get_stats()
    print(f"   总任务数: {stats['total_tasks']}")
    print(f"   完成率: {stats['completion_rate']:.1%}")
    print(f"   按状态分布: {stats['by_status']}")

    print("\n" + "=" * 60)
    print("✅ TDD 闭环测试完成")
    print("=" * 60)

    return {
        "task_id": task.task_id,
        "passed": check_result['passed'],
        "stats": stats
    }


if __name__ == "__main__":
    result = test_tdd_loop()
    print(f"\n测试结果: {json.dumps(result, indent=2, ensure_ascii=False, default=str)}")