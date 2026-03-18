#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动任务生成与调节引擎
Automatic Task Generation and Regulation Engine

核心能力：
1. 基于阴阳失衡自动生成调节任务
2. 根据四象阶段动态调整任务优先级
3. 五行循环验证任务执行效果
4. 九宫格负载均衡分配
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
import uuid


class TaskPriority(Enum):
    """任务优先级"""
    CRITICAL = "紧急重要"  # 阴阳严重失衡
    HIGH = "高"          # 单点过载
    MEDIUM = "中"        # 预防性任务
    LOW = "低"           # 优化性任务


class TaskType(Enum):
    """任务类型"""
    BALANCE_RESTORATION = "平衡恢复"
    LOAD_TRANSFER = "负载转移"
    BOTTLENECK_RESOLUTION = "瓶颈解决"
    PREVENTIVE_MAINTENANCE = "预防维护"
    OPTIMIZATION = "优化改进"


class AutoTaskGenerator:
    """
    自动任务生成器
    
    根据系统状态自动生成调节任务
    """
    
    def __init__(self):
        self.generated_tasks = []
        self.task_templates = self._load_task_templates()
        
    def _load_task_templates(self) -> Dict[TaskType, Dict]:
        """加载任务模板"""
        return {
            TaskType.BALANCE_RESTORATION: {
                "title": "恢复{pair_name}的阴阳平衡",
                "description": "检测到{pair_name}平衡度为{balance:.2f}（低于 0.7），需要采取措施恢复平衡",
                "actions": [
                    "分析{palace1}和{palace2}的当前负载差异",
                    "识别导致失衡的根本原因",
                    "制定负载重新分配方案",
                    "执行平衡调节措施",
                    "监控平衡度变化直到恢复正常"
                ],
                "success_criteria": "平衡度提升至 0.8 以上"
            },
            TaskType.LOAD_TRANSFER: {
                "title": "减轻{palace_name}宫的负载压力",
                "description": "{palace_name}宫当前负载为{load:.0%}（超过 0.8），需要分散负载",
                "actions": [
                    "梳理{palace_name}宫当前所有任务",
                    "识别可转移的任务清单",
                    "寻找可用的空闲宫位",
                    "执行任务转移",
                    "验证负载下降效果"
                ],
                "success_criteria": "负载降至 0.7 以下"
            },
            TaskType.BOTTLENECK_RESOLUTION: {
                "title": "解决系统瓶颈：{bottleneck}",
                "description": "检测到系统瓶颈：{bottleneck}，已影响整体效率",
                "actions": [
                    "成立专项攻关小组",
                    "深入分析瓶颈根因",
                    "设计解决方案并评估",
                    "实施方案并监控效果",
                    "总结经验防止复发"
                ],
                "success_criteria": "瓶颈消除，系统流畅运行"
            },
            TaskType.PREVENTIVE_MAINTENANCE: {
                "title": "对{palace_name}宫进行预防性维护",
                "description": "{palace_name}宫效率呈下降趋势（当前{efficiency:.0%}），需提前干预",
                "actions": [
                    "检查该宫位的资源配置",
                    "评估工作流程合理性",
                    "收集相关干系人反馈",
                    "实施优化措施",
                    "跟踪效率改善情况"
                ],
                "success_criteria": "效率稳定在 0.85 以上"
            },
            TaskType.OPTIMIZATION: {
                "title": "优化{target}的工作流程",
                "description": "发现{target}存在优化空间，预计可提升效率{improvement:.0%}",
                "actions": [
                    "绘制当前工作流程图",
                    "识别浪费和低效环节",
                    "设计优化后的新流程",
                    "小范围试点验证",
                    "全面推广并标准化"
                ],
                "success_criteria": "整体效率提升 15% 以上"
            }
        }
    
    def generate_tasks_from_balance_analysis(
        self, 
        balance_system: Any,
        palace_states: Dict
    ) -> List[Dict]:
        """
        从阴阳平衡分析生成任务
        
        Args:
            balance_system: 九宫格平衡系统实例
            palace_states: 各宫位状态
            
        Returns:
            生成的任务列表
        """
        tasks = []
        
        # 检查阴阳失衡对
        imbalanced_pairs = balance_system.get_imbalanced_pairs()
        for imbalance in imbalanced_pairs:
            pair_name = imbalance["pair"]
            balance = imbalance["balance"]
            palaces = imbalance["palaces"]
            
            if balance < 0.5:
                priority = TaskPriority.CRITICAL
            elif balance < 0.7:
                priority = TaskPriority.HIGH
            else:
                priority = TaskPriority.MEDIUM
            
            template = self.task_templates[TaskType.BALANCE_RESTORATION]
            
            task = {
                "id": str(uuid.uuid4())[:8],
                "type": TaskType.BALANCE_RESTORATION.value,
                "priority": priority.value,
                "title": template["title"].format(pair_name=pair_name),
                "description": template["description"].format(
                    pair_name=pair_name, 
                    balance=balance
                ),
                "actions": [
                    action.format(
                        pair_name=pair_name,
                        palace1=palace_states[palaces[0]]["name"],
                        palace2=palace_states[palaces[1]]["name"]
                    )
                    for action in template["actions"]
                ],
                "success_criteria": template["success_criteria"],
                "metadata": {
                    "pair": pair_name,
                    "palaces": palaces,
                    "current_balance": balance
                },
                "created_at": datetime.now().isoformat(),
                "status": "待执行"
            }
            
            tasks.append(task)
            print(f"   ✓ 生成平衡恢复任务：{task['title']} (优先级：{priority.value})")
        
        return tasks
    
    def generate_tasks_from_palace_loads(
        self,
        palace_states: Dict
    ) -> List[Dict]:
        """
        从宫位负载生成任务
        
        Args:
            palace_states: 各宫位状态
            
        Returns:
            生成的任务列表
        """
        tasks = []
        
        for palace_id, state in palace_states.items():
            load = state.get("load", 0)
            efficiency = state.get("efficiency", 1.0)
            
            # 过载宫位
            if load > 0.8:
                priority = TaskPriority.CRITICAL if load > 0.9 else TaskPriority.HIGH
                
                template = self.task_templates[TaskType.LOAD_TRANSFER]
                
                task = {
                    "id": str(uuid.uuid4())[:8],
                    "type": TaskType.LOAD_TRANSFER.value,
                    "priority": priority.value,
                    "title": template["title"].format(palace_name=state["name"]),
                    "description": template["description"].format(
                        palace_name=state["name"],
                        load=load
                    ),
                    "actions": [
                        action.format(palace_name=state["name"])
                        for action in template["actions"]
                    ],
                    "success_criteria": template["success_criteria"],
                    "metadata": {
                        "palace_id": palace_id,
                        "current_load": load
                    },
                    "created_at": datetime.now().isoformat(),
                    "status": "待执行"
                }
                
                tasks.append(task)
                print(f"   ✓ 生成负载转移任务：{task['title']} (优先级：{priority.value})")
            
            # 效率下降预警
            elif efficiency < 0.75 and load > 0.5:
                template = self.task_templates[TaskType.PREVENTIVE_MAINTENANCE]
                
                task = {
                    "id": str(uuid.uuid4())[:8],
                    "type": TaskType.PREVENTIVE_MAINTENANCE.value,
                    "priority": TaskPriority.MEDIUM.value,
                    "title": template["title"].format(palace_name=state["name"]),
                    "description": template["description"].format(
                        palace_name=state["name"],
                        efficiency=efficiency
                    ),
                    "actions": [
                        action.format(palace_name=state["name"])
                        for action in template["actions"]
                    ],
                    "success_criteria": template["success_criteria"],
                    "metadata": {
                        "palace_id": palace_id,
                        "current_efficiency": efficiency
                    },
                    "created_at": datetime.now().isoformat(),
                    "status": "待执行"
                }
                
                tasks.append(task)
                print(f"   ✓ 生成预防维护任务：{task['title']}")
        
        return tasks
    
    def generate_optimization_tasks(
        self,
        strategic_report: Dict
    ) -> List[Dict]:
        """
        从战略报告生成优化任务
        
        Args:
            strategic_report: 战略分析报告
            
        Returns:
            生成的任务列表
        """
        tasks = []
        
        recommendations = strategic_report.get("recommendations", [])
        for i, rec in enumerate(recommendations, 1):
            template = self.task_templates[TaskType.OPTIMIZATION]
            
            task = {
                "id": str(uuid.uuid4())[:8],
                "type": TaskType.OPTIMIZATION.value,
                "priority": TaskPriority.LOW.value,
                "title": f"落实战略建议 #{i}: {rec[:30]}...",
                "description": f"根据战略分析报告第{i}条建议：{rec}",
                "actions": template["actions"],
                "success_criteria": template["success_criteria"],
                "metadata": {
                    "source": "strategic_analysis",
                    "recommendation": rec
                },
                "created_at": datetime.now().isoformat(),
                "status": "待执行"
            }
            
            tasks.append(task)
            print(f"   ✓ 生成优化任务：{task['title']}")
        
        return tasks


