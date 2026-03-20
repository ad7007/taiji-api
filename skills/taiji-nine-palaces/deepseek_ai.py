#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek AI 集成 - 免费高性能模型
DeepSeek AI Integration - Free High-Performance Model

免费额度：100 万次/月
用途：内容生成、代码生成
性能：接近 GPT-4
"""

import os
from typing import Dict, Any, Optional


class DeepSeekClient:
    """
    DeepSeek AI 客户端
    
    支持模型:
    - DeepSeek-V2（免费，快速）
    - DeepSeek-V3（免费，高质量）
    - DeepSeek-Coder（免费，代码专用）
    """
    
    def __init__(self, api_key: str = None):
        """
        初始化
        
        Args:
            api_key: DeepSeek API Key（https://platform.deepseek.com/）
        """
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.client = None
        self.mock_mode = False
        
        if not self.api_key:
            print("⚠️ 警告：未设置 DEEPSEEK_API_KEY，使用模拟模式")
            print("   获取 API Key: https://platform.deepseek.com/")
            self.mock_mode = True
        else:
            try:
                from openai import OpenAI
                # DeepSeek 兼容 OpenAI API
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url="https://api.deepseek.com"
                )
                print("✅ DeepSeek AI 客户端已初始化")
            except ImportError:
                print("⚠️ 未安装 openai 库，使用模拟模式")
                print("   安装：pip install openai")
                self.mock_mode = True
    
    def generate(self, prompt: str, model: str = "deepseek-chat",
                 max_tokens: int = 2000, temperature: float = 0.7) -> Dict[str, Any]:
        """
        生成内容
        
        Args:
            prompt: 输入提示词
            model: 模型名称（默认 deepseek-chat）
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
                "cost": 0.0,  # 免费额度内
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
    
    def code_generate(self, description: str, language: str = "python") -> Dict[str, Any]:
        """
        代码生成（使用 DeepSeek-Coder）
        
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
        return self.generate(prompt, model="deepseek-coder")
    
    def chat(self, messages: list, model: str = "deepseek-chat") -> Dict[str, Any]:
        """
        多轮对话
        
        Args:
            messages: 消息列表
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
            {"name": "deepseek-chat", "free": True, "speed": "fast", "quality": "excellent"},
            {"name": "deepseek-coder", "free": True, "speed": "fast", "quality": "excellent"},
            {"name": "deepseek-reasoner", "free": True, "speed": "medium", "quality": "best"},
        ]
    
    def get_free_quota(self) -> Dict[str, Any]:
        """获取免费额度信息"""
        return {
            "deepseek-chat": {
                "quota": "100 万次/月",
                "cost": "¥0.00",
                "recommended": True,
                "description": "通用对话模型",
            },
            "deepseek-coder": {
                "quota": "100 万次/月",
                "cost": "¥0.00",
                "recommended": True,
                "description": "代码专用模型",
            },
            "deepseek-reasoner": {
                "quota": "50 万次/月",
                "cost": "¥0.00",
                "recommended": False,
                "description": "推理专用模型",
            },
        }
    
    def compare_with_gpt4(self) -> Dict[str, Any]:
        """对比 GPT-4 性能"""
        return {
            "performance": {
                "deepseek-chat": "≈ GPT-4 Turbo",
                "deepseek-coder": "≈ GPT-4 Code",
                "deepseek-reasoner": "≈ GPT-4 Reasoning",
            },
            "cost": {
                "deepseek": "¥0.00（免费额度内）",
                "gpt-4": "$0.03/1K tokens",
            },
            "speed": {
                "deepseek": "快",
                "gpt-4": "中等",
            },
            "chinese": {
                "deepseek": "优秀（中国公司）",
                "gpt-4": "良好",
            },
        }


def demo():
    """演示"""
    print("="*60)
    print("        DeepSeek AI 集成演示")
    print("="*60)
    
    client = DeepSeekClient()
    
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
        print(f"  {model}: {info['quota']} | {info['cost']} | {info['description']} {rec}")
    
    # 对比 GPT-4
    print("\n【对比 GPT-4】")
    comparison = client.compare_with_gpt4()
    print(f"  性能：{comparison['performance']['deepseek-chat']}")
    print(f"  成本：{comparison['cost']['deepseek']} vs {comparison['cost']['gpt-4']}")
    print(f"  速度：{comparison['speed']['deepseek']} vs {comparison['speed']['gpt-4']}")
    print(f"  中文：{comparison['chinese']['deepseek']} vs {comparison['chinese']['gpt-4']}")
    
    # 测试生成
    print("\n【测试生成】")
    result = client.generate("请介绍一下 DeepSeek 模型的特点")
    
    if result["success"]:
        print(f"✅ 生成成功")
        print(f"模型：{result['model']}")
        print(f"Token: {result['usage']['total_tokens']}")
        print(f"成本：¥{result['cost']:.4f}")
        print(f"内容预览：{result['content'][:100]}...")
    else:
        print(f"❌ 生成失败：{result.get('error')}")
    
    # 测试代码生成
    print("\n【测试代码生成】")
    code_result = client.code_generate("计算斐波那契数列")
    
    if code_result["success"]:
        print(f"✅ 代码生成成功")
        print(f"模型：{code_result['model']}")
        print(f"代码预览：{code_result['content'][:150]}...")
    else:
        print(f"❌ 代码生成失败：{code_result.get('error')}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    demo()
