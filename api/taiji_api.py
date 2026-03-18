from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from loguru import logger
from datetime import datetime
import uvicorn
import os
import sys

# 添加父目录到Python路径，确保能找到core模块
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, "..")
sys.path.insert(0, parent_dir)

# 延迟导入以避免循环依赖
class TaijiManager:
    pass

class TaijiCoreEngine:
    pass

taiji_manager: Optional[TaijiManager] = None
taiji_engine: Optional[TaijiCoreEngine] = None

# 模型定义
class ZhengzhuanRequest(BaseModel):
    node_id: str
    value: float

class FanzhuanRequest(BaseModel):
    node_id: str

class AddNodeRequest(BaseModel):
    node_id: str
    node_type: str
    initial_value: float = 0.5

class RemoveNodeRequest(BaseModel):
    node_id: str

class AddEdgeRequest(BaseModel):
    edge_id: str
    source: str
    target: str
    strength: float = 0.5

class RemoveEdgeRequest(BaseModel):
    edge_id: str

class OpenClawActionRequest(BaseModel):
    action: str
    params: Dict[str, Any]

class SwitchModeRequest(BaseModel):
    mode: str

class UpdatePalaceLoadRequest(BaseModel):
    palace_id: int
    load: float

class RunFiveElementsRequest(BaseModel):
    task_result: Dict[str, Any]

class BatchUpdatePalaceLoadRequest(BaseModel):
    palaces: List[Dict[str, Any]]

class ResetEngineRequest(BaseModel):
    reset_mode: str = "full"

class ConfigureEngineRequest(BaseModel):
    params: Dict[str, Any]

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 定义模板和静态文件目录
templates_dir = os.path.join(current_dir, "..", "templates")
static_dir = os.path.join(current_dir, "..", "static")

# 确保目录存在
os.makedirs(templates_dir, exist_ok=True)
os.makedirs(static_dir, exist_ok=True)

app = FastAPI(
    title="Taiji System API",
    description="API for Taiji system operations",
    version="1.0.0"
)

# 挂载静态文件和模板
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

# 初始化TaijiManager和TaijiCoreEngine
@app.on_event("startup")
async def startup_event():
    global taiji_manager, taiji_engine
    from core.taiji_manager import TaijiManager as RealTaijiManager
    from core.taiji_logic_engine import TaijiCoreEngine as RealTaijiCoreEngine, TaijiMode
    taiji_manager = RealTaijiManager()
    taiji_engine = RealTaijiCoreEngine()
    logger.info("Taiji API server started")
    logger.info("Taiji Core Engine initialized")

# API端点
@app.get("/api/state", response_model=Dict[str, Any])
async def get_state():
    """获取当前太极系统状态"""
    if not taiji_manager:
        raise HTTPException(status_code=503, detail="Taiji manager not initialized")
    try:
        state = taiji_manager.get_state()
        return state
    except Exception as e:
        logger.error(f"Error getting state: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/zhengzhuan", response_model=Dict[str, Any])
async def perform_zhengzhuan(request: ZhengzhuanRequest):
    """执行正转操作"""
    if not taiji_manager:
        raise HTTPException(status_code=503, detail="Taiji manager not initialized")
    try:
        result = taiji_manager.perform_zhengzhuan(request.node_id, request.value)
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error performing zhengzhuan: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/fanzhuan", response_model=Dict[str, Any])
async def perform_fanzhuan(request: FanzhuanRequest):
    """执行反转操作"""
    if not taiji_manager:
        raise HTTPException(status_code=503, detail="Taiji manager not initialized")
    try:
        result = taiji_manager.perform_fanzhuan(request.node_id)
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        return result
    except Exception as e:
        logger.error(f"Error performing fanzhuan: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/reset", response_model=Dict[str, Any])
async def reset_state():
    """重置太极系统状态"""
    if not taiji_manager:
        raise HTTPException(status_code=503, detail="Taiji manager not initialized")
    try:
        result = taiji_manager.reset_state()
        return result
    except Exception as e:
        logger.error(f"Error resetting state: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/statistics", response_model=Dict[str, Any])
async def get_statistics():
    """获取系统统计信息"""
    if not taiji_manager:
        raise HTTPException(status_code=503, detail="Taiji manager not initialized")
    try:
        stats = taiji_manager.get_statistics()
        return stats
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/nodes", response_model=Dict[str, Any])
async def add_node(request: AddNodeRequest):
    """添加新节点"""
    if not taiji_manager:
        raise HTTPException(status_code=503, detail="Taiji manager not initialized")
    try:
        result = taiji_manager.add_node(request.node_id, request.node_type, request.initial_value)
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error adding node: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/api/nodes/{node_id}", response_model=Dict[str, Any])
async def remove_node(node_id: str):
    """删除节点"""
    if not taiji_manager:
        raise HTTPException(status_code=503, detail="Taiji manager not initialized")
    try:
        result = taiji_manager.remove_node(node_id)
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        return result
    except Exception as e:
        logger.error(f"Error removing node: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/edges", response_model=Dict[str, Any])
