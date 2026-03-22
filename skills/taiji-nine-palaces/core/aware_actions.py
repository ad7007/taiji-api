#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太极感知-动作联动

感知后必须触发动作：
- on_time → 执行任务循环
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.task_manager import get_task_manager
from core.perception_action_loop import get_loop


def on_time_action():
    """定时动作：执行任务循环"""
    loop = get_loop()
    result = loop.run_once()
    return result


if __name__ == "__main__":
    result = on_time_action()
    print(f"旋转: {result['decision']['rotation']}")
    print(f"完成: {len(result['results']['completed'])}个")
