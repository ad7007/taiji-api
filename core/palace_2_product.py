#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2-产品宫子 OPENCLAW 模板
Palace 2 - Product Management Sub-OPENCLAW Template
"""

from core.sub_openclaw_base import SubOpenClawBase
from pathlib import Path


class Palace2Product(SubOpenClawBase):
    """产品管理宫模板"""
    
    def __init__(self):
        super().__init__(palace_position=2, template_name="产品管理")
    
    def install(self, target_dir: Path) -> bool:
        """安装到目标目录"""
        print(f"📥 正在安装 2-产品宫模板到 {target_dir}")
        target_dir.mkdir(parents=True, exist_ok=True)
        return True
    
    def validate(self) -> bool:
        """验证模板"""
        print("✅ 验证 2-产品宫模板配置")
        return self.config_dir.exists()
