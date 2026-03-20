#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百炼 API 客户端
Bailian API Client - Call Bailian models with auto-routing
"""

import os
import json
from typing import Dict, Any, Optional, List
from pathlib import Path

from model_router import ModelRouter, TaskType


class BailianClient:
    """
    百炼 API 客户端
    
    集成模型路由，自动选择最优模型并调用 API
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.router = ModelRouter(api_key=self.api_key)
        
        if not self.api_key:
            print("⚠️ 警告：未设置 DASHSCOPE_API_KEY，将使用模拟模式")
            self.mock_mode = True
        else:
            self.mock_mode = False
        
        # 配置
        self.config_path = Path("/root/.openclaw/workspace/config/bailian_config.json")
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置"""
        if self.config_path.exists():
            return json.loads(self.config_path.read_text(encoding="utf-8"))
        return {
            "default_model": "qwen-plus",
            "max_retries": 3,
            "timeout_seconds": 60,
            "temperature": 0.7,
            "max_tokens": 2000,
        }
    
    def _save_config(self):
        """保存配置"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(json.dumps(self.config, indent=2), encoding="utf-8")
    
    def generate(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        生成响应（自动路由）
        
        Args:
            prompt: 输入提示词
            context: 上下文信息（可选）
        
        Returns:
            包含响应内容和模型信息的字典
        """
        # 模型路由
        route_result = self.router.route(prompt, context)
        model_id = route_result["selected_model"]
        
        # 调用 API
        if self.mock_mode:
            response = self._mock_generate(prompt, model_id)
        else:
            response = self._call_bailian_api(prompt, model_id)
        
        # 合并结果
        return {
            **response,
            "model_info": route_result,
        }
    
    def _call_bailian_api(self, prompt: str, model_id: str) -> Dict[str, Any]:
        """
        调用百炼 API
        
        需要安装 dashscope 库：pip install dashscope
        """
        try:
            import dashscope
            from dashscope import Generation
            
            dashscope.api_key = self.api_key
            
            response = Generation.call(
                model=model_id,
                prompt=prompt,
                temperature=self.config.get("temperature", 0.7),
                max_tokens=self.config.get("max_tokens", 2000),
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "content": response.output.text,
                    "usage": dict(response.usage) if hasattr(response, 'usage') else {},
                    "model": model_id,
                }
            else:
                return {
                    "success": False,
                    "error": f"API 错误：{response.code} - {response.message}",
                    "model": model_id,
                }
                
        except ImportError:
            print("⚠️ 未安装 dashscope 库，使用模拟模式")
            return self._mock_generate(prompt, model_id)
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": model_id,
            }
    
    def _mock_generate(self, prompt: str, model_id: str) -> Dict[str, Any]:
        """模拟生成（用于测试）"""
        return {
            "success": True,
            "content": f"[{model_id} 模拟响应] 收到提示：{prompt[:50]}...",
            "usage": {
                "input_tokens": len(prompt) * 15 // 100,
                "output_tokens": 100,
            },
            "model": model_id,
        }
    
    def chat(self, messages: List[Dict], model_id: str = None) -> Dict[str, Any]:
        """
        多轮对话
        
        Args:
            messages: 消息列表 [{"role": "user", "content": "..."}]
            model_id: 指定模型（可选）
        
        Returns:
            对话响应
        """
        if not model_id:
            # 根据最后一条消息路由
            last_prompt = messages[-1]["content"]
            route_result = self.router.route(last_prompt)
            model_id = route_result["selected_model"]
        
        try:
            import dashscope
            from dashscope import Generation
            
            dashscope.api_key = self.api_key
            
            response = Generation.call(
                model=model_id,
                messages=messages,
                temperature=self.config.get("temperature", 0.7),
                max_tokens=self.config.get("max_tokens", 2000),
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "content": response.output.text,
                    "usage": dict(response.usage) if hasattr(response, 'usage') else {},
                    "model": model_id,
                }
            else:
                return {
                    "success": False,
                    "error": f"API 错误：{response.code} - {response.message}",
                    "model": model_id,
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": model_id,
            }
    
    def generate_with_retry(self, prompt: str, context: Dict = None) -> Dict[str, Any]:
        """带重试的生成"""
        max_retries = self.config.get("max_retries", 3)
        
        for attempt in range(max_retries):
            result = self.generate(prompt, context)
            
            if result.get("success"):
                return result
            
            # 失败时尝试降级模型
            if attempt < max_retries - 1:
                print(f"⚠️ 第{attempt+1}次失败，尝试降级模型...")
                if context is None:
                    context = {}
                context["force_model"] = "qwen-turbo"  # 降级到最便宜的模型
        
        return result
    
    def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """获取模型信息"""
        return self.router.get_model_info(model_id)
    
    def list_models(self) -> List[Dict[str, Any]]:
        """列出所有模型"""
        return self.router.list_models()
    
    def get_cost_summary(self) -> Dict[str, Any]:
        """获取成本统计"""
        return self.router.get_cost_summary()
    
    def configure(self, **kwargs):
        """更新配置"""
        self.config.update(kwargs)
        self._save_config()
        return self.config


def demo():
    """演示"""
    print("="*60)
    print("        百炼 API 客户端演示")
    print("="*60)
    
    client = BailianClient()
    
    # 测试用例
    test_prompts = [
        "你好，请介绍一下自己",
        "请帮我翻译：你好世界",
        "写一个 Python 快速排序函数",
        "总结这篇文章的主要内容...",
    ]
    
    print("\n【API 调用测试】\n")
    
    for prompt in test_prompts:
        print(f"提示：{prompt[:30]}...")
        result = client.generate(prompt)
        
        if result.get("success"):
            print(f"✅ 模型：{result['model_info']['selected_model']}")
            print(f"   成本：¥{result['model_info']['estimated_cost']:.6f}")
            print(f"   响应：{result['content'][:50]}...")
        else:
            print(f"❌ 错误：{result.get('error')}")
        print()
    
    # 显示模型列表
    print("\n【可用模型】\n")
    models = client.list_models()
    for model in models:
        print(f"- {model['name']} ({model['model_id']})")
    
    # 成本统计
    print("\n【成本统计】\n")
    summary = client.get_cost_summary()
    print(f"总请求：{summary['total_requests']}")
    print(f"总成本：¥{summary['total_cost']:.4f}")
    print(f"模型分布：{summary['model_distribution']}")


if __name__ == "__main__":
    demo()
