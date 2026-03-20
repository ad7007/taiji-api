#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
免费模型插件 - 独立插件层
Free Models Plugin - Isolated Plugin Layer

通过插件调用免费模型（智谱/DeepSeek），不影响内部系统
"""

import os
import sys
from typing import Dict, Any, Optional
from pathlib import Path

# 插件独立依赖，不影响主系统
try:
    from zhipuai import ZhipuAI
    ZHIPU_AVAILABLE = True
except ImportError:
    ZHIPU_AVAILABLE = False

try:
    from openai import OpenAI
    DEEPSEEK_AVAILABLE = True
except ImportError:
    DEEPSEEK_AVAILABLE = False


class FreeModelsPlugin:
    """
    免费模型插件
    
    特点:
    - 独立插件，不影响主系统
    - 按需加载，避免依赖冲突
    - 统一接口，方便切换
    """
    
    def __init__(self, config_path: str = None):
        """
        初始化插件
        
        Args:
            config_path: 配置文件路径（默认：~/.openclaw/plugins/free_models.json）
        """
        self.config_path = Path(config_path) if config_path else Path.home() / ".openclaw" / "plugins" / "free_models.json"
        self.config = self._load_config()
        
        self.zhipu_client = None
        self.deepseek_client = None
        
        # 按需初始化
        if self.config.get("enable_zhipu", True) and ZHIPU_AVAILABLE:
            self._init_zhipu()
        
        if self.config.get("enable_deepseek", True) and DEEPSEEK_AVAILABLE:
            self._init_deepseek()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置"""
        if self.config_path.exists():
            import json
            return json.loads(self.config_path.read_text(encoding="utf-8"))
        
        # 默认配置
        return {
            "enable_zhipu": True,
            "enable_deepseek": True,
            "zhipu_api_key": os.getenv("ZHIPU_API_KEY", ""),
            "deepseek_api_key": os.getenv("DEEPSEEK_API_KEY", ""),
            "default_model": "glm-4-flash",
            "fallback_chain": ["glm-4-flash", "deepseek-chat", "glm-4-air"],
        }
    
    def _save_config(self):
        """保存配置"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        import json
        self.config_path.write_text(json.dumps(self.config, indent=2, ensure_ascii=False), encoding="utf-8")
    
    def _init_zhipu(self):
        """初始化智谱 AI"""
        api_key = self.config.get("zhipu_api_key", "")
        if api_key:
            try:
                self.zhipu_client = ZhipuAI(api_key=api_key)
                print("✅ [插件] 智谱 AI 已初始化")
            except Exception as e:
                print(f"⚠️ [插件] 智谱 AI 初始化失败：{e}")
    
    def _init_deepseek(self):
        """初始化 DeepSeek"""
        api_key = self.config.get("deepseek_api_key", "")
        if api_key:
            try:
                self.deepseek_client = OpenAI(
                    api_key=api_key,
                    base_url="https://api.deepseek.com"
                )
                print("✅ [插件] DeepSeek 已初始化")
            except Exception as e:
                print(f"⚠️ [插件] DeepSeek 初始化失败：{e}")
    
    def generate(self, prompt: str, model: str = None, **kwargs) -> Dict[str, Any]:
        """
        生成内容（插件接口）
        
        Args:
            prompt: 输入提示词
            model: 模型名称（可选，自动选择）
            **kwargs: 其他参数
        
        Returns:
            生成结果
        """
        # 自动选择模型
        if not model:
            model = self.config.get("default_model", "glm-4-flash")
        
        # 根据模型选择客户端
        if model.startswith("glm"):
            return self._generate_zhipu(prompt, model, **kwargs)
        elif model.startswith("deepseek"):
            return self._generate_deepseek(prompt, model, **kwargs)
        else:
            return {"success": False, "error": f"未知模型：{model}"}
    
    def _generate_zhipu(self, prompt: str, model: str, **kwargs) -> Dict[str, Any]:
        """智谱 AI 生成"""
        if not self.zhipu_client:
            return {"success": False, "error": "智谱 AI 未初始化"}
        
        try:
            response = self.zhipu_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=kwargs.get("max_tokens", 2000),
                temperature=kwargs.get("temperature", 0.7),
            )
            
            return {
                "success": True,
                "content": response.choices[0].message.content,
                "model": model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
                "cost": 0.0,
                "source": "zhipu_plugin",
            }
        except Exception as e:
            return {"success": False, "error": str(e), "source": "zhipu_plugin"}
    
    def _generate_deepseek(self, prompt: str, model: str, **kwargs) -> Dict[str, Any]:
        """DeepSeek 生成"""
        if not self.deepseek_client:
            return {"success": False, "error": "DeepSeek 未初始化"}
        
        try:
            response = self.deepseek_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=kwargs.get("max_tokens", 2000),
                temperature=kwargs.get("temperature", 0.7),
            )
            
            return {
                "success": True,
                "content": response.choices[0].message.content,
                "model": model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
                "cost": 0.0,
                "source": "deepseek_plugin",
            }
        except Exception as e:
            return {"success": False, "error": str(e), "source": "deepseek_plugin"}
    
    def code_generate(self, description: str, language: str = "python") -> Dict[str, Any]:
        """
        代码生成（插件接口）
        
        Args:
            description: 代码功能描述
            language: 编程语言
        
        Returns:
            生成的代码
        """
        prompt = f"""请生成{language}代码来实现以下功能：

