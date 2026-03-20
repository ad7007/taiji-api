"""
24线程核心实现
基于 Taiji.md 的数学公式
"""

from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import numpy as np


class Direction(Enum):
    YIN_TO_YANG = "YIN→YANG"
    YANG_TO_YIN = "YANG→YIN"


@dataclass
class Thread:
    """线程：阴阳双端"""
    yin: float = 0.5  # 阴端 [0,1]
    yang: float = 0.5  # 阳端 [0,1]

    def balance(self) -> float:
        """阴阳平衡值 [-1, +1]"""
        return self.yang - self.yin

    def transform(self, direction: Direction, alpha: float = 0.3):
        """线程转换"""
        if direction == Direction.YIN_TO_YANG:
            self.yang += self.yin * alpha
            self.yin *= (1 - alpha)
        else:
            self.yin += self.yang * alpha
            self.yang *= (1 - alpha)


# 24线程阴阳拓扑
V_YANG = {3, 4, 7, 9}  # 阳卦：木木金火
V_YIN = {1, 2, 6, 8}   # 阴卦：水土金土
P_CENTER = {5}          # 中宫

# 五行属性
WUXING = {
    1: "水", 2: "土", 3: "木", 4: "木", 5: "土",
    6: "金", 7: "金", 8: "土", 9: "火"
}

# 相生链：木→火→土→金→水→木
SHENG = {
    "木": "火", "火": "土", "土": "金", "金": "水", "水": "木"
}

# 相克链：木→土→水→火→金→木
KE = {
    "木": "土", "土": "水", "水": "火", "火": "金", "金": "木"
}


def is_sheng(a: int, b: int) -> bool:
    """a 是否生 b"""
    return SHENG.get(WUXING.get(a, "")) == WUXING.get(b, "")


def is_ke(a: int, b: int) -> bool:
    """a 是否克 b"""
    return KE.get(WUXING.get(a, "")) == WUXING.get(b, "")


def build_thread_matrix() -> np.ndarray:
    """构建线程连接矩阵 M[10×10] (索引1-9)"""
    M = np.zeros((10, 10), dtype=int)  # 用1-9索引，0不使用

    for i in range(1, 10):
        for j in range(1, 10):
            if i == j or i == 5 or j == 5:  # 跳过中宫
                continue
            # 阴卦连阳卦
            if i in V_YIN and j in V_YANG:
                if is_sheng(i, j):
                    M[i][j] = 1
                elif is_ke(i, j):
                    M[i][j] = -1

    return M


# 线程连接矩阵
THREAD_MATRIX = build_thread_matrix()


class Thread24System:
    """24线程系统"""

    def __init__(self):
        self.threads: Dict[Tuple[int, int], Thread] = {}
        self._init_threads()

    def _init_threads(self):
        """初始化24线程"""
        # 阴卦→阳卦的连接
        for yin in V_YIN:
            for yang in V_YANG:
                if THREAD_MATRIX[yin][yang] != 0:
                    self.threads[(yin, yang)] = Thread()

    def transform_all(self, direction: Direction, alpha: float = 0.3):
        """批量转换所有线程"""
        for thread in self.threads.values():
            thread.transform(direction, alpha)

    def get_balance(self) -> float:
        """获取系统整体平衡值"""
        if not self.threads:
            return 0.0
        return sum(t.balance() for t in self.threads.values()) / len(self.threads)

    def get_rotation(self) -> str:
        """根据平衡值判断旋转方向"""
        balance = self.get_balance()
        if balance >= 0.2:
            return "正转"
        elif balance <= -0.2:
            return "反转"
        else:
            return "平衡"

    def get_status(self) -> dict:
        """获取状态"""
        return {
            "thread_count": len(self.threads),
            "balance": round(self.get_balance(), 2),
            "rotation": self.get_rotation(),
            "yang_endpoints": list(V_YANG),
            "yin_endpoints": list(V_YIN)
        }


# N宫组合
def n_palace_combinations(n: int) -> List[Set[int]]:
    """计算n宫组合"""
    from itertools import combinations

    P = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    return [set(c) for c in combinations(P, n)]


def triangle_stability(triangle: Set[int]) -> float:
    """三角稳定性"""
    lst = list(triangle)
    if len(lst) != 3:
        return 0.0

    total = 0
    for i in range(3):
        for j in range(3):
            if i != j:
                total += THREAD_MATRIX[lst[i]][lst[j]]

    return total / 3.0


# 相生循环
SHENG_CHAIN = {
    3: 6,  # 木→金 (震生乾)
    6: 9,  # 金→火 (乾生离)
    9: 7,  # 火→金 (离生兑)
    7: 4,  # 金→木 (兑生巽)
    4: 8,  # 木→土 (巽生艮)
    8: 3,  # 土→木 (艮生震)
    5: None  # 中宫生任何宫
}


def sheng_path(start: int, end: int, max_steps: int = 6) -> List[int]:
    """计算相生路径"""
    path = [start]
    current = start

    for _ in range(max_steps):
        if current == end:
            break
        next_p = SHENG_CHAIN.get(current)
        if next_p is None:
            break
        path.append(next_p)
        current = next_p

    return path


# 实例
thread_system = Thread24System()