"""
六爻感知数据采集接口
从系统日志、API响应、监控数据中采集信号，更新48端状态
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import os
import json
from datetime import datetime

from core.palace_hexagrams import get_hexagram_system, YaoState

router = APIRouter(prefix="/api/signals", tags=["signal-collector"])

# 信号缓存
SIGNAL_CACHE = "/root/taiji-api-v2/data/signal_cache.json"


class SystemSignal(BaseModel):
    """系统信号"""
    source: str  # 来源：log/api/metric/event
    palace_id: int
    yao_level: int
    signal_type: str  # latency/error/count/rate/score
    value: float
    unit: str = ""
    timestamp: str = None


class BatchSignals(BaseModel):
    """批量信号"""
    signals: List[SystemSignal]


def load_signal_cache() -> Dict:
    """加载信号缓存"""
    if os.path.exists(SIGNAL_CACHE):
        with open(SIGNAL_CACHE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"signals": [], "last_update": None}


def save_signal_cache(cache: Dict):
    """保存信号缓存"""
    os.makedirs(os.path.dirname(SIGNAL_CACHE), exist_ok=True)
    with open(SIGNAL_CACHE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


@router.post("/collect")
async def collect_signal(signal: SystemSignal):
    """采集单个信号并更新六爻状态"""
    system = get_hexagram_system()

    if signal.palace_id < 1 or signal.palace_id > 8:
        raise HTTPException(status_code=400, detail="palace_id must be 1-8")
    if signal.yao_level < 1 or signal.yao_level > 6:
        raise HTTPException(status_code=400, detail="yao_level must be 1-6")

    # 更新爻状态
    palace = system.palaces.get(signal.palace_id)
    if palace:
        yao = palace.yaos.get(signal.yao_level)
        if yao:
            yao.update_from_signal(signal.value)
            yao.current_signal = signal.value

            # 记录信号
            cache = load_signal_cache()
            cache["signals"].append({
                "source": signal.source,
                "palace_id": signal.palace_id,
                "yao_level": signal.yao_level,
                "signal_type": signal.signal_type,
                "value": signal.value,
                "unit": signal.unit,
                "detected_state": "阳" if yao.state == YaoState.YANG else "阴",
                "detected_keyword": yao.yang_keywords[yao.current_level] if yao.state == YaoState.YANG else yao.yin_keywords[yao.current_level],
                "timestamp": signal.timestamp or datetime.now().isoformat()
            })
            cache["last_update"] = datetime.now().isoformat()
            # 只保留最近1000条
            cache["signals"] = cache["signals"][-1000:]
            save_signal_cache(cache)

            return {
                "success": True,
                "palace_id": signal.palace_id,
                "yao_level": signal.yao_level,
                "signal_value": signal.value,
                "detected_state": "阳" if yao.state == YaoState.YANG else "阴",
                "detected_keyword": yao.yang_keywords[yao.current_level] if yao.state == YaoState.YANG else yao.yin_keywords[yao.current_level]
            }

    raise HTTPException(status_code=404, detail="Palace or Yao not found")


@router.post("/batch")
async def collect_batch(signals: BatchSignals):
    """批量采集信号"""
    results = []

    for signal in signals.signals:
        try:
            system = get_hexagram_system()
            palace = system.palaces.get(signal.palace_id)
            if palace:
                yao = palace.yaos.get(signal.yao_level)
                if yao:
                    yao.update_from_signal(signal.value)
                    results.append({
                        "palace_id": signal.palace_id,
                        "yao_level": signal.yao_level,
                        "success": True
                    })
                    continue
        except:
            pass
        results.append({
            "palace_id": signal.palace_id,
            "yao_level": signal.yao_level,
            "success": False
        })

    return {
        "success": True,
        "total": len(signals.signals),
        "processed": sum(1 for r in results if r["success"]),
        "results": results
    }


@router.get("/history")
async def get_signal_history(palace_id: int = None, limit: int = 100):
    """获取信号历史"""
    cache = load_signal_cache()
    signals = cache.get("signals", [])

    if palace_id:
        signals = [s for s in signals if s.get("palace_id") == palace_id]

    return {
        "signals": signals[-limit:],
        "total": len(signals),
        "last_update": cache.get("last_update")
    }


@router.get("/stats")
async def get_signal_stats():
    """获取信号统计"""
    cache = load_signal_cache()
    signals = cache.get("signals", [])

    # 按宫位统计
    palace_stats = {}
    for s in signals:
        pid = s.get("palace_id")
        if pid not in palace_stats:
            palace_stats[pid] = {"total": 0, "yang": 0, "yin": 0}
        palace_stats[pid]["total"] += 1
        if s.get("detected_state") == "阳":
            palace_stats[pid]["yang"] += 1
        else:
            palace_stats[pid]["yin"] += 1

    return {
        "total_signals": len(signals),
        "palace_stats": palace_stats,
        "last_update": cache.get("last_update")
    }


# 预定义的信号采集器配置
SIGNAL_COLLECTORS = {
    "system_health": {
        "description": "系统健康检查",
        "interval_seconds": 60,
        "signals": [
            {"palace_id": 5, "yao_level": 1, "source": "metric", "signal_type": "uptime"}
        ]
    },
    "api_latency": {
        "description": "API延迟监控",
        "interval_seconds": 30,
        "signals": [
            {"palace_id": 1, "yao_level": 1, "source": "metric", "signal_type": "latency"}
        ]
    }
}


@router.get("/collectors")
async def list_collectors():
    """列出可用的信号采集器"""
    return {"collectors": SIGNAL_COLLECTORS}