class TaskRegulator:
    """
    任务调节器
    
    根据四象阶段和五行循环动态调节任务
    """
    
    def __init__(self):
        self.task_queue = []
        self.completed_tasks = []
        
    def add_tasks(self, tasks: List[Dict]):
        """添加任务到队列"""
        for task in tasks:
            self.task_queue.append(task)
        print(f"   ✓ 添加 {len(tasks)} 个任务到队列")
    
    def prioritize_by_four_symbols(self, current_stage: str):
        """
        根据四象阶段重新排列任务优先级
        
        Four Symbols stages:
        - Planning: 规划类任务优先
        - Daily: 执行类任务优先
        - Review: 评审类任务优先
        - Retro: 改进类任务优先
        """
        stage_priorities = {
            "PLANNING": ["BALANCE_RESTORATION", "LOAD_TRANSFER"],
            "DAILY": ["BOTTLENECK_RESOLUTION", "PREVENTIVE_MAINTENANCE"],
            "REVIEW": ["OPTIMIZATION"],
            "RETRO": ["OPTIMIZATION", "PREVENTIVE_MAINTENANCE"]
        }
        
        priority_order = stage_priorities.get(current_stage, [])
        
        # 重新排序任务队列
        def sort_key(task):
            task_type = task.get("type", "")
            if any(pt in task_type for pt in priority_order):
                return 0
            return 1
        
        self.task_queue.sort(key=sort_key)
        print(f"   ✓ 按四象阶段 ({current_stage}) 重新排序任务队列")
    
    def regulate_by_wuxing(self, current_element: str):
        """
        根据五行元素调节任务执行策略
        
        Five Elements:
        - 金：收敛 - 专注完成已有任务，不新增
        - 水：流动 - 快速流转，清理阻塞
        - 木：生长 - 允许新增优化任务
        - 火：发散 - 并行执行多个任务
        - 土：承载 - 沉淀经验，暂停新任务
        """
        strategies = {
            "金": {"new_tasks": False, "parallel": 1, "focus": "completion"},
            "水": {"new_tasks": False, "parallel": 2, "focus": "flow"},
            "木": {"new_tasks": True, "parallel": 2, "focus": "growth"},
            "火": {"new_tasks": True, "parallel": 5, "focus": "expansion"},
            "土": {"new_tasks": False, "parallel": 1, "focus": "consolidation"}
        }
        
        strategy = strategies.get(current_element, strategies["金"])
        
        print(f"   ✓ 五行策略 ({current_element}): "
              f"新增任务={strategy['new_tasks']}, "
              f"并行数={strategy['parallel']}, "
              f"焦点={strategy['focus']}")
        
        return strategy
    
    def get_next_task(self, wuxing_strategy: Dict) -> Optional[Dict]:
        """
        获取下一个要执行的任务
        
        Args:
            wuxing_strategy: 五行策略配置
            
        Returns:
            下一个任务或 None
        """
        if not self.task_queue:
            return None
        
        # 根据并行度限制
        active_count = sum(1 for t in self.task_queue if t.get("status") == "执行中")
        if active_count >= wuxing_strategy["parallel"]:
            return None
        
        # 返回第一个待执行任务
        for task in self.task_queue:
            if task["status"] == "待执行":
                task["status"] = "执行中"
                task["started_at"] = datetime.now().isoformat()
                return task
        
        return None
    
    def complete_task(self, task_id: str, result: Dict):
        """
        完成任务
        
        Args:
            task_id: 任务 ID
            result: 执行结果
        """
        for i, task in enumerate(self.task_queue):
            if task["id"] == task_id:
                task["status"] = "已完成"
                task["completed_at"] = datetime.now().isoformat()
                task["result"] = result
                
                completed_task = self.task_queue.pop(i)
                self.completed_tasks.append(completed_task)
                
                print(f"   ✓ 任务 {task_id} 完成")
                break
    
    def get_queue_status(self) -> Dict:
        """获取队列状态"""
        return {
            "total": len(self.task_queue),
            "pending": sum(1 for t in self.task_queue if t["status"] == "待执行"),
            "running": sum(1 for t in self.task_queue if t["status"] == "执行中"),
            "completed": len(self.completed_tasks)
        }


