"""
太极任务版本系统
任务永不"完成"，只生成版本成果
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

# 任务状态 = 版本号
# v1, v2, v3, ...
# 永远问：还需要继续改进吗？

TASK_STATE_FILE = "/root/taiji-api-v2/state/task_versions.json"


def get_next_version(current_status: str) -> str:
    """获取下一版本号"""
    if current_status == "pending":
        return "v1"
    if current_status == "in_progress":
        return "v1"

    # 已有版本号，递增
    if current_status.startswith("v"):
        try:
            num = int(current_status[1:])
            return f"v{num + 1}"
        except:
            return "v1"

    return "v1"


def is_improvable(status: str) -> bool:
    """任务是否可改进（永远可以）"""
    return True  # 太极系统里，所有任务都可以继续改进


def format_task_status(status: str, version_count: int = 1) -> str:
    """格式化任务状态描述"""
    if status == "pending":
        return "待启动"

    if status == "in_progress":
        return "执行中"

    if status.startswith("v"):
        version_num = status[1:]
        return f"已生成第{version_num}版成果，是否继续改进？"

    return status


class TaskVersionSystem:
    """任务版本系统"""

    def __init__(self):
        self.versions = {}  # task_id -> [v1_result, v2_result, ...]
        self._load()

    def _load(self):
        """加载版本数据"""
        if os.path.exists(TASK_STATE_FILE):
            with open(TASK_STATE_FILE, 'r', encoding='utf-8') as f:
                self.versions = json.load(f)

    def _save(self):
        """保存版本数据"""
        os.makedirs(os.path.dirname(TASK_STATE_FILE), exist_ok=True)
        with open(TASK_STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.versions, f, ensure_ascii=False, indent=2)

    def add_version(self, task_id: str, result: str, improvements: List[str] = None):
        """添加新版本成果"""
        if task_id not in self.versions:
            self.versions[task_id] = []

        version_num = len(self.versions[task_id]) + 1
        self.versions[task_id].append({
            "version": f"v{version_num}",
            "result": result,
            "improvements": improvements or [],
            "timestamp": datetime.now().isoformat()
        })
        self._save()

    def get_versions(self, task_id: str) -> List[Dict]:
        """获取任务所有版本"""
        return self.versions.get(task_id, [])

    def get_latest_version(self, task_id: str) -> Optional[Dict]:
        """获取最新版本"""
        versions = self.versions.get(task_id, [])
        return versions[-1] if versions else None

    def ask_for_improvement(self, task_id: str) -> str:
        """生成改进询问"""
        versions = self.versions.get(task_id, [])
        if not versions:
            return "任务尚未执行"

        latest = versions[-1]
        version_num = latest["version"]

        return f"""
【任务{task_id}】已生成{version_num}版成果

成果摘要：{latest.get("result", "无")[:100]}...

是否继续改进？
- 需要改进 → 输入改进方向
- 暂时满意 → 保持{version_num}版
- 等待反馈 → 暂不处理
"""


# 全局实例
_task_version_system = None


def get_task_version_system() -> TaskVersionSystem:
    global _task_version_system
    if _task_version_system is None:
        _task_version_system = TaskVersionSystem()
    return _task_version_system