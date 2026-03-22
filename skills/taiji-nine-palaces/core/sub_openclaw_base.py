#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
子 OPENCLAW 基础模板类（增强版 - 支持 6 爻和插件化）
Sub-OPENCLAW Base Template Class (Enhanced with 6 Yao and Plugin Support)

6 爻结构：
初爻 (1): 基础能力
二爻 (2): 技能插件
三爻 (3): 外部接口
四爻 (4): 数据采集
五爻 (5): 任务执行
上爻 (6): 成果输出
"""

from typing import Dict, Any, Optional, List, Callable
from pathlib import Path
from enum import Enum
import importlib.util
import sys
import json


class YaoPosition(Enum):
    """爻位定义"""
    INITIAL = 1      # 初爻 - 基础能力
    SECOND = 2       # 二爻 - 技能插件
    THIRD = 3        # 三爻 - 外部接口
    FOURTH = 4       # 四爻 - 数据采集
    FIFTH = 5        # 五爻 - 任务执行
    TOP = 6          # 上爻 - 成果输出


class YaoStatus(Enum):
    """爻的状态"""
    INACTIVE = "inactive"     # 未激活
    ACTIVE = "active"         # 已激活
    ENHANCED = "enhanced"     # 已增强
    BLOCKED = "blocked"       # 阻塞


class Plugin:
    """插件基类"""
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.status = "inactive"
        self.version = "1.0.0"
        
    def activate(self) -> bool:
        """激活插件"""
        self.status = "active"
        return True
    
    def deactivate(self) -> bool:
        """停用插件"""
        self.status = "inactive"
        return True
    
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """执行插件功能"""
        raise NotImplementedError("插件必须实现此方法")
    
    def get_info(self) -> Dict[str, Any]:
        """获取插件信息"""
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status,
            "config": self.config
        }


class SubOpenClawBase:
    """八宫子 OPENCLAW 基础类（支持 6 爻变化和插件化）"""
    
    def __init__(self, palace_position: int, template_name: str):
        self.palace_position = palace_position
        self.template_name = template_name
        self.config_dir = Path.home() / ".openclaw" / f"palace_{palace_position}"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # 6 爻状态管理
        self.yao_states: Dict[YaoPosition, YaoStatus] = {
            YaoPosition.INITIAL: YaoStatus.ACTIVE,    # 初爻默认激活
            YaoPosition.SECOND: YaoStatus.INACTIVE,   # 二爻待扩展
            YaoPosition.THIRD: YaoStatus.INACTIVE,    # 三爻待连接
            YaoPosition.FOURTH: YaoStatus.ACTIVE,     # 四爻默认激活
            YaoPosition.FIFTH: YaoStatus.ACTIVE,      # 五爻默认激活
            YaoPosition.TOP: YaoStatus.ACTIVE,        # 上爻默认激活
        }
        
        # 技能插件列表（二爻）
        self.skill_plugins: List[Plugin] = []
        
        # 外部接口配置（三爻）
        self.external_interfaces: List[Dict[str, str]] = []
        
        # 插件事件监听器
        self.plugin_listeners: Dict[str, List[Callable]] = {}
    
    def get_yao_status(self, position: YaoPosition) -> YaoStatus:
        """获取指定爻位的状态"""
        return self.yao_states.get(position, YaoStatus.INACTIVE)
    
    def activate_yao(self, position: YaoPosition, status: YaoStatus = YaoStatus.ACTIVE) -> bool:
        """激活或更新爻位状态"""
        if position in self.yao_states:
            self.yao_states[position] = status
            print(f"✅ {position.name}({position.value}爻) 已激活：{status.value}")
            return True
        return False
    
    def get_all_yao_status(self) -> Dict[str, str]:
        """获取所有爻位状态"""
        return {
            f"{pos.name}({pos.value}爻)": status.value
            for pos, status in self.yao_states.items()
        }
    
    def load_plugin(self, plugin_path: Path, config: Optional[Dict] = None) -> Optional[Plugin]:
        """加载插件"""
        try:
            # 动态加载插件模块
            spec = importlib.util.spec_from_file_location(plugin_path.stem, plugin_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[plugin_path.stem] = module
                spec.loader.exec_module(module)
                
                # 查找插件类
                for name, obj in module.__dict__.items():
                    if isinstance(obj, type) and issubclass(obj, Plugin) and obj != Plugin:
                        plugin_instance = obj(plugin_path.stem, config or {})
                        return plugin_instance
            return None
        except Exception as e:
            print(f"❌ 加载插件失败：{e}")
            return None
    
    def add_skill_plugin(self, plugin_name: str, config: Optional[Dict] = None) -> bool:
        """添加技能插件（二爻能力）"""
        # 只有二爻激活时才能添加插件
        if self.yao_states[YaoPosition.SECOND] == YaoStatus.INACTIVE:
            print(f"⚠️ 二爻未激活，无法添加技能插件：{plugin_name}")
            return False
        
        # 检查插件是否已存在
        for plugin in self.skill_plugins:
            if plugin.name == plugin_name:
                print(f"⚠️ 插件已存在：{plugin_name}")
                return False
        
        # 尝试加载插件
        plugin_path = self.config_dir / f"plugins" / f"{plugin_name}.py"
        if plugin_path.exists():
            plugin = self.load_plugin(plugin_path, config)
            if plugin:
                plugin.activate()
                self.skill_plugins.append(plugin)
                print(f"✅ 已添加技能插件：{plugin_name}")
                self._notify_plugin_event("plugin_added", {"plugin_name": plugin_name})
                return True
        else:
            # 创建默认插件
            class DefaultPlugin(Plugin):
                def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
                    return {"result": f"Plugin {self.name} executed", "data": data}
            
            plugin = DefaultPlugin(plugin_name, config or {})
            plugin.activate()
            self.skill_plugins.append(plugin)
            print(f"✅ 已添加默认技能插件：{plugin_name}")
            self._notify_plugin_event("plugin_added", {"plugin_name": plugin_name})
            return True
    
    def remove_skill_plugin(self, plugin_name: str) -> bool:
        """移除技能插件"""
        for i, plugin in enumerate(self.skill_plugins):
            if plugin.name == plugin_name:
                plugin.deactivate()
                self.skill_plugins.pop(i)
                print(f"✅ 已移除技能插件：{plugin_name}")
                self._notify_plugin_event("plugin_removed", {"plugin_name": plugin_name})
                return True
        print(f"⚠️ 插件不存在：{plugin_name}")
        return False
    
    def execute_plugin(self, plugin_name: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """执行插件"""
        for plugin in self.skill_plugins:
            if plugin.name == plugin_name and plugin.status == "active":
                try:
                    result = plugin.execute(data)
                    self._notify_plugin_event("plugin_executed", {"plugin_name": plugin_name, "result": result})
                    return result
                except Exception as e:
                    print(f"❌ 插件执行失败：{e}")
                    return {"error": str(e)}
        print(f"⚠️ 插件未找到或未激活：{plugin_name}")
        return None
    
    def get_plugin_info(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """获取插件信息"""
        for plugin in self.skill_plugins:
            if plugin.name == plugin_name:
                return plugin.get_info()
        return None
    
    def get_all_plugins(self) -> List[Dict[str, Any]]:
        """获取所有插件信息"""
        return [plugin.get_info() for plugin in self.skill_plugins]
    
    def add_external_interface(self, interface_type: str, endpoint: str) -> bool:
        """添加外部接口（三爻能力）"""
        if self.yao_states[YaoPosition.THIRD] == YaoStatus.INACTIVE:
            print(f"⚠️ 三爻未激活，无法添加外部接口")
            return False
        
        interface = {
            "type": interface_type,
            "endpoint": endpoint
        }
        self.external_interfaces.append(interface)
        print(f"✅ 已添加外部接口：{interface_type} -> {endpoint}")
        return True
    
    def register_plugin_listener(self, event: str, listener: Callable):
        """注册插件事件监听器"""
        if event not in self.plugin_listeners:
            self.plugin_listeners[event] = []
        if listener not in self.plugin_listeners[event]:
            self.plugin_listeners[event].append(listener)
    
    def unregister_plugin_listener(self, event: str, listener: Callable):
        """注销插件事件监听器"""
        if event in self.plugin_listeners and listener in self.plugin_listeners[event]:
            self.plugin_listeners[event].remove(listener)
    
    def _notify_plugin_event(self, event: str, data: Dict[str, Any]):
        """通知插件事件"""
        if event in self.plugin_listeners:
            for listener in self.plugin_listeners[event]:
                try:
                    listener(data)
                except Exception as e:
                    print(f"❌ 事件通知失败：{e}")
    
    def get_palace_config(self) -> Dict[str, Any]:
        """获取宫殿配置（包含 6 爻状态）"""
        return {
            'position': self.palace_position,
            'template': self.template_name,
            'config_path': str(self.config_dir),
            'yao_states': self.get_all_yao_status(),
            'skill_plugins': [plugin.get_info() for plugin in self.skill_plugins],
            'external_interfaces': self.external_interfaces,
            'plugin_count': len(self.skill_plugins)
        }
    
    def save_config(self):
        """保存配置到文件"""
        config_path = self.config_dir / "config.json"
        config = self.get_palace_config()
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print(f"✅ 配置已保存到：{config_path}")
    
    def load_config(self):
        """从文件加载配置"""
        config_path = self.config_dir / "config.json"
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # 加载插件配置
                if 'skill_plugins' in config:
                    for plugin_info in config['skill_plugins']:
                        self.add_skill_plugin(plugin_info['name'], plugin_info['config'])
                
                # 加载外部接口
                if 'external_interfaces' in config:
                    self.external_interfaces = config['external_interfaces']
                
                print(f"✅ 配置已从：{config_path} 加载")
                return True
            except Exception as e:
                print(f"❌ 加载配置失败：{e}")
                return False
        return False
    
    def install(self, target_dir: Path) -> bool:
        """安装子模板到目标目录"""
        raise NotImplementedError("子类必须实现此方法")
    
    def package(self, output_dir: Path) -> Path:
        """打包子模板为 ZIP"""
        import zipfile
        
        output_dir.mkdir(parents=True, exist_ok=True)
        zip_file = output_dir / f"palace_{self.palace_position}_template.zip"
        
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 添加配置文件
            config_content = self.get_palace_config()
            zipf.writestr("config.json", json.dumps(config_content, ensure_ascii=False, indent=2))
            
            # 添加插件目录
            plugins_dir = self.config_dir / "plugins"
            if plugins_dir.exists():
                for plugin_file in plugins_dir.glob("*.py"):
                    zipf.write(plugin_file, f"plugins/{plugin_file.name}")
        
        print(f"📦 已打包到：{zip_file}")
        return zip_file
    
    def validate(self) -> bool:
        """验证模板完整性"""
        # 基础验证
        if not self.config_dir.exists():
            print("❌ 配置目录不存在")
            return False
        
        # 验证插件
        for plugin in self.skill_plugins:
            if plugin.status == "active":
                try:
                    test_result = plugin.execute({"test": True})
                    if "error" in test_result:
                        print(f"❌ 插件验证失败：{plugin.name} - {test_result['error']}")
                        return False
                except Exception as e:
                    print(f"❌ 插件验证失败：{plugin.name} - {e}")
                    return False
        
        print("✅ 模板验证通过")
        return True
