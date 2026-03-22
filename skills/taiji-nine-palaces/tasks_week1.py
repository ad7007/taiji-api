#!/usr/bin/env python3
"""
正转第一批任务 - Week 1 执行计划

目标：启动太极API销售
"""

import sys
import os
sys.path.insert(0, '/root/.openclaw/workspace/skills/taiji-nine-palaces')

from core.task_manager import TaskManager, TaskPriority
import json

# 初始化任务管理器
manager = TaskManager()

print("=" * 60)
print("🚀 太极系统正转任务生成 - Week 1")
print("=" * 60)

# ========== P0: API销售启动 ==========

print("\n📦 P0: 太极API销售启动\n")

# 任务1: 完善API文档
task1 = manager.create_task(
    description="完善太极API文档，包括安装、接口、示例代码",
    priority=TaskPriority.CRITICAL,
    task_type="content_create"
)
print(f"✅ 任务1: {task1.task_id}")
print(f"   描述: {task1.description}")
print(f"   宫位: {task1.assigned_palaces} (4宫策略 → 8宫创作 → 7宫验收 → 5宫交付)")

# 任务2: 创建官网落地页
task2 = manager.create_task(
    description="创建太极系统官网落地页，包含产品介绍、定价、购买入口",
    priority=TaskPriority.CRITICAL,
    task_type="content_create"
)
print(f"✅ 任务2: {task2.task_id}")
print(f"   描述: {task2.description}")

# 任务3: 开通支付渠道
task3 = manager.create_task(
    description="配置微信支付/支付宝收款，创建商品链接",
    priority=TaskPriority.HIGH,
    task_type="general"
)
print(f"✅ 任务3: {task3.task_id}")
print(f"   描述: {task3.description}")
print(f"   ⚠️ 需要：余总提供微信支付商户号或支付宝账号")

# 任务4: 发布技术文章
task4 = manager.create_task(
    description="撰写并发布首篇技术文章：《1+8智能体协作：太极系统架构解析》",
    priority=TaskPriority.HIGH,
    task_type="content_create"
)
print(f"✅ 任务4: {task4.task_id}")
print(f"   描述: {task4.description}")

# 任务5: 创建定价页面
task5 = manager.create_task(
    description="创建产品定价页面，包含试用版/专业版/企业版对比",
    priority=TaskPriority.HIGH,
    task_type="content_create"
)
print(f"✅ 任务5: {task5.task_id}")
print(f"   描述: {task5.description}")

# ========== 统计 ==========

print("\n" + "=" * 60)
print("📊 任务统计")
print("=" * 60)

stats = manager.get_stats()
print(f"总任务数: {stats['total_tasks']}")
print(f"按优先级: {stats['by_priority']}")
print(f"按状态: {stats['by_status']}")

# ========== 任务清单 ==========

print("\n" + "=" * 60)
print("📋 任务清单")
print("=" * 60)

todos = manager.todos()
for i, todo in enumerate(todos, 1):
    print(f"\n{i}. [{todo['priority']}] {todo['description']}")
    print(f"   任务ID: {todo['task_id']}")
    print(f"   状态: {todo['status']}")
    print(f"   宫位: {todo['palaces']}")

# ========== 余总配合事项 ==========

print("\n" + "=" * 60)
print("👤 余总配合事项")
print("=" * 60)

print("""
1. 支付配置
   - 微信支付商户号 OR 支付宝商家账号
   - 收款二维码（已有：/root/taiji-api-v2/docs/wechat-pay.jpg）

2. 内容审核
   - API文档内容确认
   - 官网文案确认
   - 定价策略确认

3. 账号准备
   - 公众号/视频号（用于发布文章）
   - GitHub/Gitee（代码仓库）
   - ClawCities（AI站点：https://clawcities.com/sites/milo-taiji）

4. 品牌资产
   - Logo/视觉设计（如需要）
   - 品牌口号确认
""")

# ========== 保存任务 ==========

print("\n" + "=" * 60)
print("💾 任务已保存")
print("=" * 60)

print(f"存储位置: /root/.openclaw/workspace/skills/taiji-nine-palaces/data/tasks.json")
print("\n✅ 任务生成完成！米珞待命，等待余总指令！")

# 导出任务列表
export_data = {
    "generated_at": "2026-03-21T01:14:00",
    "total_tasks": len(todos),
    "tasks": todos,
    "yu_zong_actions": [
        "提供支付账号信息",
        "确认定价策略",
        "审核官网文案",
        "准备发布渠道"
    ]
}

with open("/root/.openclaw/workspace/skills/taiji-nine-palaces/data/week1_tasks.json", "w") as f:
    json.dump(export_data, f, ensure_ascii=False, indent=2)

print(f"\n📄 任务导出: data/week1_tasks.json")