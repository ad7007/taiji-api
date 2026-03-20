"""
外部智能体接入API
让其他智能体能够注册到太极系统，接收任务，汇报状态
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
import json
import os
import uuid

router = APIRouter(prefix="/api/agents", tags=["external-agents"])

# 智能体注册表
AGENTS_DB = "/root/taiji-api-v2/data/registered_agents.json"


class AgentRegister(BaseModel):
    """智能体注册信息"""
    name: str  # 智能体名称
    owner: str  # 主人/组织
    capabilities: List[str]  # 能力标签
    endpoint: str  # 回调地址
    description: str = ""


class AgentHeartbeat(BaseModel):
    """智能体心跳"""
    agent_id: str
    status: str  # idle/busy/offline
    current_task: str = None
    load: float = 0.0  # 0-1


class TaskReport(BaseModel):
    """任务汇报"""
    agent_id: str
    task_id: str
    status: str  # completed/failed/in_progress
    result: str = None


def load_agents() -> Dict:
    """加载智能体注册表"""
    if os.path.exists(AGENTS_DB):
        with open(AGENTS_DB, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_agents(agents: Dict):
    """保存智能体注册表"""
    os.makedirs(os.path.dirname(AGENTS_DB), exist_ok=True)
    with open(AGENTS_DB, 'w', encoding='utf-8') as f:
        json.dump(agents, f, ensure_ascii=False, indent=2)


@router.post("/register")
async def register_agent(agent: AgentRegister):
    """注册智能体到太极系统"""
    agent_id = f"agent_{uuid.uuid4().hex[:8]}"

    agents = load_agents()
    agents[agent_id] = {
        "agent_id": agent_id,
        "name": agent.name,
        "owner": agent.owner,
        "capabilities": agent.capabilities,
        "endpoint": agent.endpoint,
        "description": agent.description,
        "status": "idle",
        "registered_at": datetime.now().isoformat(),
        "last_heartbeat": None,
        "total_tasks_completed": 0
    }
    save_agents(agents)

    return {
        "success": True,
        "agent_id": agent_id,
        "message": f"智能体 {agent.name} 已注册到太极系统",
        "taiji_endpoint": "http://localhost:8000/api/agents"
    }


@router.get("/list")
async def list_agents(capability: str = None):
    """列出已注册的智能体"""
    agents = load_agents()

    result = []
    for agent_id, agent in agents.items():
        if capability and capability not in agent.get("capabilities", []):
            continue
        result.append({
            "agent_id": agent_id,
            "name": agent["name"],
            "owner": agent["owner"],
            "capabilities": agent["capabilities"],
            "status": agent.get("status", "unknown")
        })

    return {"agents": result, "total": len(result)}


@router.post("/heartbeat")
async def agent_heartbeat(heartbeat: AgentHeartbeat):
    """智能体发送心跳"""
    agents = load_agents()

    if heartbeat.agent_id not in agents:
        raise HTTPException(status_code=404, detail="智能体未注册")

    agents[heartbeat.agent_id]["status"] = heartbeat.status
    agents[heartbeat.agent_id]["last_heartbeat"] = datetime.now().isoformat()
    agents[heartbeat.agent_id]["current_task"] = heartbeat.current_task
    agents[heartbeat.agent_id]["load"] = heartbeat.load

    save_agents(agents)

    return {"success": True, "message": "心跳已更新"}


@router.post("/report")
async def report_task(report: TaskReport):
    """智能体汇报任务结果"""
    agents = load_agents()

    if report.agent_id not in agents:
        raise HTTPException(status_code=404, detail="智能体未注册")

    if report.status == "completed":
        agents[report.agent_id]["total_tasks_completed"] = \
            agents[report.agent_id].get("total_tasks_completed", 0) + 1
        agents[report.agent_id]["status"] = "idle"
        agents[report.agent_id]["current_task"] = None

    save_agents(agents)

    # TODO: 记录任务结果到任务系统

    return {
        "success": True,
        "message": f"任务 {report.task_id} 已汇报: {report.status}"
    }


@router.get("/{agent_id}")
async def get_agent(agent_id: str):
    """获取智能体详情"""
    agents = load_agents()

    if agent_id not in agents:
        raise HTTPException(status_code=404, detail="智能体不存在")

    return agents[agent_id]


@router.delete("/{agent_id}")
async def unregister_agent(agent_id: str):
    """注销智能体"""
    agents = load_agents()

    if agent_id not in agents:
        raise HTTPException(status_code=404, detail="智能体不存在")

    agent_name = agents[agent_id]["name"]
    del agents[agent_id]
    save_agents(agents)

    return {"success": True, "message": f"智能体 {agent_name} 已注销"}


# 任务分发接口
@router.get("/tasks/available")
async def get_available_tasks(capability: str = None):
    """获取可领取的任务"""
    # TODO: 从任务系统获取待分配任务
    # 根据能力匹配

    return {
        "tasks": [],
        "message": "任务分发功能开发中"
    }


@router.post("/tasks/claim")
async def claim_task(agent_id: str, task_id: str):
    """智能体领取任务"""
    agents = load_agents()

    if agent_id not in agents:
        raise HTTPException(status_code=404, detail="智能体未注册")

    # TODO: 从任务系统分配任务

    agents[agent_id]["status"] = "busy"
    agents[agent_id]["current_task"] = task_id
    save_agents(agents)

    return {
        "success": True,
        "message": f"任务 {task_id} 已分配给 {agents[agent_id]['name']}"
    }