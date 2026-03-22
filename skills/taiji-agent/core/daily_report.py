#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
米珞日报生成器

生成每日任务状态报告
"""

from datetime import datetime
from typing import Dict, Any, List
import json
import sys
import os

# 添加父目录
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.task_manager import get_task_manager, TaskStatus, TaskPriority


class DailyReportGenerator:
    """米珞日报生成器"""
    
    def __init__(self):
        self.tm = get_task_manager()
    
    def generate(self) -> Dict[str, Any]:
        """生成日报"""
        
        # 基本信息
        now = datetime.now()
        weekdays = ["一", "二", "三", "四", "五", "六", "日"]
        
        report = {
            "title": "米珞日报",
            "date": f"{now.year}年{now.month}月{now.day}日 星期{weekdays[now.weekday()]}",
            "generated_at": now.isoformat(),
        }
        
        # 系统状态
        status = self.tm.get_system_status()
        report["system_status"] = {
            "alive_palaces": status["alive_palaces"],
            "total_palaces": status["total_palaces"],
            "status_icon": "🟢" if status["status"] == "alive" else "🔴",
            "status_text": "活着" if status["status"] == "alive" else "死亡",
        }
        
        # 任务统计
        report["task_stats"] = {
            "total": status["total_tasks"],
            "pending": status["total_pending_tasks"],
            "in_progress": 0,
            "completed": status["total_completed_tasks"],
            "blocked": 0,
        }
        
        # 计算进行中和阻塞
        for queue in self.tm.queues.values():
            for task in queue.tasks:
                if task.status == TaskStatus.IN_PROGRESS:
                    report["task_stats"]["in_progress"] += 1
                elif task.status == TaskStatus.BLOCKED:
                    report["task_stats"]["blocked"] += 1
        
        # 各宫任务概览
        report["palace_overview"] = {}
        for p_id, queue in self.tm.queues.items():
            pending_tasks = [t for t in queue.tasks if t.status.value == "pending"]
            in_progress_tasks = [t for t in queue.tasks if t.status.value == "in_progress"]
            completed_tasks = [t for t in queue.tasks if t.status.value == "completed"]
            
            report["palace_overview"][str(p_id)] = {
                "name": queue.palace_name,
                "is_alive": queue.is_alive(),
                "total": len(queue.tasks),
                "pending": len(pending_tasks),
                "in_progress": len(in_progress_tasks),
                "completed": len(completed_tasks),
                "current_task": queue.get_active_task().title if queue.get_active_task() else (
                    queue.get_next_task().title if queue.get_next_task() else None
                ),
            }
        
        # 今日要事（进行中的任务）
        report["today_focus"] = []
        for queue in self.tm.queues.values():
            active = queue.get_active_task()
            if active:
                report["today_focus"].append({
                    "palace": queue.palace_name,
                    "task": active.title,
                    "priority": active.priority.name,
                })
        
        # 高优先级待办
        report["high_priority"] = []
        for queue in self.tm.queues.values():
            for task in queue.tasks:
                if task.status == TaskStatus.PENDING and task.priority in [TaskPriority.CRITICAL, TaskPriority.HIGH]:
                    report["high_priority"].append({
                        "task_id": task.task_id,
                        "title": task.title,
                        "palace": queue.palace_name,
                        "priority": task.priority.name,
                        "source": task.source.value,
                    })
        
        return report
    
    def to_markdown(self) -> str:
        """转换为Markdown格式"""
        report = self.generate()
        
        lines = [
            f"# {report['title']}",
            f"**{report['date']}**",
            "",
            f"### {report['system_status']['status_icon']} 活着的宫位: {report['system_status']['alive_palaces']}/{report['system_status']['total_palaces']}",
            "",
            "### 📊 任务统计",
            "",
            f"| 状态 | 数量 |",
            f"|------|------|",
            f"| 总任务 | {report['task_stats']['total']} |",
            f"| 待办 | {report['task_stats']['pending']} |",
            f"| 进行中 | {report['task_stats']['in_progress']} |",
            f"| 已完成 | {report['task_stats']['completed']} |",
            f"| 阻塞 | {report['task_stats']['blocked']} |",
            "",
            "### 📋 各宫任务概览",
            "",
        ]
        
        for p_id_str, overview in report["palace_overview"].items():
            status_icon = "🟢" if overview["is_alive"] else "🔴"
            lines.append(f"**{p_id_str}宫 {overview['name']}** {status_icon}")
            lines.append(f"- 待办: {overview['pending']} | 进行中: {overview['in_progress']} | 已完成: {overview['completed']}")
            if overview["current_task"]:
                lines.append(f"- 当前: {overview['current_task']}")
            lines.append("")
        
        if report["high_priority"]:
            lines.append("### ⚠️ 高优先级待办")
            lines.append("")
            for task in report["high_priority"][:5]:  # 只显示前5个
                lines.append(f"- [{task['priority']}] {task['title']} ({task['palace']})")
            lines.append("")
        
        return "\n".join(lines)


def generate_daily_report() -> Dict[str, Any]:
    """生成日报（便捷函数）"""
    generator = DailyReportGenerator()
    return generator.generate()


def generate_daily_report_markdown() -> str:
    """生成Markdown日报"""
    generator = DailyReportGenerator()
    return generator.to_markdown()


if __name__ == "__main__":
    print(generate_daily_report_markdown())