#!/usr/bin/env python3
"""
免费图片生成工具

使用免费API生成米珞形象
"""

import requests
import json
import os
from pathlib import Path


class FreeImageGenerator:
    """免费图片生成器"""
    
    def __init__(self):
        self.output_dir = Path("assets/images")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 米珞形象提示词
        self.milo_prompt = """
professional Asian woman, late 20s, 
futuristic Chinese-style outfit, 
black and gold colors, 
taiji yin-yang symbol decoration, 
intelligent gentle expression, 
long black hair, 
tech accessories, 
character design, 
high quality digital art
"""
    
    def generate_with_pollinations(self, prompt: str, filename: str = "milo.png") -> str:
        """
        使用Pollinations免费API生成图片
        
        完全免费，无需API Key
        """
        url = f"https://image.pollinations.ai/prompt/{prompt}"
        
        print(f"正在生成图片: {filename}...")
        
        try:
            response = requests.get(url, timeout=60)
            
            if response.status_code == 200:
                output_path = self.output_dir / filename
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print(f"✅ 图片已保存: {output_path}")
                return str(output_path)
            else:
                print(f"❌ 生成失败: HTTP {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ 错误: {e}")
            return None
    
    def generate_milo(self) -> str:
        """生成米珞形象"""
        return self.generate_with_pollinations(
            prompt=self.milo_prompt,
            filename="milo_character.png"
        )
    
    def generate_multiple(self, count: int = 3) -> list:
        """生成多张图片"""
        paths = []
        for i in range(count):
            path = self.generate_with_pollinations(
                prompt=self.milo_prompt,
                filename=f"milo_v{i+1}.png"
            )
            if path:
                paths.append(path)
        return paths


if __name__ == "__main__":
    print("=== 免费图片生成测试 ===\n")
    
    generator = FreeImageGenerator()
    
    # 生成米珞形象
    print("生成米珞虚拟形象...")
    path = generator.generate_milo()
    
    if path:
        print(f"\n✅ 成功！图片位置: {path}")
    else:
        print("\n❌ 生成失败，请检查网络")
    
    print("\n=== 完成 ===")