#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
24线程系统实现

实现Taiji.md中的核心公式：
- 线程连接矩阵 M[8×8]
- 线程阴阳双端 T = (T_yin, T_yang)
- 线程转换函数 Transform(T, direction)
- 线程执行引擎 Execute(ThreadGroup(S))
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum


# ==================== 基础定义 ====================

YANG_PALACES = {3, 4, 7, 9}  # 阳卦: 震巽兑离
YIN_PALACES = {1, 2, 6, 8}   # 阴卦: 坎坤乾坤
CENTER = 5                   # 中宫

# 相生关系
GENERATION = {
    3: 6,  # 木→金 (震生乾)
    6: 9,  # 金→火 (乾生离)
    9: 7,  # 火→金 (离生兑)
    7: 4,  # 金→木 (兑生巽)
    4: 8,  # 木→土 (巽生艮)
    8: 3,  # 土→木 (艮生震)
}

# 相克关系
CONTROL = {
    3: 6,  # 木克金
    6: 9,  # 金克火
    9: 7,  # 火克金
    7: 4,  # 金克木
    4: 8,  # 木克土
    8: 1,  # 土克水
    1: 3,  # 水克木
}


# ==================== 线程连接矩阵 ====================

def build_thread_matrix() -> np.ndarray:
    """
    构建线程连接矩阵 M[8×8]
    
    M[i][j] = {
        1  if (i,j) ∈ E 且 相生(i,j)
        -1 if (i,j) ∈ E 且 相克(i,j)
        0  otherwise
    }
    """
    # 宫位列表 (排除中宫)
    palaces = [1, 2, 3, 4, 6, 7, 8, 9]
    M = np.zeros((8, 8), dtype=int)
    
    for i, p1 in enumerate(palaces):
        for j, p2 in enumerate(palaces):
            # 阴阳连接边
            if (p1 in YIN_PALACES and p2 in YANG_PALACES) or \
               (p1 in YANG_PALACES and p2 in YIN_PALACES):
                
                # 检查相生
                if GENERATION.get(p1) == p2 or GENERATION.get(p2) == p1:
                    M[i][j] = 1
                # 检查相克
                elif CONTROL.get(p1) == p2 or CONTROL.get(p2) == p1:
                    M[i][j] = -1
                else:
                    M[i][j] = 0.5  # 中性连接
    
    return M, palaces


# ==================== 线程阴阳双端 ====================

@dataclass
class Thread:
    """
    线程：阴阳双端
    
    T = (T_yin, T_yang)
    """
    palace_id: int
    yao_position: int  # 1-6 爻位
    yin_value: float = 0.5   # 阴端值 [0,1]
    yang_value: float = 0.5  # 阳端值 [0,1]
    
    def balance(self) -> float:
        """
        线程阴阳度量
        YinYang_Balance(T) = T_yang - T_yin ∈ [-1, +1]
        """
        return self.yang_value - self.yin_value
    
    def state(self) -> str:
        """判断线程状态"""
        b = self.balance()
        if b > 0.3:
            return "发散(阳)"
        elif b < -0.3:
            return "收敛(阴)"
        else:
            return "平衡"
    
    def transform(self, direction: str, alpha: float = 0.3):
        """
        线程转换函数
        
        Args:
            direction: 'YIN→YANG' 或 'YANG→YIN'
            alpha: 转换系数
        """
        if direction == 'YIN→YANG':
            self.yang_value += self.yin_value * alpha
            self.yin_value *= (1 - alpha)
        elif direction == 'YANG→YIN':
            self.yin_value += self.yang_value * alpha
            self.yang_value *= (1 - alpha)
        
        # 确保在[0,1]范围
        self.yin_value = max(0, min(1, self.yin_value))
        self.yang_value = max(0, min(1, self.yang_value))


# ==================== 线程组 ====================

class ThreadGroup:
    """
    线程组：N宫的所有线程
    
    ThreadGroup(S) = ⋃{Thread(p,y) | p∈S, y∈[1,6]}
    """
    
    def __init__(self, palaces: List[int]):
        self.palaces = palaces
        self.threads: Dict[Tuple[int, int], Thread] = {}
        
        # 初始化所有线程
        for p in palaces:
            if p != 5:  # 排除中宫
                for y in range(1, 7):  # 6爻
                    self.threads[(p, y)] = Thread(palace_id=p, yao_position=y)
    
    def size(self) -> int:
        """线程数量"""
        return len(self.threads)
    
    def get_palace_threads(self, palace_id: int) -> List[Thread]:
        """获取某宫的所有线程"""
        return [t for (p, y), t in self.threads.items() if p == palace_id]
    
    def total_balance(self) -> float:
        """总阴阳平衡"""
        if not self.threads:
            return 0.0
        return sum(t.balance() for t in self.threads.values()) / len(self.threads)


# ==================== 线程执行引擎 ====================

