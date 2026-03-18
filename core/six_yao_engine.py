#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
6 爻变化引擎
Six Yao Changes Engine

实现每个宫位的 6 爻变化逻辑：
- 初爻：基础能力激活/失位
- 二爻：技能插件加载/卸载
- 三爻：外部接口连接/断开
- 四爻：数据采集配置
- 五爻：任务执行策略
- 上爻：成果输出格式

爻变规则：
- 当位：阳爻在阳位（1,3,5），阴爻在阴位（2,4,6）
- 相应：初爻与四爻、二爻与五爻、三爻与上爻相互呼应
- 承乘：相邻爻位的关系（承=下托上，乘=上压下）
"""

from typing import Dict, List, Any, Optional
from enum import Enum
from datetime import datetime


class YaoType(Enum):
    """爻的类型"""
    YANG = "yang"      # 阳爻 —
    YIN = "yin"        # 阴爻 - -


class SixYaoEngine:
    """
    6 爻变化引擎
    
    每个宫位都有独立的 6 爻系统
    """
    
    def __init__(self, palace_position: int, palace_name: str):
        self.palace_position = palace_position
        self.palace_name = palace_name
        
        # 初始化 6 爻（从下到上：初、二、三、四、五、上）
        self.yao_lines: List[Dict[str, Any]] = [
            {"position": 1, "name": "初爻", "type": YaoType.YANG, "status": "active", "description": "基础能力"},
            {"position": 2, "name": "二爻", "type": YaoType.YIN, "status": "inactive", "description": "技能插件"},
            {"position": 3, "name": "三爻", "type": YaoType.YANG, "status": "inactive", "description": "外部接口"},
            {"position": 4, "name": "四爻", "type": YaoType.YIN, "status": "active", "description": "数据采集"},
            {"position": 5, "name": "五爻", "type": YaoType.YANG, "status": "active", "description": "任务执行"},
            {"position": 6, "name": "上爻", "type": YaoType.YIN, "status": "active", "description": "成果输出"},
        ]
        
        # 技能插件库（二爻）
        self.available_plugins = self._load_skill_plugins()
        
        # 外部接口库（三爻）
        self.available_interfaces = self._load_external_interfaces()
    
    def _load_skill_plugins(self) -> List[Dict]:
        """加载可用的技能插件"""
        return [
            {"name": "数据爬虫", "category": "采集", "version": "1.0"},
            {"name": "需求分析", "category": "产品", "version": "1.0"},
            {"name": "代码生成", "category": "技术", "version": "1.0"},
            {"name": "测试自动化", "category": "质量", "version": "1.0"},
            {"name": "文档生成", "category": "生态", "version": "1.0"},
        ]
    
    def _load_external_interfaces(self) -> List[Dict]:
        """加载可用的外部接口"""
        return [
            {"name": "GitHub API", "type": "REST", "auth": "OAuth2"},
            {"name": "Slack Bot", "type": "Webhook", "auth": "Token"},
            {"name": "Database", "type": "SQL", "auth": "Password"},
            {"name": "Cloud Storage", "type": "OSS", "auth": "Key"},
        ]
    
    def get_yao_status(self, position: int) -> Dict[str, Any]:
        """获取指定爻位的状态"""
        if 1 <= position <= 6:
            yao = self.yao_lines[position - 1]
            return {
                "position": yao["position"],
                "name": yao["name"],
                "type": yao["type"].value,
                "status": yao["status"],
                "description": yao["description"]
            }
        return {}
    
    def change_yao(self, position: int, new_type: YaoType) -> bool:
        """
        改变爻的类型（爻变）
        
        Args:
            position: 爻位 (1-6)
            new_type: 新的爻类型（阳/阴）
            
        Returns:
            是否成功改变
        """
        if 1 <= position <= 6:
            old_type = self.yao_lines[position - 1]["type"]
            self.yao_lines[position - 1]["type"] = new_type
            
            print(f"🔄 {self.palace_name}-{self.yao_lines[position-1]['name']}: "
                  f"{old_type.value} → {new_type.value}")
            return True
        return False
    
    def activate_yao(self, position: int, status: str = "active") -> bool:
        """激活或停用爻位"""
        if 1 <= position <= 6:
            self.yao_lines[position - 1]["status"] = status
            yao_name = self.yao_lines[position - 1]["name"]
            print(f"{'✅' if status == 'active' else '⏸️'} {self.palace_name}-{yao_name}: {status}")
            return True
        return False
    
    def load_plugin(self, plugin_name: str) -> bool:
        """
        加载技能插件（二爻能力）
        
        只有二爻为阳爻且激活时才能加载
        """
        er_yao = self.get_yao_status(2)
        
        if er_yao["type"] != YaoType.YANG.value or er_yao["status"] != "active":
            print(f"⚠️ {self.palace_name}二爻未就绪，无法加载插件：{plugin_name}")
            return False
        
        # 查找插件
        plugin = next((p for p in self.available_plugins if p["name"] == plugin_name), None)
        
        if plugin:
            print(f"✅ {self.palace_name} 加载技能插件：{plugin_name}")
            return True
        else:
            print(f"❌ 未找到插件：{plugin_name}")
            return False
    
    def connect_interface(self, interface_name: str) -> bool:
        """
        连接外部接口（三爻能力）
        
        只有三爻为阳爻且激活时才能连接
        """
        san_yao = self.get_yao_status(3)
        
        if san_yao["type"] != YaoType.YANG.value or san_yao["status"] != "active":
            print(f"⚠️ {self.palace_name}三爻未就绪，无法连接接口：{interface_name}")
            return False
        
        interface = next((i for i in self.available_interfaces if i["name"] == interface_name), None)
        
        if interface:
            print(f"✅ {self.palace_name} 连接外部接口：{interface_name}")
            return True
        return False
    
    def check_correspondence(self) -> Dict[str, bool]:
        """
        检查爻位之间的相应关系
        
        相应规则：
        - 初爻 (1) ↔ 四爻 (4)
        - 二爻 (2) ↔ 五爻 (5)
        - 三爻 (3) ↔ 上爻 (6)
        
        一阴一阳为"有应"（吉），同阴或同阳为"无应"（凶）
        """
        correspondence = {}
        
        pairs = [(1, 4), (2, 5), (3, 6)]
        for pos1, pos2 in pairs:
            yao1 = self.get_yao_status(pos1)
            yao2 = self.get_yao_status(pos2)
            
            has_response = yao1["type"] != yao2["type"]
            key = f"{self.yao_lines[pos1-1]['name']}↔{self.yao_lines[pos2-1]['name']}"
            correspondence[key] = has_response
            
            status = "✅ 有应 (吉)" if has_response else "⚠️ 无应 (凶)"
            print(f"   {self.palace_name}-{key}: {status}")
        
        return correspondence
    
    def get_hexagram(self) -> str:
        """
        获取当前卦象
            
        Returns:
            6 爻组成的卦象字符串（从下到上）
        """
        hexagram = ""
        for yao in self.yao_lines:
            if yao["type"] == YaoType.YANG:
                hexagram += "—"    # 阳爻
            else:
                hexagram += "- -"  # 阴爻
            if yao["position"] < 6:
                hexagram += "\n"
        
        return hexagram
    
    def get_full_status(self) -> Dict[str, Any]:
        """获取完整的 6 爻状态报告"""
        return {
            "palace": self.palace_name,
            "position": self.palace_position,
            "yao_lines": [self.get_yao_status(i) for i in range(1, 7)],
            "correspondence": self.check_correspondence(),
            "hexagram": self.get_hexagram(),
            "timestamp": datetime.now().isoformat()
        }


def demo_six_yao():
    """演示 6 爻引擎"""
    print("="*60)
    print("6 爻变化引擎演示".center(60))
    print("="*60)
    
    # 创建技术宫（位置 3）的 6 爻引擎
    tech_palace = SixYaoEngine(palace_position=3, palace_name="技术宫")
    
    print("\n【初始状态】")
    status = tech_palace.get_full_status()
    print(f"宫位：{status['palace']}")
    print(f"卦象:")
    print(status['hexagram'])
    
    print("\n【爻变演示】")
    # 激活二爻（技能插件）
    tech_palace.activate_yao(2, "active")
    tech_palace.change_yao(2, YaoType.YANG)
    
    # 激活三爻（外部接口）
    tech_palace.activate_yao(3, "active")
    tech_palace.change_yao(3, YaoType.YANG)
    
    print("\n【加载技能插件】")
    tech_palace.load_plugin("代码生成")
    tech_palace.load_plugin("测试自动化")
    
    print("\n【连接外部接口】")
    tech_palace.connect_interface("GitHub API")
    
    print("\n【检查相应关系】")
    tech_palace.check_correspondence()
    
    print("\n【最终卦象】")
    print(tech_palace.get_hexagram())
    
    print("\n" + "="*60)
    print("演示完成".center(60))
    print("="*60)


if __name__ == "__main__":
    demo_six_yao()
