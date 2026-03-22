"""
六爻探测关键词定义
每爻的探测关键词，用于从文本/信号中自动识别状态
"""

# 每个爻的探测关键词（可扩展）
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
}


def get_detect_keywords(palace_id: int, yao_level: int) -> list:
    """获取指定爻的探测关键词"""
    return YAO_DETECT_KEYWORDS.get(palace_id, {}).get(yao_level, [])


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
    
    palaces_to_check = [palace_id] if palace_id else range(1, 9)
    
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
                    "match_count": len(matched)
                })
    
    # 按匹配数量排序
    all_matches.sort(key=lambda x: x["match_count"], reverse=True)
    
    best_match = all_matches[0] if all_matches else None
    
    return {
        "matched_palace": best_match["palace_id"] if best_match else None,
        "matched_yao": best_match["yao_level"] if best_match else None,
        "matched_keywords": best_match["matched_keywords"] if best_match else [],
        "match_count": best_match["match_count"] if best_match else 0,
        "all_matches": all_matches
    }