def demo_auto_task_generation():
    """演示自动任务生成与调节"""
    print("="*60)
    print("自动任务生成与调节引擎演示".center(60))
    print("="*60)
    
    # 模拟系统数据
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    from taiji_logic_engine import NinePalacesBalance
    
    balance_system = NinePalacesBalance()
    
    # 设置一些失衡场景
    palace_states = {
        1: {"name": "采集", "load": 0.3, "efficiency": 0.9},
        2: {"name": "产品", "load": 0.6, "efficiency": 0.85},
        3: {"name": "技术", "load": 0.95, "efficiency": 0.6},  # 过载
        4: {"name": "团队", "load": 0.4, "efficiency": 0.8},
        5: {"name": "中宫", "load": 0.5, "efficiency": 0.9},
        6: {"name": "质量", "load": 0.3, "efficiency": 0.85},  # 与技术失衡
        7: {"name": "监控", "load": 0.7, "efficiency": 0.8},
        8: {"name": "安全", "load": 0.5, "efficiency": 0.9},
        9: {"name": "生态", "load": 0.4, "efficiency": 0.85}
    }
    
    # 更新负载以触发失衡
    for palace_id, state in palace_states.items():
        balance_system.update_load(palace_id, state["load"])
    
    print("\n【步骤 1】从阴阳平衡分析生成任务...")
    generator = AutoTaskGenerator()
    balance_tasks = generator.generate_tasks_from_balance_analysis(
        balance_system, palace_states
    )
    
    print("\n【步骤 2】从宫位负载生成任务...")
    load_tasks = generator.generate_tasks_from_palace_loads(palace_states)
    
    # 初始化调节器
    regulator = TaskRegulator()
    all_tasks = balance_tasks + load_tasks
    regulator.add_tasks(all_tasks)
    
    print(f"\n【汇总】共生成 {len(all_tasks)} 个自动任务")
    
    print("\n【步骤 3】按四象阶段排序任务...")
    regulator.prioritize_by_four_symbols("DAILY")
    
    print("\n【步骤 4】根据五行策略执行任务...")
    wuxing_strategy = regulator.regulate_by_wuxing("木")
    
    # 模拟执行几个任务
    for _ in range(3):
        task = regulator.get_next_task(wuxing_strategy)
        if task:
            print(f"   → 执行任务：{task['title']}")
            regulator.complete_task(task["id"], {"success": True})
    
    print("\n【队列状态】")
    status = regulator.get_queue_status()
    print(f"   总计：{status['total']}")
    print(f"   待执行：{status['pending']}")
    print(f"   执行中：{status['running']}")
    print(f"   已完成：{status['completed']}")
    
    print("\n" + "="*60)
    print("演示完成".center(60))
    print("="*60)


if __name__ == "__main__":
    demo_auto_task_generation()
