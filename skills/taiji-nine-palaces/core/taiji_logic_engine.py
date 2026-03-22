#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太极两仪核心逻辑引擎
Taiji-YinYang Core Logic Engine

实现：
- 两仪正反转（任务推进/Ask 模式）
- 四象循环（Planning/Daily/Review/Retro）
- 九宫格阴阳平衡（4 对矛盾自动调节）
- 五行循环验证（金木水火土自我修正）
"""

from enum import Enum
from typing import Dict, List, Any, Optional
from datetime import datetime
from loguru import logger

from core.palace_constants import get_palace_name, get_palace_element


class TaijiMode(Enum):
    """两仪模式"""
    YANG_FORWARD = "阳_正转"  # 任务推进模式
    YIN_REVERSE = "阴_反转"   # Ask 模式/智能体会议


class FourSymbols(Enum):
    """四象阶段"""
    PLANNING = "阳_规划"      # 发散愿景 → 收敛承诺
    DAILY = "阴_执行"         # 执行同步 → 障碍暴露
    REVIEW = "阳_展示"        # 展示成果 → 收集反馈
    RETRO = "阴_沉淀"         # 反思改进 → 文化沉淀


class NinePalacesBalance:
    """
    九宫格阴阳平衡系统
    
    4 对主要矛盾（使用官方名称）：
    1. 4-品牌战略 vs 5-中央控制 - 灵活性 vs 标准化
    2. 3-技术团队 vs 6-物联监控 - 速度 vs 稳定
    3. 2-产品质量 vs 1-数据采集 - 需求 vs 数据
    4. 7-法务框架 vs 9-行业生态 - 度量 vs 报告
    """
    
    def __init__(self):
        self.palace_states = self._initialize_palace_states()
        self.balance_pairs = self._initialize_balance_pairs()
    
    def _initialize_palace_states(self) -> Dict[int, Dict[str, Any]]:
        """初始化宫位状态"""
        states = {}
        for pos in range(1, 10):
            states[pos] = {
                "name": get_palace_name(pos),
                "element": get_palace_element(pos),
                "load": 0.0
            }
        return states
    
    def _initialize_balance_pairs(self) -> Dict[str, Dict[str, Any]]:
        """初始化阴阳平衡对"""
        return {
            "team_process": {"palaces": (4, 5), "balance": 1.0},
            "tech_quality": {"palaces": (3, 6), "balance": 1.0},
            "product_data": {"palaces": (2, 1), "balance": 1.0},
            "monitor_eco": {"palaces": (7, 9), "balance": 1.0},
        }
    
    def update_load(self, palace_id: int, load: float):
        """更新宫位负载"""
        # 输入验证
        if not isinstance(palace_id, int) or palace_id < 1 or palace_id > 9:
            raise ValueError("宫位ID必须是1-9之间的整数")
        if not isinstance(load, (int, float)) or load < 0 or load > 1:
            raise ValueError("负载必须是0-1之间的数字")
        
        if palace_id in self.palace_states:
            self.palace_states[palace_id]["load"] = load
            self._recalculate_balance()
            logger.debug(f"更新宫位 {palace_id} 负载为 {load}")
    
    def _recalculate_balance(self):
        """重新计算阴阳平衡"""
        for pair_name, pair_data in self.balance_pairs.items():
            p1, p2 = pair_data["palaces"]
            load1 = self.palace_states[p1]["load"]
            load2 = self.palace_states[p2]["load"]
            
            # 平衡度 = 较小负载 / 较大负载 (0~1)
            if max(load1, load2) > 0:
                pair_data["balance"] = min(load1, load2) / max(load1, load2)
            else:
                pair_data["balance"] = 1.0
    
    def get_imbalanced_pairs(self) -> List[Dict]:
        """获取失衡的阴阳对（平衡度 < 0.7）"""
        imbalanced = []
        for pair_name, pair_data in self.balance_pairs.items():
            if pair_data["balance"] < 0.7:
                imbalanced.append({
                    "pair": pair_name,
                    "balance": pair_data["balance"],
                    "palaces": pair_data["palaces"]
                })
        return imbalanced
    
    def get_palace_state(self, palace_id: int) -> Optional[Dict[str, Any]]:
        """获取宫位状态"""
        return self.palace_states.get(palace_id)
    
    def get_all_palace_states(self) -> Dict[int, Dict[str, Any]]:
        """获取所有宫位状态"""
        return self.palace_states.copy()
    
    def get_balance_status(self) -> Dict[str, float]:
        """获取所有平衡对的状态"""
        return {pair: data["balance"] for pair, data in self.balance_pairs.items()}


class FiveElementsLoop:
    """
    五行循环验证系统
    
    相生循环：金→水→木→火→土
    相克循环：金→木→土→水→火
    """
    
    def __init__(self):
        self.elements = ["金", "水", "木", "火", "土"]
        self.current_element = "金"
        self.loop_count = 0
        self.element_meanings = self._initialize_element_meanings()
        
    def _initialize_element_meanings(self) -> Dict[str, str]:
        """初始化五行含义"""
        return {
            "金": "收敛 - 收集执行数据",
            "水": "流动 - 分析问题根因",
            "木": "生长 - 生成改进方案",
            "火": "发散 - 实施优化措施",
            "土": "承载 - 沉淀经验知识"
        }
    
    def next_element(self) -> str:
        """进入下一个五行阶段"""
        idx = self.elements.index(self.current_element)
        self.current_element = self.elements[(idx + 1) % 5]
        self.loop_count += 1
        logger.debug(f"进入五行阶段：{self.current_element}，循环次数：{self.loop_count}")
        return self.current_element
    
    def get_element_meaning(self) -> Dict[str, Any]:
        """获取当前五行的含义"""
        return {
            "element": self.current_element,
            "meaning": self.element_meanings[self.current_element],
            "loop_count": self.loop_count
        }
    
    def get_current_element(self) -> str:
        """获取当前五行元素"""
        return self.current_element
    
    def get_loop_count(self) -> int:
        """获取循环次数"""
        return self.loop_count


class TaskManager:
    """
    任务管理器
    负责任务的添加、执行和管理
    """
    
    def __init__(self):
        self.tasks = []
        self.task_queue_mode = "FIFO"  # 或 "PRIORITY"
    
    def add_task(self, task: Dict[str, Any]):
        """添加任务"""
        self.tasks.append(task)
        logger.debug(f"添加任务：{task.get('task_id', 'N/A')}")
    
    def get_tasks(self) -> List[Dict[str, Any]]:
        """获取所有任务"""
        return self.tasks.copy()
    
    def get_task_count(self) -> int:
        """获取任务数量"""
        return len(self.tasks)
    
    def clear_tasks(self):
        """清空任务"""
        self.tasks.clear()
        logger.debug("任务已清空")


class TaijiCoreEngine:
    """
    太极核心引擎
    
    统一调度：
    - 两仪模式切换
    - 四象阶段流转
    - 九宫格平衡调节
    - 五行循环验证
    """
    
    def __init__(self):
        self.mode = TaijiMode.YANG_FORWARD
        self.symbols_stage = FourSymbols.PLANNING
        self.balance_system = NinePalacesBalance()
        self.loop_system = FiveElementsLoop()
        self.task_manager = TaskManager()
        
        # 战略目标
        self.strategic_goals = []
        
        logger.info("初始化太极核心引擎")
    
    def switch_mode(self, new_mode: TaijiMode):
        """切换两仪模式"""
        old_mode = self.mode
        self.mode = new_mode
        
        logger.info(f"两仪转换：{old_mode.value} → {new_mode.value}")
        
        if new_mode == TaijiMode.YIN_REVERSE:
            logger.info("进入 Ask 模式：智能体开始开会讨论")
            self._start_agent_meeting()
        else:
            logger.info("进入执行模式：任务开始推进")
            self._resume_task_execution()
    
    def advance_symbols(self):
        """推进四象阶段"""
        old_stage = self.symbols_stage
        
        stage_order = list(FourSymbols)
        current_idx = stage_order.index(self.symbols_stage)
        next_idx = (current_idx + 1) % len(stage_order)
        self.symbols_stage = stage_order[next_idx]
        
        logger.info(f"四象流转：{old_stage.value} → {self.symbols_stage.value}")
        
        # 根据四象阶段调整任务策略
        self._adjust_task_strategy_by_stage()
    
    def check_balance_and_adjust(self) -> List[Dict]:
        """检查阴阳平衡并自动调整"""
        imbalanced = self.balance_system.get_imbalanced_pairs()
        
        if imbalanced:
            logger.warning(f"检测到 {len(imbalanced)} 组阴阳失衡:")
            for item in imbalanced:
                logger.warning(f"   {item['pair']}: 平衡度 {item['balance']:.2f}")
            
            # 自动调整任务优先级
            self._auto_adjust_tasks_for_balance(imbalanced)
        
        return imbalanced
    
    def run_five_elements_check(self, task_result: Dict):
        """运行五行循环检查"""
        element_info = self.loop_system.get_element_meaning()
        
        logger.info(f"【五行循环 · {element_info['element']}】含义：{element_info['meaning']}")
        
        # 根据五行阶段处理任务结果
        if self.loop_system.current_element == "金":
            self._collect_task_data(task_result)
        elif self.loop_system.current_element == "水":
            self._analyze_problems(task_result)
        elif self.loop_system.current_element == "木":
            self._generate_improvements(task_result)
        elif self.loop_system.current_element == "火":
            self._implement_changes(task_result)
        elif self.loop_system.current_element == "土":
            self._record_experience(task_result)
        
        # 进入下一个五行阶段
        self.loop_system.next_element()
    
    def add_task(self, task: Dict[str, Any]):
        """添加任务"""
        # 输入验证
        if not isinstance(task, dict):
            raise ValueError("任务必须是字典类型")
        if 'task_id' not in task:
            raise ValueError("任务必须包含task_id字段")
        self.task_manager.add_task(task)
    
    def get_task_count(self) -> int:
        """获取任务数量"""
        return self.task_manager.get_task_count()
    
    def update_palace_load(self, palace_id: int, load: float):
        """更新宫位负载"""
        # 输入验证
        if not isinstance(palace_id, int) or palace_id < 1 or palace_id > 9:
            raise ValueError("宫位ID必须是1-9之间的整数")
        if not isinstance(load, (int, float)) or load < 0 or load > 1:
            raise ValueError("负载必须是0-1之间的数字")
        self.balance_system.update_load(palace_id, load)
    
    def get_palace_state(self, palace_id: int) -> Optional[Dict[str, Any]]:
        """获取宫位状态"""
        # 输入验证
        if not isinstance(palace_id, int) or palace_id < 1 or palace_id > 9:
            raise ValueError("宫位ID必须是1-9之间的整数")
        return self.balance_system.get_palace_state(palace_id)
    
    def get_balance_status(self) -> Dict[str, float]:
        """获取平衡状态"""
        return self.balance_system.get_balance_status()
    
    def reset_state(self):
        """重置太极引擎状态"""
        logger.info("重置太极引擎状态")
        self.mode = TaijiMode.YANG_FORWARD
        self.symbols_stage = FourSymbols.PLANNING
        self.balance_system = NinePalacesBalance()
        self.loop_system = FiveElementsLoop()
        self.task_manager = TaskManager()
        self.strategic_goals = []
        logger.info("太极引擎状态已重置")
    
    def _start_agent_meeting(self):
        """启动智能体会议（Ask 模式）"""
        logger.info("智能体会议开始...")
        participating_palaces = []
        for i in range(1, 10):
            if i != 5:  # 排除中宫
                palace_name = self.balance_system.palace_states[i]['name']
                participating_palaces.append(f"{i}-{palace_name}")
        logger.info(f"参与宫位: {', '.join(participating_palaces)}")
    
    def _resume_task_execution(self):
        """恢复任务执行"""
        task_count = self.task_manager.get_task_count()
        logger.info(f"任务执行继续... 当前任务数：{task_count}")
    
    def _adjust_task_strategy_by_stage(self):
        """根据四象阶段调整任务策略"""
        strategies = {
            FourSymbols.PLANNING: "规划阶段：任务拆解、资源分配",
            FourSymbols.DAILY: "执行阶段：每日站会、障碍清除",
            FourSymbols.REVIEW: "评审阶段：成果演示、反馈收集",
            FourSymbols.RETRO: "回顾阶段：反思改进、流程优化"
        }
        strategy = strategies[self.symbols_stage]
        logger.info(strategy)
    
    def _auto_adjust_tasks_for_balance(self, imbalanced_pairs: List[Dict]):
        """自动调整任务以恢复阴阳平衡"""
        logger.info("开始自动调整任务优先级...")
        
        for imbalance in imbalanced_pairs:
            pair_name = imbalance["pair"]
            logger.info(f"调整 {pair_name} 的任务分配")
        
        # TODO: 实际的任务重排序逻辑
    
    def _collect_task_data(self, result: Dict):
        """金：收集数据"""
        task_id = result.get('task_id', 'N/A')
        logger.info(f"收集任务数据：{task_id}")
    
    def _analyze_problems(self, result: Dict):
        """水：分析问题"""
        problems = result.get('problems', [])
        logger.info(f"分析 {len(problems)} 个问题")
    
    def _generate_improvements(self, result: Dict):
        """木：生成改进方案"""
        logger.info("生成改进建议...")
    
    def _implement_changes(self, result: Dict):
        """火：实施变更"""
        logger.info("实施优化措施...")
    
    def _record_experience(self, result: Dict):
        """土：沉淀经验"""
        logger.info("记录经验教训...")


def demo_taiji_core():
    """演示太极核心引擎"""
    logger.info("太极核心引擎演示")
    
    engine = TaijiCoreEngine()
    
    # 演示两仪切换
    engine.switch_mode(TaijiMode.YIN_REVERSE)
    engine.switch_mode(TaijiMode.YANG_FORWARD)
    
    # 演示四象流转
    for _ in range(4):
        engine.advance_symbols()
    
    # 演示九宫格平衡检查
    engine.update_palace_load(3, 0.9)  # 技术宫高负载
    engine.update_palace_load(6, 0.3)  # 质量宫低负载
    engine.check_balance_and_adjust()
    
    # 演示五行循环
    for _ in range(5):
        engine.run_five_elements_check({"task_id": "TASK-001", "problems": []})
    
    logger.info("演示完成")


if __name__ == "__main__":
    demo_taiji_core()
