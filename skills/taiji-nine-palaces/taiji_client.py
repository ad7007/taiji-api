#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太极九宫任务管理系统客户端
Taiji Nine Palaces Task Management System Client
"""

import requests
import json
from typing import Dict, Any, Optional, List

TAIJI_API_URL = "http://localhost:8000"


class TaijiClient:
    """太极 API 客户端"""
    
    def __init__(self, base_url: str = TAIJI_API_URL):
        self.base_url = base_url
        self.session = requests.Session()
    
    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """发送 HTTP 请求"""
        url = f"{self.base_url}{endpoint}"
        try:
            if method == "GET":
                response = self.session.get(url, timeout=10)
            elif method == "POST":
                response = self.session.post(url, json=data, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    # ========== 基础状态查询 ==========
    
    def get_state(self) -> Dict[str, Any]:
        """获取太极系统状态"""
        return self._request("GET", "/api/state")
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取系统统计信息"""
        return self._request("GET", "/api/statistics")
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        return self._request("GET", "/health")
    
    # ========== 九宫格相关 ==========
    
    def get_all_palaces(self) -> Dict[str, Any]:
        """获取所有宫位状态"""
        return self._request("GET", "/api/taiji/palaces")
    
    def get_palace(self, palace_id: int) -> Dict[str, Any]:
        """获取单个宫位状态"""
        return self._request("GET", f"/api/taiji/palace/{palace_id}")
    
    def update_palace_load(self, palace_id: int, load: float) -> Dict[str, Any]:
        """更新宫位负载"""
        if not 0 <= load <= 1:
            return {"success": False, "error": "负载值必须在 0-1 之间"}
        return self._request("POST", "/api/taiji/update-palace-load", {
            "palace_id": palace_id,
            "load": load
        })
    
    def batch_update_palaces(self, palaces: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量更新宫位负载"""
        return self._request("POST", "/api/taiji/batch-update-palaces", {
            "palaces": palaces
        })
    
    # ========== 阴阳平衡 ==========
    
    def get_balance_status(self) -> Dict[str, Any]:
        """获取阴阳平衡状态"""
        return self._request("GET", "/api/taiji/balance")
    
    def adjust_balance(self) -> Dict[str, Any]:
        """手动触发阴阳平衡调整"""
        return self._request("POST", "/api/taiji/adjust-balance")
    
    # ========== 两仪操作 ==========
    
    def switch_mode(self, mode: str) -> Dict[str, Any]:
        """切换太极模式"""
        if mode not in ["yang", "yin"]:
            return {"success": False, "error": "模式必须是 'yang' 或 'yin'"}
        return self._request("POST", "/api/taiji/switch-mode", {"mode": mode})
    
    def perform_zhengzhuan(self, node_id: str, value: float) -> Dict[str, Any]:
        """执行正转操作"""
        return self._request("POST", "/api/zhengzhuan", {
            "node_id": node_id,
            "value": value
        })
    
    def perform_fanzhuan(self, node_id: str) -> Dict[str, Any]:
        """执行反转操作"""
        return self._request("POST", "/api/fanzhuan", {"node_id": node_id})
    
    # ========== 四象循环 ==========
    
    def advance_symbols(self) -> Dict[str, Any]:
        """推进四象阶段"""
        return self._request("POST", "/api/taiji/advance-symbols")
    
    # ========== 五行循环 ==========
    
    def run_five_elements(self, task_result: Dict[str, Any]) -> Dict[str, Any]:
        """运行五行循环检查"""
        return self._request("POST", "/api/taiji/five-elements", {
            "task_result": task_result
        })
    
    def get_five_elements_status(self) -> Dict[str, Any]:
        """获取五行循环状态"""
        return self._request("GET", "/api/taiji/five-elements/status")
    
    # ========== 引擎控制 ==========
    
    def get_taiji_status(self) -> Dict[str, Any]:
        """获取太极引擎状态"""
        return self._request("GET", "/api/taiji/status")
    
    def reset_engine(self, reset_mode: str = "full") -> Dict[str, Any]:
        """重置太极引擎状态"""
        return self._request("POST", "/api/taiji/reset-engine", {
            "reset_mode": reset_mode
        })
    
    def configure_engine(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """配置太极引擎参数"""
        return self._request("POST", "/api/taiji/configure", {"params": params})
    
    # ========== 节点和边管理 ==========
    
    def add_node(self, node_id: str, node_type: str, initial_value: float = 0.5) -> Dict[str, Any]:
        """添加新节点"""
        return self._request("POST", "/api/nodes", {
            "node_id": node_id,
            "node_type": node_type,
            "initial_value": initial_value
        })
    
    def remove_node(self, node_id: str) -> Dict[str, Any]:
        """删除节点"""
        return self._request("DELETE", f"/api/nodes/{node_id}")
    
    def add_edge(self, edge_id: str, source: str, target: str, strength: float = 0.5) -> Dict[str, Any]:
        """添加新边"""
        return self._request("POST", "/api/edges", {
            "edge_id": edge_id,
            "source": source,
            "target": target,
            "strength": strength
        })
    
    def remove_edge(self, edge_id: str) -> Dict[str, Any]:
        """删除边"""
        return self._request("DELETE", f"/api/edges/{edge_id}")
    
    # ========== OpenClaw 集成端点 ==========
    
    def openclaw_action(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """OpenClaw 集成操作"""
        return self._request("POST", "/api/openclaw/integration", {
            "action": action,
            "params": params
        })


def display_palaces(palaces_data: Dict[str, Any]) -> str:
    """格式化显示九宫格状态"""
    if "palaces" not in palaces_data:
        return json.dumps(palaces_data, indent=2, ensure_ascii=False)
    
    palaces = palaces_data["palaces"]
    
    # 九宫格布局映射
    layout = [
        [4, 9, 2],
        [3, 5, 7],
        [8, 1, 6]
    ]
    
    lines = []
    lines.append("┌────────────────┬────────────────┬────────────────┐")
    for row in layout:
        row_str = "│"
        for palace_id in row:
            palace = palaces.get(str(palace_id), {})
            name = palace.get("name", f"{palace_id}-未知")
            load = palace.get("load", 0)
            element = palace.get("element", "?")
            load_bar = "█" * int(load * 10) + "░" * (10 - int(load * 10))
            row_str += f" {name[:10]:<10} │"
        lines.append(row_str)
        row_str2 = "│"
        for palace_id in row:
            palace = palaces.get(str(palace_id), {})
            load = palace.get("load", 0)
            element = palace.get("element", "?")
            row_str2 += f" {element} 负载：{load:.1f} │"
        lines.append(row_str2)
        lines.append("├────────────────┼────────────────┼────────────────┤")
    
    # 移除最后一行的分隔线
    lines.pop()
    lines.append("└────────────────┴────────────────┴────────────────┘")
    
    return "\n".join(lines)


def display_balance(balance_data: Dict[str, Any]) -> str:
    """格式化显示阴阳平衡状态"""
    lines = ["\n【阴阳平衡状态】"]
    
    balance = balance_data.get("balance", {})
    if isinstance(balance, dict):
        for pair, value in balance.items():
            if isinstance(value, (int, float)):
                status = "✅" if value >= 0.7 else "⚠️"
                lines.append(f"  {status} {pair}: {value:.2f}")
    
    if "imbalanced_pairs" in balance_data and balance_data["imbalanced_pairs"]:
        lines.append("\n【失衡告警】")
        for pair in balance_data["imbalanced_pairs"]:
            lines.append(f"  ⚠️ {pair['pair']}: {pair['balance']:.2f}")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # 测试连接
    client = TaijiClient()
    
    print("=== 太极九宫任务管理系统 ===\n")
    
    # 健康检查
    health = client.health_check()
    print(f"服务状态：{health.get('status', 'unknown')}")
    
    # 获取所有宫位
    palaces = client.get_all_palaces()
    print(display_palaces(palaces))
    
    # 获取平衡状态
    balance = client.get_balance_status()
    print(display_balance(balance))
    
    # 获取引擎状态
    status = client.get_taiji_status()
    print(f"\n引擎状态：{json.dumps(status, indent=2, ensure_ascii=False)}")