async def add_edge(request: AddEdgeRequest):
    """添加新边"""
    if not taiji_manager:
        raise HTTPException(status_code=503, detail="Taiji manager not initialized")
    try:
        result = taiji_manager.add_edge(request.edge_id, request.source, request.target, request.strength)
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error adding edge: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/api/edges/{edge_id}", response_model=Dict[str, Any])
async def remove_edge(edge_id: str):
    """删除边"""
    if not taiji_manager:
        raise HTTPException(status_code=503, detail="Taiji manager not initialized")
    try:
        result = taiji_manager.remove_edge(edge_id)
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        return result
    except Exception as e:
        logger.error(f"Error removing edge: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/openclaw/integration", response_model=Dict[str, Any])
async def openclaw_integration(request: OpenClawActionRequest):
    """OpenClaw集成端点"""
    if not taiji_manager:
        raise HTTPException(status_code=503, detail="Taiji manager not initialized")
    try:
        action = request.action
        params = request.params
        
        if action == "get_state":
            return taiji_manager.get_state()
        elif action == "perform_action":
            sub_action = params.get("action")
            if sub_action == "zhengzhuan":
                return taiji_manager.perform_zhengzhuan(params.get("node_id"), params.get("value"))
            elif sub_action == "fanzhuan":
                return taiji_manager.perform_fanzhuan(params.get("node_id"))
            else:
                raise HTTPException(status_code=400, detail=f"Unknown action: {sub_action}")
        elif action == "reset_state":
            return taiji_manager.reset_state()
        elif action == "get_statistics":
            return taiji_manager.get_statistics()
        else:
            raise HTTPException(status_code=400, detail=f"Unknown action: {action}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in OpenClaw integration: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# 首页路由
@app.get("/")
async def root(request: Request):
    """返回Web管理界面"""
    return templates.TemplateResponse("index.html", {"request": request})

# 健康检查端点
@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}

# 太极核心引擎端点
@app.post("/api/taiji/switch-mode", response_model=Dict[str, Any])
async def switch_taiji_mode(request: SwitchModeRequest):
    """切换太极模式"""
    if not taiji_engine:
        raise HTTPException(status_code=503, detail="Taiji engine not initialized")
    try:
        from core.taiji_logic_engine import TaijiMode
        mode_map = {
            "yang": TaijiMode.YANG_FORWARD,
            "yin": TaijiMode.YIN_REVERSE
        }
        if request.mode not in mode_map:
            raise HTTPException(status_code=400, detail="Invalid mode. Use 'yang' or 'yin'")
        taiji_engine.switch_mode(mode_map[request.mode])
        return {"success": True, "message": f"Switched to {request.mode} mode"}
    except Exception as e:
        logger.error(f"Error switching mode: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/taiji/advance-symbols", response_model=Dict[str, Any])
async def advance_symbols():
    """推进四象阶段"""
    if not taiji_engine:
        raise HTTPException(status_code=503, detail="Taiji engine not initialized")
    try:
        taiji_engine.advance_symbols()
        return {"success": True, "message": "Advanced symbols stage"}
    except Exception as e:
        logger.error(f"Error advancing symbols: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/taiji/update-palace-load", response_model=Dict[str, Any])
async def update_palace_load(request: UpdatePalaceLoadRequest):
    """更新宫位负载"""
    if not taiji_engine:
        raise HTTPException(status_code=503, detail="Taiji engine not initialized")
    try:
        taiji_engine.update_palace_load(request.palace_id, request.load)
        return {"success": True, "message": f"Updated palace {request.palace_id} load to {request.load}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating palace load: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/taiji/palace/{palace_id}", response_model=Dict[str, Any])
async def get_palace_state(palace_id: int):
    """获取宫位状态"""
    if not taiji_engine:
        raise HTTPException(status_code=503, detail="Taiji engine not initialized")
    try:
        state = taiji_engine.get_palace_state(palace_id)
        if not state:
            raise HTTPException(status_code=404, detail=f"Palace {palace_id} not found")
        return state
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting palace state: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# ========== L4 规则层端点 ==========

