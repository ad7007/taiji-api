"""
太极系统内部心跳
不依赖外部触发，自己运行
"""

import threading
import time
from datetime import datetime
from typing import Callable, List
import json
import os

# 心跳间隔（毫秒）
DEFAULT_HEARTBEAT_INTERVAL_MS = 10 * 60 * 1000  # 10分钟

# 心跳状态文件
HEARTBEAT_STATE = "/root/taiji-api-v2/data/heartbeat_state.json"


class TaijiHeartbeat:
    """太极系统心跳"""

    def __init__(self, interval_ms: int = DEFAULT_HEARTBEAT_INTERVAL_MS):
        self.interval_ms = interval_ms
        self.running = False
        self.thread = None
        self.callbacks: List[Callable] = []
        self.state = self._load_state()

    def _load_state(self) -> dict:
        """加载心跳状态"""
        if os.path.exists(HEARTBEAT_STATE):
            try:
                with open(HEARTBEAT_STATE, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "last_heartbeat": None,
            "total_heartbeats": 0,
            "actions_taken": []
        }

    def _save_state(self):
        """保存心跳状态"""
        os.makedirs(os.path.dirname(HEARTBEAT_STATE), exist_ok=True)
        with open(HEARTBEAT_STATE, 'w') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)

    def register_callback(self, callback: Callable):
        """注册心跳回调"""
        self.callbacks.append(callback)

    def start(self):
        """启动心跳"""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self.thread.start()
        print(f"[太极心跳] 已启动，间隔 {self.interval_ms / 1000 / 60:.0f} 分钟")

    def stop(self):
        """停止心跳"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)

    def _heartbeat_loop(self):
        """心跳循环"""
        while self.running:
            time.sleep(self.interval_ms / 1000)
            self._execute_heartbeat()

    def _execute_heartbeat(self):
        """执行心跳"""
        now = datetime.now()
        self.state["last_heartbeat"] = now.isoformat()
        self.state["total_heartbeats"] += 1

        actions = []

        # 1. 检查任务系统状态
        try:
            action = self._check_tasks()
            if action:
                actions.append(action)
        except Exception as e:
            actions.append(f"任务检查失败: {e}")

        # 2. 检查48端状态
        try:
            action = self._check_hexagram()
            if action:
                actions.append(action)
        except Exception as e:
            actions.append(f"六爻检查失败: {e}")

        # 3. 检查智能体状态
        try:
            action = self._check_agents()
            if action:
                actions.append(action)
        except Exception as e:
            actions.append(f"智能体检查失败: {e}")

        # 4. 执行注册的回调
        for callback in self.callbacks:
            try:
                result = callback()
                if result:
                    actions.append(result)
            except Exception as e:
                actions.append(f"回调失败: {e}")

        self.state["actions_taken"] = actions[-10:]  # 保留最近10条
        self._save_state()

        print(f"[太极心跳] {now.isoformat()} - {len(actions)}个动作")

    def _check_tasks(self) -> str:
        """检查任务状态"""
        from core.task_manager import TaijiTaskManager

        tm = TaijiTaskManager()
        tm.load()

        alive = sum(1 for q in tm.queues.values() if q.is_alive())
        total = len(tm.queues)

        if alive < total:
            return f"警告: {alive}/{total}宫存活"
        return None

    def _check_hexagram(self) -> str:
        """检查48端状态"""
        from core.palace_hexagrams import get_hexagram_system

        system = get_hexagram_system()
        balance = system.get_system_balance()

        if balance < -0.3:
            return f"系统偏阴({balance:.2f})，建议反转修炼"
        elif balance > 0.3:
            return f"系统偏阳({balance:.2f})，可以正转创造"
        return None

    def _check_agents(self) -> str:
        """检查外部智能体状态"""
        agents_file = "/root/taiji-api-v2/data/registered_agents.json"
        if not os.path.exists(agents_file):
            return None

        with open(agents_file, 'r') as f:
            agents = json.load(f)

        idle = sum(1 for a in agents.values() if a.get("status") == "idle")
        busy = sum(1 for a in agents.values() if a.get("status") == "busy")

        if idle > 0:
            return f"{idle}个智能体空闲可分配任务"
        return None

    def get_status(self) -> dict:
        """获取心跳状态"""
        return {
            "running": self.running,
            "interval_ms": self.interval_ms,
            "last_heartbeat": self.state.get("last_heartbeat"),
            "total_heartbeats": self.state.get("total_heartbeats", 0),
            "recent_actions": self.state.get("actions_taken", [])
        }


# 全局实例
_heartbeat: TaijiHeartbeat = None


def get_heartbeat() -> TaijiHeartbeat:
    """获取全局心跳实例"""
    global _heartbeat
    if _heartbeat is None:
        _heartbeat = TaijiHeartbeat()
    return _heartbeat


def start_heartbeat(interval_ms: int = None):
    """启动心跳"""
    hb = get_heartbeat()
    if interval_ms:
        hb.interval_ms = interval_ms
    hb.start()
    return hb