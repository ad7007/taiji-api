#!/usr/bin/env python3
"""
六爻探测关键词定义
用于从文本/信号中自动识别宫位爻位状态

数据来源：太极API开发版
同步时间：2026-03-20
"""

from typing import Dict, List, Optional
from enum import Enum


# ==================== 爻位阴阳定义 ====================

class YaoType(Enum):
    """爻位阴阳（奇数为阴，偶数为阳）"""
    YIN = "阴"
    YANG = "阳"


def get_yao_type(yao_level: int) -> str:
    """根据爻位获取阴阳类型"""
    return "阴" if yao_level % 2 == 1 else "阳"


# ==================== 基础关键词（数据库版）====================

# 每宫每爻的核心关键词（从数据库同步）
YAO_BASIC_KEYWORDS = {
    1: {  # 1宫 - 数据采集
        1: {"keyword": "采集", "type": "阴", "desc": "数据采集"},
        2: {"keyword": "清洗", "type": "阳", "desc": "数据清洗"},
        3: {"keyword": "存储", "type": "阴", "desc": "数据存储"},
        4: {"keyword": "分析", "type": "阳", "desc": "数据分析"},
        5: {"keyword": "挖掘", "type": "阴", "desc": "数据挖掘"},
        6: {"keyword": "安全", "type": "阳", "desc": "数据安全"},
    },
    2: {  # 2宫 - 产品质量
        1: {"keyword": "承载", "type": "阴", "desc": "产品承载"},
        2: {"keyword": "优化", "type": "阳", "desc": "产品优化"},
        3: {"keyword": "交付", "type": "阴", "desc": "产品交付"},
        4: {"keyword": "迭代", "type": "阳", "desc": "产品迭代"},
        5: {"keyword": "稳定", "type": "阴", "desc": "产品稳定"},
        6: {"keyword": "扩展", "type": "阳", "desc": "产品扩展"},
    },
    3: {  # 3宫 - 技术团队
        1: {"keyword": "开发", "type": "阴", "desc": "技术开发"},
        2: {"keyword": "测试", "type": "阳", "desc": "技术测试"},
        3: {"keyword": "部署", "type": "阴", "desc": "技术部署"},
        4: {"keyword": "优化", "type": "阳", "desc": "技术优化"},
        5: {"keyword": "重构", "type": "阴", "desc": "技术重构"},
        6: {"keyword": "集成", "type": "阳", "desc": "技术集成"},
    },
    4: {  # 4宫 - 品牌战略
        1: {"keyword": "传播", "type": "阴", "desc": "品牌传播"},
        2: {"keyword": "分析", "type": "阳", "desc": "品牌分析"},
        3: {"keyword": "策划", "type": "阴", "desc": "品牌策划"},
        4: {"keyword": "洞察", "type": "阳", "desc": "品牌洞察"},
        5: {"keyword": "定位", "type": "阴", "desc": "品牌定位"},
        6: {"keyword": "创新", "type": "阳", "desc": "品牌创新"},
    },
    5: {  # 5宫 - 中央控制 (OpenClaw本体)
        1: {"keywords": ["会话", "session", "对话", "消息", "message", "连接", "在线"], "type": "阴", "desc": "会话管理"},
        2: {"keywords": ["工具", "tool", "调用", "API", "执行", "exec", "超时", "timeout"], "type": "阳", "desc": "工具调用"},
        3: {"keywords": ["模型", "model", "token", "推理", "LLM", "响应", "延迟"], "type": "阴", "desc": "模型推理"},
        4: {"keywords": ["记忆", "memory", "MEMORY.md", "上下文", "context", "历史"], "type": "阳", "desc": "记忆系统"},
        5: {"keywords": ["技能", "skill", "SKILL.md", "能力", "扩展", "clawhub"], "type": "阴", "desc": "技能系统"},
        6: {"keywords": ["服务", "gateway", "daemon", "进程", "健康", "status", "重启"], "type": "阳", "desc": "服务状态"},
    },
    6: {  # 6宫 - 质量监控
        1: {"keyword": "监控", "type": "阴", "desc": "质量监控"},
        2: {"keyword": "告警", "type": "阳", "desc": "质量告警"},
        3: {"keyword": "备份", "type": "阴", "desc": "质量备份"},
        4: {"keyword": "恢复", "type": "阳", "desc": "质量恢复"},
        5: {"keyword": "优化", "type": "阴", "desc": "质量优化"},
        6: {"keyword": "保障", "type": "阳", "desc": "质量保障"},
    },
    7: {  # 7宫 - 法务框架
        1: {"keyword": "合规", "type": "阴", "desc": "法务合规"},
        2: {"keyword": "风控", "type": "阳", "desc": "法务风控"},
        3: {"keyword": "验收", "type": "阴", "desc": "法务验收"},
        4: {"keyword": "审计", "type": "阳", "desc": "法务审计"},
        5: {"keyword": "标准", "type": "阴", "desc": "法务标准"},
        6: {"keyword": "认证", "type": "阳", "desc": "法务认证"},
    },
    8: {  # 8宫 - 营销客服
        1: {"keyword": "服务", "type": "阴", "desc": "营销服务"},
        2: {"keyword": "营销", "type": "阳", "desc": "营销推广"},
        3: {"keyword": "响应", "type": "阴", "desc": "营销响应"},
        4: {"keyword": "推广", "type": "阳", "desc": "营销推广"},
        5: {"keyword": "维护", "type": "阴", "desc": "营销维护"},
        6: {"keyword": "增长", "type": "阳", "desc": "营销增长"},
    },
    9: {  # 9宫 - 行业生态
        1: {"keyword": "研究", "type": "阴", "desc": "行业研究"},
        2: {"keyword": "合作", "type": "阳", "desc": "行业合作"},
        3: {"keyword": "拓展", "type": "阴", "desc": "行业拓展"},
        4: {"keyword": "洞察", "type": "阳", "desc": "行业洞察"},
        5: {"keyword": "连接", "type": "阴", "desc": "行业连接"},
        6: {"keyword": "繁荣", "type": "阳", "desc": "行业繁荣"},
    },
}


