#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L4 规则层 - 5 宫指挥官与 7 宫 TDD 集成
Level 4 Rules - Palace 5 Commander & Palace 7 TDD Integration

实现:
1. 5 宫中枢指挥机制（感知→决策→调配→闭环）
2. 7 宫 TDD 验收机制（红灯→执行→绿灯→交付）
3. 任务自动优先级排序
4. 宫位动态调配规则
5. 阴阳平衡自适应调整
"""

from enum import Enum
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field
import time
import json
from loguru import logger

from core.palace_constants import get_palace_name, get_palace_element


# ========== 枚举定义 ==========

class TaskPriority(Enum):
    """任务优先级（L4 规则）"""
    CRITICAL = 1    # 紧急且重要 - 余总直接指令
    HIGH = 2        # 重要不紧急 - 今天内完成
    MEDIUM = 3      # 常规任务 - 普通指令
    LOW = 4         # 可延后 - 有空时处理


class TaskStatus(Enum):
    """任务状态（L4 规则）"""
    RED = "red"              # 未开始/失败 - 红灯
    RUNNING = "running"      # 执行中
    GREEN = "green"          # 通过 - 绿灯
    DELIVERED = "delivered"  # 已交付


class PalaceRole(Enum):
    """宫位角色（L4 规则）"""
    COMMANDER = 5    # 5 宫 - 中央控制（指挥官）
    TDD_GATE = 7     # 7 宫 - 法务框架（TDD 验收）
    DATA_COLLECTOR = 1  # 1 宫 - 数据采集
    TECH_TEAM = 3       # 3 宫 - 技术团队
    BRAND_STRATEGY = 4  # 4 宫 - 品牌战略
    PRODUCT_QUALITY = 2 # 2 宫 - 产品质量
    IOT_MONITOR = 6     # 6 宫 - 物联监控
    MARKETING = 8       # 8 宫 - 营销客服
    ECOLOGY = 9         # 9 宫 - 行业生态


# ========== 数据模型 ==========

@dataclass
class TDDStandard:
    """TDD 验收标准（L4 规则）"""
    name: str
    required: bool
    check: str
    passed: Optional[bool] = None


@dataclass
class TaskDefinition:
    """任务定义（L4 规则）"""
    task_id: str
    description: str
    priority: TaskPriority
    assigned_palaces: List[int]
    status: TaskStatus = TaskStatus.RED
    tdd_standards: List[TDDStandard] = field(default_factory=list)
    output: Any = None
    model_allocation: Optional[Dict[str, Any]] = None  # 3 宫模型分配
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    rework_count: int = 0
    
    def is_overdue(self) -> bool:
        """是否超时（默认 2 小时）"""
        if self.completed_at:
            return False
        elapsed = time.time() - self.created_at
        timeout_map = {
            TaskPriority.CRITICAL: 1800,    # 30 分钟
            TaskPriority.HIGH: 3600,        # 1 小时
            TaskPriority.MEDIUM: 7200,      # 2 小时
            TaskPriority.LOW: 14400         # 4 小时
        }
        return elapsed > timeout_map.get(self.priority, 7200)


@dataclass
class PalaceCapacity:
    """宫位容量（L4 规则）"""
    palace_id: int
    current_load: float
    max_capacity: float = 0.8  # 超过此值认为繁忙
    available: bool = True
    
    def update_availability(self):
        """更新可用性"""
        self.available = self.current_load < self.max_capacity


# ========== L4 规则引擎 ==========

class L4RuleEngine:
    """
    L4 规则引擎 - 5 宫指挥官与 7 宫 TDD 集成
    
    核心规则:
    1. 5 宫感知规则 - 监控九宫、检测失衡
    2. 5 宫决策规则 - 优先级判断、宫位分配
    3. 7 宫 TDD 规则 - 红灯确认、验收标准、绿灯检查
    4. 闭环管理规则 - 交付/返工
    5. 自适应规则 - 负载平衡、优先级动态调整
    """
    
    # ========== 规则配置 ==========
    
    # 任务类型 → 宫位映射规则
    TASK_PALACE_MAPPING = {
        "video_process": [1, 7, 5],       # 数据采集 → TDD 验收 → 中宫交付
        "file_download": [1, 7, 5],        # 下载 → 验收 → 交付
        "data_analysis": [1, 3, 7, 5],     # 采集 → 分析 → 验收 → 交付
        "skill_install": [3, 7, 5],        # 技术 → 验收 → 交付
        "content_create": [4, 8, 7, 5],    # 品牌 → 营销 → 验收 → 交付
        "monitoring": [6, 9, 5],           # 监控 → 生态 → 交付
        "legal_compliance": [7, 5],        # 法务 → 交付
        "general": [5]                     # 通用 → 中宫协调
    }
    
    # 任务类型推断关键词规则
    TASK_TYPE_KEYWORDS = {
        "video_process": ["视频", "video", "抖音", "摘要", "转录"],
        "file_download": ["下载", "download", "文件", "pdf", "配置"],
        "data_analysis": ["分析", "analysis", "数据", "统计", "报告"],
        "skill_install": ["技能", "skill", "安装", "插件"],
        "content_create": ["内容", "content", "创作", "文章", "文案"],
        "monitoring": ["监控", "monitor", "告警", "状态"],
        "legal_compliance": ["法务", "legal", "合规", "合同", "协议"]
    }
    
    # TDD 验收标准模板规则
    TDD_STANDARDS_TEMPLATES = {
        "video_process": [
            TDDStandard("核心方法论", True, "必须提取视频核心观点"),
            TDDStandard("可行动建议", True, "必须有具体行动项"),
            TDDStandard("关键数据/案例", True, "必须引用视频中的数据或案例"),
            TDDStandard("结构清晰", True, "必须有清晰的标题和分段"),
        ],
        "file_download": [
            TDDStandard("文件完整性", True, "文件大小>0 且格式正确"),
            TDDStandard("命名规范", True, "文件名包含任务名和时间戳"),
            TDDStandard("落盘位置", True, "保存到指定目录"),
        ],
        "data_analysis": [
            TDDStandard("数据来源", True, "必须说明数据来源"),
            TDDStandard("分析方法", True, "必须说明使用的分析方法"),
            TDDStandard("核心洞察", True, "必须有 3 条以上洞察"),
        ],
        "skill_install": [
            TDDStandard("技能来源", True, "必须说明来自 skillhub 或 clawhub"),
            TDDStandard("版本信息", True, "必须记录版本号"),
            TDDStandard("依赖检查", True, "必须检查并安装依赖"),
            TDDStandard("功能验证", True, "必须执行基本功能测试"),
        ]
    }
    
    # 优先级关键词规则
    PRIORITY_KEYWORDS = {
        TaskPriority.CRITICAL: ["现在", "立刻", "马上", "紧急", "优先", "立即"],
        TaskPriority.HIGH: ["今天", "今天内", "尽快", "优先处理"],
        TaskPriority.LOW: ["有空", "不着急", "延后", "下次"]
    }
    
    def __init__(self):
        self.tasks: Dict[str, TaskDefinition] = {}
        self.palace_capacities: Dict[int, PalaceCapacity] = {}
        self.tdd_node_states: Dict[str, Dict[str, Any]] = {}
        
        # 初始化宫位容量
        for i in range(1, 10):
            self.palace_capacities[i] = PalaceCapacity(palace_id=i, current_load=0.5)
        
        logger.info("L4 Rule Engine initialized")
    
    # ========== 规则 1: 5 宫感知规则 ==========
    
    def detect_task_priority(self, description: str) -> TaskPriority:
        """
        规则 1.1: 任务优先级检测
        
        基于关键词匹配判断优先级
        """
        desc_lower = description.lower()
        
        # 检查 CRITICAL 关键词
        for kw in self.PRIORITY_KEYWORDS[TaskPriority.CRITICAL]:
            if kw in description:
                return TaskPriority.CRITICAL
        
        # 检查 HIGH 关键词
        for kw in self.PRIORITY_KEYWORDS[TaskPriority.HIGH]:
            if kw in description:
                return TaskPriority.HIGH
        
        # 检查 LOW 关键词
        for kw in self.PRIORITY_KEYWORDS[TaskPriority.LOW]:
            if kw in description:
                return TaskPriority.LOW
        
        return TaskPriority.MEDIUM
    
    def infer_task_type(self, description: str) -> str:
        """
        规则 1.2: 任务类型推断
        
        基于关键词匹配推断任务类型
        """
        desc_lower = description.lower()
        
        for task_type, keywords in self.TASK_TYPE_KEYWORDS.items():
            if any(kw in desc_lower for kw in keywords):
                return task_type
        
        return "general"
    
    def get_available_palaces(self, min_capacity: float = 0.3) -> List[int]:
        """
        规则 1.3: 获取可用宫位
        
        返回负载<0.7 的宫位
        """
        available = []
        for pid, cap in self.palace_capacities.items():
            cap.update_availability()
            if cap.available and cap.current_load < 0.7:
                available.append(pid)
        return available
    
    def detect_imbalances(self, palace_loads: Dict[int, float]) -> List[str]:
        """
        规则 1.4: 检测阴阳失衡
        
        平衡对:
        - team_process: 4-5
        - tech_quality: 3-6
        - product_data: 2-1
        - monitor_eco: 7-9
        """
        balance_pairs = {
            "team_process": (4, 5),
            "tech_quality": (3, 6),
            "product_data": (2, 1),
            "monitor_eco": (7, 9)
        }
        
        warnings = []
        for pair_name, (p1, p2) in balance_pairs.items():
            load1 = palace_loads.get(p1, 0.5)
            load2 = palace_loads.get(p2, 0.5)
            
            if max(load1, load2) > 0:
                balance = min(load1, load2) / max(load1, load2)
                if balance < 0.6:
                    warnings.append(f"{pair_name}: {balance:.2f}")
        
        return warnings
    
    # ========== 规则 2: 5 宫决策规则 ==========
    
    def assign_palaces(self, task_type: str) -> List[int]:
        """
        规则 2.1: 宫位分配
        
        根据任务类型返回参与宫位列表
        """
        return self.TASK_PALACE_MAPPING.get(task_type, [5])
    
    def create_task(self, task_id: str, description: str) -> TaskDefinition:
        """
        规则 2.2: 创建任务
        
        自动推断优先级和分配宫位
        """
        priority = self.detect_task_priority(description)
        task_type = self.infer_task_type(description)
        assigned_palaces = self.assign_palaces(task_type)
        
        # 🆕 3 宫模型分配
        model_allocation = self._allocate_model(task_type, priority)
        
        task = TaskDefinition(
            task_id=task_id,
            description=description,
            priority=priority,
            assigned_palaces=assigned_palaces
        )
        
        # 附加模型分配信息
        task.model_allocation = model_allocation  # type: ignore
        
        self.tasks[task_id] = task
        logger.info(f"Created task {task_id}: {description[:50]}... Model: {model_allocation['model']}")
        
        return task
    
    def _allocate_model(self, task_type: str, priority: int) -> Dict[str, Any]:
        """
        3 宫模型分配
        
        调用 palace_3_model_allocator 模块
        """
        try:
            from core.palace_3_model_allocator import palace3_allocate_model
            return palace3_allocate_model(task_type, priority)
        except Exception as e:
            logger.warning(f"Model allocation failed: {e}, using default")
            return {
                "model": "qwen3.5-plus",
                "provider": "qwen",
                "access_mode": "api_token",
                "reason": "默认模型",
                "estimated_cost": 0.004,
                "estimated_time_seconds": 2.0
            }
    
    # ========== 规则 3: 7 宫 TDD 规则 ==========
    
    def red_light_confirm(self, task: TaskDefinition) -> Dict[str, Any]:
        """
        规则 3.1: 红灯确认
        
        确认任务未开始（失败状态）
        """
        return {
            "confirmed": True,
            "message": f"红灯确认：任务未开始 - {task.description[:50]}",
            "timestamp": datetime.now().isoformat(),
            "task_status": task.status.value
        }
    
    def define_tdd_standards(self, task: TaskDefinition) -> List[TDDStandard]:
        """
        规则 3.2: 定义 TDD 验收标准
        
        根据任务类型加载模板
        """
        task_type = self.infer_task_type(task.description)
        templates = self.TDD_STANDARDS_TEMPLATES.get(task_type, [])
        
        # 深拷贝避免修改模板
        standards = [
            TDDStandard(s.name, s.required, s.check)
            for s in templates
        ]
        
        task.tdd_standards = standards
        logger.info(f"Defined {len(standards)} TDD standards for task {task.task_id}")
        
        return standards
    
    def green_light_check(self, task: TaskDefinition, output: Any) -> Dict[str, Any]:
        """
        规则 3.3: 绿灯检查
        
        对照验收标准验证输出
        """
        if not task.tdd_standards:
            return {
                "passed": True,
                "message": "无验收标准，默认通过"
            }
        
        # 简化检查：基于输出长度和内容
        output_str = str(output) if not isinstance(output, str) else output
        output_len = len(output_str)
        
        failed_reasons = []
        
        for std in task.tdd_standards:
            passed = False
            
            # 简单规则检查
            if std.name == "结构清晰" and ("##" in output_str or "\n" in output_str):
                passed = True
            elif std.name == "核心方法论" and any(kw in output_str for kw in ["核心", "方法", "关键", "TDD", "测试"]):
                passed = True
            elif std.name == "文件完整性" and output_len > 100:
                passed = True
            elif std.name == "可行动建议" and any(kw in output_str for kw in ["建议", "行动", "步骤", "先", "然后"]):
                passed = True
            elif std.name == "关键数据/案例" and any(kw in output_str for kw in ["数据", "案例", "美元", "$", "一周", "工程师", "AI", "框架"]):
                passed = True
            elif output_len > 150:  # 默认规则
                passed = True
            
            std.passed = passed
            
            if not passed and std.required:
                failed_reasons.append(f"{std.name}: {std.check}")
        
        all_passed = len(failed_reasons) == 0
        
        return {
            "passed": all_passed,
            "reasons": failed_reasons,
            "details": [
                {"name": s.name, "passed": s.passed, "check": s.check}
                for s in task.tdd_standards
            ],
            "timestamp": datetime.now().isoformat()
        }
    
    # ========== 规则 4: 闭环管理规则 ==========
    
    def start_task(self, task_id: str) -> Dict[str, Any]:
        """
        规则 4.1: 启动任务
        
        状态：RED → RUNNING
        """
        task = self.tasks.get(task_id)
        if not task:
            return {"error": "Task not found"}
        
        task.status = TaskStatus.RUNNING
        task.started_at = time.time()
        
        # 更新宫位负载
        for pid in task.assigned_palaces:
            self._increase_palace_load(pid, 0.05)
        
        logger.info(f"Task {task_id} started")
        
        return {
            "task_id": task_id,
            "status": "running",
            "started_at": task.started_at
        }
    
    def complete_task(self, task_id: str, output: Any) -> Dict[str, Any]:
        """
        规则 4.2: 完成任务（绿灯交付或返工）
        
        状态：RUNNING → GREEN/RED
        """
        task = self.tasks.get(task_id)
        if not task:
            return {"error": "Task not found"}
        
        # 绿灯检查
        check_result = self.green_light_check(task, output)
        
        if check_result["passed"]:
            task.status = TaskStatus.GREEN
            task.completed_at = time.time()
            task.output = output
            
            # 额外增加负载（完成任务）
            for pid in task.assigned_palaces:
                self._increase_palace_load(pid, 0.05)
            
            logger.info(f"Task {task_id} completed successfully")
            
            return {
                "status": "delivered",
                "check_result": check_result,
                "output": output
            }
        else:
            # 返工
            task.status = TaskStatus.RED
            task.rework_count += 1
            
            logger.warning(f"Task {task_id} needs rework: {check_result['reasons']}")
            
            return {
                "status": "rework",
                "reasons": check_result["reasons"],
                "rework_count": task.rework_count
            }
    
    def _increase_palace_load(self, palace_id: int, delta: float):
        """增加宫位负载（内部方法）"""
        if palace_id in self.palace_capacities:
            cap = self.palace_capacities[palace_id]
            cap.current_load = min(1.0, cap.current_load + delta)
    
    # ========== 规则 5: 自适应规则 ==========
    
    def adjust_priority(self, task_id: str, elapsed_minutes: float) -> TaskPriority:
        """
        规则 5.1: 动态优先级调整
        
        任务等待时间越长，优先级越高
        """
        task = self.tasks.get(task_id)
        if not task:
            return TaskPriority.MEDIUM
        
        original_priority = task.priority
        
        # 等待超过 30 分钟，提升一级
        if elapsed_minutes > 30 and original_priority.value > 2:
            return TaskPriority(original_priority.value - 1)
        
        # 等待超过 1 小时，直接 CRITICAL
        if elapsed_minutes > 60:
            return TaskPriority.CRITICAL
        
        return original_priority
    
    def balance_palace_loads(self) -> Dict[str, Any]:
        """
        规则 5.2: 宫位负载平衡
        
        自动检测并建议负载均衡
        """
        loads = {pid: cap.current_load for pid, cap in self.palace_capacities.items()}
        avg_load = sum(loads.values()) / len(loads)
        
        overloaded = [pid for pid, load in loads.items() if load > 0.8]
        underloaded = [pid for pid, load in loads.items() if load < 0.4]
        
        return {
            "average_load": avg_load,
            "overloaded": overloaded,
            "underloaded": underloaded,
            "suggestion": f"考虑将任务分配给宫位：{underloaded}" if underloaded else "负载均衡良好"
        }
    
    # ========== 主入口：5 宫指挥官 ==========
    
    def handle_user_command(self, command: str) -> Dict[str, Any]:
        """
        5 宫指挥官主入口
        
        完整流程:
        1. 感知（优先级、类型）
        2. 决策（分配宫位）
        3. 创建任务
        4. 红灯确认
        5. 定义 TDD 标准
        6. 启动执行
        """
        # 1. 感知
        priority = self.detect_task_priority(command)
        task_type = self.infer_task_type(command)
        assigned_palaces = self.assign_palaces(task_type)
        
        # 2. 创建任务（包含 3 宫模型分配）
        task_id = f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        task = self.create_task(task_id, command)
        
        # 3. 红灯确认
        red_confirm = self.red_light_confirm(task)
        
        # 4. 定义 TDD 标准
        standards = self.define_tdd_standards(task)
        
        # 5. 启动
        self.start_task(task_id)
        
        # 6. 返回执行计划（包含模型分配）
        return {
            "task_id": task_id,
            "priority": priority.name,
            "task_type": task_type,
            "assigned_palaces": assigned_palaces,
            "model_allocation": task.model_allocation,
            "tdd_standards": [
                {"name": s.name, "required": s.required, "check": s.check}
                for s in standards
            ],
            "red_confirm": red_confirm,
            "status": "ready_to_execute"
        }
    
    def get_task_report(self) -> Dict[str, Any]:
        """获取任务报告"""
        active = [t for t in self.tasks.values() if t.status != TaskStatus.DELIVERED]
        completed = [t for t in self.tasks.values() if t.status == TaskStatus.DELIVERED]
        
        return {
            "active_tasks": len(active),
            "completed_tasks": len(completed),
            "recent_tasks": [
                {
                    "task_id": t.task_id,
                    "description": t.description[:50],
                    "status": t.status.value,
                    "priority": t.priority.name
                }
                for t in list(self.tasks.values())[-10:]
            ]
        }


# ========== 导出给 API 使用 ==========

# 全局 L4 引擎实例
_l4_engine: Optional[L4RuleEngine] = None


def get_l4_engine() -> L4RuleEngine:
    """获取 L4 引擎单例"""
    global _l4_engine
    if _l4_engine is None:
        _l4_engine = L4RuleEngine()
    return _l4_engine


def l4_handle_command(command: str) -> Dict[str, Any]:
    """L4 命令处理入口（供 API 调用）"""
    engine = get_l4_engine()
    return engine.handle_user_command(command)


def l4_complete_task(task_id: str, output: Any) -> Dict[str, Any]:
    """L4 任务完成入口（供 API 调用）"""
    engine = get_l4_engine()
    return engine.complete_task(task_id, output)


def l4_get_status() -> Dict[str, Any]:
    """L4 状态查询（供 API 调用）"""
    engine = get_l4_engine()
    return {
        "tasks": engine.get_task_report(),
        "palace_loads": {
            pid: cap.current_load for pid, cap in engine.palace_capacities.items()
        },
        "balance": engine.balance_palace_loads()
    }
