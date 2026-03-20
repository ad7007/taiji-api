"""
48端状态持久化
定期保存和恢复六爻状态，支持重启后恢复
"""

import json
import os
from datetime import datetime
from typing import Dict
import threading
import time

# 持久化文件
YAO_STATE_FILE = "/root/taiji-api-v2/data/yao_state_persist.json"

# 自动保存间隔（秒）
AUTO_SAVE_INTERVAL = 60


def save_yao_state(hexagram_system) -> bool:
    """保存48端状态到文件"""
    try:
        state = {
            "palaces": {},
            "milo_state": hexagram_system.get_milo_state(),
            "rotation": hexagram_system.get_rotation_decision(),
            "timestamp": datetime.now().isoformat()
        }

        for palace_id, palace in hexagram_system.palaces.items():
            state["palaces"][str(palace_id)] = {
                "state": palace.get_state(),
                "balance": palace.get_balance(),
                "yang_count": palace.get_yang_count(),
                "yin_count": palace.get_yin_count(),
                "yaos": {}
            }
            for level, yao in palace.yaos.items():
                state["palaces"][str(palace_id)]["yaos"][str(level)] = {
                    "state": yao.state.value,
                    "current_level": yao.current_level,
                    "current_signal": yao.current_signal,
                    "last_updated": yao.last_updated.isoformat() if yao.last_updated else None
                }

        os.makedirs(os.path.dirname(YAO_STATE_FILE), exist_ok=True)
        with open(YAO_STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

        return True
    except Exception as e:
        print(f"保存48端状态失败: {e}")
        return False


def load_yao_state(hexagram_system) -> bool:
    """从文件恢复48端状态"""
    try:
        if not os.path.exists(YAO_STATE_FILE):
            return False

        with open(YAO_STATE_FILE, 'r', encoding='utf-8') as f:
            state = json.load(f)

        for palace_id, palace_data in state.get("palaces", {}).items():
            palace_id = int(palace_id)
            if palace_id in hexagram_system.palaces:
                palace = hexagram_system.palaces[palace_id]
                for level, yao_data in palace_data.get("yaos", {}).items():
                    level = int(level)
                    if level in palace.yaos:
                        yao = palace.yaos[level]
                        yao.state = YaoState(yao_data["state"])
                        yao.current_level = yao_data.get("current_level", 1)
                        yao.current_signal = yao_data.get("current_signal")
                        # last_updated 不恢复，使用当前时间
                        yao.last_updated = datetime.now()

        return True
    except Exception as e:
        print(f"恢复48端状态失败: {e}")
        return False


class YaoStatePersistence:
    """48端状态持久化管理器"""

    def __init__(self, hexagram_system):
        self.hexagram_system = hexagram_system
        self._running = False
        self._thread = None

    def start_auto_save(self):
        """启动自动保存"""
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(target=self._auto_save_loop, daemon=True)
        self._thread.start()

    def stop_auto_save(self):
        """停止自动保存"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)

    def _auto_save_loop(self):
        """自动保存循环"""
        while self._running:
            time.sleep(AUTO_SAVE_INTERVAL)
            save_yao_state(self.hexagram_system)

    def save(self) -> bool:
        """手动保存"""
        return save_yao_state(self.hexagram_system)

    def load(self) -> bool:
        """手动加载"""
        return load_yao_state(self.hexagram_system)

    def get_state_summary(self) -> Dict:
        """获取状态摘要"""
        if os.path.exists(YAO_STATE_FILE):
            with open(YAO_STATE_FILE, 'r', encoding='utf-8') as f:
                state = json.load(f)
            return {
                "file_exists": True,
                "last_saved": state.get("timestamp"),
                "milo_state": state.get("milo_state", {}).get("form"),
                "rotation": state.get("rotation", {}).get("direction")
            }
        return {"file_exists": False}


# 需要导入YaoState
from core.palace_hexagrams import YaoState