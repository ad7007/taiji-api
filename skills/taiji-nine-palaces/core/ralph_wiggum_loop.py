#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
五行代码AI循环 - Ralph Wiggum Loop

借鉴自 Geoffrey Huntley 的五行代码AI理念：
"默认AI生成的代码第一次肯定是错的，但可以通过不断测试、看报错、自动修正，直到代码能成功运行为止"

应用到太极任务三角循环：
- 执行宫(1/3/8)执行任务
- 2宫(产品质量)验收，假设第一次做不好
- 反馈修正，循环直到通过

循环公式：
while not 验收通过:
    执行任务()
    测试结果 = 验收宫.验收(任务)
    if 测试结果.通过:
        break
    修正 = 分析错误(测试结果)
    应用修正(修正)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any
from enum import Enum
from datetime import datetime


class LoopState(Enum):
    """循环状态"""
    RUNNING = "running"      # 循环运行中
    PASSED = "passed"        # 验收通过
    FAILED = "failed"        # 循环失败（超过最大次数）
    BLOCKED = "blocked"      # 被阻塞


@dataclass
class LoopResult:
    """循环结果"""
    state: LoopState
    iterations: int
    final_output: Optional[str] = None
    error_log: List[str] = field(default_factory=list)
    feedback_log: List[str] = field(default_factory=list)


@dataclass
class TaskTriplet:
    """
    任务三角
    
    执行宫 → 验收宫 → 反馈修正 → 循环
    """
    task_id: str
    task_title: str
    
    # 三角宫位
    executor_palace: int      # 执行宫
    validator_palace: int = 2  # 验收宫（默认2宫产品质量）
    feedback_palace: int = 5   # 反馈宫（默认5宫主控）
    
    # 循环参数
    max_iterations: int = 10   # 最大循环次数
    current_iteration: int = 0
    
    # 验收标准
    acceptance_criteria: List[str] = field(default_factory=list)
    
    # 循环状态
    state: LoopState = LoopState.RUNNING
    error_log: List[str] = field(default_factory=list)
    feedback_log: List[str] = field(default_factory=list)