功能描述：
{description}

要求：
1. 代码完整可运行
2. 遵循最佳实践
3. 添加必要的注释
4. 包含错误处理

代码：
"""
        # 使用 DeepSeek-Coder（代码专用）
        return self.generate(prompt, model="deepseek-coder")
    
    def set_api_key(self, provider: str, api_key: str):
        """
        设置 API Key（插件接口）
        
        Args:
            provider: 提供商（zhipu/deepseek）
            api_key: API Key
        """
        if provider == "zhipu":
            self.config["zhipu_api_key"] = api_key
            self._init_zhipu()
        elif provider == "deepseek":
            self.config["deepseek_api_key"] = api_key
            self._init_deepseek()
        
        self._save_config()
    
    def get_status(self) -> Dict[str, Any]:
        """获取插件状态"""
        return {
            "zhipu": {
                "available": ZHIPU_AVAILABLE,
                "initialized": self.zhipu_client is not None,
                "api_key_set": bool(self.config.get("zhipu_api_key", "")),
            },
            "deepseek": {
                "available": DEEPSEEK_AVAILABLE,
                "initialized": self.deepseek_client is not None,
                "api_key_set": bool(self.config.get("deepseek_api_key", "")),
            },
            "config_path": str(self.config_path),
            "default_model": self.config.get("default_model", "glm-4-flash"),
        }
    
    def get_models(self) -> list:
        """获取可用模型列表"""
        return [
            {"name": "glm-4-flash", "provider": "zhipu", "free": True, "recommended": True},
            {"name": "glm-4-air", "provider": "zhipu", "free": True, "recommended": True},
            {"name": "deepseek-chat", "provider": "deepseek", "free": True, "recommended": True},
            {"name": "deepseek-coder", "provider": "deepseek", "free": True, "recommended": True},
        ]


# ========== 插件注册 ==========

PLUGIN_NAME = "free_models"
PLUGIN_VERSION = "1.0.0"
PLUGIN_DESCRIPTION = "免费模型插件（智谱/DeepSeek），不影响内部系统"


def init_plugin(config: Dict[str, Any] = None) -> FreeModelsPlugin:
    """插件初始化入口"""
    plugin = FreeModelsPlugin()
    if config:
        plugin.config.update(config)
    return plugin


def generate_content(prompt: str, model: str = "glm-4-flash") -> Dict[str, Any]:
    """插件调用接口 - 内容生成"""
    plugin = FreeModelsPlugin()
    return plugin.generate(prompt, model)


def generate_code(description: str, language: str = "python") -> Dict[str, Any]:
    """插件调用接口 - 代码生成"""
    plugin = FreeModelsPlugin()
    return plugin.code_generate(description, language)


# ========== 演示 ==========

def demo():
    """演示"""
    print("="*60)
    print("        免费模型插件演示（独立插件层）")
    print("="*60)
    
    plugin = FreeModelsPlugin()
    
    # 显示状态
    print("\n【插件状态】")
    status = plugin.get_status()
    print(f"  智谱 AI: {'✅' if status['zhipu']['initialized'] else '❌'}")
    print(f"  DeepSeek: {'✅' if status['deepseek']['initialized'] else '❌'}")
    print(f"  配置文件：{status['config_path']}")
    
    # 显示可用模型
    print("\n【可用模型】")
    models = plugin.get_models()
    for model in models:
        free_tag = "✅免费" if model["free"] else "❌付费"
        rec_tag = "⭐推荐" if model["recommended"] else ""
        print(f"  {model['name']} ({model['provider']}): {free_tag} {rec_tag}")
    
    # 测试生成（如果已配置）
    if status['zhipu']['initialized'] or status['deepseek']['initialized']:
        print("\n【测试生成】")
        result = plugin.generate("你好，请介绍一下自己", model="glm-4-flash")
        
        if result["success"]:
            print(f"✅ 生成成功")
            print(f"模型：{result['model']}")
            print(f"来源：{result['source']}")
            print(f"成本：¥{result['cost']:.4f}")
            print(f"内容预览：{result['content'][:50]}...")
        else:
            print(f"❌ 生成失败：{result.get('error')}")
    else:
        print("\n⚠️ 未配置 API Key，无法测试")
        print("   使用方法:")
        print("   plugin.set_api_key('zhipu', 'your_zhipu_key')")
        print("   plugin.set_api_key('deepseek', 'your_deepseek_key')")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    demo()
