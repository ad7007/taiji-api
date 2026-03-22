#!/usr/bin/env python3
"""
免费内容生成器 - 无头浏览器 + 免费API
"""

import asyncio
from playwright.async_api import async_playwright


async def generate_with_kimi(prompt: str) -> str:
    """使用Kimi免费生成"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto("https://kimi.moonshot.cn")
            await page.wait_for_load_state('networkidle')
            
            # 输入框
            textarea = await page.query_selector('textarea')
            if textarea:
                await textarea.fill(prompt)
                await textarea.press('Enter')
                await asyncio.sleep(5)
                
                # 提取回复
                content = await page.evaluate('''
                    () => {
                        const msgs = document.querySelectorAll('[class*="message"]');
                        return msgs[msgs.length-1]?.innerText || null;
                    }
                ''')
                return content
        except Exception as e:
            print(f"Kimi错误: {e}")
        finally:
            await browser.close()
    
    return None


async def scrape_free_image(query: str) -> str:
    """爬取免费图片"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # Unsplash完全免费
            await page.goto(f"https://unsplash.com/s/photos/{query}")
            await page.wait_for_load_state('networkidle')
            
            img = await page.query_selector('img[srcset*="images.unsplash.com"]')
            if img:
                return await img.get_attribute('src')
        except Exception as e:
            print(f"爬取错误: {e}")
        finally:
            await browser.close()
    
    return None


async def main():
    print("=== 免费内容生成 ===\n")
    
    # Kimi生成
    print("Kimi生成...")
    result = await generate_with_kimi("介绍AI智能体")
    print(f"结果: {result[:100] if result else '需要登录'}...")
    
    # 免费图片
    print("\n免费图片...")
    img = await scrape_free_image("technology")
    print(f"图片: {img[:60] if img else '未找到'}...")


if __name__ == "__main__":
    asyncio.run(main())