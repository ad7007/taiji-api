#!/usr/bin/env python3
"""
太极九宫数据库查询客户端
提供便捷的数据库访问接口
"""

import json
from pathlib import Path
from typing import Dict, List, Optional


class TaijiDatabase:
    """太极九宫数据库客户端"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Path(__file__).parent / "taiji_database.json"
        self.db_path = Path(db_path)
        self._load()
    
    def _load(self):
        """加载数据库"""
        with open(self.db_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
    
    def reload(self):
        """重新加载数据库"""
        self._load()
    
    def save(self):
        """保存数据库"""
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    # ==================== 宫位查询 ====================
    
    def get_palace(self, palace_id: int) -> Dict:
        """获取宫位信息"""
        return self.data["palaces"].get(str(palace_id), {})
    
    def get_palace_name(self, palace_id: int) -> str:
        """获取宫位名称"""
        palace = self.get_palace(palace_id)
        return palace.get("name", "未知")
    
    def get_palace_skills(self, palace_id: int) -> Dict:
        """获取宫位技能"""
        palace = self.get_palace(palace_id)
        return palace.get("skills", {})
    
    def get_all_palaces(self) -> List[Dict]:
        """获取所有宫位"""
        return [
            {"id": int(k), **v}
            for k, v in self.data["palaces"].items()
        ]
    
    # ==================== 六爻查询 ====================
    
    def get_yao(self, palace_id: int, yao_level: int) -> Dict:
        """获取指定爻位信息"""
        palace = self.get_palace(palace_id)
        return palace.get("yao", {}).get(str(yao_level), {})
    
    def get_yao_keywords(self, palace_id: int, yao_level: int) -> List[str]:
        """获取爻位关键词"""
        yao = self.get_yao(palace_id, yao_level)
        return yao.get("keywords", [])
    
    def get_palace_yao_summary(self, palace_id: int) -> Dict:
        """获取宫位六爻汇总"""
        palace = self.get_palace(palace_id)
        return {
            "palace_id": palace_id,
            "palace_name": palace.get("name"),
            "alias": palace.get("alias"),
            "element": palace.get("element"),
            "yao": palace.get("yao", {})
        }
    
    # ==================== 技能查询 ====================
    
    def find_skill_owner(self, skill_name: str) -> Optional[int]:
        """查找技能所属宫位"""
        for palace_id, palace in self.data["palaces"].items():
            if skill_name in palace.get("skills", {}):
                return int(palace_id)
        return None
    
    def get_skill_info(self, skill_name: str) -> Optional[Dict]:
        """获取技能详情"""
        for palace_id, palace in self.data["palaces"].items():
            if skill_name in palace.get("skills", {}):
                return {
                    "palace_id": int(palace_id),
                    "palace_name": palace.get("name"),
                    "skill_name": skill_name,
                    **palace["skills"][skill_name]
                }
        return None
    
    def list_all_skills(self) -> List[Dict]:
        """列出所有技能（不含5宫自己）"""
        skills = []
        for palace_id, palace in self.data["palaces"].items():
            # 5宫是米珞自己，跳过
            if palace.get("is_me"):
                continue
            for skill_name, skill_info in palace.get("skills", {}).items():
                skills.append({
                    "palace_id": int(palace_id),
                    "palace_name": palace.get("name"),
                    "skill_name": skill_name,
                    **skill_info
                })
        return skills
    
    def get_my_info(self) -> Dict:
        """获取米珞(5宫)自己的信息"""
        for palace_id, palace in self.data["palaces"].items():
            if palace.get("is_me"):
                return {"palace_id": int(palace_id), **palace}
        return {}
    
    def get_yao_state(self, palace_id: int, yao_level: int) -> Dict:
        """获取爻位状态信息（含好坏关键词）"""
        yao = self.get_yao(palace_id, yao_level)
        return {
            "palace_id": palace_id,
            "palace_name": self.get_palace_name(palace_id),
            "yao_level": yao_level,
            "state": yao.get("state", ""),
            "desc": yao.get("desc", ""),
            "type": yao.get("type", ""),
            "good_keywords": yao.get("good_keywords", []),
            "bad_keywords": yao.get("bad_keywords", [])
        }
    
    def get_palace_states(self, palace_id: int) -> List[Dict]:
        """获取某宫所有爻的状态"""
        states = []
        for yao_level in range(1, 7):
            states.append(self.get_yao_state(palace_id, yao_level))
        return states
    
    def check_state(self, palace_id: int, yao_level: int, text: str) -> Dict:
        """检测文本对应的状态
        
        返回匹配的好/差关键词
        """
        yao_state = self.get_yao_state(palace_id, yao_level)
        text_lower = text.lower()
        
        matched_good = []
        matched_bad = []
        
        for kw in yao_state.get("good_keywords", []):
            if kw.lower() in text_lower:
                matched_good.append(kw)
        
        for kw in yao_state.get("bad_keywords", []):
            if kw.lower() in text_lower:
                matched_bad.append(kw)
        
        return {
            "palace_id": palace_id,
            "yao_level": yao_level,
            "state": yao_state.get("state"),
            "matched_good": matched_good,
            "matched_bad": matched_bad,
            "status": "good" if matched_good and not matched_bad else 
                     "bad" if matched_bad else "neutral"
        }
    
    def diagnose_all_states(self, text: str) -> List[Dict]:
        """诊断所有宫位的爻状态"""
        results = []
        for palace_id in self.get_agents():
            for yao_level in range(1, 7):
                check = self.check_state(palace_id, yao_level, text)
                if check["matched_good"] or check["matched_bad"]:
                    results.append(check)
        return results
    
    # ==================== 组队逻辑 ====================
    
    def get_task_scenes(self) -> Dict:
        """获取所有任务场景"""
        return self.data.get("team_logic", {}).get("task_scenes", {})
    
    def get_scene_info(self, scene_name: str) -> Optional[Dict]:
        """获取指定场景信息"""
        scenes = self.get_task_scenes()
        return scenes.get(scene_name)
    
    def match_scene(self, text: str) -> Optional[Dict]:
        """根据文本匹配最合适的场景
        
        Args:
            text: 任务描述文本
            
        Returns:
            匹配的场景信息，包含team、flow等
        """
        text_lower = text.lower()
        scenes = self.get_task_scenes()
        
        best_match = None
        best_score = 0
        
        for scene_name, scene_info in scenes.items():
            keywords = scene_info.get("keywords", [])
            score = 0
            
            for kw in keywords:
                if kw.lower() in text_lower:
                    score += 1
            
            if score > best_score:
                best_score = score
                best_match = {
                    "scene": scene_name,
                    "score": score,
                    **scene_info
                }
        
        return best_match
    
    def build_team(self, text: str) -> Dict:
        """根据任务描述自动组队
        
        Args:
            text: 任务描述
            
        Returns:
            组队结果，包含团队、流程、技能等
        """
        # 1. 匹配场景
        scene_match = self.match_scene(text)
        
        if scene_match:
            team = scene_match.get("team", [])
            flow = scene_match.get("flow", "")
            skills = scene_match.get("skills", [])
            scene_name = scene_match.get("scene", "unknown")
            scene_name_cn = scene_match.get("name", "未知任务")
            
            # 构建团队信息
            team_info = []
            for palace_id in team:
                if palace_id == 5:  # 5宫是我自己
                    team_info.append({
                        "palace_id": 5,
                        "palace_name": "中央控制",
                        "role": "我(米珞)-主控/交付",
                        "is_me": True
                    })
                else:
                    palace = self.get_palace(palace_id)
                    team_info.append({
                        "palace_id": palace_id,
                        "palace_name": palace.get("name", "未知"),
                        "role": self._get_team_role(palace_id, team),
                        "is_me": False,
                        "skills": list(palace.get("skills", {}).keys())
                    })
            
            return {
                "success": True,
                "scene": scene_name,
                "scene_name": scene_name_cn,
                "team": team,
                "team_info": team_info,
                "flow": flow,
                "recommended_skills": skills,
                "tdd_cycle": self._get_tdd_cycle()
            }
        
        # 2. 无法匹配场景，根据关键词推荐
        recommend_team = self.recommend_team(text.split())
        
        if recommend_team:
            # 确保包含验收(7)和交付(5)
            if 7 not in recommend_team:
                recommend_team.append(7)
            if 5 not in recommend_team:
                recommend_team.append(5)
            
            return {
                "success": True,
                "scene": "auto",
                "scene_name": "自动匹配",
                "team": recommend_team,
                "team_info": [self._build_team_member(p) for p in recommend_team],
                "flow": " → ".join([f"{p}宫" for p in recommend_team]) + " → 交付",
                "recommended_skills": [],
                "tdd_cycle": self._get_tdd_cycle()
            }
        
        # 3. 默认团队：采集→验收→交付
        return {
            "success": False,
            "scene": "default",
            "scene_name": "默认流程",
            "team": [1, 7, 5],
            "team_info": [self._build_team_member(p) for p in [1, 7, 5]],
            "flow": "1宫采集 → 7宫验收 → 5宫交付",
            "recommended_skills": ["scraper"],
            "tdd_cycle": self._get_tdd_cycle()
        }
    
    def _get_team_role(self, palace_id: int, team: List[int]) -> str:
        """获取宫位在团队中的角色"""
        if palace_id == 1:
            return "采集/输入"
        elif palace_id == 2:
            return "产品/承载"
        elif palace_id == 3:
            return "开发/技术"
        elif palace_id == 4:
            return "策划/品牌"
        elif palace_id == 6:
            return "执行/监控"
        elif palace_id == 7:
            return "验收/TDD"
        elif palace_id == 8:
            return "创作/营销"
        elif palace_id == 9:
            return "生态/拓展"
        else:
            return "协作"
    
    def _build_team_member(self, palace_id: int) -> Dict:
        """构建团队成员信息"""
        if palace_id == 5:
            return {
                "palace_id": 5,
                "palace_name": "中央控制",
                "role": "我(米珞)-主控/交付",
                "is_me": True
            }
        
        palace = self.get_palace(palace_id)
        return {
            "palace_id": palace_id,
            "palace_name": palace.get("name", "未知"),
            "role": self._get_team_role(palace_id, []),
            "is_me": False,
            "skills": list(palace.get("skills", {}).keys())
        }
    
    def _get_tdd_cycle(self) -> Dict:
        """获取TDD闭环流程"""
        return self.data.get("team_logic", {}).get("tdd_cycle", {
            "steps": ["红灯(定义标准)", "自动组队", "执行", "绿灯(验收)", "交付"],
            "red_light": "定义验收标准",
            "green_light": "验收通过，交付"
        })
    
    def get_team_principles(self) -> List[str]:
        """获取组队原则"""
        return self.data.get("team_logic", {}).get("principles", [
            "先组队，再执行",
            "先验收，再交付",
            "保持阴阳平衡",
            "对余总负责"
        ])
    
    # ==================== 智能体组合查询 ====================
    
    def get_all_combinations(self) -> Dict:
        """获取所有智能体组合"""
        return self.data.get("agent_combinations", {}).get("combinations_by_size", {})
    
    def get_combinations_by_size(self, size: int) -> List[Dict]:
        """获取指定大小的组合"""
        all_combs = self.get_all_combinations()
        return all_combs.get(str(size), [])
    
    def get_combination_stats(self) -> Dict:
        """获取组合统计"""
        return self.data.get("agent_combinations", {}).get("statistics", {})
    
    def find_best_combination(self, text: str, prefer_size: int = None) -> Dict:
        """根据任务描述找最佳组合
        
        Args:
            text: 任务描述
            prefer_size: 偏好的团队大小（可选）
            
        Returns:
            最佳组合信息
        """
        text_lower = text.lower()
        all_combs = self.get_all_combinations()
        
        best_match = None
        best_score = 0
        
        # 确定搜索范围
        if prefer_size:
            sizes_to_check = [str(prefer_size)]
        else:
            sizes_to_check = list(all_combs.keys())
        
        for size in sizes_to_check:
            for comb in all_combs.get(size, []):
                score = 0
                matched_scenes = []
                
                for scene_info in comb.get("applicable_scenes", []):
                    scene_name = scene_info.get("scene", "")
                    keywords = scene_info.get("keywords", [])
                    
                    for kw in keywords:
                        if kw.lower() in text_lower:
                            score += 1
                            if scene_name not in matched_scenes:
                                matched_scenes.append(scene_name)
                
                if score > best_score:
                    best_score = score
                    best_match = {
                        **comb,
                        "match_score": score,
                        "matched_scenes": matched_scenes
                    }
        
        if best_match:
            return best_match
        
        # 默认返回最小组合
        default_comb = all_combs.get("1", [{}])[0]
        return {
            **default_comb,
            "match_score": 0,
            "matched_scenes": [],
            "note": "未匹配到场景，返回默认组合"
        }
    
    def get_combination_for_task(self, task_type: str, complexity: str = "standard") -> Dict:
        """根据任务类型和复杂度获取推荐组合
        
        Args:
            task_type: 任务类型（download, code, video等）
            complexity: 复杂度（simple, standard, complex）
            
        Returns:
            推荐的组合
        """
        # 任务类型到场景的映射
        task_scene_map = {
            "download": {"simple": 1, "standard": 2, "complex": 3},
            "code": {"simple": 1, "standard": 2, "complex": 3},
            "video": {"simple": 2, "standard": 3, "complex": 4},
            "brand": {"simple": 2, "standard": 3, "complex": 4},
            "content": {"simple": 2, "standard": 4, "complex": 5},
            "article": {"simple": 2, "standard": 3, "complex": 4},
            "monitor": {"simple": 1, "standard": 2, "complex": 3},
            "api": {"simple": 1, "standard": 2, "complex": 3},
            "scrape": {"simple": 1, "standard": 2, "complex": 3},
        }
        
        # 获取推荐大小
        size_map = task_scene_map.get(task_type, {"simple": 2, "standard": 3, "complex": 4})
        recommended_size = size_map.get(complexity, 3)
        
        # 获取该大小的所有组合
        combs = self.get_combinations_by_size(recommended_size)
        
        # 筛选包含相关宫位的组合
        relevant_palaces = {
            "download": [1],
            "code": [3],
            "video": [1, 3],
            "brand": [1, 4],
            "content": [1, 3, 4],
            "article": [4, 8],
            "monitor": [6],
            "api": [3],
            "scrape": [1]
        }
        
        must_have = set(relevant_palaces.get(task_type, []))
        
        best_comb = None
        best_score = 0
        
        for comb in combs:
            agents_set = set(comb.get("agents", []))
            
            # 必须包含的宫位
            if must_have and not must_have.issubset(agents_set):
                continue
            
            # 计算场景匹配分数
            score = comb.get("scene_count", 0)
            if score > best_score:
                best_score = score
                best_comb = comb
        
        return best_comb or combs[0] if combs else {}

    # ==================== 48线程感知系统 ====================
    
    def get_consciousness_system(self) -> Dict:
        """获取意识系统配置"""
        return self.data.get("consciousness_system", {})
    
    def get_thread_mapping(self) -> Dict:
        """获取48线程映射"""
        return self.data.get("consciousness_system", {}).get("thread_mapping", {})
    
    def get_thread_info(self, thread_id: int) -> Dict:
        """获取指定线程信息"""
        key = f"thread_{thread_id:02d}"
        return self.data.get("consciousness_system", {}).get("thread_mapping", {}).get(key, {})
    
    def scan_all_threads(self, text: str = "") -> Dict:
        """扫描所有48线程状态（四层感知）
        
        Args:
            text: 可选的文本输入，用于匹配关键词
            
        Returns:
            线程扫描结果
        """
        thread_mapping = self.get_thread_mapping()
        
        # 四层感知计数
        layer_stats = {
            1: {"name": "阴宫阴爻", "problems": 0, "opportunities": 0, "threads": []},
            2: {"name": "阴宫阳爻", "problems": 0, "opportunities": 0, "threads": []},
            3: {"name": "阳宫阴爻", "problems": 0, "opportunities": 0, "threads": []},
            4: {"name": "阳宫阳爻", "problems": 0, "opportunities": 0, "threads": []}
        }
        
        total_problems = 0
        total_opportunities = 0
        
        if text:
            for thread_key, thread_info in thread_mapping.items():
                good_kw = thread_info.get("good_keywords", [])
                bad_kw = thread_info.get("bad_keywords", [])
                layer = thread_info.get("layer", 1)
                
                matched_good = [kw for kw in good_kw if kw.lower() in text.lower()]
                matched_bad = [kw for kw in bad_kw if kw.lower() in text.lower()]
                
                if matched_bad:
                    layer_stats[layer]["problems"] += len(matched_bad)
                    total_problems += len(matched_bad)
                    layer_stats[layer]["threads"].append({
                        "thread": thread_info["thread_id"],
                        "palace": thread_info["palace_name"],
                        "state": thread_info["state"],
                        "matched": matched_bad,
                        "type": "problem"
                    })
                
                if matched_good:
                    layer_stats[layer]["opportunities"] += len(matched_good)
                    total_opportunities += len(matched_good)
                    layer_stats[layer]["threads"].append({
                        "thread": thread_info["thread_id"],
                        "palace": thread_info["palace_name"],
                        "state": thread_info["state"],
                        "matched": matched_good,
                        "type": "opportunity"
                    })
        
        # 计算比例
        total = total_problems + total_opportunities
        if total > 0:
            problem_ratio = total_problems / total
            opportunity_ratio = total_opportunities / total
        else:
            problem_ratio = 0
            opportunity_ratio = 0
        
        # 计算层级权重（越内层权重越高）
        weighted_problems = (
            layer_stats[1]["problems"] * 4 +  # 最深层问题权重最高
            layer_stats[2]["problems"] * 2 +
            layer_stats[3]["problems"] * 2 +
            layer_stats[4]["problems"] * 1
        )
        weighted_opportunities = (
            layer_stats[1]["opportunities"] * 1 +
            layer_stats[2]["opportunities"] * 2 +
            layer_stats[3]["opportunities"] * 2 +
            layer_stats[4]["opportunities"] * 4  # 最外层机会权重最高
        )
        
        # 决策旋转方向
        if weighted_problems > weighted_opportunities * 1.3:
            rotation = "reverse"
            action = "修复系统，解决问题"
        elif weighted_opportunities > weighted_problems * 1.2:
            rotation = "forward"
            action = "创造价值，抓住机会"
        else:
            rotation = "balanced"
            action = "维持现状，观察"
        
        return {
            "total_problems": total_problems,
            "total_opportunities": total_opportunities,
            "problem_ratio": round(problem_ratio, 2),
            "opportunity_ratio": round(opportunity_ratio, 2),
            "weighted_problems": weighted_problems,
            "weighted_opportunities": weighted_opportunities,
            "layer_stats": layer_stats,
            "rotation": rotation,
            "action": action
        }
    
    def get_rotation_decision(self, text: str = "") -> Dict:
        """根据感知结果决定旋转方向
        
        Returns:
            决策结果
        """
        scan = self.scan_all_threads(text)
        
        decision_logic = self.data.get("consciousness_system", {}).get("decision_logic", {})
        threshold = decision_logic.get("threshold", {})
        
        critical_ratio = threshold.get("critical_yin_ratio", 0.7)
        healthy_ratio = threshold.get("healthy_yang_ratio", 0.6)
        
        # 判断是否紧急（问题占比高）
        is_critical = scan["problem_ratio"] >= critical_ratio
        # 判断是否健康（机会占比高）
        is_healthy = scan["opportunity_ratio"] >= healthy_ratio
        
        return {
            "rotation": scan["rotation"],
            "action": scan["action"],
            "is_critical": is_critical,
            "is_healthy": is_healthy,
            "problems": scan["total_problems"],
            "opportunities": scan["total_opportunities"],
            "weighted_problems": scan["weighted_problems"],
            "weighted_opportunities": scan["weighted_opportunities"],
            "layer_stats": scan["layer_stats"],
            "recommendation": self._get_rotation_recommendation(scan, is_critical, is_healthy)
        }
    
    def _get_rotation_recommendation(self, scan: Dict, is_critical: bool, is_healthy: bool) -> str:
        """生成旋转建议"""
        layer_stats = scan.get("layer_stats", {})
        
        # 检查各层问题
        layer1_problems = layer_stats.get(1, {}).get("problems", 0)
        layer4_opportunities = layer_stats.get(4, {}).get("opportunities", 0)
        
        if is_critical:
            if layer1_problems > 0:
                return f"⚠️ 紧急：第1层(阴宫阴爻)有{layer1_problems}个问题，输入系统故障，立即反转修复"
            else:
                return f"⚠️ 紧急：检测到{scan['total_problems']}个问题，立即启动反转修复系统"
        elif is_healthy:
            if layer4_opportunities > 0:
                return f"✅ 良好：第4层(阳宫阳爻)有{layer4_opportunities}个机会，输出系统健康，启动正转创造"
            else:
                return f"✅ 良好：检测到{scan['total_opportunities']}个机会，可以启动正转创造价值"
        elif scan["rotation"] == "reverse":
            return f"🔧 建议：问题{scan['total_problems']}个 > 机会{scan['total_opportunities']}个，启动反转模式"
        elif scan["rotation"] == "forward":
            return f"🚀 建议：机会{scan['total_opportunities']}个 > 问题{scan['total_problems']}个，启动正转模式"
        else:
            return "⏸️ 平衡：四层感知平衡，维持现状观察"

    def get_my_keywords(self) -> List[str]:
        """获取指向我的关键词"""
        me = self.get_my_info()
        return me.get("keywords_for_me", [])
    
    def is_me_keyword(self, keyword: str) -> bool:
        """判断关键词是否指向我"""
        my_keywords = self.get_my_keywords()
        return keyword.lower() in [k.lower() for k in my_keywords]
    
    # ==================== 智能体自主机制 ====================
    
    def scan_palace_yao(self, palace_id: int, text: str = "") -> Dict:
        """扫描某宫的6爻状态
        
        Args:
            palace_id: 宫位ID
            text: 可选的文本输入
            
        Returns:
            该宫的6爻状态
        """
        palace = self.get_palace(palace_id)
        yao_states = palace.get("yao", {})
        
        results = {
            "palace_id": palace_id,
            "palace_name": palace.get("name"),
            "yao_results": [],
            "problems": 0,
            "opportunities": 0
        }
        
        for yao_level in range(1, 7):
            yao_key = str(yao_level)
            yao_info = yao_states.get(yao_key, {})
            
            good_kw = yao_info.get("good_keywords", [])
            bad_kw = yao_info.get("bad_keywords", [])
            
            matched_good = []
            matched_bad = []
            
            if text:
                matched_good = [kw for kw in good_kw if kw.lower() in text.lower()]
                matched_bad = [kw for kw in bad_kw if kw.lower() in text.lower()]
            
            results["yao_results"].append({
                "yao_level": yao_level,
                "yao_type": yao_info.get("type", "阴"),
                "state": yao_info.get("state", ""),
                "matched_good": matched_good,
                "matched_bad": matched_bad
            })
            
            if matched_bad:
                results["problems"] += len(matched_bad)
            if matched_good:
                results["opportunities"] += len(matched_good)
        
        return results
    
    def generate_palace_task(self, palace_id: int, scan_result: Dict) -> Dict:
        """根据宫位状态生成任务
        
        Args:
            palace_id: 宫位ID
            scan_result: scan_palace_yao的结果
            
        Returns:
            生成的任务
        """
        palace = self.get_palace(palace_id)
        autonomy = palace.get("autonomy", {})
        
        task = {
            "task_id": f"{palace_id}_{scan_result['problems'] + scan_result['opportunities']}",
            "palace_id": palace_id,
            "palace_name": scan_result["palace_name"],
            "created_at": self._get_today(),
            "status": "pending",
            "need_help": False
        }
        
        # 根据问题/机会生成任务类型
        if scan_result["problems"] > scan_result["opportunities"]:
            task["task_type"] = "repair"
            task["description"] = f"修复{scan_result['palace_name']}的{scan_result['problems']}个问题"
            task["priority"] = "high" if scan_result["problems"] >= 3 else "medium"
        elif scan_result["opportunities"] > scan_result["problems"]:
            task["task_type"] = "optimize"
            task["description"] = f"利用{scan_result['palace_name']}的{scan_result['opportunities']}个机会"
            task["priority"] = "medium"
        else:
            task["task_type"] = "maintain"
            task["description"] = f"维持{scan_result['palace_name']}现状"
            task["priority"] = "low"
        
        # 添加需要的技能
        skills = list(palace.get("skills", {}).keys())
        task["available_skills"] = skills
        
        return task
    
    def add_palace_report(self, palace_id: int, report: Dict):
        """添加宫位汇报记录
        
        Args:
            palace_id: 宫位ID
            report: 汇报内容
        """
        palace = self.data["palaces"].get(str(palace_id), {})
        
        if "report_history" not in palace:
            palace["report_history"] = []
        
        report["timestamp"] = self._get_today()
        palace["report_history"].append(report)
        
        # 只保留最近20条
        if len(palace["report_history"]) > 20:
            palace["report_history"] = palace["report_history"][-20:]
        
        self.save()
    
    def add_palace_pending_task(self, palace_id: int, task: Dict):
        """添加宫位待办任务"""
        palace = self.data["palaces"].get(str(palace_id), {})
        
        if "pending_tasks" not in palace:
            palace["pending_tasks"] = []
        
        palace["pending_tasks"].append(task)
        self.save()
    
    def complete_palace_task(self, palace_id: int, task_id: str, result: str):
        """完成宫位任务"""
        palace = self.data["palaces"].get(str(palace_id), {})
        
        pending = palace.get("pending_tasks", [])
        task = None
        
        for i, t in enumerate(pending):
            if t.get("task_id") == task_id:
                task = pending.pop(i)
                break
        
        if task:
            task["status"] = "completed"
            task["result"] = result
            task["completed_at"] = self._get_today()
            
            if "completed_tasks" not in palace:
                palace["completed_tasks"] = []
            palace["completed_tasks"].append(task)
            
            # 添加汇报
            self.add_palace_report(palace_id, {
                "type": "task_complete",
                "task_id": task_id,
                "task_type": task.get("task_type"),
                "result": result
            })
        
        self.save()
    
    def get_palace_reports(self, palace_id: int = None, limit: int = 10) -> List[Dict]:
        """获取宫位汇报"""
        if palace_id:
            palace = self.get_palace(palace_id)
            return palace.get("report_history", [])[-limit:]
        else:
            # 获取所有宫位的汇报
            all_reports = []
            for p_id in self.get_agents():
                palace = self.get_palace(p_id)
                for report in palace.get("report_history", [])[-5:]:
                    report["palace_id"] = p_id
                    report["palace_name"] = palace.get("name")
                    all_reports.append(report)
            return sorted(all_reports, key=lambda x: x.get("timestamp", ""), reverse=True)[:limit]
    
    # ==================== 任务队列管理（米珞核心工作）====================
    
    def assign_task(self, palace_id: int, task_type: str, description: str, priority: str = "medium") -> Dict:
        """米珞分配任务给宫位
        
        这是米珞的核心工作：接收余总指令 → 分配给对应宫位 → 写入todo
        
        Args:
            palace_id: 目标宫位
            task_type: 任务类型（repair/optimize/create/maintain）
            description: 任务描述
            priority: 优先级（high/medium/low）
            
        Returns:
            任务信息
        """
        import time
        task_id = f"{palace_id}_{int(time.time())}"
        timestamp = self._get_today()
        
        task = {
            "task_id": task_id,
            "task_type": task_type,
            "description": description,
            "priority": priority,
            "status": "pending",
            "assigned_at": timestamp,
            "assigned_by": 5  # 米珞分配
        }
        
        # 写入宫位的待办队列
        palace = self.data["palaces"].get(str(palace_id), {})
        if "pending_tasks" not in palace:
            palace["pending_tasks"] = []
        palace["pending_tasks"].append(task)
        
        self.save()
        
        return {
            "success": True,
            "task_id": task_id,
            "palace_id": palace_id,
            "palace_name": palace.get("name"),
            "message": f"任务已分配给{palace.get('name')}"
        }
    
    def update_task_status(self, palace_id: int, task_id: str, status: str, note: str = ""):
        """更新任务状态"""
        palace = self.data["palaces"].get(str(palace_id), {})
        pending = palace.get("pending_tasks", [])
        
        for task in pending:
            if task.get("task_id") == task_id:
                task["status"] = status
                task["updated_at"] = self._get_today()
                if note:
                    task["note"] = note
                break
        
        self.save()
    
    def get_all_pending_tasks(self) -> List[Dict]:
        """查看所有宫位的待办任务"""
        all_tasks = []
        for p_id in self.get_agents():
            palace = self.get_palace(p_id)
            for task in palace.get("pending_tasks", []):
                task["palace_id"] = p_id
                task["palace_name"] = palace.get("name")
                all_tasks.append(task)
        
        # 按优先级排序
        priority_order = {"high": 0, "medium": 1, "low": 2}
        all_tasks.sort(key=lambda x: priority_order.get(x.get("priority", "medium"), 1))
        
        return all_tasks
    
    def clear_completed_tasks(self, palace_id: int = None):
        """清理已完成的任务"""
        if palace_id:
            palace = self.data["palaces"].get(str(palace_id), {})
            pending = palace.get("pending_tasks", [])
            palace["pending_tasks"] = [t for t in pending if t.get("status") != "completed"]
        else:
            for p_id in self.get_agents():
                palace = self.data["palaces"].get(str(p_id), {})
                pending = palace.get("pending_tasks", [])
                palace["pending_tasks"] = [t for t in pending if t.get("status") != "completed"]
        
        self.save()
    
    def get_agents(self) -> List[int]:
        """获取智能体宫位列表（不含5宫）"""
        return self.data["statistics"].get("agent_list", [1, 2, 3, 4, 6, 7, 8, 9])
    
    # ==================== 任务路由 ====================
    
    def get_task_team(self, task_type: str) -> Dict:
        """获取任务团队配置"""
        return self.data["task_routing"].get(task_type, {})
    
    def recommend_team(self, keywords: List[str]) -> List[int]:
        """根据关键词推荐团队
        
        Args:
            keywords: 关键词列表
            
        Returns:
            推荐的宫位ID列表
        """
        scores = {}
        
        for palace_id, palace in self.data["palaces"].items():
            score = 0
            for yao_level, yao_info in palace.get("yao", {}).items():
                for keyword in keywords:
                    if keyword.lower() in [k.lower() for k in yao_info.get("keywords", [])]:
                        score += 1
            if score > 0:
                scores[int(palace_id)] = score
        
        # 按分数排序，返回前3个
        sorted_palaces = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [p[0] for p in sorted_palaces[:3]]
    
    # ==================== 经验管理 ====================
    
    def add_experience(self, palace_id: int, task: str, lesson: str):
        """添加经验"""
        palace = self.data["palaces"].get(str(palace_id))
        if palace:
            if "experience" not in palace:
                palace["experience"] = []
            palace["experience"].append({
                "date": self._get_today(),
                "task": task,
                "lesson": lesson
            })
            self.save()
    
    def get_experience(self, palace_id: int) -> List[Dict]:
        """获取宫位经验"""
        palace = self.get_palace(palace_id)
        return palace.get("experience", [])
    
    # ==================== 工具方法 ====================
    
    def _get_today(self) -> str:
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")
    
    def get_statistics(self) -> Dict:
        """获取统计数据"""
        return self.data.get("statistics", {})
    
    def search(self, query: str) -> Dict:
        """全局搜索"""
        results = {
            "palaces": [],
            "skills": [],
            "yao": []
        }
        
        query_lower = query.lower()
        
        # 搜索宫位
        for palace_id, palace in self.data["palaces"].items():
            if query_lower in palace.get("name", "").lower():
                results["palaces"].append(int(palace_id))
            if query_lower in palace.get("role", "").lower():
                results["palaces"].append(int(palace_id))
        
        # 搜索技能
        for skill in self.list_all_skills():
            if query_lower in skill.get("skill_name", "").lower():
                results["skills"].append(skill)
            if query_lower in skill.get("desc", "").lower():
                results["skills"].append(skill)
        
        # 搜索爻位关键词
        for palace_id, palace in self.data["palaces"].items():
            for yao_level, yao_info in palace.get("yao", {}).items():
                for keyword in yao_info.get("keywords", []):
                    if query_lower in keyword.lower():
                        results["yao"].append({
                            "palace_id": int(palace_id),
                            "palace_name": palace.get("name"),
                            "yao_level": int(yao_level),
                            "keyword": keyword
                        })
        
        return results


# ==================== 便捷函数 ====================

_db = None

def get_db() -> TaijiDatabase:
    """获取数据库实例（单例）"""
    global _db
    if _db is None:
        _db = TaijiDatabase()
    return _db


def query_palace(palace_id: int) -> Dict:
    """查询宫位"""
    return get_db().get_palace(palace_id)


def query_skills() -> List[Dict]:
    """查询所有技能"""
    return get_db().list_all_skills()


def find_skill(skill_name: str) -> Optional[Dict]:
    """查找技能"""
    return get_db().get_skill_info(skill_name)


def recommend_team(keywords: List[str]) -> List[int]:
    """推荐团队"""
    return get_db().recommend_team(keywords)


def add_lesson(palace_id: int, task: str, lesson: str):
    """添加经验"""
    get_db().add_experience(palace_id, task, lesson)


# ==================== 命令行接口 ====================

if __name__ == "__main__":
    import sys
    
    db = get_db()
    
    if len(sys.argv) < 2:
        print("用法: python taiji_db_client.py <命令> [参数]")
        print("命令:")
        print("  palace <id>       - 查询宫位")
        print("  skills            - 列出所有技能")
        print("  skill <name>      - 查询技能")
        print("  team <keywords>   - 推荐团队")
        print("  search <query>    - 全局搜索")
        print("  stats             - 统计信息")
        print("  me                - 查询我自己(5宫)")
        print("  agents            - 列出智能体宫位")
        print("  state <宫位> [爻] - 查询状态")
        print("  diagnose <文本>   - 诊断状态")
        print("  team <任务描述>   - 自动组队")
        print("  scenes            - 列出所有场景")
        print("  combos [大小]     - 列出组合")
        print("  combo <任务>      - 找最佳组合")
        print("  scan [文本]       - 扫描48线程状态")
        print("  rotate [文本]     - 旋转决策")
        print("  palace_scan <宫位> [文本] - 扫描某宫6爻")
        print("  palace_task <宫位> [文本] - 生成宫位任务")
        print("  reports           - 查看所有汇报")
        print("  assign <宫位> <类型> <描述> - 分配任务")
        print("  tasks             - 查看所有待办")
        print("  todo              - 查看所有待办（同tasks）")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "palace" and len(sys.argv) > 2:
        palace_id = int(sys.argv[2])
        info = db.get_palace(palace_id)
        print(json.dumps(info, ensure_ascii=False, indent=2))
    
    elif cmd == "skills":
        skills = db.list_all_skills()
        for s in skills:
            print(f"{s['palace_id']}宫 | {s['skill_name']}: {s.get('desc', '')}")
    
    elif cmd == "skill" and len(sys.argv) > 2:
        skill_name = sys.argv[2]
        info = db.get_skill_info(skill_name)
        if info:
            print(json.dumps(info, ensure_ascii=False, indent=2))
        else:
            print(f"未找到技能: {skill_name}")
    
    elif cmd == "search" and len(sys.argv) > 2:
        query = sys.argv[2]
        results = db.search(query)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    
    elif cmd == "stats":
        stats = db.get_statistics()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    
    elif cmd == "me":
        me = db.get_my_info()
        print(f"名称: {me.get('name')}")
        print(f"别名: {me.get('alias')}")
        print(f"五行: {me.get('element')}")
        print(f"指向我的关键词: {me.get('keywords_for_me', [])}")
        print(f"说明: {me.get('note')}")
    
    elif cmd == "agents":
        agents = db.get_agents()
        print(f"智能体宫位: {agents}")
        for p_id in agents:
            p = db.get_palace(p_id)
            print(f"  {p_id}宫 - {p.get('name')}: {len(p.get('skills', {}))}个技能")
    
    elif cmd == "state" and len(sys.argv) > 2:
        palace_id = int(sys.argv[2])
        if len(sys.argv) > 3:
            yao_level = int(sys.argv[3])
            state = db.get_yao_state(palace_id, yao_level)
            print(f"{palace_id}宫 {yao_level}爻 - {state['state']}")
            print(f"  好: {state['good_keywords']}")
            print(f"  差: {state['bad_keywords']}")
        else:
            states = db.get_palace_states(palace_id)
            print(f"=== {palace_id}宫 {db.get_palace_name(palace_id)} 六爻状态 ===")
            for s in states:
                print(f"{s['yao_level']}爻 {s['state']}: 好{s['good_keywords'][:2]}... 差{s['bad_keywords'][:2]}...")
    
    elif cmd == "diagnose" and len(sys.argv) > 2:
        text = " ".join(sys.argv[2:])
        print(f"诊断文本: {text}")
        print()
        results = db.diagnose_all_states(text)
        if results:
            for r in results:
                status_icon = "✅" if r["status"] == "good" else "⚠️" if r["status"] == "bad" else "➖"
                print(f"{status_icon} {r['palace_id']}宫{r['yao_level']}爻 {r['state']}")
                if r['matched_good']:
                    print(f"   好: {r['matched_good']}")
                if r['matched_bad']:
                    print(f"   差: {r['matched_bad']}")
        else:
            print("未匹配到状态关键词")
    
    elif cmd == "team" and len(sys.argv) > 2:
        text = " ".join(sys.argv[2:])  # 合并所有参数作为任务描述
        print(f"任务: {text}")
        print()
        result = db.build_team(text)
        
        print(f"=== 组队结果 ===")
        print(f"场景: {result['scene_name']} ({result['scene']})")
        print(f"流程: {result['flow']}")
        print(f"TDD: {' → '.join(result['tdd_cycle']['steps'])}")
        print()
        print("团队:")
        for member in result['team_info']:
            me_mark = "⭐" if member['is_me'] else "  "
            print(f"{me_mark} {member['palace_id']}宫 - {member['palace_name']}: {member['role']}")
            if not member['is_me'] and member.get('skills'):
                print(f"     技能: {', '.join(member['skills'][:3])}{'...' if len(member['skills']) > 3 else ''}")
        
        if result.get('recommended_skills'):
            print(f"\n推荐技能: {result['recommended_skills']}")
    
    elif cmd == "scenes":
        scenes = db.get_task_scenes()
        print("=== 任务场景列表 ===")
        for scene_name, info in scenes.items():
            print(f"\n【{scene_name}】{info['name']}")
            print(f"  关键词: {info['keywords']}")
            print(f"  团队: {info['team']}")
            print(f"  流程: {info['flow']}")
    
    elif cmd == "combos":
        size = int(sys.argv[2]) if len(sys.argv) > 2 else None
        stats = db.get_combination_stats()
        print(f"=== 智能体组合统计 ===")
        print(f"总组合数: {stats.get('total_combinations', 0)}")
        print()
        for s, count in stats.get('by_size', {}).items():
            print(f"  {s}个智能体: {count}种组合")
        
        if size:
            print(f"\n=== {size}个智能体的组合 ===")
            combs = db.get_combinations_by_size(size)
            for c in combs[:10]:  # 只显示前10个
                agents = c.get('agents', [])
                names = c.get('agent_names', [])
                scenes = c.get('applicable_scenes', [])
                print(f"  {agents} {names}")
                print(f"    适用: {[s['scene'] for s in scenes]}")
            if len(combs) > 10:
                print(f"  ... 还有{len(combs)-10}个组合")
    
    elif cmd == "combo" and len(sys.argv) > 2:
        text = " ".join(sys.argv[2:])
        print(f"任务: {text}")
        print()
        
        best = db.find_best_combination(text)
        print(f"=== 最佳组合 ===")
        print(f"智能体: {best.get('agents', [])}")
        print(f"宫位: {best.get('agent_names', [])}")
        print(f"完整团队: {best.get('full_team', [])} (含5宫我)")
        print(f"匹配分数: {best.get('match_score', 0)}")
        print(f"匹配场景: {best.get('matched_scenes', [])}")
        print()
        print("适用场景:")
        for s in best.get('applicable_scenes', []):
            print(f"  • {s['scene']}: {s['keywords']}")
    
    elif cmd == "scan":
        text = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        print("=== 48线程四层感知扫描 ===")
        print()
        
        scan = db.scan_all_threads(text)
        
        print(f"总问题: {scan['total_problems']}个")
        print(f"总机会: {scan['total_opportunities']}个")
        print(f"加权问题: {scan['weighted_problems']}")
        print(f"加权机会: {scan['weighted_opportunities']}")
        print()
        print(f"旋转方向: {scan['rotation']}")
        print(f"行动建议: {scan['action']}")
        
        print()
        print("【四层感知详情】")
        for layer in [1, 2, 3, 4]:
            stats = scan['layer_stats'][layer]
            print(f"\n第{layer}层 {stats['name']}:")
            print(f"  问题: {stats['problems']}个 | 机会: {stats['opportunities']}个")
            if stats['threads']:
                for t in stats['threads'][:3]:
                    icon = "⚠️" if t['type'] == "problem" else "✅"
                    print(f"  {icon} 线程{t['thread']:02d} {t['palace']}-{t['state']}: {t['matched']}")
    
    elif cmd == "rotate":
        text = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        print("=== 旋转决策（四层感知）===")
        print()
        
        decision = db.get_rotation_decision(text)
        
        print(f"旋转方向: {decision['rotation']}")
        print(f"行动: {decision['action']}")
        print()
        
        print("【四层加权分析】")
        layer_stats = decision['layer_stats']
        print(f"第1层(阴宫阴爻): 问题{layer_stats[1]['problems']}个 × 4 = {layer_stats[1]['problems']*4}")
        print(f"第2层(阴宫阳爻): 问题{layer_stats[2]['problems']}个 × 2 = {layer_stats[2]['problems']*2}")
        print(f"第3层(阳宫阴爻): 问题{layer_stats[3]['problems']}个 × 2 = {layer_stats[3]['problems']*2}")
        print(f"第4层(阳宫阳爻): 问题{layer_stats[4]['problems']}个 × 1 = {layer_stats[4]['problems']*1}")
        print()
        print(f"加权问题总分: {decision['weighted_problems']}")
        print(f"加权机会总分: {decision['weighted_opportunities']}")
        print()
        
        if decision['is_critical']:
            print("⚠️ 状态: 紧急")
        elif decision['is_healthy']:
            print("✅ 状态: 健康")
        else:
            print("⏸️ 状态: 正常")
        
        print()
        print(f"建议: {decision['recommendation']}")
    
    elif cmd == "palace_scan" and len(sys.argv) > 2:
        palace_id = int(sys.argv[2])
        text = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
        
        print(f"=== {palace_id}宫 6爻状态扫描 ===")
        print()
        
        result = db.scan_palace_yao(palace_id, text)
        print(f"宫位: {result['palace_name']}")
        print(f"问题: {result['problems']}个")
        print(f"机会: {result['opportunities']}个")
        print()
        
        print("【六爻状态】")
        for yao in result['yao_results']:
            status = "⚠️" if yao['matched_bad'] else ("✅" if yao['matched_good'] else "➖")
            print(f"  {status} {yao['yao_level']}爻({yao['yao_type']}) {yao['state']}")
            if yao['matched_bad']:
                print(f"     差关键词: {yao['matched_bad']}")
            if yao['matched_good']:
                print(f"     好关键词: {yao['matched_good']}")
    
    elif cmd == "palace_task" and len(sys.argv) > 2:
        palace_id = int(sys.argv[2])
        text = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
        
        print(f"=== {palace_id}宫 任务生成 ===")
        print()
        
        scan_result = db.scan_palace_yao(palace_id, text)
        task = db.generate_palace_task(palace_id, scan_result)
        
        print(f"任务ID: {task['task_id']}")
        print(f"类型: {task['task_type']}")
        print(f"描述: {task['description']}")
        print(f"优先级: {task['priority']}")
        print(f"可用技能: {task['available_skills']}")
        
        # 添加到待办
        db.add_palace_pending_task(palace_id, task)
        print()
        print("✅ 任务已添加到待办列表")
    
    elif cmd == "reports":
        print("=== 宫位汇报记录 ===")
        print()
        
        reports = db.get_palace_reports(limit=20)
        if reports:
            for r in reports:
                print(f"[{r.get('palace_name', 'N/A')}] {r.get('type', 'N/A')}")
                print(f"  时间: {r.get('timestamp', 'N/A')}")
                if r.get('task_id'):
                    print(f"  任务: {r.get('task_id')}")
                if r.get('result'):
                    print(f"  结果: {r.get('result')}")
                print()
        else:
            print("暂无汇报记录")
    
    elif cmd == "assign" and len(sys.argv) > 4:
        palace_id = int(sys.argv[2])
        task_type = sys.argv[3]
        description = " ".join(sys.argv[4:])
        
        result = db.assign_task(palace_id, task_type, description)
        
        print(f"=== 任务分配 ===")
        print(f"目标: {result['palace_name']} ({palace_id}宫)")
        print(f"任务ID: {result['task_id']}")
        print(f"类型: {task_type}")
        print(f"描述: {description}")
        print()
        print(f"✅ {result['message']}")
        print()
        print("已写入该宫位的任务队列（todo）")
    
    elif cmd in ["tasks", "todo"]:
        print("=== 所有待办任务 ===")
        print()
        
        tasks = db.get_all_pending_tasks()
        if tasks:
            for t in tasks:
                status_icon = "🔴" if t.get("status") == "pending" else "🟡" if t.get("status") == "in_progress" else "🟢"
                priority_icon = "⚡" if t.get("priority") == "high" else ""
                print(f"{status_icon} {priority_icon} [{t.get('palace_name')}] {t.get('task_id')}")
                print(f"   类型: {t.get('task_type')} | 优先级: {t.get('priority')}")
                print(f"   描述: {t.get('description')}")
                print()
        else:
            print("暂无待办任务")
            print()
            print("使用 assign <宫位> <类型> <描述> 来分配任务")
    
    else:
        print(f"未知命令: {cmd}")