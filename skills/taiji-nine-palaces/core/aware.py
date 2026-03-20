"""
太极 Aware 自主感知系统

替代 Heartbeat，实现事件驱动感知
包含 6 种触发器：
- on_message: 消息触发
- on_task: 任务触发
- on_time: 定时触发
- on_event: 事件触发
- on_state: 状态变化触发
- on_external: 外部系统触发
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Any, Optional
from datetime import datetime
import threading
import time


# ==================== 触发器类型 ====================

class TriggerType(Enum):
    """触发器类型"""
    ON_MESSAGE = "on_message"
    ON_TASK = "on_task"
    ON_TIME = "on_time"
    ON_EVENT = "on_event"
    ON_STATE = "on_state"
    ON_EXTERNAL = "on_external"


class TriggerPriority(Enum):
    """触发器优先级"""
    CRITICAL = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3


# ==================== 触发器定义 ====================

@dataclass
class Trigger:
    """触发器定义"""
    trigger_id: str
    trigger_type: TriggerType
    action: str
    priority: TriggerPriority = TriggerPriority.MEDIUM
    enabled: bool = True
    source: Optional[str] = None
    event: Optional[str] = None
    interval: Optional[int] = None
    watch: Optional[str] = None
    threshold: Optional[float] = None


@dataclass
class TriggerEvent:
    """触发事件"""
    timestamp: str
    trigger_type: TriggerType
    trigger_id: str
    source: Optional[str]
    data: Dict[str, Any]
    processed: bool = False
    result: Optional[str] = None


# ==================== 触发器注册表 ====================

class TriggerRegistry:
    """触发器注册表"""
    
    def __init__(self):
        self.triggers: Dict[str, Trigger] = {}
        self.handlers: Dict[str, Callable] = {}
    
    def register(self, trigger: Trigger, handler: Callable):
        self.triggers[trigger.trigger_id] = trigger
        self.handlers[trigger.trigger_id] = handler
    
    def get_triggers_by_type(self, trigger_type: TriggerType) -> List[Trigger]:
        return [t for t in self.triggers.values() 
                if t.trigger_type == trigger_type and t.enabled]


# ==================== Aware 系统 ====================

class AwareSystem:
    """Aware 自主感知系统"""
    
    def __init__(self):
        self.registry = TriggerRegistry()
        self.state_cache: Dict[str, Any] = {}
        self.event_queue: List[TriggerEvent] = []
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self.last_fired: Dict[str, float] = {}
    
    def start(self, scan_interval: int = 15):
        """启动系统"""
        self._running = True
        self._thread = threading.Thread(target=self._scan_loop, args=(scan_interval,))
        self._thread.daemon = True
        self._thread.start()
    
    def stop(self):
        """停止系统"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
    
    def _scan_loop(self, interval: int):
        """扫描循环"""
        while self._running:
            self._check_time_triggers()
            time.sleep(interval)
    
    def _check_time_triggers(self):
        """检查定时触发器"""
        triggers = self.registry.get_triggers_by_type(TriggerType.ON_TIME)
        now = time.time()
        
        for trigger in triggers:
            if trigger.interval:
                last = self.last_fired.get(trigger.trigger_id, 0)
                if now - last >= trigger.interval:
                    self.last_fired[trigger.trigger_id] = now
                    self._execute(trigger, {})
    
    def _execute(self, trigger: Trigger, data: Dict[str, Any]):
        """执行触发器"""
        handler = self.registry.handlers.get(trigger.trigger_id)
        if handler:
            try:
                return handler(data)
            except Exception as e:
                print(f"Trigger {trigger.trigger_id} failed: {e}")
        return None
    
    # ==================== 6 种触发器接口 ====================
    
    def register_trigger(self, trigger: Trigger, handler: Callable):
        """注册触发器"""
        self.registry.register(trigger, handler)
    
    def on_message(self, source: str, message: Dict[str, Any]) -> Any:
        """消息触发"""
        triggers = self.registry.get_triggers_by_type(TriggerType.ON_MESSAGE)
        for trigger in triggers:
            if trigger.source and trigger.source != source:
                continue
            return self._execute(trigger, {"source": source, "message": message})
    
    def on_task_event(self, event_name: str, task_data: Dict[str, Any]) -> Any:
        """任务触发"""
        triggers = self.registry.get_triggers_by_type(TriggerType.ON_TASK)
        for trigger in triggers:
            if trigger.event and trigger.event != event_name:
                continue
            return self._execute(trigger, {"event": event_name, "task": task_data})
    
    def on_time_trigger(self) -> Any:
        """定时触发（内部调用）"""
        pass  # 由 _scan_loop 处理
    
    def on_event(self, event_name: str, event_data: Dict[str, Any]) -> Any:
        """事件触发"""
        triggers = self.registry.get_triggers_by_type(TriggerType.ON_EVENT)
        for trigger in triggers:
            if trigger.event and trigger.event != event_name:
                continue
            return self._execute(trigger, {"event": event_name, "data": event_data})
    
    def on_state_change(self, key: str, value: Any) -> Any:
        """状态变化触发"""
        old_value = self.state_cache.get(key)
        self.state_cache[key] = value
        
        if old_value != value:
            triggers = self.registry.get_triggers_by_type(TriggerType.ON_STATE)
            for trigger in triggers:
                if trigger.watch and trigger.watch != key:
                    continue
                if trigger.threshold is not None:
                    if isinstance(value, (int, float)) and value > trigger.threshold:
                        return self._execute(trigger, {
                            "key": key, 
                            "old": old_value, 
                            "new": value,
                            "threshold": trigger.threshold
                        })
                else:
                    return self._execute(trigger, {"key": key, "old": old_value, "new": value})
    
    def on_external(self, endpoint: str, request_data: Dict[str, Any]) -> Any:
        """外部触发"""
        triggers = self.registry.get_triggers_by_type(TriggerType.ON_EXTERNAL)
        for trigger in triggers:
            # 可以用正则匹配 endpoint
            return self._execute(trigger, {"endpoint": endpoint, "data": request_data})
    
    def get_state(self, key: str) -> Any:
        """获取状态"""
        return self.state_cache.get(key)


