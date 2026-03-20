"""
六爻感知系统 API 端点
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from core.palace_hexagrams import (
    get_hexagram_system,
    YaoState,
    YaoLevel
)
from core.yao_detect_keywords import detect_yao_from_text
from core.yao_learning_db import get_yao_learning_db

router = APIRouter(prefix="/api/hexagram", tags=["hexagram"])


class UpdateYaoRequest(BaseModel):
    palace_id: int
    level: int  # 1-6
    state: int  # 0=阴, 1=阳
    current_level: int = 1  # 程度级别 0=低, 1=中, 2=高


class UpdateLoadRequest(BaseModel):
    palace_id: int
    load: float  # 0.0 - 1.0


class UpdateBySignalRequest(BaseModel):
    palace_id: int
    level: int  # 1-6
    signal_value: float  # 实际信号值


class DetectByTextRequest(BaseModel):
    text: str  # 待分析的文本
    palace_id: int = None  # 可选，指定宫位则只在该宫位探测


class RecordTaskRequest(BaseModel):
    palace_id: int
    yao_level: int  # 1-6
    input_text: str
    manual_state: str = None  # 可选，人工标注：阳/阴


class KeywordTrendRequest(BaseModel):
    keyword: str
    palace_id: int = None


@router.get("/status")
async def get_hexagram_status():
    """获取整个六爻感知系统状态"""
    system = get_hexagram_system()
    return system.get_all_palaces_status()


@router.get("/milo-state")
async def get_milo_state():
    """获取米珞当前形态（由8宫状态决定）"""
    system = get_hexagram_system()
    return system.get_milo_state()


@router.get("/rotation")
async def get_rotation_decision():
    """获取旋转决策（正转/反转/平衡）"""
    system = get_hexagram_system()
    return system.get_rotation_decision()


@router.get("/palace/{palace_id}")
async def get_palace_hexagram(palace_id: int):
    """获取单个宫位的六爻状态"""
    if palace_id < 1 or palace_id > 8:
        raise HTTPException(status_code=400, detail="palace_id must be 1-8")
    
    system = get_hexagram_system()
    if palace_id not in system.palaces:
        raise HTTPException(status_code=404, detail="Palace not found")
    
    return system.palaces[palace_id].to_dict()


@router.post("/yao")
async def update_yao_state(req: UpdateYaoRequest):
    """手动更新宫位的爻状态"""
    if req.palace_id < 1 or req.palace_id > 8:
        raise HTTPException(status_code=400, detail="palace_id must be 1-8")
    if req.level < 1 or req.level > 6:
        raise HTTPException(status_code=400, detail="level must be 1-6")
    if req.state not in [0, 1]:
        raise HTTPException(status_code=400, detail="state must be 0(YIN) or 1(YANG)")
    if req.current_level < 0 or req.current_level > 2:
        raise HTTPException(status_code=400, detail="current_level must be 0, 1, or 2")
    
    system = get_hexagram_system()
    system.update_palace_yao(
        req.palace_id,
        req.level,
        YaoState.YANG if req.state == 1 else YaoState.YIN,
        req.current_level
    )
    
    palace = system.palaces[req.palace_id]
    yao = palace.yaos[req.level]
    
    return {
        "success": True,
        "palace_id": req.palace_id,
        "level": req.level,
        "state": "阳" if req.state == 1 else "阴",
        "current_keyword": yao.yang_keywords[req.current_level] if req.state == 1 else yao.yin_keywords[req.current_level],
        "palace_status": palace.to_dict()
    }


@router.post("/load")
async def update_from_load(req: UpdateLoadRequest):
    """根据负载自动更新宫位爻状态"""
    if req.palace_id < 1 or req.palace_id > 8:
        raise HTTPException(status_code=400, detail="palace_id must be 1-8")
    if req.load < 0 or req.load > 1:
        raise HTTPException(status_code=400, detail="load must be 0.0-1.0")
    
    system = get_hexagram_system()
    system.update_palace_from_load(req.palace_id, req.load)
    
    return {
        "success": True,
        "palace_id": req.palace_id,
        "load": req.load,
        "active_level": system.palaces[req.palace_id].get_active_level(),
        "hexagram_pattern": system.palaces[req.palace_id].get_hexagram_pattern(),
        "palace_status": system.palaces[req.palace_id].to_dict()
    }


@router.post("/signal")
async def update_by_signal(req: UpdateBySignalRequest):
    """根据信号值自动识别爻状态（核心识别能力）"""
    if req.palace_id < 1 or req.palace_id > 8:
        raise HTTPException(status_code=400, detail="palace_id must be 1-8")
    if req.level < 1 or req.level > 6:
        raise HTTPException(status_code=400, detail="level must be 1-6")
    
    system = get_hexagram_system()
    palace = system.palaces.get(req.palace_id)
    if not palace:
        raise HTTPException(status_code=404, detail="Palace not found")
    
    yao = palace.yaos.get(req.level)
    if not yao:
        raise HTTPException(status_code=404, detail="Yao not found")
    
    # 根据信号自动识别状态
    yao.update_from_signal(req.signal_value)
    
    return {
        "success": True,
        "palace_id": req.palace_id,
        "level": req.level,
        "signal_source": yao.signal_source,
        "signal_value": req.signal_value,
        "signal_unit": yao.signal_unit,
        "detected_state": "阳" if yao.state == YaoState.YANG else "阴",
        "detected_keyword": yao.yang_keywords[yao.current_level] if yao.state == YaoState.YANG else yao.yin_keywords[yao.current_level],
        "detected_level": yao.current_level,
        "thresholds": yao.thresholds,
        "yao_status": yao.to_dict()
    }


@router.post("/detect")
async def detect_from_text(req: DetectByTextRequest):
    """从文本中探测匹配的爻（关键词识别）"""
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="text cannot be empty")
    
    # 探测匹配的爻
    result = detect_yao_from_text(req.text, req.palace_id)
    
    return {
        "success": True,
        "text": req.text[:100] + "..." if len(req.text) > 100 else req.text,
        "matched_palace": result["matched_palace"],
        "matched_yao": result["matched_yao"],
        "matched_keywords": result["matched_keywords"],
        "match_count": result["match_count"],
        "all_matches": result["all_matches"][:5]  # 返回前5个匹配
    }


@router.post("/task")
async def record_task(req: RecordTaskRequest):
    """记录一次任务执行（用于学习）
    
    执行3次任务会自动总结一次关键词分析
    
    Args:
        palace_id: 宫位(1-8)
        yao_level: 爻位(1-6)
        input_text: 输入文本
        manual_state: 可选，人工标注状态(阳/阴)
    """
    if req.palace_id < 1 or req.palace_id > 8:
        raise HTTPException(status_code=400, detail="palace_id must be 1-8")
    if req.yao_level < 1 or req.yao_level > 6:
        raise HTTPException(status_code=400, detail="yao_level must be 1-6")
    if not req.input_text or not req.input_text.strip():
        raise HTTPException(status_code=400, detail="input_text cannot be empty")
    if req.manual_state and req.manual_state not in ["阳", "阴"]:
        raise HTTPException(status_code=400, detail="manual_state must be '阳' or '阴'")
    
    # 检测关键词
    detect_result = detect_yao_from_text(req.input_text, req.palace_id)
    detected_keywords = detect_result["matched_keywords"]
    
    # 记录任务
    db = get_yao_learning_db()
    result = db.record_task(
        palace_id=req.palace_id,
        yao_level=req.yao_level,
        input_text=req.input_text,
        detected_keywords=detected_keywords,
        manual_state=req.manual_state
    )
    
    return {
        "success": True,
        "task_id": result["task_id"],
        "task_counter": result["task_counter"],
        "detected_keywords": detected_keywords,
        "should_summarize": result["should_summarize"],
        "summary": result["summary"]
    }


@router.get("/summary")
async def get_learning_summary():
    """获取学习总结（关键词分析）"""
    db = get_yao_learning_db()
    summary = db.summarize()
    return summary


@router.post("/trend")
async def get_keyword_trend(req: KeywordTrendRequest):
    """获取关键词趋势"""
    if not req.keyword or not req.keyword.strip():
        raise HTTPException(status_code=400, detail="keyword cannot be empty")
    
    db = get_yao_learning_db()
    trend = db.get_keyword_trend(req.keyword, req.palace_id)
    return trend


@router.get("/stats")
async def get_learning_stats():
    """获取学习统计数据"""
    db = get_yao_learning_db()
    return db.export_stats()


@router.get("/anomalies")
async def detect_anomalies():
    """检测系统异常状态"""
    system = get_hexagram_system()
    anomalies = system.detect_anomaly()
    
    return {
        "has_anomaly": len(anomalies) > 0,
        "anomaly_count": len(anomalies),
        "anomalies": anomalies
    }


@router.get("/system-hexagram")
async def get_system_hexagram():
    """获取系统整体卦象（0-63）"""
    system = get_hexagram_system()
    hex_value = system.get_system_hexagram()
    
    # 64卦名称映射
    HEXAGRAM_NAMES = {
        0: "坤", 1: "复", 2: "师", 3: "谦",
        4: "豫", 5: "比", 6: "萃", 7: "晋",
        8: "否", 9: "无妄", 10: "讼", 11: "遁",
        12: "观", 13: "巽", 14: "中孚", 15: "乾",
        # ... 完整64卦
        63: "既济"
    }
    
    return {
        "hexagram_value": hex_value,
        "hexagram_name": HEXAGRAM_NAMES.get(hex_value, "未知"),
        "binary": bin(hex_value)[2:].zfill(6)
    }


@router.get("/visualize")
async def visualize_hexagrams():
    """可视化所有宫位的六爻状态"""
    system = get_hexagram_system()
    
    # 生成ASCII可视化
    lines = []
    lines.append("╔════════════════════════════════════════════════╗")
    lines.append("║            太极九宫 六爻感知系统                ║")
    lines.append("╠════════════════════════════════════════════════╣")
    
    # 顶部三个宫位：4-9-2
    row1 = [4, 9, 2]
    # 中间三个宫位：3-5-7
    row2 = [3, 5, 7]
    # 底部三个宫位：8-1-6
    row3 = [8, 1, 6]
    
    palace_names = {
        1: "数据采集", 2: "物联产品", 3: "技术团队",
        4: "品牌战略", 5: "中央控制", 6: "质量监控",
        7: "法务框架", 8: "营销客服", 9: "行业生态"
    }
    
    def render_palace(palace_id: int) -> list:
        """渲染单个宫位的六爻"""
        if palace_id == 9:
            # 9宫暂时没有定义
            return ["[9-行业生态]", "  待定义  ", "  ──────  ", "  ──────  ", "  ──────  "]
        
        palace = system.palaces.get(palace_id)
        if not palace:
            return [f"[{palace_id}]", "  N/A  "]
        
        lines = []
        lines.append(f"[{palace_id}-{palace_names.get(palace_id, '')}]")
        
        # 从上爻到初爻渲染
        for level in range(6, 0, -1):
            yao = palace.yaos[level]
            symbol = "━━━阳━━━" if yao.state == YaoState.YANG else "━ ━阴━ ━"
            lines.append(f"  {symbol}")
        
        return lines
    
    # 渲染三行
    for row in [row1, row2, row3]:
        row_lines = []
        for palace_id in row:
            palace_render = render_palace(palace_id)
            row_lines.append(palace_render)
        
        # 合并行
        max_lines = max(len(r) for r in row_lines)
        for i in range(max_lines):
            parts = []
            for r in row_lines:
                if i < len(r):
                    parts.append(f"{r[i]:^16}")
                else:
                    parts.append(" " * 16)
            lines.append("║ " + " │ ".join(parts) + " ║")
        
        if row != row3:
            lines.append("╟────────────────────────────────────────────────╢")
    
    lines.append("╚════════════════════════════════════════════════╝")
    
    return {
        "ascii": "\n".join(lines),
        "status": system.get_all_palaces_status()
    }