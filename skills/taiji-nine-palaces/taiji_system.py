#!/usr/bin/env python3
"""
太极系统 - 统一入口
Taiji System - Unified Entry Point

整合所有核心功能：
- 意识系统
- 任务系统
- 六爻系统
- 决策感知
- 循环系统
- 宫位管理

米珞直接使用，无需API调用
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import sys

# 检测是否作为包导入
if __name__ == "__main__" and __package__ is None:
    # 直接运行时添加路径
    sys.path.insert(0, str(Path(__file__).parent))
    from local_client import TaijiLocalClient, get_client
    from yao_keywords import detect_yao_from_text, get_palace_yao_summary, get_keyword_stats
    from core import (
        auto_group_by_mode, get_generation_path, get_control_relations,
        get_central_axis, YANG_PALACES, YIN_PALACES,
        TeamBuilder, TaskComplexity,
        TaijiConsciousness, TaijiHeartbeat,
        l4_handle_command, l4_complete_task, l4_get_status, TaskManager,
        SixYaoEngine, YaoLearningDB,
        TaijiDecisionEngine, IdleDetector,
        RalphWiggumLoop, TaijiWuxingLoop,
        DailyReport, TaijiChatbot, get_chatbot,
    )
else:
    # 作为包导入
    from .local_client import TaijiLocalClient, get_client
    from .yao_keywords import detect_yao_from_text, get_palace_yao_summary, get_keyword_stats
    from .core import (
        auto_group_by_mode, get_generation_path, get_control_relations,
        get_central_axis, YANG_PALACES, YIN_PALACES,
        TeamBuilder, TaskComplexity,
        TaijiConsciousness, TaijiHeartbeat,
        l4_handle_command, l4_complete_task, l4_get_status, TaskManager,
        SixYaoEngine, YaoLearningDB,
        TaijiDecisionEngine, IdleDetector,
        RalphWiggumLoop, TaijiWuxingLoop,
        DailyReport, TaijiChatbot, get_chatbot,
    )


class TaijiSystem:
    """
    太极系统 - 完整功能入口
    
    整合所有模块，提供统一接口
    """
    
    def __init__(self, data_dir: str = None):
        """
        初始化太极系统
        
        Args:
            data_dir: 数据目录
        """
        self.skill_dir = Path(__file__).parent
        self.data_dir = Path(data_dir) if data_dir else self.skill_dir / "data"
        self.data_dir.mkdir(exist_ok=True)
        
        # 初始化各子系统
        self.client = TaijiLocalClient(str(self.data_dir))
        self.consciousness = TaijiConsciousness()
        self.heartbeat = TaijiHeartbeat()
        self.task_manager = TaskManager()
        self.yao_engine = SixYaoEngine()
        self.yao_learning = YaoLearningDB(str(self.data_dir / "yao_learning.db"))
        self.decision_engine = TaijiDecisionEngine()
        self.idle_detector = IdleDetector()
        self.wuxing_loop = TaijiWuxingLoop()
        self.daily_report = DailyReport()
        self.chatbot = get_chatbot()
        
        # 宫位名称
        self.palace_names = {
            1: "1-数据采集",
            2: "2-产品质量",
            3: "3-技术团队",
            4: "4-品牌战略",
            5: "5-中央控制",
            6: "6-物联监控",
            7: "7-法务框架",
            8: "8-营销客服",
            9: "9-行业生态",
        }
    
    # ========== 状态查询 ==========
    
    def get_status(self) -> Dict[str, Any]:
        """获取系统整体状态"""
        return {
            "palaces": self.client.get_all_palaces(),
            "consciousness": self.consciousness.get_status(),
            "balance": self.client.get_balance_status(),
            "idle": self.idle_detector.check_idle(),
            "tasks": self.task_manager.get_active_tasks(),
        }
    
    def get_palaces(self) -> Dict[str, Any]:
        """获取九宫状态"""
        return self.client.get_all_palaces()
    
    def update_palace_load(self, palace_id: int, load: float) -> Dict[str, Any]:
        """更新宫位负载"""
        return self.client.update_palace_load(palace_id, load)
    
    # ========== 意识系统 ==========
    
    def get_consciousness_status(self) -> Dict[str, Any]:
        """获取意识状态"""
        return self.consciousness.get_status()
    
    def decide_rotation(self) -> Dict[str, Any]:
        """决定旋转方向（正转/反转）"""
        return self.consciousness.decide_rotation()
    
    def get_recommendation(self) -> Dict[str, Any]:
        """获取行动建议"""
        return self.consciousness.get_recommendation()
    
    # ========== 任务系统 ==========
    
    def handle_command(self, command: str) -> Dict[str, Any]:
        """
        处理用户命令（L4规则层）
        
        Args:
            command: 用户指令
        
        Returns:
            任务分配结果
        """
        return l4_handle_command(command)
    
    def complete_task(self, task_id: str, output: Any) -> Dict[str, Any]:
        """完成任务（绿灯验收）"""
        return l4_complete_task(task_id, output)
    
    def get_task_status(self) -> Dict[str, Any]:
        """获取任务状态"""
        return l4_get_status()
    
    def create_task(self, task_id: str, title: str, scene: str, complexity: str = "standard") -> Dict[str, Any]:
        """创建任务"""
        return self.client.create_task(task_id, title, scene, complexity)
    
    # ========== 六爻系统 ==========
    
    def detect_yao(self, text: str, palace_id: int = None) -> Dict[str, Any]:
        """从文本探测六爻"""
        return detect_yao_from_text(text, palace_id)
    
    def get_yao_keywords(self, palace_id: int, yao_level: int) -> List[str]:
        """获取爻位关键词"""
        from .yao_keywords import get_detect_keywords
        return get_detect_keywords(palace_id, yao_level)
    
    def get_yao_summary(self, palace_id: int) -> Dict[str, Any]:
        """获取宫位六爻汇总"""
        return get_palace_yao_summary(palace_id)
    
    def learn_yao(self, palace_id: int, yao_level: int, text: str, state: str) -> Dict[str, Any]:
        """学习六爻状态"""
        return self.yao_learning.learn(palace_id, yao_level, text, state)
    
    def get_yao_stats(self, palace_id: int = None) -> Dict[str, Any]:
        """获取六爻学习统计"""
        return self.yao_learning.get_stats(palace_id)
    
    # ========== 组队系统 ==========
    
    def build_team(self, scene: str, complexity: str = "standard") -> Dict[str, Any]:
        """场景组队"""
        return self.client.build_team(scene, complexity)
    
    def match_scene(self, text: str) -> Dict[str, Any]:
        """匹配场景"""
        return self.client.match_scene(text)
    
    # ========== 决策系统 ==========
    
    def make_decision(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """做出决策"""
        return self.decision_engine.decide(context)
    
    def check_idle(self) -> Dict[str, Any]:
        """检查空闲状态"""
        return self.idle_detector.check_idle()
    
    # ========== 五行循环 ==========
    
    def run_wuxing_check(self, task_result: Dict[str, Any] = None) -> Dict[str, Any]:
        """运行五行循环检查"""
        return self.wuxing_loop.check(task_result)
    
    def get_wuxing_status(self) -> Dict[str, Any]:
        """获取五行状态"""
        return self.wuxing_loop.get_status()
    
    # ========== 日报 ==========
    
    def generate_daily_report(self) -> Dict[str, Any]:
        """生成日报"""
        return self.daily_report.generate()
    
    # ========== 聊天 ==========
    
    def chat(self, message: str, history: List[Dict] = None) -> Dict[str, Any]:
        """与米珞聊天"""
        return self.chatbot.chat(message, history)
    
    # ========== 统计 ==========
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取系统统计"""
        return {
            "keywords": get_keyword_stats(),
            "yao_learning": self.yao_learning.get_stats(),
            "tasks": self.task_manager.get_statistics(),
            "palaces": self.client.get_all_palaces(),
        }
    
    # ========== 阴阳平衡 ==========
    
    def get_balance(self) -> Dict[str, Any]:
        """获取阴阳平衡状态"""
        return self.client.get_balance_status()
    
    def adjust_balance(self) -> Dict[str, Any]:
        """调整阴阳平衡"""
        return self.client.adjust_balance()