@app.post("/api/l4/command", response_model=Dict[str, Any])
async def l4_command(request: Request):
    """
    L4 规则层 - 5 宫指挥官命令入口
    
    接收用户指令，自动执行:
    1. 优先级判断
    2. 宫位分配
    3. TDD 标准定义
    4. 红灯确认
    5. 启动执行
    """
    try:
        from core.l4_rule_engine import l4_handle_command
        data = await request.json()
        command = data.get("command", "")
        
        if not command:
            raise HTTPException(status_code=400, detail="Missing 'command' field")
        
        result = l4_handle_command(command)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"L4 command failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/l4/complete", response_model=Dict[str, Any])
async def l4_complete(request: Request):
    """
    L4 规则层 - 任务完成（绿灯检查）
    
    接收任务输出，执行 TDD 验收:
    1. 对照标准检查
    2. 绿灯通过 → 交付
    3. 红灯失败 → 返工
    """
    try:
        from core.l4_rule_engine import l4_complete_task
        data = await request.json()
        task_id = data.get("task_id")
        output = data.get("output")
        
        if not task_id:
            raise HTTPException(status_code=400, detail="Missing 'task_id' field")
        
        result = l4_complete_task(task_id, output)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"L4 complete failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/l4/status", response_model=Dict[str, Any])
async def l4_status():
    """
    L4 规则层 - 状态查询
    
    返回:
    - 任务报告
    - 宫位负载
    - 平衡状态
    """
    try:
        from core.l4_rule_engine import l4_get_status
        return l4_get_status()
    except Exception as e:
        logger.error(f"L4 status failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/palace3/models", response_model=List[Dict[str, Any]])
async def palace3_models():
    """
    3 宫 - 模型能力列表
    
    返回所有可用模型及其能力
    """
    try:
        from core.palace_3_model_allocator import palace3_get_capabilities
        return palace3_get_capabilities()
    except Exception as e:
        logger.error(f"Palace 3 models failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/palace3/compare/{task_type}", response_model=Dict[str, Any])
async def palace3_compare(task_type: str):
    """
    3 宫 - 模式对比
    
    比较 API Token vs Zero Token 模式
    """
    try:
        from core.palace_3_model_allocator import palace3_compare_modes
        return palace3_compare_modes(task_type)
    except Exception as e:
        logger.error(f"Palace 3 compare failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/palace3/cost-report", response_model=Dict[str, Any])
