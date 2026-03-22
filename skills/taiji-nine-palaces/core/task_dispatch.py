"""
任务分发协议
将任务分发给注册的智能体执行
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import httpx

# 数据文件
TASK_DISPATCH_DB = "/root/taiji-api-v2/data/task_dispatch.json"
AGENTS_DB = "/root/taiji-api-v2/data/registered_agents.json"


def load_dispatch_db() -> Dict:
    """加载分发数据库"""
    if os.path.exists(TASK_DISPATCH_DB):
        with open(TASK_DISPATCH_DB, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"dispatches": [], "pending_queue": []}


def save_dispatch_db(db: Dict):
    """保存分发数据库"""
    os.makedirs(os.path.dirname(TASK_DISPATCH_DB), exist_ok=True)
    with open(TASK_DISPATCH_DB, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


def load_agents() -> Dict:
    """加载智能体注册表"""
    if os.path.exists(AGENTS_DB):
        with open(AGENTS_DB, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def find_capable_agents(capability: str) -> List[Dict]:
    """找到具备指定能力的智能体"""
    agents = load_agents()
    capable = []

    for agent_id, agent in agents.items():
        if capability in agent.get("capabilities", []):
            if agent.get("status") == "idle":
                capable.append(agent)

    # 按负载排序，优先分配给负载低的
    capable.sort(key=lambda x: x.get("load", 0))
    return capable


async def dispatch_task(task_id: str, task_type: str, task_data: Dict) -> Dict:
    """分发任务给智能体

    Args:
        task_id: 任务ID
        task_type: 任务类型（用于匹配能力）
        task_data: 任务数据

    Returns:
        分发结果
    """
    # 1. 找到能执行此任务的智能体
    capable_agents = find_capable_agents(task_type)

    if not capable_agents:
        # 加入待分发队列
        db = load_dispatch_db()
        db["pending_queue"].append({
            "task_id": task_id,
            "task_type": task_type,
            "task_data": task_data,
            "queued_at": datetime.now().isoformat()
        })
        save_dispatch_db(db)
        return {
            "success": False,
            "message": "没有可用的智能体，任务已加入队列",
            "queue_position": len(db["pending_queue"])
        }

    # 2. 选择负载最低的智能体
    selected_agent = capable_agents[0]

    # 3. 发送任务到智能体端点
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{selected_agent['endpoint']}/task",
                json={
                    "task_id": task_id,
                    "task_type": task_type,
                    "task_data": task_data,
                    "taiji_callback": "http://localhost:8000/api/agents/report"
                }
            )

            if response.status_code == 200:
                # 记录分发
                db = load_dispatch_db()
                db["dispatches"].append({
                    "task_id": task_id,
                    "agent_id": selected_agent["agent_id"],
                    "agent_name": selected_agent["name"],
                    "dispatched_at": datetime.now().isoformat(),
                    "status": "in_progress"
                })
                save_dispatch_db(db)

                return {
                    "success": True,
                    "message": f"任务已分发给 {selected_agent['name']}",
                    "agent_id": selected_agent["agent_id"],
                    "agent_name": selected_agent["name"]
                }
            else:
                return {
                    "success": False,
                    "message": f"智能体响应异常: {response.status_code}"
                }

    except Exception as e:
        return {
            "success": False,
            "message": f"分发失败: {str(e)}"
        }


def get_dispatch_status(task_id: str) -> Optional[Dict]:
    """获取任务分发状态"""
    db = load_dispatch_db()

    for dispatch in db.get("dispatches", []):
        if dispatch["task_id"] == task_id:
            return dispatch

    # 检查是否在队列中
    for i, queued in enumerate(db.get("pending_queue", [])):
        if queued["task_id"] == task_id:
            return {
                "task_id": task_id,
                "status": "queued",
                "queue_position": i + 1
            }

    return None


def process_pending_queue():
    """处理待分发队列"""
    db = load_dispatch_db()
    pending = db.get("pending_queue", [])

    if not pending:
        return {"processed": 0, "message": "队列为空"}

    # 尝试分发队列中的任务
    # 简化版：每次只处理第一个
    # TODO: 批量处理

    return {"processed": 0, "message": "队列处理功能待完善"}


# 能力映射：任务类型 → 所需能力
TASK_TYPE_TO_CAPABILITY = {
    "download": "data_collection",
    "scrape": "data_collection",
    "transcribe": "media_processing",
    "code": "coding",
    "analyze": "analysis",
    "write": "content_creation",
    "translate": "translation",
    "monitor": "monitoring",
    "backup": "backup",
    "search": "search"
}


def get_required_capability(task_type: str) -> str:
    """获取任务类型所需的能力"""
    return TASK_TYPE_TO_CAPABILITY.get(task_type, task_type)