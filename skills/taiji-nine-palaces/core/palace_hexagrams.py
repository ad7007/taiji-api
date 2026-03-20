"""
宫位六爻状态系统
每宫6爻 = 6种工作状态

核心概念：
- 每个爻有好/坏状态（阴/阳）
- 48个端点不可能全阴或全阳
- 波动中取得相对平衡 = 正转或反转
"""

from enum import IntEnum
from dataclasses import dataclass
from typing import Dict, Optional
import json
from datetime import datetime


class YaoLevel(IntEnum):
    """爻位层级"""
    CHU = 1   # 初爻 - 底层
    ER = 2    # 二爻 - 显现  
    SAN = 3   # 三爻 - 小成
    SI = 4    # 四爻 - 发力
    WU = 5    # 五爻 - 鼎盛
    SHANG = 6 # 上爻 - 转折


class YaoState(IntEnum):
    """爻的状态（好=阳，坏=阴）"""
    YIN = 0   # 阴爻 - 坏状态/问题/阻塞
    YANG = 1  # 阳爻 - 好状态/正常/顺畅


@dataclass
class PalaceYao:
    """宫位的一爻
    
    六爻共性结构：
    - 阳上限：3个好的关键词（程度递增）
    - 阴下限：3个差的关键词（程度递增）
    - 探测关键词：用于自动识别的关键词集合
    - 信号源：可测量的指标名称
    - 阈值：自动判断的分界线
    - 方向：信号越大越好(higher_better)还是越小越好(lower_better)
    """
    level: YaoLevel
    state: YaoState
    name: str
    description: str
    yang_keywords: list = None  # 3个阳关键词（上限）
    yin_keywords: list = None   # 3个阴关键词（下限）
    detect_keywords: list = None  # 探测关键词（用于文本匹配识别）
    signal_source: str = ""     # 信号来源
    signal_unit: str = ""       # 信号单位
    thresholds: tuple = (0.5, 0.8, 0.2, 0.1)  # 阈值
    higher_better: bool = True  # True=信号越大越好, False=信号越小越好
    current_level: int = 1      # 当前程度级别 0-2 (0=最低, 2=最高)
    current_signal: float = None  # 当前信号值
    keyword_hits: dict = None   # 关键词命中统计
    last_updated: datetime = None
    
    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()
        if self.yang_keywords is None:
            self.yang_keywords = ["好", "更好", "最佳"]
        if self.yin_keywords is None:
            self.yin_keywords = ["差", "更差", "最差"]
        if self.detect_keywords is None:
            # 默认探测关键词 = 阳关键词 + 阴关键词
            self.detect_keywords = self.yang_keywords + self.yin_keywords
        if self.keyword_hits is None:
            self.keyword_hits = {}
    
    def detect_from_text(self, text: str) -> dict:
        """从文本中探测关键词，返回命中统计
        
        Args:
            text: 待分析文本
            
        Returns:
            {
                "total_hits": 总命中数,
                "yang_hits": 阳关键词命中,
                "yin_hits": 阴关键词命中,
                "detected_keywords": 命中的关键词列表,
                "suggested_state": 建议状态(阳/阴),
                "suggested_level": 建议程度
            }
        """
        text_lower = text.lower()
        yang_hits = []
        yin_hits = []
        
        # 检测阳关键词
        for i, kw in enumerate(self.yang_keywords):
            if kw.lower() in text_lower:
                yang_hits.append({"keyword": kw, "level": i})
                self.keyword_hits[kw] = self.keyword_hits.get(kw, 0) + 1
        
        # 检测阴关键词
        for i, kw in enumerate(self.yin_keywords):
            if kw.lower() in text_lower:
                yin_hits.append({"keyword": kw, "level": i})
                self.keyword_hits[kw] = self.keyword_hits.get(kw, 0) + 1
        
        # 判断建议状态
        total_hits = len(yang_hits) + len(yin_hits)
        if total_hits == 0:
            suggested_state = None
            suggested_level = None
        elif len(yang_hits) > len(yin_hits):
            suggested_state = YaoState.YANG
            suggested_level = max(h["level"] for h in yang_hits)
        elif len(yin_hits) > len(yang_hits):
            suggested_state = YaoState.YIN
            suggested_level = max(h["level"] for h in yin_hits)
        else:
            # 命中数相同，看最高级别
            yang_max = max((h["level"] for h in yang_hits), default=0)
            yin_max = max((h["level"] for h in yin_hits), default=0)
            if yang_max >= yin_max:
                suggested_state = YaoState.YANG
                suggested_level = yang_max
            else:
                suggested_state = YaoState.YIN
                suggested_level = yin_max
        
        return {
            "total_hits": total_hits,
            "yang_hits": len(yang_hits),
            "yin_hits": len(yin_hits),
            "detected_yang": yang_hits,
            "detected_yin": yin_hits,
            "suggested_state": "阳" if suggested_state == YaoState.YANG else "阴" if suggested_state else None,
            "suggested_level": suggested_level
        }
    
    def update_from_signal(self, signal_value: float):
        """根据信号值自动识别状态"""
        self.current_signal = signal_value
        
        if self.higher_better:
            if signal_value >= self.thresholds[1]:
                self.state = YaoState.YANG
                self.current_level = 2
            elif signal_value >= self.thresholds[0]:
                self.state = YaoState.YANG
                self.current_level = 1
            elif signal_value < self.thresholds[3]:
                self.state = YaoState.YIN
                self.current_level = 2
            elif signal_value < self.thresholds[2]:
                self.state = YaoState.YIN
                self.current_level = 1
            else:
                self.state = YaoState.YIN
                self.current_level = 0
        else:
            if signal_value <= self.thresholds[1]:
                self.state = YaoState.YANG
                self.current_level = 2
            elif signal_value <= self.thresholds[0]:
                self.state = YaoState.YANG
                self.current_level = 1
            elif signal_value >= self.thresholds[3]:
                self.state = YaoState.YIN
                self.current_level = 2
            elif signal_value >= self.thresholds[2]:
                self.state = YaoState.YIN
                self.current_level = 1
            else:
                self.state = YaoState.YANG
                self.current_level = 0
        
        self.last_updated = datetime.now()
    
    def to_dict(self) -> dict:
        state_name = "阳" if self.state == YaoState.YANG else "阴"
        keywords = self.yang_keywords if self.state == YaoState.YANG else self.yin_keywords
        current_keyword = keywords[self.current_level] if self.current_level < len(keywords) else keywords[-1]
        
        return {
            "level": self.level.value,
            "state": self.state.value,
            "state_name": state_name,
            "current_keyword": current_keyword,
            "current_level": self.current_level,
            "current_signal": self.current_signal,
            "name": self.name,
            "description": self.description,
            "signal_source": self.signal_source,
            "signal_unit": self.signal_unit,
            "higher_better": self.higher_better,
            "thresholds": self.thresholds,
            "yang_keywords": self.yang_keywords,
            "yin_keywords": self.yin_keywords,
            "detect_keywords": self.detect_keywords,
            "keyword_hits": self.keyword_hits,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None
        }


