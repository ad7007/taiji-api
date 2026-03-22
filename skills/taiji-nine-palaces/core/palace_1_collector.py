#!/usr/bin/env python3
"""
1 宫 - 数据采集核心

职责：
1. 视频下载（抖音、B站、YouTube、小红书）
2. 文件下载（任意URL）
3. 网页抓取（内容提取）
4. API数据采集

自动组队：1宫采集 → 7宫验收 → 5宫交付
"""

import os
import sys
import json
import subprocess
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class CollectionResult:
    """采集结果"""
    success: bool
    source_type: str  # video/file/web/api
    source_url: str
    output_path: Optional[str] = None
    output_content: Optional[str] = None
    metadata: Dict = field(default_factory=dict)
    error: Optional[str] = None
    collected_at: datetime = field(default_factory=datetime.now)


class Palace1Collector:
    """
    1 宫 - 数据采集器
    
    使用示例:
        collector = Palace1Collector()
        
        # 下载视频
        result = collector.download_video("https://v.douyin.com/xxx")
        
        # 下载文件
        result = collector.download_file("https://example.com/data.json")
        
        # 抓取网页
        result = collector.scrape_web("https://example.com/article")
    """
    
    def __init__(self, output_dir: Optional[str] = None):
        self.palace_id = 1
        self.palace_name = "数据采集"
        
        # 输出目录
        self.output_dir = Path(output_dir or "/root/.openclaw/workspace/downloads")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 采集历史
        self.history: List[CollectionResult] = []
        
        # 支持的平台
        self.video_platforms = {
            "douyin": ["douyin.com", "v.douyin.com"],
            "bilibili": ["bilibili.com", "b23.tv"],
            "youtube": ["youtube.com", "youtu.be"],
            "xiaohongshu": ["xiaohongshu.com", "xhslink.com"]
        }
    
    # ========== 视频下载 ==========
    
    def download_video(self, url: str, 
                      output_name: Optional[str] = None,
                      format: str = "best") -> CollectionResult:
        """
        下载视频 - 支持抖音、B站、YouTube、小红书
        
        Args:
            url: 视频URL
            output_name: 输出文件名（不含扩展名）
            format: 视频格式 (best/bestvideo/bestaudio)
        
        Returns:
            CollectionResult
        """
        # 检测平台
        platform = self._detect_platform(url)
        
        # 生成输出文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = output_name or f"video_{timestamp}"
        
        # 输出路径
        output_path = self.output_dir / "videos" / platform
        output_path.mkdir(parents=True, exist_ok=True)
        
        try:
            # 使用 yt-dlp 下载
            cmd = [
                "yt-dlp",
                "-f", format,
                "-o", str(output_path / f"{output_name}.%(ext)s"),
                "--no-playlist",
                "--quiet",
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                # 查找下载的文件
                downloaded_files = list(output_path.glob(f"{output_name}.*"))
                
                if downloaded_files:
                    actual_path = str(downloaded_files[0])
                    
                    collection_result = CollectionResult(
                        success=True,
                        source_type="video",
                        source_url=url,
                        output_path=actual_path,
                        metadata={
                            "platform": platform,
                            "format": format,
                            "file_size": os.path.getsize(actual_path)
                        }
                    )
                else:
                    raise Exception("下载成功但未找到文件")
            else:
                raise Exception(result.stderr or "yt-dlp 下载失败")
        
        except FileNotFoundError:
            collection_result = CollectionResult(
                success=False,
                source_type="video",
                source_url=url,
                error="yt-dlp 未安装，请运行: pip install yt-dlp"
            )
        except Exception as e:
            collection_result = CollectionResult(
                success=False,
                source_type="video",
                source_url=url,
                error=str(e)
            )
        
        self.history.append(collection_result)
        return collection_result
    
    # ========== 文件下载 ==========
    
    def download_file(self, url: str,
                     output_name: Optional[str] = None,
                     timeout: int = 60) -> CollectionResult:
        """
        下载文件 - 支持任意URL
        
        Args:
            url: 文件URL
            output_name: 输出文件名
            timeout: 超时时间（秒）
        
        Returns:
            CollectionResult
        """
        # 从URL提取文件名
        if not output_name:
            output_name = url.split("/")[-1].split("?")[0]
            if not output_name or "." not in output_name:
                output_name = f"file_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        output_path = self.output_dir / "files"
        output_path.mkdir(parents=True, exist_ok=True)
        
        full_path = output_path / output_name
        
        try:
            response = requests.get(url, timeout=timeout, stream=True)
            response.raise_for_status()
            
            with open(full_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            collection_result = CollectionResult(
                success=True,
                source_type="file",
                source_url=url,
                output_path=str(full_path),
                metadata={
                    "file_size": os.path.getsize(full_path),
                    "content_type": response.headers.get("content-type", "unknown")
                }
            )
        
        except Exception as e:
            collection_result = CollectionResult(
                success=False,
                source_type="file",
                source_url=url,
                error=str(e)
            )
        
        self.history.append(collection_result)
        return collection_result
    
    # ========== 网页抓取 ==========
    
    def scrape_web(self, url: str,
                   extract_mode: str = "text") -> CollectionResult:
        """
        抓取网页内容
        
        Args:
            url: 网页URL
            extract_mode: 提取模式 (text/markdown/html)
        
        Returns:
            CollectionResult
        """
        try:
            # 尝试使用 web_fetch 工具
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            content = response.text
            
            # 简单提取文本
            if extract_mode in ["text", "markdown"]:
                # 移除HTML标签（简化版）
                import re
                text = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
                text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
                text = re.sub(r'<[^>]+>', ' ', text)
                text = re.sub(r'\s+', ' ', text).strip()
                content = text
            
            collection_result = CollectionResult(
                success=True,
                source_type="web",
                source_url=url,
                output_content=content,
                metadata={
                    "extract_mode": extract_mode,
                    "content_length": len(content)
                }
            )
        
        except Exception as e:
            collection_result = CollectionResult(
                success=False,
                source_type="web",
                source_url=url,
                error=str(e)
            )
        
        self.history.append(collection_result)
        return collection_result
    
    # ========== API 采集 ==========
    
    def fetch_api(self, url: str,
                  method: str = "GET",
                  headers: Optional[Dict] = None,
                  params: Optional[Dict] = None,
                  data: Optional[Dict] = None) -> CollectionResult:
        """
        采集 API 数据
        
        Args:
            url: API URL
            method: HTTP方法 (GET/POST/PUT/DELETE)
            headers: 请求头
            params: URL参数
            data: 请求体数据
        
        Returns:
            CollectionResult
        """
        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=headers or {},
                params=params,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            json_data = response.json()
            
            collection_result = CollectionResult(
                success=True,
                source_type="api",
                source_url=url,
                output_content=json.dumps(json_data, ensure_ascii=False, indent=2),
                metadata={
                    "method": method,
                    "status_code": response.status_code,
                    "response_time_ms": response.elapsed.total_seconds() * 1000
                }
            )
        
        except Exception as e:
            collection_result = CollectionResult(
                success=False,
                source_type="api",
                source_url=url,
                error=str(e)
            )
        
        self.history.append(collection_result)
        return collection_result
    
    # ========== 工具方法 ==========
    
    def _detect_platform(self, url: str) -> str:
        """检测视频平台"""
        url_lower = url.lower()
        for platform, domains in self.video_platforms.items():
            if any(domain in url_lower for domain in domains):
                return platform
        return "unknown"
    
    def get_stats(self) -> Dict[str, Any]:
        """获取采集统计"""
        if not self.history:
            return {
                "total": 0,
                "success": 0,
                "failed": 0,
                "by_type": {}
            }
        
        success_count = sum(1 for r in self.history if r.success)
        by_type = {}
        
        for r in self.history:
            source_type = r.source_type
            if source_type not in by_type:
                by_type[source_type] = {"total": 0, "success": 0}
            by_type[source_type]["total"] += 1
            if r.success:
                by_type[source_type]["success"] += 1
        
        return {
            "total": len(self.history),
            "success": success_count,
            "failed": len(self.history) - success_count,
            "success_rate": success_count / len(self.history),
            "by_type": by_type
        }
    
    def clear_history(self):
        """清空历史记录"""
        self.history = []


# ========== 全局实例 ==========

_collector_instance = None

def get_collector() -> Palace1Collector:
    """获取全局采集器实例"""
    global _collector_instance
    if _collector_instance is None:
        _collector_instance = Palace1Collector()
    return _collector_instance


# ========== 快捷函数 ==========

def download_video(url: str, **kwargs) -> CollectionResult:
    """快捷函数：下载视频"""
    return get_collector().download_video(url, **kwargs)

def download_file(url: str, **kwargs) -> CollectionResult:
    """快捷函数：下载文件"""
    return get_collector().download_file(url, **kwargs)

def scrape_web(url: str, **kwargs) -> CollectionResult:
    """快捷函数：抓取网页"""
    return get_collector().scrape_web(url, **kwargs)

def fetch_api(url: str, **kwargs) -> CollectionResult:
    """快捷函数：采集API"""
    return get_collector().fetch_api(url, **kwargs)


# ========== 测试 ==========

if __name__ == "__main__":
    print("=== 1 宫数据采集测试 ===\n")
    
    collector = Palace1Collector()
    
    # 测试1: 文件下载
    print("1. 测试文件下载:")
    result = collector.download_file(
        "https://httpbin.org/json",
        output_name="test_api.json"
    )
    print(f"   成功: {result.success}")
    if result.success:
        print(f"   路径: {result.output_path}")
    else:
        print(f"   错误: {result.error}")
    
    # 测试2: 网页抓取
    print("\n2. 测试网页抓取:")
    result = collector.scrape_web("https://httpbin.org/html")
    print(f"   成功: {result.success}")
    if result.success:
        print(f"   内容长度: {len(result.output_content)} 字符")
    
    # 测试3: API采集
    print("\n3. 测试 API 采集:")
    result = collector.fetch_api("https://httpbin.org/get", params={"test": "value"})
    print(f"   成功: {result.success}")
    if result.success:
        print(f"   响应时间: {result.metadata.get('response_time_ms', 0):.1f}ms")
    
    # 测试4: 统计
    print("\n4. 采集统计:")
    stats = collector.get_stats()
    print(f"   总计: {stats['total']}")
    print(f"   成功率: {stats['success_rate']:.1%}")
    
    print("\n=== 1 宫就绪 ===")