class ThreadExecutor:
    """
    线程执行引擎
    
    Execute(ThreadGroup(S)) = {
        parallel: 并行执行相生组
        sequential: 串行执行相克组
        hybrid: 混合执行
    }
    """
    
    def __init__(self):
        self.M, self.palaces = build_thread_matrix()
    
    def find_parallel_groups(self, thread_group: ThreadGroup) -> List[List[int]]:
        """
        找出可并行执行的宫位组（相生关系）
        """
        parallel_groups = []
        palaces = thread_group.palaces
        
        # 按相生链分组
        visited = set()
        for p in palaces:
            if p in visited or p == 5:
                continue
            
            group = [p]
            visited.add(p)
            
            # 沿相生链扩展
            current = p
            while GENERATION.get(current) in palaces and GENERATION[current] not in visited:
                current = GENERATION[current]
                group.append(current)
                visited.add(current)
            
            if len(group) > 1:
                parallel_groups.append(group)
        
        return parallel_groups
    
    def find_sequential_pairs(self, thread_group: ThreadGroup) -> List[Tuple[int, int]]:
        """
        找出需要串行执行的宫位对（相克关系）
        """
        sequential_pairs = []
        palaces = set(thread_group.palaces)
        
        for p1, p2 in CONTROL.items():
            if p1 in palaces and p2 in palaces:
                sequential_pairs.append((p1, p2))
        
        return sequential_pairs
    
    def execute(self, thread_group: ThreadGroup, mode: str = 'hybrid') -> Dict:
        """
        执行线程组
        
        Args:
            mode: 'parallel', 'sequential', 'hybrid'
        
        Returns:
            执行计划
        """
        plan = {
            "mode": mode,
            "parallel_groups": [],
            "sequential_pairs": [],
            "total_threads": thread_group.size(),
            "balance": thread_group.total_balance(),
        }
        
        if mode in ['parallel', 'hybrid']:
            plan["parallel_groups"] = self.find_parallel_groups(thread_group)
        
        if mode in ['sequential', 'hybrid']:
            plan["sequential_pairs"] = self.find_sequential_pairs(thread_group)
        
        return plan


# ==================== 48规则路由表 ====================

class RuleRouter:
    """
    48规则路由表
    
    中宫5连接48规则，路由到正确的宫位执行
    """
    
    def __init__(self):
        # 48规则关键词
        self.rules = self._load_rules()
        self.palace_keywords = self._build_keyword_index()
    
    def _load_rules(self) -> Dict[Tuple[int, int], str]:
        """加载48规则"""
        rules = {}
        
        # 阳24规则
        yang_rules = {
            (4, 1): "传播", (4, 2): "分析", (4, 3): "策划", (4, 4): "洞察", (4, 5): "定位", (4, 6): "创新",
            (7, 1): "合规", (7, 2): "风控", (7, 3): "验收", (7, 4): "审计", (7, 5): "标准", (7, 6): "认证",
            (3, 1): "开发", (3, 2): "测试", (3, 3): "部署", (3, 4): "优化", (3, 5): "重构", (3, 6): "集成",
            (9, 1): "研究", (9, 2): "合作", (9, 3): "拓展", (9, 4): "洞察", (9, 5): "连接", (9, 6): "繁荣",
        }
        
        # 阴24规则
        yin_rules = {
            (1, 1): "采集", (1, 2): "清洗", (1, 3): "存储", (1, 4): "分析", (1, 5): "挖掘", (1, 6): "安全",
            (2, 1): "承载", (2, 2): "优化", (2, 3): "交付", (2, 4): "迭代", (2, 5): "稳定", (2, 6): "扩展",
            (8, 1): "服务", (8, 2): "营销", (8, 3): "响应", (8, 4): "推广", (8, 5): "维护", (8, 6): "增长",
            (6, 1): "监控", (6, 2): "告警", (6, 3): "备份", (6, 4): "恢复", (6, 5): "优化", (6, 6): "保障",
        }
        
        rules.update(yang_rules)
        rules.update(yin_rules)
        return rules
    
    def _build_keyword_index(self) -> Dict[str, int]:
        """构建关键词到宫位的索引"""
        index = {}
        for (palace, yao), keyword in self.rules.items():
            index[keyword] = palace
        return index
    
    def route(self, keyword: str) -> Optional[int]:
        """
        路由关键词到宫位
        
        Args:
            keyword: 关键词
        
        Returns:
            宫位ID
        """
        return self.palace_keywords.get(keyword)
    
    def get_palace_rules(self, palace_id: int) -> List[str]:
        """获取某宫的所有规则"""
        return [kw for (p, y), kw in self.rules.items() if p == palace_id]
    
    def get_all_rules(self) -> Dict[Tuple[int, int], str]:
        """获取所有48规则"""
        return self.rules


# ==================== 测试 ====================

if __name__ == "__main__":
    print("=== 24线程系统 ===\n")
    
    # 1. 线程连接矩阵
    M, palaces = build_thread_matrix()
    print(f"【线程连接矩阵 M[8×8]】")
    print(f"  宫位顺序: {palaces}")
    print(f"  矩阵:\n{M}\n")
    
    # 2. 线程阴阳双端
    print("【线程阴阳双端】")
    t = Thread(palace_id=3, yao_position=1)
    print(f"  初始: yin={t.yin_value:.2f}, yang={t.yang_value:.2f}, balance={t.balance():.2f}, state={t.state()}")
    t.transform('YIN→YANG')
    print(f"  转换后: yin={t.yin_value:.2f}, yang={t.yang_value:.2f}, balance={t.balance():.2f}, state={t.state()}\n")
    
    # 3. 线程组
    print("【线程组】")
    tg = ThreadGroup([1, 3, 6, 9])
    print(f"  宫位: {tg.palaces}")
    print(f"  线程数: {tg.size()}")
    print(f"  总平衡: {tg.total_balance():.2f}\n")
    
    # 4. 线程执行
    print("【线程执行引擎】")
    executor = ThreadExecutor()
    plan = executor.execute(tg)
    print(f"  模式: {plan['mode']}")
    print(f"  并行组: {plan['parallel_groups']}")
    print(f"  串行对: {plan['sequential_pairs']}\n")
    
    # 5. 48规则路由
    print("【48规则路由表】")
    router = RuleRouter()
    print(f"  总规则数: {len(router.get_all_rules())}")
    print(f"  '开发' → {router.route('开发')}宫")
    print(f"  '采集' → {router.route('采集')}宫")
    print(f"  3宫规则: {router.get_palace_rules(3)}")