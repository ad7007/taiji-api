#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智谱 AI 集成 - GLM-4-Flash 免费模型
Zhipu AI Integration - Free GLM-4-Flash Model

免费额度：100 万次/月
用途：替代 qwen-max，节省 57% 成本
"""

import os
from typing import Dict, Any, Optional


class ZhipuAIClient:
    """
    智谱 AI 客户端
    
    支持模型:
    - GLM-4-Flash（免费，快速）
    - GLM-4-Air（免费，平衡）
    - GLM-4（付费，高质量）
    """
    
    def __init__(self, api_key: str = None):
        """
        初始化
        
        Args:
            api_key: 智谱 API Key（https://open.bigmodel.cn/）
        """
        self.api_key = api_key or os.getenv("ZHIPU_API_KEY")
        self.client = None
        self.mock_mode = False
        
        if not self.api_key:
            print("⚠️ 警告：未设置 ZHIPU_API_KEY，使用模拟模式")
            self.mock_mode = True
        else:
            try:
                from zhipuai import ZhipuAI
                self.client = ZhipuAI(api_key=self.api_key)
                print("✅ 智谱 AI 客户端已初始化")
            except ImportError:
                print("⚠️ 未安装 zhipuai 库，使用模拟模式")
                print("   安装：pip install zhipuai")
                self.mock_mode = True
    
    def generate(self, prompt: str, model: str = "glm-4-flash", 
                 max_tokens: int = 2000, temperature: float = 0.7) -> Dict[str, Any]:
        """
        生成内容
        
        Args:
            prompt: 输入提示词
            model: 模型名称（默认 glm-4-flash）
            max_tokens: 最大输出长度
            temperature: 温度参数
        
        Returns:
            生成结果
        """
        if self.mock_mode:
            return self._mock_generate(prompt, model)
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            
            content = response.choices[0].message.content
            usage = response.usage
            
            return {
                "success": True,
                "content": content,
                "model": model,
                "usage": {
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens,
                },
                "cost": 0.0,  # GLM-4-Flash 免费
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": model,
            }
    
    def _mock_generate(self, prompt: str, model: str) -> Dict[str, Any]:
        """模拟生成（用于测试）"""
        return {
            "success": True,
            "content": f"[{model} 模拟响应] 收到提示：{prompt[:50]}...",
            "model": model,
            "usage": {
                "prompt_tokens": len(prompt) * 15 // 100,
                "completion_tokens": 100,
                "total_tokens": 200,
            },
            "cost": 0.0,
        }
    
    def chat(self, messages: list, model: str = "glm-4-flash") -> Dict[str, Any]:
        """
        多轮对话
        
        Args:
            messages: 消息列表 [{"role": "user", "content": "..."}]
            model: 模型名称
        
        Returns:
            对话响应
        """
        if self.mock_mode:
            return self._mock_generate(messages[-1]["content"], model)
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=2000,
                temperature=0.7,
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
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": model,
            }
    
    def get_models(self) -> list:
        """获取可用模型列表"""
        return [
            {"name": "glm-4-flash", "free": True, "speed": "fast", "quality": "good"},
            {"name": "glm-4-air", "free": True, "speed": "medium", "quality": "better"},
            {"name": "glm-4", "free": False, "speed": "medium", "quality": "best"},
            {"name": "glm-4-flashx", "free": True, "speed": "fastest", "quality": "good"},
        ]
    
    def get_free_quota(self) -> Dict[str, Any]:
        """获取免费额度信息"""
        return {
            "glm-4-flash": {
                "quota": "100 万次/月",
                "cost": "¥0.00",
                "recommended": True,
            },
            "glm-4-air": {
                "quota": "50 万次/月",
                "cost": "¥0.00",
                "recommended": True,
            },
            "glm-4": {
                "quota": "需购买",
                "cost": "¥0.05/1K tokens",
                "recommended": False,
            },
        }


def demo():
    """演示"""
    print("="*60)
    print("        智谱 AI 集成演示")
    print("="*60)
    
    client = ZhipuAIClient()
    
    # 显示可用模型
    print("\n【可用模型】")
    models = client.get_models()
    for model in models:
        free_tag = "✅免费" if model["free"] else "❌付费"
        print(f"  {model['name']}: {free_tag} | 速度：{model['speed']} | 质量：{model['quality']}")
    
    # 显示免费额度
    print("\n【免费额度】")
    quota = client.get_free_quota()
    for model, info in quota.items():
        rec = "⭐推荐" if info["recommended"] else ""
        print(f"  {model}: {info['quota']} | {info['cost']} {rec}")
    
    # 测试生成
    print("\n【测试生成】")
    result = client.generate("请介绍一下智谱 AI 的 GLM-4-Flash 模型")
    
    if result["success"]:
        print(f"✅ 生成成功")
        print(f"模型：{result['model']}")
        print(f"Token: {result['usage']['total_tokens']}")
        print(f"成本：¥{result['cost']:.4f}")
        print(f"内容预览：{result['content'][:100]}...")
    else:
        print(f"❌ 生成失败：{result.get('error')}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    demo()