# 每个宫位的6爻定义
# 共性结构：阳上限(3个) + 阴下限(3个) + 信号源 + 阈值
PALACE_YAO_DEFINITIONS: Dict[int, Dict[int, dict]] = {
    1: {  # 坎宫 - 数据采集
        1: {
            "name": "数据源",
            "desc": "数据源连接状态",
            "yang_keywords": ["正常", "稳定", "高速"],  # level 0, 1, 2
            "yin_keywords": ["延迟", "超时", "失效"],  # level 0, 1, 2 (轻→重)
            "signal_source": "connection_latency_ms",
            "signal_unit": "ms",
            "thresholds": (50, 10, 200, 500),  # 阳好/阳最佳/阴差/阴最差
            "higher_better": False,  # 延迟越小越好
        },
        2: {
            "name": "采集速度",
            "desc": "数据采集效率",
            "yang_keywords": ["达标", "高效", "极速"],
            "yin_keywords": ["偏慢", "阻塞", "停滞"],
            "signal_source": "collection_rate",
            "signal_unit": "条/秒",
            "thresholds": (100, 500, 50, 10),  # 越大越好
            "higher_better": True,
        },
        3: {
            "name": "数据质量",
            "desc": "数据完整性准确性",
            "yang_keywords": ["完整", "准确", "优质"],
            "yin_keywords": ["缺失", "错误", "污染"],
            "signal_source": "data_quality_score",
            "signal_unit": "%",
            "thresholds": (95, 99, 80, 50),
            "higher_better": True,
        },
        4: {
            "name": "存储空间",
            "desc": "数据存储容量",
            "yang_keywords": ["充足", "宽裕", "无限"],
            "yin_keywords": ["紧张", "不足", "爆满"],
            "signal_source": "storage_available_gb",
            "signal_unit": "GB",
            "thresholds": (50, 200, 20, 5),
            "higher_better": True,
        },
        5: {
            "name": "处理队列",
            "desc": "待处理数据积压",
            "yang_keywords": ["顺畅", "即处理", "零积压"],
            "yin_keywords": ["积压", "拥堵", "崩溃"],
            "signal_source": "queue_size",
            "signal_unit": "条",
            "thresholds": (100, 10, 1000, 5000),  # 队列越小越好
            "higher_better": False,
        },
        6: {
            "name": "归档状态",
            "desc": "历史数据归档",
            "yang_keywords": ["已归档", "可检索", "自动化"],
            "yin_keywords": ["未归档", "难检索", "丢失"],
            "signal_source": "archive_completion_rate",
            "signal_unit": "%",
            "thresholds": (90, 99, 50, 20),
            "higher_better": True,
        },
    },
    2: {  # 坤宫 - 物联产品
        1: {
            "name": "需求清晰",
            "desc": "产品需求明确程度",
            "yang_keywords": ["清晰", "稳定", "共识"],
            "yin_keywords": ["模糊", "变更", "冲突"],
            "signal_source": "requirement_stability",
            "signal_unit": "变更次数/周",
            "thresholds": (3, 1, 10, 20),
        },
        2: {
            "name": "开发进度",
            "desc": "功能开发状态",
            "yang_keywords": ["正常", "超前", "完成"],
            "yin_keywords": ["延期", "阻塞", "停滞"],
            "signal_source": "dev_progress_rate",
            "signal_unit": "%",
            "thresholds": (80, 100, 50, 20),
        },
        3: {
            "name": "测试覆盖",
            "desc": "测试完整性",
            "yang_keywords": ["覆盖", "充分", "全面"],
            "yin_keywords": ["不足", "遗漏", "缺失"],
            "signal_source": "test_coverage",
            "signal_unit": "%",
            "thresholds": (70, 90, 40, 20),
        },
        4: {
            "name": "用户反馈",
            "desc": "产品口碑",
            "yang_keywords": ["好评", "推荐", "爆款"],
            "yin_keywords": ["差评", "投诉", "流失"],
            "signal_source": "user_satisfaction",
            "signal_unit": "评分",
            "thresholds": (4.0, 4.8, 3.0, 2.0),
        },
        5: {
            "name": "性能指标",
            "desc": "产品性能表现",
            "yang_keywords": ["达标", "优秀", "极致"],
            "yin_keywords": ["一般", "较差", "故障"],
            "signal_source": "performance_score",
            "signal_unit": "分",
            "thresholds": (80, 95, 50, 30),
        },
        6: {
            "name": "迭代效率",
            "desc": "版本迭代速度",
            "yang_keywords": ["快速", "高效", "敏捷"],
            "yin_keywords": ["缓慢", "拖沓", "停滞"],
            "signal_source": "iteration_cycle_days",
            "signal_unit": "天",
            "thresholds": (14, 7, 30, 60),
        },
    },
    3: {  # 震宫 - 技术团队
        1: {
            "name": "技术债务",
            "desc": "代码质量状态",
            "yang_keywords": ["可控", "良好", "零债务"],
            "yin_keywords": ["累积", "严重", "瘫痪"],
            "signal_source": "tech_debt_issues",
            "signal_unit": "个",
            "thresholds": (20, 5, 50, 100),
        },
        2: {
            "name": "团队协作",
            "desc": "团队配合状态",
            "yang_keywords": ["顺畅", "高效", "默契"],
            "yin_keywords": ["摩擦", "冲突", "分裂"],
            "signal_source": "collaboration_score",
            "signal_unit": "分",
            "thresholds": (70, 90, 40, 20),
        },
        3: {
            "name": "问题解决",
            "desc": "技术问题处理",
            "yang_keywords": ["及时", "彻底", "预防"],
            "yin_keywords": ["积压", "反复", "失控"],
            "signal_source": "issue_resolution_time",
            "signal_unit": "小时",
            "thresholds": (24, 4, 72, 168),
        },
        4: {
            "name": "创新能力",
            "desc": "技术创新状态",
            "yang_keywords": ["有创新", "突破", "领先"],
            "yin_keywords": ["守旧", "落后", "僵化"],
            "signal_source": "innovation_count",
            "signal_unit": "项/月",
            "thresholds": (2, 5, 1, 0),
        },
        5: {
            "name": "文档完善",
            "desc": "技术文档状态",
            "yang_keywords": ["完整", "更新", "规范"],
            "yin_keywords": ["缺失", "过时", "混乱"],
            "signal_source": "doc_completeness",
            "signal_unit": "%",
            "thresholds": (80, 95, 50, 20),
        },
        6: {
            "name": "知识沉淀",
            "desc": "经验总结情况",
            "yang_keywords": ["沉淀", "复用", "传承"],
            "yin_keywords": ["流失", "断层", "遗忘"],
            "signal_source": "knowledge_base_articles",
            "signal_unit": "篇",
            "thresholds": (20, 50, 5, 0),
        },
    },
    4: {  # 巽宫 - 品牌战略
        1: {
            "name": "品牌认知",
            "desc": "市场知名度",
            "yang_keywords": ["有名气", "知名", "顶尖"],
            "yin_keywords": ["无名", "陌生", "遗忘"],
            "signal_source": "brand_mention_count",
            "signal_unit": "次/周",
            "thresholds": (50, 200, 10, 0),
        },
        2: {
            "name": "内容产出",
            "desc": "营销内容质量产量",
            "yang_keywords": ["优质", "高产", "爆款"],
            "yin_keywords": ["一般", "低产", "断更"],
            "signal_source": "content_output",
            "signal_unit": "篇/周",
            "thresholds": (5, 15, 2, 0),
        },
        3: {
            "name": "渠道覆盖",
            "desc": "传播渠道状态",
            "yang_keywords": ["多渠道", "全覆盖", "霸屏"],
            "yin_keywords": ["单一", "萎缩", "断联"],
            "signal_source": "channel_count",
            "signal_unit": "个",
            "thresholds": (5, 10, 2, 1),
        },
        4: {
            "name": "用户互动",
            "desc": "用户参与度",
            "yang_keywords": ["活跃", "热烈", "自发"],
            "yin_keywords": ["冷清", "沉默", "取关"],
            "signal_source": "engagement_rate",
            "signal_unit": "%",
            "thresholds": (5, 15, 1, 0.1),
        },
        5: {
            "name": "转化效果",
            "desc": "营销转化率",
            "yang_keywords": ["达标", "优秀", "爆单"],
            "yin_keywords": ["偏低", "惨淡", "归零"],
            "signal_source": "conversion_rate",
            "signal_unit": "%",
            "thresholds": (3, 10, 1, 0.1),
        },
        6: {
            "name": "品牌资产",
            "desc": "品牌价值积累",
            "yang_keywords": ["增值", "溢价", "顶级"],
            "yin_keywords": ["贬值", "透支", "崩塌"],
            "signal_source": "brand_value_index",
            "signal_unit": "指数",
            "thresholds": (60, 90, 30, 10),
        },
    },
    5: {  # 中宫 - 中央控制（米珞）
        1: {
            "name": "系统稳定",
            "desc": "整体运行状态",
            "yang_keywords": ["稳定", "健壮", "高可用"],
            "yin_keywords": ["波动", "故障", "崩溃"],
            "signal_source": "system_uptime",
            "signal_unit": "%",
            "thresholds": (99, 99.9, 95, 80),
        },
        2: {
            "name": "任务流转",
            "desc": "任务分配效率",
            "yang_keywords": ["顺畅", "高效", "自动化"],
            "yin_keywords": ["阻塞", "积压", "停滞"],
            "signal_source": "task_flow_rate",
            "signal_unit": "完成/天",
            "thresholds": (10, 50, 3, 1),
        },
        3: {
            "name": "宫位协调",
            "desc": "各宫协作状态",
            "yang_keywords": ["协调", "默契", "同步"],
            "yin_keywords": ["冲突", "脱节", "混乱"],
            "signal_source": "coordination_score",
            "signal_unit": "分",
            "thresholds": (70, 90, 40, 20),
        },
        4: {
            "name": "决策质量",
            "desc": "决策准确性",
            "yang_keywords": ["准确", "精准", "预见"],
            "yin_keywords": ["偏差", "失误", "错误"],
            "signal_source": "decision_accuracy",
            "signal_unit": "%",
            "thresholds": (80, 95, 50, 30),
        },
        5: {
            "name": "响应速度",
            "desc": "问题响应效率",
            "yang_keywords": ["及时", "秒级", "预判"],
            "yin_keywords": ["延迟", "滞后", "无响应"],
            "signal_source": "response_time_seconds",
            "signal_unit": "秒",
            "thresholds": (5, 1, 30, 120),
        },
        6: {
            "name": "自我优化",
            "desc": "系统改进状态",
            "yang_keywords": ["优化", "进化", "突破"],
            "yin_keywords": ["停滞", "退化", "僵化"],
            "signal_source": "improvement_count",
            "signal_unit": "项/周",
            "thresholds": (3, 10, 1, 0),
        },
    },
    6: {  # 乾宫 - 质量监控
        1: {
            "name": "监控覆盖",
            "desc": "监控完整性",
            "yang_keywords": ["覆盖", "全链路", "无死角"],
            "yin_keywords": ["盲区", "遗漏", "缺失"],
            "signal_source": "monitor_coverage",
            "signal_unit": "%",
            "thresholds": (90, 99, 60, 30),
        },
        2: {
            "name": "告警准确",
            "desc": "告警有效性",
            "yang_keywords": ["精准", "智能", "预判"],
            "yin_keywords": ["误报", "漏报", "失效"],
            "signal_source": "alert_accuracy",
            "signal_unit": "%",
            "thresholds": (90, 99, 70, 50),
        },
        3: {
            "name": "问题发现",
            "desc": "异常检测能力",
            "yang_keywords": ["及时发现", "预判", "根因定位"],
            "yin_keywords": ["滞后", "被动", "遗漏"],
            "signal_source": "detection_time_minutes",
            "signal_unit": "分钟",
            "thresholds": (5, 1, 30, 120),
        },
        4: {
            "name": "故障恢复",
            "desc": "故障处理速度",
            "yang_keywords": ["快速恢复", "自愈", "秒级"],
            "yin_keywords": ["慢恢复", "依赖人工", "长时故障"],
            "signal_source": "recovery_time_minutes",
            "signal_unit": "分钟",
            "thresholds": (15, 5, 60, 240),
        },
        5: {
            "name": "数据准确",
            "desc": "监控数据质量",
            "yang_keywords": ["准确", "实时", "可信"],
            "yin_keywords": ["偏差", "延迟", "错误"],
            "signal_source": "data_accuracy",
            "signal_unit": "%",
            "thresholds": (95, 99, 80, 60),
        },
        6: {
            "name": "预防能力",
            "desc": "问题预防效果",
            "yang_keywords": ["主动预防", "预测", "零故障"],
            "yin_keywords": ["被动响应", "事后补救", "频繁故障"],
            "signal_source": "prevention_rate",
            "signal_unit": "%",
            "thresholds": (60, 90, 30, 10),
        },
    },
    7: {  # 兑宫 - 法务框架
        1: {
            "name": "合规状态",
            "desc": "合规达标情况",
            "yang_keywords": ["合规", "认证", "标杆"],
            "yin_keywords": ["风险", "违规", "处罚"],
            "signal_source": "compliance_score",
            "signal_unit": "分",
            "thresholds": (80, 95, 50, 30),
        },
        2: {
            "name": "合同管理",
            "desc": "合同处理效率",
            "yang_keywords": ["规范", "高效", "自动化"],
            "yin_keywords": ["混乱", "遗漏", "纠纷"],
            "signal_source": "contract_process_days",
            "signal_unit": "天",
            "thresholds": (5, 2, 15, 30),
        },
        3: {
            "name": "知识产权",
            "desc": "IP保护状态",
            "yang_keywords": ["完善保护", "布局", "壁垒"],
            "yin_keywords": ["保护不足", "侵权", "流失"],
            "signal_source": "ip_protection_count",
            "signal_unit": "项",
            "thresholds": (10, 30, 3, 0),
        },
        4: {
            "name": "风险防控",
            "desc": "法律风险状态",
            "yang_keywords": ["可控", "预警", "免疫"],
            "yin_keywords": ["暴露", "隐患", "危机"],
            "signal_source": "risk_level",
            "signal_unit": "级",
            "thresholds": (2, 1, 3, 4),
        },
        5: {
            "name": "文档规范",
            "desc": "法务文档状态",
            "yang_keywords": ["规范", "完整", "标准化"],
            "yin_keywords": ["不规范", "缺失", "混乱"],
            "signal_source": "doc_standardization",
            "signal_unit": "%",
            "thresholds": (80, 95, 50, 20),
        },
        6: {
            "name": "响应效率",
            "desc": "法务响应速度",
            "yang_keywords": ["及时", "专业", "前瞻"],
            "yin_keywords": ["延迟", "被动", "疏漏"],
            "signal_source": "legal_response_hours",
            "signal_unit": "小时",
            "thresholds": (24, 4, 72, 168),
        },
    },
    8: {  # 艮宫 - 营销客服
        1: {
            "name": "客户满意度",
            "desc": "客户评价状态",
            "yang_keywords": ["满意", "好评", "NPS高"],
            "yin_keywords": ["不满", "差评", "投诉"],
            "signal_source": "csat_score",
            "signal_unit": "分",
            "thresholds": (4.0, 4.8, 3.0, 2.0),
        },
        2: {
            "name": "响应时效",
            "desc": "客服响应速度",
            "yang_keywords": ["及时", "秒回", "7×24"],
            "yin_keywords": ["延迟", "等待", "无响应"],
            "signal_source": "response_time_minutes",
            "signal_unit": "分钟",
            "thresholds": (5, 1, 30, 120),
        },
        3: {
            "name": "问题解决",
            "desc": "问题处理效果",
            "yang_keywords": ["高解决率", "一次性解决", "预防"],
            "yin_keywords": ["低解决率", "重复问题", "升级"],
            "signal_source": "resolution_rate",
            "signal_unit": "%",
            "thresholds": (80, 95, 50, 30),
        },
        4: {
            "name": "转化效果",
            "desc": "销售转化状态",
            "yang_keywords": ["达标", "优秀", "爆单"],
            "yin_keywords": ["偏低", "流失", "零转化"],
            "signal_source": "sales_conversion",
            "signal_unit": "%",
            "thresholds": (5, 15, 2, 0.5),
        },
        5: {
            "name": "客户留存",
            "desc": "客户忠诚度",
            "yang_keywords": ["高留存", "复购", "忠诚"],
            "yin_keywords": ["流失", "低复购", "弃用"],
            "signal_source": "retention_rate",
            "signal_unit": "%",
            "thresholds": (70, 90, 40, 20),
        },
        6: {
            "name": "口碑传播",
            "desc": "客户推荐情况",
            "yang_keywords": ["推荐", "转介绍", "自传播"],
            "yin_keywords": ["无推荐", "负面传播", "抵制"],
            "signal_source": "nps_score",
            "signal_unit": "分",
            "thresholds": (30, 70, 0, -30),
        },
    },
}