# ==================== 默认触发器配置 ====================

def setup_default_triggers(aware: AwareSystem, handlers: Dict[str, Callable]):
    """
    设置默认触发器
    
    handlers: {
        "parse_intent": 处理余总指令,
        "auto_group": 自动组队,
        "check_balance": 检查平衡,
        "daily_report": 每日汇报,
        "notify_alert": 告警通知,
    }
    """
    
    # on_message: 余总指令（最高优先级）
    aware.register_trigger(
        Trigger(
            trigger_id="msg_from_yuzong",
            trigger_type=TriggerType.ON_MESSAGE,
            source="feishu:direct:yuzong",
            action="parse_intent",
            priority=TriggerPriority.CRITICAL
        ),
        handlers.get("parse_intent", lambda x: x)
    )
    
    # on_task: 任务创建
    aware.register_trigger(
        Trigger(
            trigger_id="task_created",
            trigger_type=TriggerType.ON_TASK,
            event="task_created",
            action="auto_group",
            priority=TriggerPriority.HIGH
        ),
        handlers.get("auto_group", lambda x: x)
    )
    
    # on_task: 任务完成
    aware.register_trigger(
        Trigger(
            trigger_id="task_completed",
            trigger_type=TriggerType.ON_TASK,
            event="task_completed",
            action="green_light_check",
            priority=TriggerPriority.HIGH
        ),
        handlers.get("green_light", lambda x: x)
    )
    
    # on_time: 平衡检查（每5分钟）
    aware.register_trigger(
        Trigger(
            trigger_id="balance_check",
            trigger_type=TriggerType.ON_TIME,
            interval=300,
            action="check_balance",
            priority=TriggerPriority.LOW
        ),
        handlers.get("check_balance", lambda x: x)
    )
    
    # on_time: 每日汇报
    aware.register_trigger(
        Trigger(
            trigger_id="daily_report",
            trigger_type=TriggerType.ON_TIME,
            interval=86400,  # 24小时
            action="daily_report",
            priority=TriggerPriority.LOW
        ),
        handlers.get("daily_report", lambda x: x)
    )
    
    # on_event: 系统告警
    aware.register_trigger(
        Trigger(
            trigger_id="system_alert",
            trigger_type=TriggerType.ON_EVENT,
            event="system_alert",
            action="notify_alert",
            priority=TriggerPriority.HIGH
        ),
        handlers.get("notify_alert", lambda x: x)
    )
    
    # on_state: 宫位过载
    aware.register_trigger(
        Trigger(
            trigger_id="palace_overload",
            trigger_type=TriggerType.ON_STATE,
            watch="palace_load",
            threshold=0.8,
            action="rebalance",
            priority=TriggerPriority.MEDIUM
        ),
        handlers.get("rebalance", lambda x: x)
    )
    
    # on_state: 阴阳失衡
    aware.register_trigger(
        Trigger(
            trigger_id="yinyang_imbalance",
            trigger_type=TriggerType.ON_STATE,
            watch="yinyang_balance",
            threshold=0.3,
            action="rebalance",
            priority=TriggerPriority.MEDIUM
        ),
        handlers.get("rebalance", lambda x: x)
    )


# ==================== 示例用法 ====================

if __name__ == "__main__":
    # 创建 Aware 系统
    aware = AwareSystem()
    
    # 定义处理函数
    handlers = {
        "parse_intent": lambda data: print(f"[CRITICAL] 解析余总指令: {data}"),
        "auto_group": lambda data: print(f"[HIGH] 自动组队: {data}"),
        "check_balance": lambda data: print(f"[LOW] 检查平衡: {data}"),
        "daily_report": lambda data: print(f"[LOW] 每日汇报: {data}"),
        "notify_alert": lambda data: print(f"[HIGH] 系统告警: {data}"),
        "rebalance": lambda data: print(f"[MEDIUM] 重新平衡: {data}"),
    }
    
    # 设置默认触发器
    setup_default_triggers(aware, handlers)
    
    # 启动系统
    print("启动 Aware 系统...")
    aware.start(scan_interval=5)
    
    # 模拟事件
    print("\n--- 模拟消息触发 ---")
    aware.on_message("feishu:direct:yuzong", {"text": "帮我下载视频"})
    
    print("\n--- 模拟任务触发 ---")
    aware.on_task_event("task_created", {"task_id": "001", "type": "download"})
    
    print("\n--- 模拟状态触发 ---")
    aware.on_state_change("palace_load", 0.85)
    
    print("\n--- 模拟事件触发 ---")
    aware.on_event("system_alert", {"level": "warning", "message": "磁盘空间不足"})
    
    # 运行一段时间观察定时触发
    print("\n--- 等待定时触发（5秒后检查平衡）...")
    time.sleep(6)
    
    # 停止系统
    aware.stop()
    print("\nAware 系统已停止")