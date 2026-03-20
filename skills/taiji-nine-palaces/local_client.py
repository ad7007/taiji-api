#!/usr/bin/env python3
"""
太极九宫本地客户端 - 不依赖API直接执行
Taiji Nine Palaces Local Client - Direct Execution Without API

米珞直接使用，无需HTTP调用
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# 导入本地核心模块
from core.milo_core import TeamBuilder, TaskComplexity, Task, PalaceState
from core.taiji_algorithm import (
    auto_group_by_mode,
    get_generation_path,
    get_control_relations,
    get_central_axis,
    get_support_triangle,
    YANG_PALACES,
    YIN_PALACES,
    PALACE_ELEMENT,
)
# 导入六爻关键词模块
from yao_keywords import (
    detect_yao_from_text,
    get_detect_keywords,
    get_basic_keyword,
    get_palace_yao_summary,
    get_keyword_stats,
)


class TaijiLocalClient:
    """
    太极本地客户端 - 直接执行
    
    不依赖API，直接操作本地状态和算法
    """
    
    def __init__(self, data_dir: str = None):
        """
        初始化
        
        Args:
            data_dir: 数据目录（默认：skill目录下的data/）
        """
        self.data_dir = Path(data_dir) if data_dir else Path(__file__).parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        
        # 状态文件
        self.state_file = self.data_dir / "palace_states.json"
        self.task_file = self.data_dir / "active_tasks.json"
        
        # 宫位名称（必须先初始化）
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
        
        # 初始化组件
        self.team_builder = TeamBuilder()
        
        # 加载状态
        self.palace_states = self._load_states()
        self.active_tasks = self._load_tasks()
    
    # ========== 状态管理 ==========
    
    def _load_states(self) -> Dict[int, Dict]:
        """加载宫位状态"""
        if self.state_file.exists():
            data = json.loads(self.state_file.read_text())
            return {int(k): v for k, v in data.items()}
        return self._init_states()
    
    def _init_states(self) -> Dict[int, Dict]:
        """初始化宫位状态"""
        states = {}
        for i in range(1, 10):
            states[i] = {
                "name": self.palace_names.get(i, f"{i}宫"),
                "load": 0.0,
                "status": "idle",
                "current_task": None,
                "element": PALACE_ELEMENT.get(i, {}).value if hasattr(PALACE_ELEMENT.get(i), 'value') else "土"
            }
        self._save_states(states)
        return states
    
    def _save_states(self, states: Dict = None):
        """保存宫位状态"""
        states = states or self.palace_states
        self.state_file.write_text(json.dumps(states, indent=2, ensure_ascii=False))
    
    def _load_tasks(self) -> Dict[str, Dict]:
        """加载任务"""
        if self.task_file.exists():
            return json.loads(self.task_file.read_text())
        return {}
    
    def _save_tasks(self):
        """保存任务"""
        self.task_file.write_text(json.dumps(self.active_tasks, indent=2, ensure_ascii=False))
    
    # ========== 九宫查询 ==========
    
    def get_all_palaces(self) -> Dict[str, Any]:
        """获取所有宫位状态"""
        return {
            "palaces": {str(k): v for k, v in self.palace_states.items()}
        }
    
    def get_palace(self, palace_id: int) -> Dict[str, Any]:
        """获取单个宫位状态"""
        return self.palace_states.get(palace_id, {"error": f"Palace {palace_id} not found"})
    
    def update_palace_load(self, palace_id: int, load: float) -> Dict[str, Any]:
        """更新宫位负载"""
        if palace_id not in self.palace_states:
            return {"success": False, "error": f"Palace {palace_id} not found"}
        
        if not 0 <= load <= 1:
            return {"success": False, "error": "负载值必须在 0-1 之间"}
        
        self.palace_states[palace_id]["load"] = load
        self._save_states()
        
        return {"success": True, "message": f"Updated palace {palace_id} load to {load}"}
    
    # ========== 阴阳平衡 ==========
    
    def get_balance_status(self) -> Dict[str, Any]:
        """获取阴阳平衡状态"""
        # 计算各对宫位的平衡
        balance = {}
        
        # 4对主要矛盾
        pairs = [
            ("team_process", 3, 6),  # 技术团队 vs 物联监控
            ("tech_quality", 3, 2),  # 技术团队 vs 产品质量
            ("product_data", 2, 1),  # 产品质量 vs 数据采集
            ("monitor_eco", 6, 9),   # 物联监控 vs 行业生态
        ]
        
        for pair_name, p1, p2 in pairs:
            load1 = self.palace_states.get(p1, {}).get("load", 0)
            load2 = self.palace_states.get(p2, {}).get("load", 0)
            # 平衡度：差异越小越平衡
            diff = abs(load1 - load2)
            balance[pair_name] = round(1 - diff, 2)
        
        # 整体平衡
        yang_load = sum(self.palace_states.get(p, {}).get("load", 0) for p in YANG_PALACES)
        yin_load = sum(self.palace_states.get(p, {}).get("load", 0) for p in YIN_PALACES)
        
        return {
            "balance": balance,
            "yin_yang": {
                "yang_load": round(yang_load / 4, 2),
                "yin_load": round(yin_load / 4, 2),
                "balance": round(1 - abs(yang_load - yin_load) / max(yang_load + yin_load, 0.01), 2)
            },
            "imbalanced_pairs": [k for k, v in balance.items() if v < 0.6]
        }
    
    # ========== 组队与任务 ==========
    
    def build_team(self, scene: str, complexity: str = "standard") -> Dict[str, Any]:
        """
        根据场景自动组队
        
        Args:
            scene: 场景（download/code/brand等）
            complexity: 复杂度（simple/standard/complex/full）
        """
        complexity_map = {
            "simple": TaskComplexity.SIMPLE,
            "standard": TaskComplexity.STANDARD,
            "complex": TaskComplexity.COMPLEX,
            "full": TaskComplexity.FULL,
        }
        
        comp = complexity_map.get(complexity, TaskComplexity.STANDARD)
        team = self.team_builder.build_team(scene, comp)
        
        return {
            "success": True,
            "scene": scene,
            "complexity": complexity,
            "team": team,
            "team_names": [self.palace_names.get(p, str(p)) for p in team]
        }
    
    def create_task(self, task_id: str, title: str, scene: str, complexity: str = "standard") -> Dict[str, Any]:
        """创建任务"""
        team_result = self.build_team(scene, complexity)
        
        task = {
            "task_id": task_id,
            "title": title,
            "scene": scene,
            "complexity": complexity,
            "team": team_result["team"],
            "status": "created",
            "created_at": datetime.now().isoformat(),
            "flow_index": 0
        }
        
        self.active_tasks[task_id] = task
        self._save_tasks()
        
        # 更新宫位负载
        for p in task["team"]:
            self.palace_states[p]["load"] = min(1.0, self.palace_states[p]["load"] + 0.1)
            self.palace_states[p]["current_task"] = task_id
        self._save_states()
        
        return task
    
    def get_task(self, task_id: str) -> Optional[Dict]:
        """获取任务"""
        return self.active_tasks.get(task_id)
    
    def complete_task(self, task_id: str) -> Dict[str, Any]:
        """完成任务"""
        task = self.active_tasks.get(task_id)
        if not task:
            return {"success": False, "error": f"Task {task_id} not found"}
        
        # 释放宫位负载
        for p in task["team"]:
            self.palace_states[p]["load"] = max(0, self.palace_states[p]["load"] - 0.1)
            if self.palace_states[p]["current_task"] == task_id:
                self.palace_states[p]["current_task"] = None
        self._save_states()
        
        task["status"] = "completed"
        task["completed_at"] = datetime.now().isoformat()
        self._save_tasks()
        
        return {"success": True, "task": task}
    
    # ========== 太极算法 ==========
    
    def get_generation_path(self) -> List[int]:
        """五行相生路径"""
        return get_generation_path()
    
    def get_control_relations(self) -> List[tuple]:
        """相克关系"""
        return get_control_relations()
    
    def get_central_axis(self) -> tuple:
        """中轴线（1-5-9）"""
        return get_central_axis()
    
    # ========== Scene匹配 ==========
    
    def match_scene(self, text: str) -> Dict[str, Any]:
        """
        根据文本匹配场景
        
        Args:
            text: 用户输入文本
        """
        scene_keywords = {
            "download": ["下载", "download", "保存"],
            "scrape": ["抓取", "爬取", "scrape", "采集"],
            "transcribe": ["转录", "视频总结", "音频", "字幕"],
            "browser": ["打开网页", "点击", "截图", "登录"],
            "code": ["代码", "开发", "写代码", "编程"],
            "debug": ["调试", "debug", "修bug", "报错"],
            "brand": ["品牌", "竞品", "营销"],
            "research": ["行业", "研究", "分析"],
            "quality": ["质量", "检查", "质检"],
        }
        
        text_lower = text.lower()
        
        for scene, keywords in scene_keywords.items():
            for kw in keywords:
                if kw in text_lower:
                    return {
                        "matched": True,
                        "scene": scene,
                        "keyword": kw
                    }
        
        return {
            "matched": False,
            "scene": "dispatch",
            "keyword": None
        }
    
    # ========== 六爻关键词 ==========
    
    def detect_yao(self, text: str, palace_id: int = None) -> Dict[str, Any]:
        """
        从文本探测六爻状态
        
        Args:
            text: 待分析文本
            palace_id: 可选，指定宫位
        
        Returns:
            {
                "matched_palace": 匹配的宫位,
                "matched_yao": 匹配的爻位,
                "matched_keywords": 匹配的关键词,
                "yao_type": 阴/阳
            }
        """
        return detect_yao_from_text(text, palace_id)
    
    def get_yao_keywords(self, palace_id: int, yao_level: int) -> List[str]:
        """获取某爻的探测关键词"""
        return get_detect_keywords(palace_id, yao_level)
    
    def get_yao_summary(self, palace_id: int) -> Dict[str, Any]:
        """获取某宫的六爻关键词汇总"""
        return get_palace_yao_summary(palace_id)
    
    def get_keyword_statistics(self) -> Dict[str, Any]:
        """获取关键词统计"""
        return get_keyword_stats()


# 单例
_client = None

def get_client() -> TaijiLocalClient:
    """获取单例客户端"""
    global _client
    if _client is None:
        _client = TaijiLocalClient()
    return _client


if __name__ == "__main__":
    # 测试
    client = TaijiLocalClient()
    
    print("=== 太极九宫本地客户端测试 ===\n")
    
    # 获取九宫状态
    palaces = client.get_all_palaces()
    print("九宫状态:")
    for pid, pinfo in palaces["palaces"].items():
        print(f"  {pinfo['name']}: 负载={pinfo['load']}")
    
    # 组队测试
    print("\n场景组队:")
    for scene in ["download", "code", "brand"]:
        result = client.build_team(scene)
        print(f"  {scene}: {result['team_names']}")
    
    # 阴阳平衡
    print("\n阴阳平衡:")
    balance = client.get_balance_status()
    print(f"  {balance}")