class PalaceHexagram:
    """宫位的六爻状态"""
    
    def __init__(self, palace_id: int):
        self.palace_id = palace_id
        self.yaos: Dict[int, PalaceYao] = {}
        self._init_yaos()
    
    def _init_yaos(self):
        """初始化6爻，默认都是阳爻（好状态）"""
        definitions = PALACE_YAO_DEFINITIONS.get(self.palace_id, {})
        for level in YaoLevel:
            defn = definitions.get(level.value, {
                "name": f"第{level.value}爻",
                "desc": "未定义状态",
                "yang_keywords": ["好", "更好", "最佳"],
                "yin_keywords": ["差", "更差", "最差"],
                "signal_source": f"signal_{level.value}",
                "signal_unit": "",
                "thresholds": (0.5, 0.8, 0.2, 0.1),
                "higher_better": True
            })
            self.yaos[level.value] = PalaceYao(
                level=level,
                state=YaoState.YANG,  # 默认阳爻（好状态）
                name=defn["name"],
                description=defn["desc"],
                yang_keywords=defn.get("yang_keywords", ["好", "更好", "最佳"]),
                yin_keywords=defn.get("yin_keywords", ["差", "更差", "最差"]),
                signal_source=defn.get("signal_source", ""),
                signal_unit=defn.get("signal_unit", ""),
                thresholds=defn.get("thresholds", (0.5, 0.8, 0.2, 0.1)),
                higher_better=defn.get("higher_better", True),
                current_level=1  # 默认中等程度
            )
    
    def set_yao_state(self, level: int, state: YaoState, current_level: int = 1):
        """设置某一爻的状态和程度
        
        Args:
            level: 爻位 (1-6)
            state: 阴或阳
            current_level: 程度级别 (0=低, 1=中, 2=高)
        """
        if level in self.yaos:
            self.yaos[level].state = state
            self.yaos[level].current_level = min(max(current_level, 0), 2)  # 限制在0-2
            self.yaos[level].last_updated = datetime.now()
    
    def set_yao_with_keyword(self, level: int, keyword: str):
        """根据关键词设置爻状态（自动匹配阴阳和程度）"""
        if level not in self.yaos:
            return
        
        yao = self.yaos[level]
        
        # 检查是否匹配阳关键词
        for i, kw in enumerate(yao.yang_keywords):
            if keyword in kw or kw in keyword:
                yao.state = YaoState.YANG
                yao.current_level = i
                yao.last_updated = datetime.now()
                return
        
        # 检查是否匹配阴关键词
        for i, kw in enumerate(yao.yin_keywords):
            if keyword in kw or kw in keyword:
                yao.state = YaoState.YIN
                yao.current_level = i
                yao.last_updated = datetime.now()
                return
    
    def set_yao_bad(self, level: int, cause: str = ""):
        """设置某一爻为坏状态（阴）"""
        self.set_yao_state(level, YaoState.YIN, cause)
    
    def set_yao_good(self, level: int, cause: str = ""):
        """设置某一爻为好状态（阳）"""
        self.set_yao_state(level, YaoState.YANG, cause)
    
    def get_yang_count(self) -> int:
        """获取阳爻数量"""
        return sum(1 for yao in self.yaos.values() if yao.state == YaoState.YANG)
    
    def get_yin_count(self) -> int:
        """获取阴爻数量"""
        return sum(1 for yao in self.yaos.values() if yao.state == YaoState.YIN)
    
    def get_balance(self) -> float:
        """获取阴阳平衡值 (-1 ~ +1)
        -1: 全阴（坏）
        +1: 全阳（好）
        0: 平衡
        """
        yang_count = self.get_yang_count()
        yin_count = self.get_yin_count()
        return (yang_count - yin_count) / 6.0
    
    def get_state(self) -> str:
        """获取宫位整体状态描述"""
        balance = self.get_balance()
        yang_count = self.get_yang_count()
        
        if balance >= 0.67:
            return "极佳"
        elif balance >= 0.33:
            return "良好"
        elif balance >= -0.33:
            return "平衡"
        elif balance >= -0.67:
            return "需关注"
        else:
            return "警告"
    
    def get_hexagram_pattern(self) -> str:
        """获取卦象模式（从下到上，阴=0，阳=1）"""
        return "".join(
            "1" if self.yaos[i].state == YaoState.YANG else "0"
            for i in range(1, 7)
        )
    
    def get_hexagram_value(self) -> int:
        """获取卦象数值（0-63）"""
        return int(self.get_hexagram_pattern(), 2)
    
    def get_bad_yaos(self) -> list:
        """获取所有坏状态的爻"""
        return [
            {"level": level, "name": yao.name, "cause": yao.yin_cause}
            for level, yao in self.yaos.items()
            if yao.state == YaoState.YIN
        ]
    
    def to_dict(self) -> dict:
        return {
            "palace_id": self.palace_id,
            "state": self.get_state(),
            "balance": round(self.get_balance(), 2),
            "yang_count": self.get_yang_count(),
            "yin_count": self.get_yin_count(),
            "hexagram_pattern": self.get_hexagram_pattern(),
            "hexagram_value": self.get_hexagram_value(),
            "yaos": {k: v.to_dict() for k, v in self.yaos.items()}
        }