# ==================== 详细关键词（探测版）====================

# 每爻的探测关键词（可扩展）
YAO_DETECT_KEYWORDS = {
    1: {  # 1宫 - 数据采集
        1: ["连接", "数据源", "网络", "API", "接口", "响应", "延迟", "超时", "断开", "重连", "掉线"],
        2: ["采集", "爬取", "抓取", "下载", "速度", "效率", "吞吐", "并发", "阻塞", "卡顿"],
        3: ["质量", "完整", "准确", "缺失", "错误", "脏数据", "异常", "校验", "验证", "清洗"],
        4: ["存储", "磁盘", "空间", "容量", "GB", "TB", "满", "扩容", "清理"],
        5: ["队列", "积压", "待处理", "堆积", "拥堵", "消费", "生产", "Kafka", "MQ"],
        6: ["归档", "备份", "历史", "检索", "查询", "索引", "ES", "数据库"],
    },
    2: {  # 2宫 - 物联产品
        1: ["需求", "PRD", "文档", "清晰", "模糊", "变更", "频繁", "稳定"],
        2: ["进度", "延期", "开发", "功能", "迭代", "版本", "里程碑", "交付"],
        3: ["测试", "覆盖", "用例", "自动化", "遗漏", "Bug", "回归"],
        4: ["反馈", "好评", "差评", "用户", "体验", "满意度", "投诉", "NPS"],
        5: ["性能", "响应", "QPS", "TPS", "延迟", "慢", "快", "优化"],
        6: ["迭代", "发布", "上线", "频率", "周期", "敏捷", "CI/CD"],
    },
    3: {  # 3宫 - 技术团队
        1: ["技术债", "重构", "代码质量", "SonarQube", "耦合", "复杂度"],
        2: ["协作", "沟通", "会议", "Code Review", "配合", "冲突"],
        3: ["问题", "Issue", "解决", "修复", "积压", "工单", "Ticket"],
        4: ["创新", "新技术", "研究", "突破", "专利", "领先"],
        5: ["文档", "Wiki", "Readme", "API文档", "更新", "过时"],
        6: ["知识", "分享", "培训", "沉淀", "经验", "传承", "离职"],
    },
    4: {  # 4宫 - 品牌战略
        1: ["品牌", "知名度", "曝光", "传播", "认知", "口碑"],
        2: ["内容", "文章", "视频", "公众号", "抖音", "小红书", "更新"],
        3: ["渠道", "平台", "分发", "覆盖", "推广", "投放"],
        4: ["互动", "评论", "点赞", "转发", "粉丝", "活跃"],
        5: ["转化", "成交", "线索", "获客", "ROI", "CPA", "注册"],
        6: ["品牌资产", "溢价", "价值", "影响力", "IP"],
    },
    5: {  # 5宫 - 中央控制 (OpenClaw本体)
        1: ["会话", "session", "对话", "消息", "message", "连接", "在线"],
        2: ["工具", "tool", "调用", "API", "执行", "exec", "超时", "timeout"],
        3: ["模型", "model", "token", "推理", "LLM", "响应", "延迟"],
        4: ["记忆", "memory", "MEMORY.md", "上下文", "context", "历史"],
        5: ["技能", "skill", "SKILL.md", "能力", "扩展", "clawhub"],
        6: ["服务", "gateway", "daemon", "进程", "健康", "status", "重启"],
    },
    6: {  # 6宫 - 质量监控
        1: ["监控", "覆盖", "指标", "埋点", "日志", "盲区"],
        2: ["告警", "通知", "误报", "漏报", "精准", "阈值"],
        3: ["发现", "检测", "异常", "预警", "滞后", "及时"],
        4: ["恢复", "自愈", "MTTR", "故障时间", "人工", "自动"],
        5: ["数据", "准确", "实时", "延迟", "可信", "偏差"],
        6: ["预防", "预测", "主动", "被动", "预防性", "事后"],
    },
    7: {  # 7宫 - 法务框架
        1: ["合规", "法规", "认证", "审计", "风险", "违规", "处罚"],
        2: ["合同", "协议", "签署", "归档", "模板", "流程"],
        3: ["IP", "知识产权", "专利", "商标", "版权", "保护", "侵权"],
        4: ["风险", "防控", "预警", "暴露", "隐患", "危机"],
        5: ["文档", "法务", "规范", "标准化", "缺失"],
        6: ["响应", "法务", "及时", "延迟", "专业"],
    },
    8: {  # 8宫 - 营销客服
        1: ["满意度", "好评", "差评", "CSAT", "评分", "投诉"],
        2: ["响应", "客服", "回复", "及时", "等待", "排队"],
        3: ["解决", "处理", "完结", "重复", "升级", "转接"],
        4: ["转化", "销售", "成交", "线索", "跟进", "丢单"],
        5: ["留存", "复购", "续费", "流失", "召回", "活跃"],
        6: ["口碑", "推荐", "NPS", "转介绍", "传播", "负面"],
    },
    9: {  # 9宫 - 行业生态
        1: ["行业", "研究", "分析", "趋势", "报告", "白皮书"],
        2: ["合作", "伙伴", "联盟", "生态", "共赢"],
        3: ["拓展", "渠道", "市场", "区域", "全球化"],
        4: ["洞察", "机会", "威胁", "竞争", "SWOT"],
        5: ["连接", "资源", "人脉", "网络", "社区"],
        6: ["繁荣", "增长", "规模", "影响力", "领导力"],
    },
}


