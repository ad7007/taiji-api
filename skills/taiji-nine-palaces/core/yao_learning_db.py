"""
六爻学习数据库
记录任务执行和关键词分析，每3次任务总结一次
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import threading

# 数据库文件路径
DB_DIR = "/root/taiji-api-v2/data"
DB_FILE = os.path.join(DB_DIR, "yao_learning.json")


@dataclass
class TaskRecord:
    """任务执行记录"""
    task_id: str
    palace_id: int
    yao_level: int
    input_text: str
    detected_keywords: List[str]
    manual_state: Optional[str] = None  # 人工标注：阳/阴
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


@dataclass
class KeywordStats:
    """关键词统计"""
    keyword: str
    palace_id: int
    yao_level: int
    yang_count: int = 0  # 被标注为阳的次数
    yin_count: int = 0   # 被标注为阴的次数
    total_count: int = 0
    last_seen: str = None


class YaoLearningDB:
    """六爻学习数据库"""
    
    def __init__(self):
        self.tasks: List[TaskRecord] = []
        self.keyword_stats: Dict[str, KeywordStats] = {}
        self.task_counter = 0
        self.summary_frequency = 3  # 每3次任务总结一次
        self._lock = threading.Lock()
        self._load()
    
    def _load(self):
        """从文件加载数据"""
        os.makedirs(DB_DIR, exist_ok=True)
        if os.path.exists(DB_FILE):
            try:
                with open(DB_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [TaskRecord(**t) for t in data.get('tasks', [])]
                    self.keyword_stats = {
                        k: KeywordStats(**v) 
                        for k, v in data.get('keyword_stats', {}).items()
                    }
                    self.task_counter = data.get('task_counter', 0)
            except Exception as e:
                print(f"加载六爻学习数据库失败: {e}")
    
    def _save(self):
        """保存数据到文件"""
        os.makedirs(DB_DIR, exist_ok=True)
        with self._lock:
            data = {
                'tasks': [asdict(t) for t in self.tasks],
                'keyword_stats': {k: asdict(v) for k, v in self.keyword_stats.items()},
                'task_counter': self.task_counter,
                'last_updated': datetime.now().isoformat()
            }
            with open(DB_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
    
    def record_task(self, palace_id: int, yao_level: int, input_text: str, 
                    detected_keywords: List[str], manual_state: str = None) -> dict:
        """记录一次任务
        
        Args:
            palace_id: 宫位
            yao_level: 爻位
            input_text: 输入文本
            detected_keywords: 检测到的关键词
            manual_state: 人工标注状态（可选）
            
        Returns:
            {
                "task_id": 任务ID,
                "should_summarize": 是否需要总结,
                "summary": 总结内容（如果需要总结）
            }
        """
        with self._lock:
            self.task_counter += 1
            task_id = f"task_{self.task_counter}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            task = TaskRecord(
                task_id=task_id,
                palace_id=palace_id,
                yao_level=yao_level,
                input_text=input_text,
                detected_keywords=detected_keywords,
                manual_state=manual_state
            )
            self.tasks.append(task)
            
            # 更新关键词统计
            for kw in detected_keywords:
                key = f"{palace_id}_{yao_level}_{kw}"
                if key not in self.keyword_stats:
                    self.keyword_stats[key] = KeywordStats(
                        keyword=kw,
                        palace_id=palace_id,
                        yao_level=yao_level
                    )
                stats = self.keyword_stats[key]
                stats.total_count += 1
                stats.last_seen = datetime.now().isoformat()
                if manual_state == "阳":
                    stats.yang_count += 1
                elif manual_state == "阴":
                    stats.yin_count += 1
        
        self._save()
        
        # 检查是否需要总结
        should_summarize = (self.task_counter % self.summary_frequency == 0)
        summary = None
        
        if should_summarize:
            summary = self.summarize()
        
        return {
            "task_id": task_id,
            "task_counter": self.task_counter,
            "should_summarize": should_summarize,
            "summary": summary
        }
    
    def summarize(self) -> dict:
        """总结关键词分析
        
        分析逻辑：
        - 阳关键词：出现次数越多，越倾向于阳
        - 阴关键词：出现次数越多，越倾向于阴
        
        Returns:
            {
                "total_tasks": 总任务数,
                "total_keywords": 总关键词数,
                "top_yang_keywords": 最阳的关键词,
                "top_yin_keywords": 最阴的关键词,
                "keyword_recommendations": 关键词推荐
            }
        """
        # 计算每个关键词的阳/阴倾向分数
        keyword_scores = []
        
        for key, stats in self.keyword_stats.items():
            if stats.total_count == 0:
                continue
            
            # 阳分数 = yang_count / total_count
            # 阴分数 = yin_count / total_count
            yang_score = stats.yang_count / stats.total_count if stats.total_count > 0 else 0
            yin_score = stats.yin_count / stats.total_count if stats.total_count > 0 else 0
            
            # 综合分数：阳为正，阴为负
            net_score = yang_score - yin_score
            
            keyword_scores.append({
                "keyword": stats.keyword,
                "palace_id": stats.palace_id,
                "yao_level": stats.yao_level,
                "total_count": stats.total_count,
                "yang_count": stats.yang_count,
                "yin_count": stats.yin_count,
                "yang_score": round(yang_score, 2),
                "yin_score": round(yin_score, 2),
                "net_score": round(net_score, 2)
            })
        
        # 按分数排序
        keyword_scores.sort(key=lambda x: x["net_score"], reverse=True)
        
        # 最阳的关键词（net_score高）
        top_yang = [k for k in keyword_scores if k["net_score"] > 0][:10]
        
        # 最阴的关键词（net_score低）
        top_yin = [k for k in keyword_scores if k["net_score"] < 0][:10]
        
        # 生成推荐
        recommendations = []
        for kw in keyword_scores[:20]:
            if kw["total_count"] >= 3:  # 至少出现3次才推荐
                if kw["net_score"] >= 0.5:
                    recommendations.append({
                        "type": "建议加入阳关键词",
                        "keyword": kw["keyword"],
                        "palace_id": kw["palace_id"],
                        "yao_level": kw["yao_level"],
                        "confidence": abs(kw["net_score"])
                    })
                elif kw["net_score"] <= -0.5:
                    recommendations.append({
                        "type": "建议加入阴关键词",
                        "keyword": kw["keyword"],
                        "palace_id": kw["palace_id"],
                        "yao_level": kw["yao_level"],
                        "confidence": abs(kw["net_score"])
                    })
        
        return {
            "total_tasks": self.task_counter,
            "total_keywords": len(self.keyword_stats),
            "top_yang_keywords": top_yang,
            "top_yin_keywords": top_yin,
            "recommendations": recommendations,
            "summarized_at": datetime.now().isoformat()
        }
    
    def get_keyword_trend(self, keyword: str, palace_id: int = None) -> dict:
        """获取关键词趋势
        
        Args:
            keyword: 关键词
            palace_id: 可选，筛选宫位
            
        Returns:
            {
                "keyword": 关键词,
                "total_count": 总出现次数,
                "yang_count": 阳次数,
                "yin_count": 阴次数,
                "trend": 趋势（上升/下降/稳定）
            }
        """
        total = 0
        yang_total = 0
        yin_total = 0
        
        for key, stats in self.keyword_stats.items():
            if stats.keyword == keyword:
                if palace_id is None or stats.palace_id == palace_id:
                    total += stats.total_count
                    yang_total += stats.yang_count
                    yin_total += stats.yin_count
        
        # 判断趋势
        if total == 0:
            trend = "无数据"
        elif yang_total > yin_total * 1.5:
            trend = "偏阳"
        elif yin_total > yang_total * 1.5:
            trend = "偏阴"
        else:
            trend = "中性"
        
        return {
            "keyword": keyword,
            "total_count": total,
            "yang_count": yang_total,
            "yin_count": yin_total,
            "yang_ratio": round(yang_total / total, 2) if total > 0 else 0,
            "yin_ratio": round(yin_total / total, 2) if total > 0 else 0,
            "trend": trend
        }
    
    def export_stats(self) -> dict:
        """导出统计数据"""
        return {
            "tasks": [asdict(t) for t in self.tasks],
            "keyword_stats": {k: asdict(v) for k, v in self.keyword_stats.items()},
            "task_counter": self.task_counter,
            "exported_at": datetime.now().isoformat()
        }


# 全局实例
_yao_learning_db: Optional[YaoLearningDB] = None


def get_yao_learning_db() -> YaoLearningDB:
    """获取六爻学习数据库实例"""
    global _yao_learning_db
    if _yao_learning_db is None:
        _yao_learning_db = YaoLearningDB()
    return _yao_learning_db