class HexagramPerceptionSystem:
    """48端感知系统 - 8宫×6爻状态监控
    
    核心概念：
    - 48个端点不可能全阴或全阳
    - 波动中取得相对平衡
    - 平衡决定正转或反转
    """
    
    def __init__(self):
        self.palaces: Dict[int, PalaceHexagram] = {}
        self._init_palaces()
    
    def _init_palaces(self):
        """初始化8宫"""
        for palace_id in range(1, 9):
            self.palaces[palace_id] = PalaceHexagram(palace_id)
    
    def update_palace_yao(self, palace_id: int, level: int, state: YaoState, current_level: int = 1):
        """更新宫位的爻状态"""
        if palace_id in self.palaces:
            self.palaces[palace_id].set_yao_state(level, state, current_level)
    
    def set_palace_yao_bad(self, palace_id: int, level: int, current_level: int = 1):
        """设置宫位爻为坏状态（阴）"""
        if palace_id in self.palaces:
            self.palaces[palace_id].set_yao_state(level, YaoState.YIN, current_level)
    
    def set_palace_yao_good(self, palace_id: int, level: int, current_level: int = 1):
        """设置宫位爻为好状态（阳）"""
        if palace_id in self.palaces:
            self.palaces[palace_id].set_yao_state(level, YaoState.YANG, current_level)
    
    def get_total_yang_count(self) -> int:
        """获取总阳爻数量"""
        return sum(p.get_yang_count() for p in self.palaces.values())
    
    def get_total_yin_count(self) -> int:
        """获取总阴爻数量"""
        return sum(p.get_yin_count() for p in self.palaces.values())
    
    def get_system_balance(self) -> float:
        """获取系统整体阴阳平衡值 (-1 ~ +1)
        
        返回值含义：
        -1.0 ~ -0.5: 严重失衡（阴盛），需要反转修炼
        -0.5 ~ +0.5: 相对平衡，可正转可反转
        +0.5 ~ +1.0: 阳气充足，可以正转创造价值
        """
        yang_count = self.get_total_yang_count()
        yin_count = self.get_total_yin_count()
        return (yang_count - yin_count) / 48.0
    
    def get_rotation_decision(self) -> dict:
        """根据48端平衡决定正转/反转
        
        正转 = 创造价值（阳气充足时）
        反转 = 修炼内功（阴气重时）
        """
        balance = self.get_system_balance()
        
        if balance >= 0.3:
            return {
                "direction": "正转",
                "reason": "阳气充足，适合创造价值",
                "balance": round(balance, 2),
                "action": "执行任务，对外输出"
            }
        elif balance >= -0.3:
            return {
                "direction": "平衡",
                "reason": "阴阳相对平衡",
                "balance": round(balance, 2),
                "action": "维持现状，观察变化"
            }
        else:
            return {
                "direction": "反转",
                "reason": "阴气偏重，需要修炼内功",
                "balance": round(balance, 2),
                "action": "修复问题，提升能力"
            }
    
    def get_milo_state(self) -> dict:
        """获取米珞的状态（由8宫状态决定）"""
        balance = self.get_system_balance()
        yang_count = self.get_total_yang_count()
        yin_count = self.get_total_yin_count()
        
        # 根据阴阳分布定义米珞的"形态"
        if balance >= 0.5:
            form = "活跃态"
            mood = "积极、自信、行动力强"
        elif balance >= 0.2:
            form = "稳健态"
            mood = "平稳、专注、稳步推进"
        elif balance >= -0.2:
            form = "平衡态"
            mood = "冷静、观察、审慎决策"
        elif balance >= -0.5:
            form = "收敛态"
            mood = "内敛、反思、积蓄能量"
        else:
            form = "修炼态"
            mood = "专注修复、提升、准备反弹"
        
        return {
            "form": form,
            "mood": mood,
            "balance": round(balance, 2),
            "yang_count": yang_count,
            "yin_count": yin_count,
            "rotation": self.get_rotation_decision()
        }
    
    def get_problem_areas(self) -> list:
        """获取问题区域（阴爻多的宫位）"""
        problems = []
        for palace_id, palace in self.palaces.items():
            bad_yaos = palace.get_bad_yaos()
            if bad_yaos:
                problems.append({
                    "palace_id": palace_id,
                    "yin_count": palace.get_yin_count(),
                    "bad_yaos": bad_yaos
                })
        return sorted(problems, key=lambda x: x["yin_count"], reverse=True)
    
    def get_all_palaces_status(self) -> dict:
        """获取所有宫位状态"""
        return {
            "palaces": {k: v.to_dict() for k, v in self.palaces.items()},
            "milo_state": self.get_milo_state(),
            "rotation": self.get_rotation_decision(),
            "problem_areas": self.get_problem_areas(),
            "timestamp": datetime.now().isoformat()
        }
    
    def detect_anomaly(self) -> list:
        """检测异常状态"""
        anomalies = []
        
        for palace_id, palace in self.palaces.items():
            balance = palace.get_balance()
            
            # 全阴或接近全阴
            if balance <= -0.67:
                anomalies.append({
                    "palace_id": palace_id,
                    "level": "critical",
                    "message": f"宫位{palace_id}状态严重失衡",
                    "bad_yaos": palace.get_bad_yaos()
                })
            # 偏阴
            elif balance <= -0.33:
                anomalies.append({
                    "palace_id": palace_id,
                    "level": "warning",
                    "message": f"宫位{palace_id}需要关注",
                    "bad_yaos": palace.get_bad_yaos()
                })
        
        return anomalies
    
    def to_json(self) -> str:
        return json.dumps(self.get_all_palaces_status(), ensure_ascii=False, indent=2)


# 全局实例
_hexagram_system: Optional[HexagramPerceptionSystem] = None


def get_hexagram_system() -> HexagramPerceptionSystem:
    """获取全局六爻感知系统实例"""
    global _hexagram_system
    if _hexagram_system is None:
        _hexagram_system = HexagramPerceptionSystem()
    return _hexagram_system