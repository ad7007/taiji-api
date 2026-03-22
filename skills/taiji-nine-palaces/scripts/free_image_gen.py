#!/usr/bin/env python3
"""
免费图片生成工具

尝试多个免费API
"""

import requests
import urllib.parse
from pathlib import Path


class FreeImageGenerator:
    def __init__(self):
        self.output_dir = Path("assets/images")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.milo_prompt = "Asian woman tech style black gold intelligent"
    
    def generate_pollinations(self, prompt: str) -> bytes:
        """Pollinations - 完全免费"""
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}"
        try:
            r = requests.get(url, timeout=120)
            if r.status_code == 200 and len(r.content) > 5000:
                return r.content
        except:
            pass
        return None
    
    def generate_milo(self) -> str:
        """生成米珞"""
        filename = "milo_character.png"
        
        print("尝试Pollinations...")
        content = self.generate_pollinations(self.milo_prompt)
        
        if content:
            path = self.output_dir / filename
            with open(path, 'wb') as f:
                f.write(content)
            print(f"✅ 成功: {path}")
            return str(path)
        
        print("❌ 在线生成失败")
        return None


if __name__ == "__main__":
    gen = FreeImageGenerator()
    gen.generate_milo()