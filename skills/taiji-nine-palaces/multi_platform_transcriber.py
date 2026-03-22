#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多平台视频转录器 - 并发处理
Multi-Platform Video Transcriber - Concurrent Processing

支持平台：
- 抖音（备用：飞书妙记、通义听悟）
- 视频号（备用：Kimi 总结）
- 小红书（Jina、Kimi）
- B 站（Jina、B 站 API）
- YouTube（Jina、YouTube API）
"""

import subprocess
import time
import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


class MultiPlatformTranscriber:
    """
    多平台视频转录器
    
    特点：
    - 多平台支持
    - 并发处理
    - 自动降级（主服务失败时用备用）
    - 成本优化
    """
    
    def __init__(self, output_dir: str = None, max_workers: int = 3):
        """
        初始化
        
        Args:
            output_dir: 输出目录
            max_workers: 最大并发数
        """
        self.output_dir = Path(output_dir) if output_dir else Path("/root/.openclaw/workspace/content/videos")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.max_workers = max_workers
        
        # 平台服务配置（主服务 + 备用）
        self.platform_services = {
            "douyin": {
                "name": "抖音",
                "primary": "jina",
                "fallbacks": ["feishu_miaoji", "kimi", "tingwu"],
                "notes": "Jina 可能限流，备用飞书妙记",
            },
            "wechat_channels": {
                "name": "视频号",
                "primary": "kimi",
                "fallbacks": ["feishu_miaoji"],
                "notes": "微信生态封闭，用 Kimi 总结",
            },
            "xiaohongshu": {
                "name": "小红书",
                "primary": "jina",
                "fallbacks": ["kimi"],
                "notes": "Jina 通常可用",
            },
            "bilibili": {
                "name": "B 站",
                "primary": "jina",
                "fallbacks": ["bili_api", "kimi"],
                "notes": "B 站有官方 API 可提取字幕",
            },
            "youtube": {
                "name": "YouTube",
                "primary": "jina",
                "fallbacks": ["youtube_api", "kimi"],
                "notes": "YouTube API 可提取字幕",
            },
        }
        
        # 服务成本（每视频估算）- 优先免费
        self.service_costs = {
            "jina": 0.0,  # 免费 ✅ 优先
            "kimi": 0.0,  # 免费额度内 ✅
            "feishu_miaoji": 0.0,  # 免费额度内 ✅
            "tingwu": 0.0,  # 免费额度内 ✅
            "bili_api": 0.0,  # 免费 ✅
            "youtube_api": 0.0,  # 免费额度内 ✅
            "qwen_plus": 0.008,  # 付费，最后选择
            "qwen_max": 0.04,  # 付费，避免使用
        }
        
        # 成本上限（默认只用免费服务）
        self.cost_limit = 0.0  # 0 = 只用免费
    
    def transcribe(self, video_url: str, platform: str = None,
                   use_fallback: bool = True, respect_cost_limit: bool = True) -> Dict[str, Any]:
        """
        转录视频（自动选择服务）
        
        Args:
            video_url: 视频链接
            platform: 平台名称（可选，自动检测）
            use_fallback: 是否使用备用服务
        
        Returns:
            转录结果
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 自动检测平台
        if not platform:
            platform = self._detect_platform(video_url)
        
        result = {
            "success": False,
            "video_url": video_url,
            "platform": platform,
            "service_used": None,
            "transcript": "",
            "summary": "",
            "output_files": [],
            "cost": 0.0,
            "steps": [],
        }
        
        # 获取服务配置
        service_config = self.platform_services.get(platform)
        if not service_config:
            result["error"] = f"不支持的平台：{platform}"
            return result
        
        # 尝试主服务
        services_to_try = [service_config["primary"]]
        if use_fallback:
            services_to_try.extend(service_config["fallbacks"])
        
        self._log(f"平台：{platform}, 尝试服务：{services_to_try}")
        
        # 依次尝试服务（遵守成本限制）
        for service in services_to_try:
            # 检查成本
            if respect_cost_limit and self.service_costs.get(service, 0.0) > self.cost_limit:
                self._log(f"⚠️ 跳过 {service}（成本¥{self.service_costs[service]} > 限制¥{self.cost_limit}）")
                continue
            
            self._log(f"尝试使用 {service}...")
            
            try:
                if service == "jina":
                    service_result = self._try_jina(video_url, timestamp)
                elif service == "kimi":
                    service_result = self._try_kimi(video_url, timestamp)
                elif service == "feishu_miaoji":
                    service_result = self._try_feishu(video_url, timestamp)
                elif service == "tingwu":
                    service_result = self._try_tingwu(video_url, timestamp)
                elif service == "bili_api":
                    service_result = self._try_bili_api(video_url, timestamp)
                elif service == "youtube_api":
                    service_result = self._try_youtube_api(video_url, timestamp)
                else:
                    service_result = {"success": False, "error": f"未知服务：{service}"}
                
                if service_result.get("success"):
                    # 成功
                    result.update(service_result)
                    result["success"] = True
                    result["service_used"] = service
                    result["cost"] = self.service_costs.get(service, 0.0)
                    result["steps"].append({"service": service, "status": "success"})
                    self._log(f"✅ {service} 成功")
                    break
                else:
                    # 失败，尝试下一个
                    self._log(f"❌ {service} 失败：{service_result.get('error', '未知')}")
                    result["steps"].append({"service": service, "status": "failed", "error": service_result.get("error")})
            
            except Exception as e:
                self._log(f"❌ {service} 异常：{e}")
                result["steps"].append({"service": service, "status": "error", "error": str(e)})
        
        if not result["success"]:
            result["error"] = "所有服务都失败了"
        
        return result
    
    def batch_transcribe(self, video_urls: List[str], 
                        concurrent: bool = True) -> List[Dict[str, Any]]:
        """
        批量转录视频
        
        Args:
            video_urls: 视频链接列表
            concurrent: 是否并发处理
        
        Returns:
            结果列表
        """
        if not concurrent:
            # 串行处理
            results = []
            for i, url in enumerate(video_urls):
                self._log(f"\n[{i+1}/{len(video_urls)}] 处理：{url}")
                result = self.transcribe(url)
                results.append(result)
                time.sleep(1)  # 避免限流
            return results
        
        # 并发处理
        self._log(f"\n开始并发处理 {len(video_urls)} 个视频（最大并发：{self.max_workers}）")
        
        results = [None] * len(video_urls)
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_index = {
                executor.submit(self.transcribe, url): i
                for i, url in enumerate(video_urls)
            }
            
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    result = future.result()
                    results[index] = result
                    self._log(f"[{index+1}/{len(video_urls)}] 完成：{result['platform']} - {'✅' if result['success'] else '❌'}")
                except Exception as e:
                    self._log(f"[{index+1}/{len(video_urls)}] 异常：{e}")
                    results[index] = {
                        "success": False,
                        "video_url": video_urls[index],
                        "error": str(e),
                    }
        
        return results
    
    def _detect_platform(self, url: str) -> str:
        """检测视频平台"""
        if "douyin.com" in url or "iesdouyin.com" in url:
            return "douyin"
        elif "channels.weixin.qq.com" in url:
            return "wechat_channels"
        elif "xiaohongshu.com" in url or "xhslink.com" in url:
            return "xiaohongshu"
        elif "bilibili.com" in url or "b23.tv" in url:
            return "bilibili"
        elif "youtube.com" in url or "youtu.be" in url:
            return "youtube"
        else:
            return "unknown"
    
    def _try_jina(self, url: str, timestamp: str) -> Dict[str, Any]:
        """尝试 Jina Reader"""
        jina_url = f"https://r.jina.ai/{url}"
        
        try:
            result = subprocess.run(
                f'curl -s --max-time 30 "{jina_url}"',
                shell=True,
                capture_output=True,
                text=True,
                timeout=35
            )
            
            if result.returncode == 0 and result.stdout.strip():
                # 检查是否错误
                if "SecurityCompromiseError" in result.stdout or "DDoS attack" in result.stdout:
                    return {"success": False, "error": "Jina 限流"}
                
                transcript = result.stdout.strip()
                output_file = self.output_dir / f"jina_{timestamp}.md"
                output_file.write_text(transcript, encoding="utf-8")
                
                return {
                    "success": True,
                    "transcript": transcript,
                    "output_files": [str(output_file)],
                }
            else:
                return {"success": False, "error": "Jina 无返回"}
        
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Jina 超时"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _try_kimi(self, url: str, timestamp: str) -> Dict[str, Any]:
        """尝试 Kimi 总结"""
        from browser_automation import KimiPDFGenerator
        
        generator = KimiPDFGenerator(output_dir=str(self.output_dir))
        
        prompt = f"""请帮我总结这个视频的内容：

视频链接：{url}

请提供：
1. 视频主要内容概述（300 字）
2. 关键观点/知识点列表
3.  actionable 建议或结论

如果无法访问链接，请告知。
"""
        
        result = generator.generate_report(
            prompt=prompt,
            title=f"video_kimi_{timestamp}",
            wait_seconds=30,
        )
        
        if result["success"]:
            return {
                "success": True,
                "summary": f"PDF: {result['pdf_path']}",
                "output_files": result.get("output_files", [result["pdf_path"]]),
            }
        else:
            return {"success": False, "error": result.get("error", "Kimi 失败")}
    
    def _try_feishu(self, url: str, timestamp: str) -> Dict[str, Any]:
        """尝试飞书妙记（需要实现 API 调用）"""
        # TODO: 实现飞书妙记 API
        return {"success": False, "error": "飞书妙记 API 待实现"}
    
    def _try_tingwu(self, url: str, timestamp: str) -> Dict[str, Any]:
        """尝试通义听悟（需要实现 API 调用）"""
        # TODO: 实现通义听悟 API
        return {"success": False, "error": "通义听悟 API 待实现"}
    
    def _try_bili_api(self, url: str, timestamp: str) -> Dict[str, Any]:
        """尝试 B 站 API 提取字幕"""
        # TODO: 实现 B 站 API
        return {"success": False, "error": "B 站 API 待实现"}
    
    def _try_youtube_api(self, url: str, timestamp: str) -> Dict[str, Any]:
        """尝试 YouTube API 提取字幕"""
        # TODO: 实现 YouTube API
        return {"success": False, "error": "YouTube API 待实现"}
    
    def _log(self, message: str):
        """日志输出"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def get_status_report(self) -> Dict[str, Any]:
        """获取服务状态报告"""
        return {
            "platforms": self.platform_services,
            "costs": self.service_costs,
            "output_dir": str(self.output_dir),
            "max_workers": self.max_workers,
        }


def demo():
    """演示"""
    print("="*60)
    print("        多平台视频转录器演示")
    print("="*60)
    
    transcriber = MultiPlatformTranscriber(max_workers=2)
    
    # 测试用例
    test_urls = [
        ("https://www.bilibili.com/video/BV1xx411c7mD", "bilibili"),
        ("https://www.xiaohongshu.com/explore/xxx", "xiaohongshu"),
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "youtube"),
    ]
    
    print("\n【并发处理测试】\n")
    
    urls_only = [url for url, _ in test_urls]
    results = transcriber.batch_transcribe(urls_only, concurrent=True)
    
    print("\n" + "="*60)
    print("处理结果:\n")
    
    for i, result in enumerate(results):
        status = "✅" if result["success"] else "❌"
        print(f"{i+1}. {status} {result.get('platform', 'unknown')}")
        print(f"   服务：{result.get('service_used', 'N/A')}")
        print(f"   成本：¥{result.get('cost', 0):.4f}")
        if result.get("output_files"):
            print(f"   文件：{result['output_files'][0]}")
        if result.get("error"):
            print(f"   错误：{result['error']}")
        print()
    
    # 服务状态
    print("\n【服务状态】\n")
    status = transcriber.get_status_report()
    for platform, config in status["platforms"].items():
        print(f"{config['name']}: {config['primary']} (备用：{', '.join(config['fallbacks'])})")
    
    print("="*60)


if __name__ == "__main__":
    demo()
