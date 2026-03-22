#!/usr/bin/env python3
"""
5 宫 - 中央控制 · 中枢指挥模块

核心职责:
1. 与余总对话（感知意图）
2. 监控九宫状态（感知系统）
3. 任务优先级排序（决策）
4. 按需调配宫位（指挥）
5. 任务闭环管理（红灯→执行→绿灯→交付）
"""

import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

TAIJI_API_URL = "http://localhost:8000"


class TaskPriority(Enum):
    """任务优先级"""
    CRITICAL = 1  # 紧急且重要
    HIGH = 2      # 重要不紧急
    MEDIUM = 3    # 紧急不重要
    LOW = 4       # 不紧急不重要


class TaskStatus(Enum):
    """任务状态"""
    RED = "red"      # 未开始/失败
    RUNNING = "running"  # 执行中
    GREEN = "green"  # 通过
    DELIVERED = "delivered"  # 已交付


class Palace5Commander:
    """5 宫指挥官类"""
    
    def __init__(self, api_url: str = TAIJI_API_URL):
        self.api_url = api_url
        self.active_tasks: Dict[str, Dict[str, Any]] = {}
        self.palace_load_history: List[Dict[str, Any]] = []
    
    # ========== 感知层 ==========
    
    def get_palace_states(self) -> Dict[str, Any]:
        """获取九宫格状态"""
        try:
            response = requests.get(f"{self.api_url}/api/taiji/palaces", timeout=5)
            if response.status_code == 200:
                return response.json().get("palaces", {})
        except Exception as e:
            return {"error": str(e)}
        return {}
    
    def get_balance_status(self) -> Dict[str, Any]:
        """获取阴阳平衡状态"""
        try:
            response = requests.get(f"{self.api_url}/api/taiji/balance", timeout=5)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return {}
    
    def detect_imbalances(self) -> List[str]:
        """检测失衡宫位"""
        balance = self.get_balance_status()
        imbalanced = balance.get("imbalanced_pairs", [])
        
        warnings = []
        # imbalanced_pairs 可能是列表或字典
        if isinstance(imbalanced, list):
            for pair in imbalanced:
                warnings.append(f"⚠️ {pair} 失衡")
        elif isinstance(imbalanced, dict):
            for pair, value in imbalanced.items():
                if value < 0.6:
                    warnings.append(f"⚠️ {pair} 失衡：{value:.2f}")
        
        return warnings
    
    def get_available_palaces(self, min_capacity: float = 0.3) -> List[int]:
        """获取可用宫位（负载<0.7）"""
        palaces = self.get_palace_states()
        available = []
        
        for pid, pdata in palaces.items():
            load = pdata.get("load", 1.0)
            if load < 0.7:
                available.append(int(pid))
        
        return available
    
    # ========== 决策层 ==========
    
    def prioritize_task(self, task_description: str, context: Optional[Dict] = None) -> TaskPriority:
        """
        任务优先级判断
        
        规则:
        - 余总直接指令 → CRITICAL
        - 涉及多个宫位 → HIGH
        - 单一宫位 → MEDIUM
        - 可延后 → LOW
        """
        # 简单规则：包含"现在"、"立刻"、"马上" → CRITICAL
        critical_keywords = ["现在", "立刻", "马上", "紧急", "优先"]
        if any(kw in task_description for kw in critical_keywords):
            return TaskPriority.CRITICAL
        
        # 包含"今天"、"今天内" → HIGH
        high_keywords = ["今天", "今天内", "尽快"]
        if any(kw in task_description for kw in high_keywords):
            return TaskPriority.HIGH
        
        return TaskPriority.MEDIUM
    
    def assign_palaces(self, task_type: str) -> List[int]:
        """
        根据任务类型分配宫位
        
        返回宫位 ID 列表（按参与顺序）
        """
        # 任务类型 → 宫位映射
        task_palace_map = {
            "video_process": [1, 7, 5],      # 数据采集 → TDD 验收 → 中宫交付
            "file_download": [1, 7, 5],       # 下载 → 验收 → 交付
            "data_analysis": [1, 3, 7, 5],    # 采集 → 分析 → 验收 → 交付
            "skill_install": [3, 7, 5],       # 技术 → 验收 → 交付
            "content_create": [4, 8, 7, 5],   # 品牌 → 营销 → 验收 → 交付
            "monitoring": [6, 9, 5],          # 监控 → 生态 → 交付
            "legal_compliance": [7, 5],       # 法务 → 交付
            "general": [5]                    # 通用 → 中宫协调
        }
        
        return task_palace_map.get(task_type, [5])
    
    # ========== 指挥层 ==========
    
    def create_task(self, task_id: str, description: str, priority: TaskPriority,
                    assigned_palaces: List[int]) -> Dict[str, Any]:
        """创建任务"""
        task = {
            "task_id": task_id,
            "description": description,
            "priority": priority.name,
            "assigned_palaces": assigned_palaces,
            "status": TaskStatus.RED.value,
            "created_at": datetime.now().isoformat(),
            "tdd_standards": None,
            "output": None
        }
        
        self.active_tasks[task_id] = task
        return task
    
    def invoke_palace(self, palace_id: int, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """调用宫位执行动作"""
        # 这里调用各宫位的 Python 模块
        # 简化版：直接返回成功
        return {
            "success": True,
            "palace_id": palace_id,
            "action": action,
            "result": params
        }
    
    def update_task_status(self, task_id: str, status: TaskStatus, output: Any = None):
        """更新任务状态"""
        if task_id in self.active_tasks:
            self.active_tasks[task_id]["status"] = status.value
            if output:
                self.active_tasks[task_id]["output"] = output
    
    # ========== 闭环管理 ==========
    
    def execute_task_with_tdd(self, task_id: str) -> Dict[str, Any]:
        """
        执行任务（带 TDD 闭环）
        
        流程:
        1. 红灯确认
        2. 7 宫定义验收标准
        3. 指挥执行
        4. 7 宫绿灯检查
        5. 交付或返工
        """
        task = self.active_tasks.get(task_id)
        if not task:
            return {"error": "Task not found"}
        
        result = {
            "task_id": task_id,
            "steps": []
        }
        
        # Step 1: 红灯确认
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from palace_7_tdd import Palace7TDD
        tdd = Palace7TDD()
        
        red_confirm = tdd.red_light_confirm(task["description"])
        result["steps"].append({"step": "red_confirm", "result": red_confirm})
        self.update_task_status(task_id, TaskStatus.RED)
        
        # Step 2: 7 宫定义验收标准
        task_type = self._infer_task_type(task["description"])
        standards = tdd.define_acceptance_criteria(task_type)
        task["tdd_standards"] = standards
        result["steps"].append({"step": "define_standards", "result": standards})
        
        # Step 3: 指挥执行（简化：直接标记为执行中）
        self.update_task_status(task_id, TaskStatus.RUNNING)
        result["steps"].append({"step": "execute", "message": "执行中..."})
        
        # Step 4: 绿灯检查（需要实际输出，这里用占位符）
        # 实际执行后调用
        result["steps"].append({
            "step": "green_check",
            "message": "待执行完成后调用 green_light_check"
        })
        
        return result
    
    def green_light_deliver(self, task_id: str, output: Any) -> Dict[str, Any]:
        """绿灯检查并交付"""
        task = self.active_tasks.get(task_id)
        if not task:
            return {"error": "Task not found"}
        
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from palace_7_tdd import Palace7TDD
        tdd = Palace7TDD()
        
        task_type = self._infer_task_type(task["description"])
        standards = task.get("tdd_standards")
        
        check_result = tdd.green_light_check(task_type, output, standards)
        
        if check_result["passed"]:
            self.update_task_status(task_id, TaskStatus.GREEN, output)
            self.update_task_status(task_id, TaskStatus.DELIVERED)
            
            # 更新宫位负载
            for palace_id in task["assigned_palaces"]:
                self._increase_palace_load(palace_id, 0.05)
            
            return {
                "status": "delivered",
                "check_result": check_result,
                "output": output
            }
        else:
            # 返工
            self.update_task_status(task_id, TaskStatus.RED)
            return {
                "status": "rework",
                "reasons": check_result["reasons"],
                "check_result": check_result
            }
    
    # ========== 工具方法 ==========
    
    def _infer_task_type(self, description: str) -> str:
        """从任务描述推断任务类型"""
        desc_lower = description.lower()
        
        if any(kw in desc_lower for kw in ["视频", "video", "抖音", "摘要"]):
            return "video_process"
        elif any(kw in desc_lower for kw in ["下载", "download", "文件"]):
            return "file_download"
        elif any(kw in desc_lower for kw in ["分析", "analysis", "数据"]):
            return "data_analysis"
        elif any(kw in desc_lower for kw in ["技能", "skill", "安装"]):
            return "skill_install"
        elif any(kw in desc_lower for kw in ["内容", "content", "创作"]):
            return "content_create"
        elif any(kw in desc_lower for kw in ["监控", "monitor", "监控"]):
            return "monitoring"
        elif any(kw in desc_lower for kw in ["法务", "legal", "合规"]):
            return "legal_compliance"
        
        return "general"
    
    def _increase_palace_load(self, palace_id: int, delta: float):
        """增加宫位负载"""
        try:
            current = self.get_palace_states().get(str(palace_id), {}).get("load", 0.5)
            new_load = min(1.0, current + delta)
            
            requests.post(
                f"{self.api_url}/api/taiji/update-palace-load",
                json={"palace_id": palace_id, "load": new_load},
                timeout=5
            )
        except:
            pass
    
    def get_task_report(self) -> Dict[str, Any]:
        """生成任务报告"""
        return {
            "active_tasks": len([t for t in self.active_tasks.values() 
                                if t["status"] not in [TaskStatus.DELIVERED.value]]),
            "completed_tasks": len([t for t in self.active_tasks.values() 
                                   if t["status"] == TaskStatus.DELIVERED.value]),
            "tasks": list(self.active_tasks.values())[-10:]  # 最近 10 个
        }


# ========== 余总对话接口 ==========

def handle_user_message(message: str) -> Dict[str, Any]:
    """
    处理余总消息
    
    这是 5 宫与余总对话的主入口
    """
    commander = Palace5Commander()
    
    # 1. 感知意图
    priority = commander.prioritize_task(message)
    
    # 2. 感知系统状态
    palaces = commander.get_palace_states()
    balance = commander.get_balance_status()
    warnings = commander.detect_imbalances()
    
    # 3. 决策
    task_type = commander._infer_task_type(message)
    assigned_palaces = commander.assign_palaces(task_type)
    
    # 4. 创建任务
    task_id = f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    task = commander.create_task(task_id, message, priority, assigned_palaces)
    
    # 5. 执行（带 TDD 闭环）
    execution = commander.execute_task_with_tdd(task_id)
    
    return {
        "task_id": task_id,
        "priority": priority.name,
        "assigned_palaces": assigned_palaces,
        "system_status": {
            "palaces": palaces,
            "balance": balance,
            "warnings": warnings
        },
        "execution": execution
    }


if __name__ == "__main__":
    # 测试示例
    print("=== 5 宫指挥官测试 ===\n")
    
    # 模拟余总指令
    test_message = "下载这个抖音视频并总结"
    
    result = handle_user_message(test_message)
    print(json.dumps(result, indent=2, ensure_ascii=False))
