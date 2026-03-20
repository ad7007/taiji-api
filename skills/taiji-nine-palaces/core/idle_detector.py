#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太极空闲检测与自完善任务生成器

每次心跳时：
1. 检测空闲宫位（无进行中任务）
2. 为空闲宫位生成自我完善任务
3. 确保所有宫位永远有任务（永不死亡）
"""

from typing import List, Dict
from core.task_manager import get_task_manager, TaskStatus, TaskPriority, TaskSource


# 各宫自我完善任务模板
SELF_IMPROVEMENT_TEMPLATES = {
    1: [
        "扫描新数据源，扩展数据覆盖",
        "清洗历史数据，提升数据质量",
        "更新数据字典，记录新增字段",
        "检查数据安全，修复潜在风险",
    ],
    2: [
        "优化产品文档，提升用户体验",
        "收集用户反馈，分析改进点",
        "设计新功能原型，验证可行性",
        "检查产品健康度，修复问题",
    ],
    3: [
        "重构核心代码，提升可维护性",
        "优化性能瓶颈，提升响应速度",
        "编写单元测试，提升覆盖率",
        "更新技术文档，同步最新架构",
        "检查代码规范，清理技术债务",
    ],
    4: [
        "分析竞品动态，更新竞争地图",
        "更新品牌定位，保持差异化",
        "策划新内容主题，储备素材",
        "检查品牌一致性，优化素材",
    ],
    5: [
        "检查系统健康，确保稳定运行",
        "优化调度算法，提升效率",
        "更新核心文档，同步最新状态",
        "检查各宫状态，识别瓶颈",
        "复盘近期决策，总结经验",
    ],
    6: [
        "检查监控告警，确保覆盖完整",
        "优化备份策略，确保数据安全",
        "性能基准测试，建立基线",
        "检查日志完整性，优化存储",
    ],
    7: [
        "审查代码规范，确保合规",
        "更新合规文档，同步法规变化",
        "风险评估，识别新风险",
        "检查测试覆盖率，补充用例",
    ],
    8: [
        "优化客服话术，提升转化率",
        "更新FAQ，覆盖新问题",
        "整理案例库，沉淀最佳实践",
        "检查用户反馈，发现改进点",
        "设计新营销素材，测试效果",
    ],
    9: [
        "研究行业新趋势，发现机会",
        "更新生态地图，保持同步",
        "寻找新合作伙伴，扩展网络",
        "分析政策变化，评估影响",
    ],
}


def detect_idle_palaces(tm=None) -> List[int]:
    """
    检测空闲宫位
    
    Args:
        tm: 任务管理器实例
    
    Returns:
        空闲宫位ID列表
    """
    if tm is None:
        tm = get_task_manager()
    
    idle = []
    for p_id, queue in tm.queues.items():
        # 检查是否有进行中或高优先级待办任务
        has_active = any(t.status == TaskStatus.IN_PROGRESS for t in queue.tasks)
        has_high_priority = any(
            t.status == TaskStatus.PENDING and t.priority in [TaskPriority.CRITICAL, TaskPriority.HIGH]
            for t in queue.tasks
        )
        
        if not has_active and not has_high_priority:
            idle.append(p_id)
    
    return idle


def generate_self_improvement_task(palace_id: int, existing_titles: List[str] = None) -> str:
    """
    为指定宫位生成自我完善任务
    
    Args:
        palace_id: 宫位ID
        existing_titles: 已存在的任务标题（避免重复）
    
    Returns:
        任务标题
    """
    if existing_titles is None:
        existing_titles = []
    
    templates = SELF_IMPROVEMENT_TEMPLATES.get(palace_id, ["自我检查", "优化流程"])
    
    # 找一个不重复的任务
    for title in templates:
        if title not in existing_titles:
            return title
    
    # 如果都重复了，加个时间戳
    import time
    return f"{templates[0]} (v{int(time.time()) % 1000})"


def ensure_all_palaces_busy(tm=None) -> Dict[int, str]:
    """
    确保所有宫位都有任务
    
    每次心跳调用此函数
    
    Returns:
        {宫位ID: 新增任务标题}
    """
    if tm is None:
        tm = get_task_manager()
    
    result = {}
    
    for p_id, queue in tm.queues.items():
        # 检查是否有任务（任何状态）
        has_any_task = len(queue.tasks) > 0
        
        # 检查是否有进行中任务
        has_active = any(t.status == TaskStatus.IN_PROGRESS for t in queue.tasks)
        
        if not has_active:
            # 没有进行中任务，生成自完善任务
            existing_titles = [t.title for t in queue.tasks]
            task_title = generate_self_improvement_task(p_id, existing_titles)
            
            tm.create_task(
                title=f"[自完善]{task_title}",
                palace_id=p_id,
                priority=TaskPriority.LOW,
                source=TaskSource.AUTO
            )
            result[p_id] = f"[自完善]{task_title}"
    
    if result:
        tm.save()
    
    return result


def heartbeat_ensure_alive() -> Dict:
    """
    心跳：确保所有宫位活着
    
    每次心跳调用
    """
    tm = get_task_manager()
    
    # 1. 检测空闲宫位
    idle = detect_idle_palaces(tm)
    
    # 2. 为空闲宫位生成任务
    new_tasks = ensure_all_palaces_busy(tm)
    
    # 3. 统计
    status = tm.get_system_status()
    
    return {
        "idle_palaces": idle,
        "new_tasks": new_tasks,
        "total_tasks": status["total_tasks"],
        "alive": status["alive_palaces"] == 9,
    }


# 测试
if __name__ == "__main__":
    print("=== 空闲检测与自完善任务生成测试 ===\n")
    
    result = heartbeat_ensure_alive()
    
    print(f"空闲宫位: {result['idle_palaces']}")
    print(f"新增任务: {result['new_tasks']}")
    print(f"总任务: {result['total_tasks']}")
    print(f"全部存活: {result['alive']}")