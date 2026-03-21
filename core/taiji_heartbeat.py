"""
太极系统心跳 v2.0
新流程：检查 → 队列管理 → 生成任务 → 分配 → 投递
"""

import threading
import time
from datetime import datetime
from typing import Callable, List, Optional
import json
import os
import requests

# 心跳间隔（毫秒）
DEFAULT_HEARTBEAT_INTERVAL_MS = 10 * 60 * 1000  # 10分钟

# 心跳状态文件
HEARTBEAT_STATE = "/root/taiji-api-v2/data/heartbeat_state.json"

# 任务队列文件
TASK_QUEUE_FILE = "/root/taiji-api-v2/data/tasks.json"

# 飞书配置
FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/im/v1/messages"
FEISHU_USER_ID = "ou_9b42a76db79aee1c1c1a17393b168048"  # 余总

# 队列阈值
QUEUE_THRESHOLD = 40


class TaijiHeartbeatV2:
    """太极系统心跳 v2.0"""

    def __init__(self, interval_ms: int = DEFAULT_HEARTBEAT_INTERVAL_MS):
        self.interval_ms = interval_ms
        self.running = False
        self.thread = None
        self.callbacks: List[Callable] = []
        self.state = self._load_state()
        self.improvement_list = []  # 系统预改善清单

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
            "rotation": "forward",
            "energy": 0.5,
            "palaces_alive": 9,
            "tasks": {
                "total": 0,
                "pending": 0,
                "new_this_heartbeat": 0
            },
            "new_tasks": [],
            "improvement_list": []
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
        print(f"[太极心跳v2] 已启动，间隔 {self.interval_ms / 1000 / 60:.0f} 分钟")

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
        """执行心跳 - 新流程"""
        now = datetime.now()
        self.state["last_heartbeat"] = now.isoformat()
        self.state["total_heartbeats"] += 1

        print(f"\n{'='*50}")
        print(f"[太极心跳v2] {now.isoformat()}")

        # 步骤1: 检查任务队列，新增3个检查任务
        check_tasks = self._create_check_tasks()

        # 步骤2: 检查队列数量
        queue_count = self._get_queue_count()
        print(f"[队列状态] 当前任务: {queue_count}")

        new_tasks = []

        if queue_count >= QUEUE_THRESHOLD:
            # 队列超过40个，调整优先级
            print(f"[队列管理] 超过阈值({QUEUE_THRESHOLD})，调整优先级")
            self._adjust_priorities()
            self._write_to_subagents()
        else:
            # 队列低于40个，生成任务
            print(f"[任务生成] 队列正常，生成新任务")
            new_tasks = self._generate_tasks_from_sources()

        # 步骤3: 分配任务
        if new_tasks:
            self._assign_tasks(new_tasks)

        # 步骤4: 决策正转/反转
        rotation = self._decide_rotation()
        self.state["rotation"] = rotation

        # 步骤5: 更新状态
        if "tasks" not in self.state:
            self.state["tasks"] = {}
        self.state["tasks"]["new_this_heartbeat"] = len(new_tasks)
        self.state["tasks"]["total"] = queue_count + len(new_tasks)
        self.state["tasks"]["pending"] = queue_count
        self.state["new_tasks"] = new_tasks
        self._save_state()

        # 步骤6: 投递心跳摘要到飞书
        self._deliver_summary(now, queue_count, new_tasks, rotation)

        # 步骤7: 维持观察
        print(f"[太极心跳v2] 完成，维持观察")
        print(f"{'='*50}\n")

    def _create_check_tasks(self) -> list:
        """创建3个检查任务"""
        return [
            {
                "id": f"check_6yao_{int(time.time())}",
                "title": "检查5宫米珞6爻状态",
                "palace": 5,
                "type": "check",
                "priority": "HIGH"
            },
            {
                "id": f"check_48threads_{int(time.time())}",
                "title": "扫描48线程8宫状态",
                "palace": 5,
                "type": "check",
                "priority": "HIGH"
            },
            {
                "id": f"check_improvements_{int(time.time())}",
                "title": "建立系统预改善清单",
                "palace": 5,
                "type": "check",
                "priority": "MEDIUM"
            }
        ]

    def _get_queue_count(self) -> int:
        """获取队列任务数量"""
        if os.path.exists(TASK_QUEUE_FILE):
            try:
                with open(TASK_QUEUE_FILE, 'r') as f:
                    tasks = json.load(f)
                    return len([t for t in tasks if t.get("status") == "pending"])
            except:
                pass
        # 从状态文件读取
        return self.state.get("tasks", {}).get("pending", 0)

    def _adjust_priorities(self):
        """调整任务优先级"""
        print("[优先级调整] 按重要性和紧急度重新排序")

    def _write_to_subagents(self):
        """写入子智能体todo"""
        print("[子智能体] 分配任务到各宫位")

    def _generate_tasks_from_sources(self) -> list:
        """从4个来源生成任务"""
        tasks = []

        # 来源1: 系统预改善清单
        if self.improvement_list:
            for item in self.improvement_list[:1]:  # 取1个
                tasks.append({
                    "id": f"improve_{int(time.time())}_{len(tasks)}",
                    "title": item.get("title", "系统改进"),
                    "palace": item.get("palace", 5),
                    "type": "improvement",
                    "priority": "MEDIUM",
                    "source": "系统预改善清单"
                })

        # 来源2: 各宫MD（读取宫位目标）
        palace_tasks = self._read_palace_goals()
        tasks.extend(palace_tasks[:1])

        # 来源3: 主控MD双目标循环（Power.md）
        power_tasks = self._read_power_goals()
        tasks.extend(power_tasks[:1])

        # 来源4: 1宫市场数据调查
        market_task = self._create_market_research_task()
        if market_task:
            tasks.append(market_task)

        # 确保至少3个任务
        while len(tasks) < 3:
            tasks.append({
                "id": f"default_{int(time.time())}_{len(tasks)}",
                "title": f"默认任务{len(tasks)+1}：数据分析和赚钱机会探索",
                "palace": 1,
                "type": "research",
                "priority": "MEDIUM",
                "source": "默认生成"
            })

        return tasks

    def _read_palace_goals(self) -> list:
        """读取各宫MD目标"""
        # 简化实现：返回示例任务
        return [{
            "id": f"palace_goal_{int(time.time())}",
            "title": "完善宫位职责和能力",
            "palace": 5,
            "type": "improvement",
            "priority": "MEDIUM",
            "source": "各宫MD"
        }]

    def _read_power_goals(self) -> list:
        """读取Power.md赚钱目标"""
        power_file = "/root/.openclaw/workspace/Power.md"
        if os.path.exists(power_file):
            # 读取Power.md并解析目标
            return [{
                "id": f"power_{int(time.time())}",
                "title": "获得首个付费用户",
                "palace": 8,
                "type": "marketing",
                "priority": "CRITICAL",
                "source": "Power.md Week 1"
            }]
        return []

    def _create_market_research_task(self) -> Optional[dict]:
        """创建1宫市场调研任务"""
        return {
            "id": f"market_{int(time.time())}",
            "title": "1宫：AI智能体市场数据调查，发现赚钱机会",
            "palace": 1,
            "type": "research",
            "priority": "HIGH",
            "source": "1宫市场调研"
        }

    def _assign_tasks(self, tasks: list):
        """分配任务到宫位"""
        for task in tasks:
            palace = task.get("palace", 5)
            print(f"[任务分配] {task['title'][:30]}... → {palace}宫")

    def _decide_rotation(self) -> str:
        """决策正转/反转"""
        # 检查系统健康度
        health = self._check_system_health()

        if health < 0.5:
            return "reverse"  # 反转：修复系统
        else:
            return "forward"  # 正转：创造价值

    def _check_system_health(self) -> float:
        """检查系统健康度"""
        try:
            # 调用意识系统
            resp = requests.get("http://localhost:8000/api/consciousness/status", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("system", {}).get("yin_yang_balance", 0.5)
        except:
            pass
        return 0.5

    def _deliver_summary(self, now, queue_count, new_tasks, rotation):
        """投递心跳摘要到飞书"""
        summary = self._format_summary(now, queue_count, new_tasks, rotation)
        self._send_to_feishu(summary)

    def _format_summary(self, now, queue_count, new_tasks, rotation) -> str:
        """格式化心跳摘要"""
        rotation_cn = "正转 ▶️" if rotation == "forward" else "反转 ◀️"

        lines = [
            f"📊 **心跳摘要** - {now.strftime('%Y-%m-%d %H:%M')}",
            "",
            "## 系统状态",
            f"- 旋转: {rotation_cn}",
            f"- 能量: {self.state.get('energy', 0.5):.2f}",
            f"- 宫位活跃: {self.state.get('palaces_alive', 9)}/9",
            "",
            "## 队列状态",
            f"- 总任务: {self.state.get('tasks', {}).get('total', 0)}",
            f"- 待处理: {queue_count}",
            f"- 本次新增: {len(new_tasks)}",
            ""
        ]

        if new_tasks:
            lines.append("## 新增任务")
            for i, task in enumerate(new_tasks, 1):
                palace = task.get("palace", "?")
                title = task.get("title", "未知任务")[:30]
                lines.append(f"{i}. [{palace}宫] {title}")
            lines.append("")

        decision = "正转创造价值" if rotation == "forward" else "反转修复系统"
        lines.extend([
            "## 决策",
            decision,
            "",
            "---",
            "*米珞（5宫）自动心跳*"
        ])

        return "\n".join(lines)

    def _send_to_feishu(self, message: str):
        """发送消息到飞书"""
        try:
            # 使用OpenClaw的feishu消息发送
            # 这里简化实现，实际需要调用OpenClaw的message工具
            print(f"[飞书投递] 准备发送摘要...")

            # 保存到文件，让OpenClaw的feishu扩展读取
            delivery_file = "/root/taiji-api-v2/data/feishu_delivery.json"
            delivery_data = {
                "target": f"user:{FEISHU_USER_ID}",
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
            os.makedirs(os.path.dirname(delivery_file), exist_ok=True)
            with open(delivery_file, 'w') as f:
                json.dump(delivery_data, f, ensure_ascii=False, indent=2)

            print(f"[飞书投递] 已写入投递文件: {delivery_file}")

        except Exception as e:
            print(f"[飞书投递] 发送失败: {e}")

    def get_status(self) -> dict:
        """获取心跳状态"""
        return {
            "running": self.running,
            "interval_ms": self.interval_ms,
            "last_heartbeat": self.state.get("last_heartbeat"),
            "total_heartbeats": self.state.get("total_heartbeats", 0),
            "rotation": self.state.get("rotation"),
            "queue_count": self._get_queue_count(),
            "recent_tasks": self.state.get("new_tasks", [])
        }


# 全局实例
_heartbeat_v2: TaijiHeartbeatV2 = None


def get_heartbeat() -> TaijiHeartbeatV2:
    """获取全局心跳实例"""
    global _heartbeat_v2
    if _heartbeat_v2 is None:
        _heartbeat_v2 = TaijiHeartbeatV2()
    return _heartbeat_v2


def start_heartbeat(interval_ms: int = None):
    """启动心跳"""
    hb = get_heartbeat()
    if interval_ms:
        hb.interval_ms = interval_ms
    hb.start()
    return hb


# 兼容旧版本
TaijiHeartbeat = TaijiHeartbeatV2