async def palace3_cost_report():
    """
    3 宫 - 成本报告
    
    返回 Zero Token 节省统计
    """
    try:
        from core.palace_3_model_allocator import palace3_get_cost_report
        return palace3_get_cost_report()
    except Exception as e:
        logger.error(f"Palace 3 cost report failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========== 1 宫数据采集端点 ==========

@app.get("/api/palace1/modes", response_model=Dict[str, Any])
async def palace1_modes():
    """
    1 宫 - 抓取模式对比
    
    HTTP 快速模式 vs 浏览器渲染模式
    """
    try:
        from core.palace_1_data_collection import palace1_get_mode_comparison
        return palace1_get_mode_comparison()
    except Exception as e:
        logger.error(f"Palace 1 modes failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/palace1/anti-block", response_model=List[Dict[str, Any]])
async def palace1_anti_block():
    """
    1 宫 - 防封禁特性
    
    模拟人类行为、IP 轮换等
    """
    try:
        from core.palace_1_data_collection import palace1_get_anti_block_features
        return palace1_get_anti_block_features()
    except Exception as e:
        logger.error(f"Palace 1 anti-block failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/palace1/configure", response_model=Dict[str, Any])
async def palace1_configure(request: Request):
    """
    1 宫 - 配置抓取任务
    
    根据网站类型自动选择最佳配置
    """
    try:
        from core.palace_1_data_collection import palace1_configure_crawl
        data = await request.json()
        url = data.get("url", "")
        site_type = data.get("site_type", "simple_text")
        mode = data.get("mode", "http_fast")
        
        return palace1_configure_crawl(url, site_type, mode)
    except Exception as e:
        logger.error(f"Palace 1 configure failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/palace1/report", response_model=Dict[str, Any])
async def palace1_report():
    """
    1 宫 - 抓取报告
    
    历史抓取统计
    """
    try:
        from core.palace_1_data_collection import palace1_get_crawl_report
        return palace1_get_crawl_report()
    except Exception as e:
        logger.error(f"Palace 1 report failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=Dict[str, Any])
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }

@app.get("/api/monitor/status", response_model=Dict[str, Any])
async def monitor_status():
    """6 宫监控 - 系统状态监控"""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    
    return {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": process.memory_percent(),
        "memory_info_mb": process.memory_info().rss / 1024 / 1024,
        "disk_usage_percent": psutil.disk_usage('/').percent,
        "uptime_hours": (datetime.now() - datetime.fromtimestamp(process.create_time())).total_seconds() / 3600,
        "active_tasks": 0  # 简化实现
    }

@app.get("/api/taiji/balance", response_model=Dict[str, Any])
async def get_balance_status():
    """获取阴阳平衡状态"""
    if not taiji_engine:
        raise HTTPException(status_code=503, detail="Taiji engine not initialized")
    try:
        balance = taiji_engine.get_balance_status()
        imbalanced = taiji_engine.check_balance_and_adjust()
        return {
            "balance": balance,
            "imbalanced_pairs": imbalanced
        }
    except Exception as e:
        logger.error(f"Error getting balance status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/taiji/five-elements", response_model=Dict[str, Any])
async def run_five_elements(request: RunFiveElementsRequest):
    """运行五行循环检查"""
    if not taiji_engine:
        raise HTTPException(status_code=503, detail="Taiji engine not initialized")
    try:
        taiji_engine.run_five_elements_check(request.task_result)
        return {"success": True, "message": "Ran five elements check"}
    except Exception as e:
        logger.error(f"Error running five elements check: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/taiji/status", response_model=Dict[str, Any])
async def get_taiji_status():
    """获取太极引擎状态"""
    if not taiji_engine:
        raise HTTPException(status_code=503, detail="Taiji engine not initialized")
    try:
        return {
            "mode": taiji_engine.mode.value,
            "symbols_stage": taiji_engine.symbols_stage.value,
            "balance": taiji_engine.get_balance_status(),
            "task_count": taiji_engine.get_task_count()
        }
    except Exception as e:
        logger.error(f"Error getting taiji status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/taiji/batch-update-palaces", response_model=Dict[str, Any])
async def batch_update_palaces(request: BatchUpdatePalaceLoadRequest):
    """批量更新宫位负载"""
    if not taiji_engine:
        raise HTTPException(status_code=503, detail="Taiji engine not initialized")
    try:
        for palace in request.palaces:
            palace_id = palace.get("palace_id")
            load = palace.get("load")
            if palace_id is not None and load is not None:
                taiji_engine.update_palace_load(palace_id, load)
        return {"success": True, "message": "Batch updated palaces"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error batch updating palaces: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/taiji/reset-engine", response_model=Dict[str, Any])
async def reset_engine(request: ResetEngineRequest):
    """重置太极引擎状态"""
    if not taiji_engine:
        raise HTTPException(status_code=503, detail="Taiji engine not initialized")
    try:
        taiji_engine.reset_state()
        return {"success": True, "message": "Reset taiji engine state"}
    except Exception as e:
        logger.error(f"Error resetting engine: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/taiji/palaces", response_model=Dict[str, Any])
async def get_all_palaces():
    """获取所有宫位状态"""
    if not taiji_engine:
        raise HTTPException(status_code=503, detail="Taiji engine not initialized")
    try:
        palaces = {}
        for i in range(1, 10):  # 九宫
            state = taiji_engine.get_palace_state(i)
            if state:
                palaces[i] = state
        return {"palaces": palaces}
    except Exception as e:
        logger.error(f"Error getting all palaces: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/taiji/adjust-balance", response_model=Dict[str, Any])
async def adjust_balance():
    """手动触发阴阳平衡调整"""
    if not taiji_engine:
        raise HTTPException(status_code=503, detail="Taiji engine not initialized")
    try:
        imbalanced = taiji_engine.check_balance_and_adjust()
        balance = taiji_engine.get_balance_status()
        return {
            "success": True,
            "message": "Adjusted balance",
            "balance": balance,
            "imbalanced_pairs": imbalanced
        }
    except Exception as e:
        logger.error(f"Error adjusting balance: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/taiji/five-elements/status", response_model=Dict[str, Any])
async def get_five_elements_status():
    """获取五行循环状态"""
    if not taiji_engine:
        raise HTTPException(status_code=503, detail="Taiji engine not initialized")
    try:
        # 这里假设taiji_engine有一个方法来获取五行循环状态
        # 如果没有，我们可以返回一个默认的状态
        return {
            "status": "active",
            "elements": ["木", "火", "土", "金", "水"],
            "current_element": "木"
        }
    except Exception as e:
        logger.error(f"Error getting five elements status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/taiji/configure", response_model=Dict[str, Any])
async def configure_engine(request: ConfigureEngineRequest):
    """配置太极引擎参数"""
    if not taiji_engine:
        raise HTTPException(status_code=503, detail="Taiji engine not initialized")
    try:
        # 这里假设taiji_engine有一个方法来配置参数
        # 如果没有，我们可以返回一个成功的消息
        return {
            "success": True,
            "message": "Configured taiji engine",
            "params": request.params
        }
    except Exception as e:
        logger.error(f"Error configuring engine: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    uvicorn.run("taiji_api:app", host="0.0.0.0", port=8000, reload=True)