# ==================== 工具函数 ====================

def get_detect_keywords(palace_id: int, yao_level: int) -> list:
    """获取指定爻的探测关键词"""
    return YAO_DETECT_KEYWORDS.get(palace_id, {}).get(yao_level, [])


def get_basic_keyword(palace_id: int, yao_level: int) -> Optional[Dict]:
    """获取指定爻的基础关键词"""
    return YAO_BASIC_KEYWORDS.get(palace_id, {}).get(yao_level)


def detect_yao_from_text(text: str, palace_id: int = None) -> dict:
    """从文本中探测最匹配的爻
    
    Args:
        text: 待分析文本
        palace_id: 可选，指定宫位则只在该宫位内探测
        
    Returns:
        {
            "matched_palace": 最匹配的宫位,
            "matched_yao": 最匹配的爻位,
            "matched_keywords": 匹配的关键词,
            "all_matches": 所有匹配列表
        }
    """
    text_lower = text.lower()
    all_matches = []
    
    palaces_to_check = [palace_id] if palace_id else range(1, 10)
    
    for p_id in palaces_to_check:
        if p_id not in YAO_DETECT_KEYWORDS:
            continue
        for y_level, keywords in YAO_DETECT_KEYWORDS[p_id].items():
            matched = []
            for kw in keywords:
                if kw.lower() in text_lower:
                    matched.append(kw)
            if matched:
                all_matches.append({
                    "palace_id": p_id,
                    "yao_level": y_level,
                    "matched_keywords": matched,
                    "match_count": len(matched),
                    "yao_type": get_yao_type(y_level)
                })
    
    # 按匹配数量排序
    all_matches.sort(key=lambda x: x["match_count"], reverse=True)
    
    best_match = all_matches[0] if all_matches else None
    
    return {
        "matched_palace": best_match["palace_id"] if best_match else None,
        "matched_yao": best_match["yao_level"] if best_match else None,
        "matched_keywords": best_match["matched_keywords"] if best_match else [],
        "match_count": best_match["match_count"] if best_match else 0,
        "yao_type": best_match["yao_type"] if best_match else None,
        "all_matches": all_matches
    }


