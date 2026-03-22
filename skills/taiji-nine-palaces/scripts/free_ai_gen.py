#!/usr/bin/env python3
"""
免费AI生成器 - 使用免费API

支持的免费模型：
1. 智谱GLM - 免费API额度
2. DeepSeek - 免费API
3. 通义千问 - 免费额度

无需浏览器，直接API调用
"""

import requests
import json
import os


class FreeAI:
    """免费AI生成器"""
    
    def __init__(self):
        self.endpoints = {
            # 智谱免费API（需要申请免费key）
            "zhipu": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
            
            # DeepSeek免费API（需要申请）
            "deepseek": "https://api.deepseek.com/v1/chat/completions",
        }
    
    def generate_zhipu(self, prompt: str, api_key: str = None) -> str:
        """智谱GLM免费生成"""
        if not api_key:
            # 尝试从环境变量获取
            api_key = os.environ.get("ZHIPU_API_KEY", "")
        
        if not api_key:
            return "需要智谱API Key（免费申请：https://open.bigmodel.cn）"
        
        try:
            response = requests.post(
                self.endpoints["zhipu"],
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "glm-4-flash",  # 免费模型
                    "messages": [{"role": "user", "content": prompt}]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"错误: {response.status_code}"
                
        except Exception as e:
            return f"错误: {e}"
    
    def generate_deepseek(self, prompt: str, api_key: str = None) -> str:
        """DeepSeek免费生成"""
        if not api_key:
            api_key = os.environ.get("DEEPSEEK_API_KEY", "")
        
        if not api_key:
            return "需要DeepSeek API Key（免费申请：https://platform.deepseek.com）"
        
        try:
            response = requests.post(
                self.endpoints["deepseek"],
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"错误: {response.status_code}"
                
        except Exception as e:
            return f"错误: {e}"
    
    def generate(self, prompt: str) -> str:
        """使用免费API生成"""
        # 优先使用智谱
        result = self.generate_zhipu(prompt)
        if "错误" not in result and "需要" not in result:
            return result
        
        # 备选DeepSeek
        result = self.generate_deepseek(prompt)
        return result


# 课程内容生成器
class CourseGenerator:
    """免费课程内容生成"""
    
    def __init__(self):
        self.ai = FreeAI()
    
    def generate_lesson_intro(self, lesson_num: int, topic: str) -> str:
        """生成课程开场白"""
        prompt = f"为《AI智能体入门课》第{lesson_num}节生成开场白，主题：{topic}。要求简短有力，30秒内说完。"
        return self.ai.generate(prompt)
    
    def generate_douyin_script(self, topic: str) -> str:
        """生成抖音脚本"""
        prompt = f"为抖音短视频写脚本，主题：{topic}。要求：60秒内，吸引眼球，有爆款潜质。"
        return self.ai.generate(prompt)
    
    def generate_article(self, topic: str) -> str:
        """生成文章"""
        prompt = f"写一篇关于{topic}的技术文章，800字左右，通俗易懂。"
        return self.ai.generate(prompt)


if __name__ == "__main__":
    print("=== 免费AI生成测试 ===\n")
    
    ai = FreeAI()
    
    # 测试智谱
    print("智谱GLM:")
    print(ai.generate_zhipu("你好"))
    
    # 测试DeepSeek  
    print("\nDeepSeek:")
    print(ai.generate_deepseek("你好"))
    
    print("\n提示: 免费API Key申请地址:")
    print("- 智谱: https://open.bigmodel.cn")
    print("- DeepSeek: https://platform.deepseek.com")