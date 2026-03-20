#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太极协作会议系统

让9宫真正协作：
1. 共享状态
2. 协商任务
3. 协调执行
4. 同步结果

开会流程：
1. 各宫报告状态
2. 协商任务分配
3. 协调执行顺序
4. 同步完成结果
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.taiji_l0_protocol import get_l0_registry
from core.task_manager import get_task_manager, TaskStatus


@dataclass
class PalaceReport:
    """宫位报告"""
    palace_id: int
    palace_name: str
    status: str
    pending_tasks: int
    active_task: Optional[str]
    need_help: bool
    can_help: List[str]
    request: Optional[str] = None


@dataclass
class MeetingAgenda:
    """会议议程"""
    meeting_id: str
    start_time: str
    reports: List[PalaceReport] = field(default_factory=list)
    decisions: List[Dict] = field(default_factory=list)
    task_handoffs: List[Dict] = field(default_factory=list)


class TaijiMeeting:
    """太极协作会议"""
    
    def __init__(self):
        self.registry = get_l0_registry()
        self.tm = get_task_manager()
        self.meeting_count = 0
    
    def call_meeting(self) -> MeetingAgenda:
        """召集会议"""
        self.meeting_count += 1
        meeting_id = f"meeting_{self.meeting_count}"
        
        agenda = MeetingAgenda(
            meeting_id=meeting_id,
            start_time=datetime.now().isoformat()
        )
        
        # 1. 各宫报告
        agenda.reports = self._collect_reports()
        
        # 2. 协商决策
        agenda.decisions = self._negotiate(agenda.reports)
        
        # 3. 任务交接
        agenda.task_handoffs = self._coordinate(agenda.decisions)
        
        return agenda
    
    def _collect_reports(self) -> List[PalaceReport]:
        """各宫报告状态"""
        reports = []
        
        for p_id, palace in self.registry.palaces.items():
            queue = self.tm.queues[p_id]
            pending = queue.get_pending_count()
            active = queue.get_active_task()
            
            report = PalaceReport(
                palace_id=p_id,
                palace_name=palace.name,
                status=palace.mind.rotation.value,
                pending_tasks=pending,
                active_task=active.title if active else None,
                need_help=pending > 5,
                can_help=palace.outputs.copy()
            )
            reports.append(report)
        
        return reports
    
    def _negotiate(self, reports: List[PalaceReport]) -> List[Dict]:
        """协商决策"""
        decisions = []
        
        # 找需要帮助的宫
        overloaded = [r for r in reports if r.need_help]
        available = [r for r in reports if not r.need_help]
        
        # 任务转移
        for report in overloaded[:3]:  # 最多处理3个
            for other in available:
                decisions.append({
                    "action": "transfer",
                    "from": report.palace_id,
                    "to": other.palace_id,
                    "reason": f"{report.palace_name}过载"
                })
                break
        
        # 协作识别
        for report in reports:
            if report.active_task:
                palace = self.registry.palaces[report.palace_id]
                for collab_id in palace.collaborators:
                    decisions.append({
                        "action": "collaborate",
                        "palace1": report.palace_id,
                        "palace2": collab_id,
                        "task": report.active_task[:20]
                    })
                    break
        
        return decisions
    
    def _coordinate(self, decisions: List[Dict]) -> List[Dict]:
        """执行协调"""
        handoffs = []
        
        for d in decisions[:3]:
            if d["action"] == "transfer":
                handoffs.append({
                    "from": d["from"],
                    "to": d["to"],
                    "status": "已转移"
                })
            elif d["action"] == "collaborate":
                # 启动协作任务
                p2_queue = self.tm.queues[d["palace2"]]
                for task in p2_queue.tasks:
                    if task.status == TaskStatus.PENDING:
                        self.tm.start_task(task.task_id)
                        handoffs.append({
                            "palace": d["palace2"],
                            "started": task.title[:20]
                        })
                        break
        
        self.tm.save()
        return handoffs
    
    def summary(self, agenda: MeetingAgenda) -> str:
        """会议摘要"""
        lines = [
            f"=== 协作会议 #{self.meeting_count} ===",
            f"时间: {agenda.start_time[:19]}",
            "",
            "【各宫报告】"
        ]
        
        for r in agenda.reports:
            icon = "🟢" if r.status == "forward" else "🔴"
            help_flag = " ⚠️" if r.need_help else ""
            lines.append(f"  {r.palace_id}宫 {icon} {r.pending_tasks}任务{help_flag}")
        
        if agenda.decisions:
            lines.append("")
            lines.append("【协商结果】")
            for d in agenda.decisions[:3]:
                if d["action"] == "transfer":
                    lines.append(f"  {d['from']}宫 → {d['to']}宫 转移任务")
                elif d["action"] == "collaborate":
                    lines.append(f"  {d['palace1']}宫 ↔ {d['palace2']}宫 协作")
        
        return "\n".join(lines)


# ========== 便捷函数 ==========

def call_meeting() -> str:
    """开会"""
    meeting = TaijiMeeting()
    agenda = meeting.call_meeting()
    return meeting.summary(agenda)


if __name__ == "__main__":
    print(call_meeting())