def get_palace_yao_summary(palace_id: int) -> dict:
    """获取某宫的六爻关键词汇总"""
    if palace_id not in YAO_DETECT_KEYWORDS:
        return {"error": f"Palace {palace_id} not found"}
    
    summary = {
        "palace_id": palace_id,
        "palace_name": {
            1: "数据采集", 2: "产品质量", 3: "技术团队",
            4: "品牌战略", 5: "中央控制", 6: "质量监控",
            7: "法务框架", 8: "营销客服", 9: "行业生态"
        }.get(palace_id, "未知"),
        "yao_keywords": {}
    }
    
    for yao_level in range(1, 7):
        basic = get_basic_keyword(palace_id, yao_level)
        detect = get_detect_keywords(palace_id, yao_level)
        
        summary["yao_keywords"][yao_level] = {
            "type": get_yao_type(yao_level),
            "basic": basic.get("keyword") if basic else None,
            "detect": detect,
            "count": len(detect)
        }
    
    return summary


# ==================== 统计 ====================

def get_keyword_stats() -> dict:
    """获取关键词统计"""
    total = 0
    by_palace = {}
    
    for palace_id in YAO_DETECT_KEYWORDS:
        palace_count = 0
        for yao_level in YAO_DETECT_KEYWORDS[palace_id]:
            count = len(YAO_DETECT_KEYWORDS[palace_id][yao_level])
            palace_count += count
            total += count
        by_palace[palace_id] = palace_count
    
    return {
        "total_keywords": total,
        "palaces": 9,
        "yao_per_palace": 6,
        "by_palace": by_palace
    }


if __name__ == "__main__":
    print("=== 六爻关键词系统 ===\n")
    
    # 统计
    stats = get_keyword_stats()
    print(f"总关键词数: {stats['total_keywords']}")
    print(f"覆盖宫位: {stats['palaces']}宫 × {stats['yao_per_palace']}爻")
    print()
    
    # 5宫详情
    print("=== 5宫 (OpenClaw本体) 六爻关键词 ===")
    summary = get_palace_yao_summary(5)
    for yao, info in summary["yao_keywords"].items():
        print(f"{yao}爻 ({info['type']}): {info['detect']}")
    print()
    
    # 探测测试
    print("=== 文本探测测试 ===")
    test_texts = [
        "API延迟很高，连接超时",
        "帮我写个Python脚本",
        "监控系统显示CPU使用率过高",
    ]
    
    for text in test_texts:
        result = detect_yao_from_text(text)
        print(f"文本: \"{text}\"")
        print(f"  → {result['matched_palace']}宫 {result['matched_yao']}爻 ({result['yao_type']})")
        print(f"  → 匹配关键词: {result['matched_keywords']}")
        print()