class RalphWiggumLoop:
    """
    五行代码AI循环
    
    核心理念：假设第一次做不好，通过验收循环不断修正
    """
    
    def __init__(self, max_iterations: int = 10):
        self.max_iterations = max_iterations
        self.active_loops: Dict[str, TaskTriplet] = {}
    
    def create_triplet(
        self,
        task_id: str,
        task_title: str,
        executor_palace: int,
        acceptance_criteria: List[str] = None
    ) -> TaskTriplet:
        """
        创建任务三角
        
        Args:
            task_id: 任务ID
            task_title: 任务标题
            executor_palace: 执行宫位
            acceptance_criteria: 验收标准
        """
        triplet = TaskTriplet(
            task_id=task_id,
            task_title=task_title,
            executor_palace=executor_palace,
            validator_palace=2,  # 2宫产品质量
            feedback_palace=5,   # 5宫主控
            acceptance_criteria=acceptance_criteria or []
        )
        
        self.active_loops[task_id] = triplet
        return triplet
    
    def execute_iteration(
        self,
        triplet: TaskTriplet,
        execute_fn: Callable[[], str],
        validate_fn: Callable[[str], Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        执行一次循环迭代
        
        核心逻辑：
        1. 执行宫执行任务
        2. 验收宫验收（假设不好）
        3. 反馈修正
        
        Args:
            triplet: 任务三角
            execute_fn: 执行函数
            validate_fn: 验收函数
        
        Returns:
            {
                "iteration": 当前迭代次数,
                "output": 输出,
                "passed": 是否通过,
                "feedback": 反馈
            }
        """
        triplet.current_iteration += 1
        
        # 1. 执行宫执行任务
        try:
            output = execute_fn()
        except Exception as e:
            output = f"ERROR: {str(e)}"
            triplet.error_log.append(f"Iteration {triplet.current_iteration}: {str(e)}")
        
        # 2. 验收宫验收（假设第一次不好）
        validation = validate_fn(output)
        passed = validation.get("passed", False)
        feedback = validation.get("feedback", "")
        
        if feedback:
            triplet.feedback_log.append(f"Iteration {triplet.current_iteration}: {feedback}")
        
        # 3. 判断是否继续
        if passed:
            triplet.state = LoopState.PASSED
        elif triplet.current_iteration >= self.max_iterations:
            triplet.state = LoopState.FAILED
        
        return {
            "iteration": triplet.current_iteration,
            "output": output,
            "passed": passed,
            "feedback": feedback,
            "state": triplet.state.value
        }
    
    def run_loop(
        self,
        triplet: TaskTriplet,
        execute_fn: Callable[[], str],
        validate_fn: Callable[[str], Dict[str, Any]]
    ) -> LoopResult:
        """
        运行完整循环
        
        无限循环直到：
        - 验收通过
        - 超过最大迭代次数
        """
        while triplet.state == LoopState.RUNNING:
            result = self.execute_iteration(triplet, execute_fn, validate_fn)
            
            if result["passed"]:
                break
        
        return LoopResult(
            state=triplet.state,
            iterations=triplet.current_iteration,
            final_output=result.get("output") if 'result' in dir() else None,
            error_log=triplet.error_log,
            feedback_log=triplet.feedback_log
        )
    
    def get_triplet_status(self, task_id: str) -> Optional[Dict]:
        """获取三角状态"""
        triplet = self.active_loops.get(task_id)
        if not triplet:
            return None
        
        return {
            "task_id": triplet.task_id,
            "task_title": triplet.task_title,
            "executor": triplet.executor_palace,
            "validator": triplet.validator_palace,
            "iteration": triplet.current_iteration,
            "max_iterations": triplet.max_iterations,
            "state": triplet.state.value,
            "errors": len(triplet.error_log),
            "feedbacks": len(triplet.feedback_log)
        }


# ==================== 集成到任务管理 ====================

def create_task_with_loop(
    title: str,
    executor_palace: int,
    acceptance_criteria: List[str] = None
) -> Dict[str, Any]:
    """
    创建带验收循环的任务
    
    自动创建任务三角：
    - 执行宫执行
    - 2宫验收
    - 5宫反馈
    """
    from core.task_manager import get_task_manager, TaskPriority, TaskSource
    
    tm = get_task_manager()
    
    # 创建主任务
    main_task = tm.create_task(
        title=title,
        palace_id=executor_palace,
        priority=TaskPriority.HIGH,
        source=TaskSource.SELF
    )
    
    # 创建验收子任务（2宫）
    validate_task = tm.create_task(
        title=f"[验收]{title}",
        palace_id=2,
        priority=TaskPriority.HIGH,
        source=TaskSource.SELF
    )
    
    # 创建三角
    loop = RalphWiggumLoop()
    triplet = loop.create_triplet(
        task_id=main_task.task_id,
        task_title=title,
        executor_palace=executor_palace,
        acceptance_criteria=acceptance_criteria
    )
    
    tm.save()
    
    return {
        "main_task_id": main_task.task_id,
        "validate_task_id": validate_task.task_id,
        "triplet": triplet
    }


# ==================== 测试 ====================

if __name__ == "__main__":
    print("=== Ralph Wiggum Loop 测试 ===\n")
    
    loop = RalphWiggumLoop(max_iterations=5)
    
    # 创建三角
    triplet = loop.create_triplet(
        task_id="test_001",
        task_title="测试任务",
        executor_palace=3,  # 技术团队执行
        acceptance_criteria=["输出不为空", "无错误"]
    )
    
    print(f"三角创建: {triplet.executor_palace}→{triplet.validator_palace}→{triplet.feedback_palace}")
    print(f"最大迭代: {triplet.max_iterations}")
    
    # 模拟执行和验收
    outputs = ["错误输出", "还是有错", "终于对了"]
    output_index = [0]  # 用列表包装以便在闭包中修改
    
    def mock_execute():
        idx = output_index[0]
        result = outputs[min(idx, len(outputs)-1)]
        output_index[0] = idx + 1
        return result
    
    def mock_validate(output: str):
        passed = "对了" in output
        feedback = None if passed else f"输出'{output}'不符合标准"
        return {"passed": passed, "feedback": feedback}
    
    # 运行循环
    print("\n开始循环...\n")
    while triplet.state == LoopState.RUNNING:
        result = loop.execute_iteration(triplet, mock_execute, mock_validate)
        print(f"迭代 {result['iteration']}: {result['output']} → {'✓通过' if result['passed'] else '✗继续'}")
    
    print(f"\n最终状态: {triplet.state.value}")
    print(f"迭代次数: {triplet.current_iteration}")