# 单例
_system = None

def get_system() -> TaijiSystem:
    """获取太极系统单例"""
    global _system
    if _system is None:
        _system = TaijiSystem()
    return _system


if __name__ == "__main__":
    # 测试
    print("=== 太极系统完整功能测试 ===\n")
    
    system = TaijiSystem()
    
    # 意识状态
    print("【意识状态】")
    status = system.get_consciousness_status()
    print(f"  旋转: {status.get('current_rotation', 'N/A')}")
    print(f"  能量: {status.get('energy', {}).get('level', 'N/A')}")
    print()
    
    # 九宫状态
    print("【九宫状态】")
    palaces = system.get_palaces()
    for pid, pinfo in palaces["palaces"].items():
        print(f"  {pinfo['name']}: 负载={pinfo['load']:.1f}")
    print()
    
    # 六爻探测
    print("【六爻探测】")
    result = system.detect_yao("API延迟很高，连接超时")
    if result['matched_palace']:
        print(f"  → {result['matched_palace']}宫 {result['matched_yao']}爻")
        print(f"  → 关键词: {result['matched_keywords']}")
    print()
    
    # 组队
    print("【场景组队】")
    team = system.build_team("download")
    print(f"  download: {team['team_names']}")
    print()
    
    # 统计
    print("【关键词统计】")
    stats = system.get_statistics()
    print(f"  总关键词: {stats['keywords']['total_keywords']}")
    print(f"  覆盖宫位: {stats['keywords']['palaces']}宫")