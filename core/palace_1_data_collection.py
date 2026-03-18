#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1 宫 - 数据采集 · 增强版
Palace 1 - Data Collection · Enhanced

核心能力升级:
1. Crawlee 数据抓取（模拟人类行为，防反爬）
2. 多模式切换（HTTP 快速模式 vs 浏览器渲染模式）
3. 代理 IP 轮换（自动切换 IP 防封禁）
4. 鼠标移动模拟（绕过行为检测）

灵感来源：Crawlee 项目（GitHub 2 万 star）
抖音视频：https://v.douyin.com/zD8x1PSYFgw/
"""

from enum import Enum
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


# ========== 枚举定义 ==========

class CrawlMode(Enum):
    """抓取模式"""
    HTTP_FAST = "http_fast"           # HTTP 快速模式（纯文字）
    BROWSER_RENDER = "browser_render"  # 浏览器渲染模式（图片/视频/JS）


class DataType(Enum):
    """数据类型"""
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    HTML = "html"
    JSON = "json"
    MIXED = "mixed"


# ========== 数据模型 ==========

@dataclass
class CrawlConfig:
    """抓取配置"""
    url: str
    mode: CrawlMode = CrawlMode.HTTP_FAST
    use_proxy: bool = True
    rotate_ip: bool = True
    simulate_human: bool = True
    max_pages: int = 100
    timeout: int = 30


@dataclass
class CrawlResult:
    """抓取结果"""
    success: bool
    url: str
    mode: CrawlMode
    data_type: DataType
    content: Any
    pages_crawled: int
    time_elapsed: float
    ip_rotations: int
    error: Optional[str] = None


# ========== 1 宫数据采集器 ==========

class Palace1DataCollector:
    """
    1 宫数据采集专家（增强版）
    
    核心能力:
    1. Crawlee 数据抓取（模拟人类行为）
    2. 双模式切换（HTTP 快速 / 浏览器渲染）
    3. 代理 IP 轮换（防封禁）
    4. 鼠标移动模拟（绕过行为检测）
    
    灵感来源：Crawlee 项目（GitHub 2 万 star）
    """
    
    # 抓取配置模板
    CRAWL_TEMPLATES = {
        "simple_text": CrawlConfig(
            url="",
            mode=CrawlMode.HTTP_FAST,
            use_proxy=False,
            rotate_ip=False,
            simulate_human=False,
            max_pages=50,
            timeout=30
        ),
        "anti_bot_site": CrawlConfig(
            url="",
            mode=CrawlMode.BROWSER_RENDER,
            use_proxy=True,
            rotate_ip=True,
            simulate_human=True,
            max_pages=100,
            timeout=60
        ),
        "media_rich": CrawlConfig(
            url="",
            mode=CrawlMode.BROWSER_RENDER,
            use_proxy=False,
            rotate_ip=False,
            simulate_human=False,
            max_pages=30,
            timeout=120
        ),
        "large_scale": CrawlConfig(
            url="",
            mode=CrawlMode.HTTP_FAST,
            use_proxy=True,
            rotate_ip=True,
            simulate_human=False,
            max_pages=1000,
            timeout=300
        )
    }
    
    # 代理池配置（示例）
    PROXY_POOLS = {
        "free": [
            "http://proxy1.example.com:8080",
            "http://proxy2.example.com:8080",
        ],
        "paid": [
            "http://premium-proxy1.example.com:8080",
            "http://premium-proxy2.example.com:8080",
        ]
    }
    
    def __init__(self, default_mode: CrawlMode = CrawlMode.HTTP_FAST):
        """
        初始化 1 宫数据采集器
        
        Args:
            default_mode: 默认抓取模式
        """
        self.default_mode = default_mode
        self.crawl_history: List[Dict[str, Any]] = []
        self.ip_rotation_count = 0
    
    def select_template(self, site_type: str) -> CrawlConfig:
        """
        根据网站类型选择抓取模板
        
        Args:
            site_type: 网站类型 (simple_text, anti_bot_site, media_rich, large_scale)
        
        Returns:
            CrawlConfig 配置
        """
        template = self.CRAWL_TEMPLATES.get(site_type, self.CRAWL_TEMPLATES["simple_text"])
        return template
    
    def configure_crawl(
        self,
        url: str,
        mode: Optional[CrawlMode] = None,
        use_proxy: bool = True,
        rotate_ip: bool = True,
        simulate_human: bool = True,
        max_pages: int = 100,
        timeout: int = 60
    ) -> CrawlConfig:
        """
        配置抓取任务
        
        Args:
            url: 目标 URL
            mode: 抓取模式
            use_proxy: 使用代理
            rotate_ip: 轮换 IP
            simulate_human: 模拟人类行为
            max_pages: 最大页数
            timeout: 超时时间（秒）
        
        Returns:
            CrawlConfig 配置
        """
        return CrawlConfig(
            url=url,
            mode=mode or self.default_mode,
            use_proxy=use_proxy,
            rotate_ip=rotate_ip,
            simulate_human=simulate_human,
            max_pages=max_pages,
            timeout=timeout
        )
    
    def execute_crawl(self, config: CrawlConfig) -> CrawlResult:
        """
        执行抓取（模拟实现）
        
        实际实现需要集成 Crawlee 库:
        ```python
        from crawlee.playwright_crawler import PlaywrightCrawler
        
        crawler = PlaywrightCrawler(
            max_requests_per_crawl=config.max_pages,
            headless=True,
            proxy=config.use_proxy,
        )
        
        # 模拟人类行为
        if config.simulate_human:
            crawler.pre_navigation_hooks.append(self._simulate_mouse_movement)
        
        # IP 轮换
        if config.rotate_ip:
            crawler.proxy_configuration = self._get_next_proxy()
        
        # 执行抓取
        result = await crawler.run([config.url])
        ```
        
        Args:
            config: 抓取配置
        
        Returns:
            CrawlResult 结果
        """
        # 模拟执行
        import random
        import time
        
        start_time = time.time()
        
        # 模拟 IP 轮换
        ip_rotations = 0
        if config.rotate_ip:
            ip_rotations = max(1, config.max_pages // 20)
            self.ip_rotation_count += ip_rotations
        
        # 模拟抓取时间
        base_time = 2.0 if config.mode == CrawlMode.HTTP_FAST else 10.0
        elapsed = base_time * (config.max_pages / 10)
        
        # 模拟成功率
        success_rate = 0.95 if config.simulate_human else 0.8
        success = random.random() < success_rate
        
        return CrawlResult(
            success=success,
            url=config.url,
            mode=config.mode,
            data_type=DataType.MIXED if config.mode == CrawlMode.BROWSER_RENDER else DataType.TEXT,
            content=f"模拟抓取内容：{config.url}",
            pages_crawled=min(config.max_pages, random.randint(50, 100)),
            time_elapsed=elapsed,
            ip_rotations=ip_rotations,
            error=None if success else "模拟失败：网站反爬检测"
        )
    
    def _simulate_mouse_movement(self):
        """模拟鼠标移动（防检测）"""
        # Crawlee 实现
        pass
    
    def _get_next_proxy(self) -> str:
        """获取下一个代理 IP"""
        # 代理池轮换逻辑
        return self.PROXY_POOLS["free"][0] if self.PROXY_POOLS["free"] else ""
    
    def get_mode_comparison(self) -> Dict[str, Any]:
        """
        获取模式对比
        
        Returns:
            HTTP 快速模式 vs 浏览器渲染模式 对比
        """
        return {
            "http_fast": {
                "mode": CrawlMode.HTTP_FAST.value,
                "speed": "极快",
                "suitable_for": ["简单文字信息", "结构化数据", "API 接口"],
                "limitations": ["无法渲染 JS", "无法获取图片/视频"],
                "proxy_recommended": True
            },
            "browser_render": {
                "mode": CrawlMode.BROWSER_RENDER.value,
                "speed": "较慢",
                "suitable_for": ["图片", "视频", "复杂 JavaScript 脚本", "动态内容"],
                "limitations": ["速度慢", "资源消耗大"],
                "proxy_recommended": True
            },
            "recommendation": "简单文字用 HTTP 模式，复杂内容用浏览器模式"
        }
    
    def get_anti_block_features(self) -> List[Dict[str, Any]]:
        """
        获取防封禁特性列表
        
        Returns:
            防封禁特性
        """
        return [
            {
                "feature": "模拟人类鼠标移动",
                "description": "让网站看起来像正常用户在浏览",
                "effectiveness": "高"
            },
            {
                "feature": "代理 IP 轮换",
                "description": "配合代理池自动切换 IP 地址",
                "effectiveness": "极高",
                "analogy": "100 个穿不同衣服的人轮流进去拿货"
            },
            {
                "feature": "请求频率控制",
                "description": "自动限制请求速度，避免触发反爬",
                "effectiveness": "中"
            },
            {
                "feature": "User-Agent 轮换",
                "description": "模拟不同浏览器和设备",
                "effectiveness": "中"
            },
            {
                "feature": "Cookie 管理",
                "description": "自动处理会话和登录状态",
                "effectiveness": "高"
            }
        ]
    
    def record_crawl(self, result: CrawlResult, task_id: str):
        """记录抓取历史"""
        self.crawl_history.append({
            "task_id": task_id,
            "url": result.url,
            "mode": result.mode.value,
            "success": result.success,
            "pages_crawled": result.pages_crawled,
            "time_elapsed": result.time_elapsed,
            "ip_rotations": result.ip_rotations,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_crawl_report(self) -> Dict[str, Any]:
        """生成抓取报告"""
        if not self.crawl_history:
            return {"message": "暂无抓取记录"}
        
        total_tasks = len(self.crawl_history)
        success_count = sum(1 for r in self.crawl_history if r["success"])
        total_pages = sum(r["pages_crawled"] for r in self.crawl_history)
        total_time = sum(r["time_elapsed"] for r in self.crawl_history)
        
        return {
            "total_tasks": total_tasks,
            "success_rate": success_count / total_tasks if total_tasks > 0 else 0,
            "total_pages_crawled": total_pages,
            "total_time_seconds": total_time,
            "avg_pages_per_task": total_pages / total_tasks if total_tasks > 0 else 0,
            "total_ip_rotations": self.ip_rotation_count,
            "http_fast_tasks": sum(1 for r in self.crawl_history if r["mode"] == "http_fast"),
            "browser_render_tasks": sum(1 for r in self.crawl_history if r["mode"] == "browser_render")
        }


# ========== 导出给 L4 引擎使用 ==========

# 全局 1 宫采集器实例
_palace1_collector: Optional[Palace1DataCollector] = None


def get_palace1_collector() -> Palace1DataCollector:
    """获取 1 宫采集器单例"""
    global _palace1_collector
    if _palace1_collector is None:
        _palace1_collector = Palace1DataCollector()
    return _palace1_collector


def palace1_configure_crawl(
    url: str,
    site_type: str = "simple_text",
    mode: str = "http_fast"
) -> Dict[str, Any]:
    """
    1 宫配置抓取（供 L4 引擎调用）
    
    Returns:
        抓取配置字典
    """
    collector = get_palace1_collector()
    
    # 根据网站类型选择模板
    config = collector.select_template(site_type)
    config.url = url
    
    # 模式覆盖
    if mode == "browser_render":
        config.mode = CrawlMode.BROWSER_RENDER
    
    return {
        "url": config.url,
        "mode": config.mode.value,
        "use_proxy": config.use_proxy,
        "rotate_ip": config.rotate_ip,
        "simulate_human": config.simulate_human,
        "max_pages": config.max_pages,
        "timeout": config.timeout
    }


def palace1_get_mode_comparison() -> Dict[str, Any]:
    """获取模式对比（供 L4 引擎调用）"""
    return get_palace1_collector().get_mode_comparison()


def palace1_get_anti_block_features() -> List[Dict[str, Any]]:
    """获取防封禁特性（供 L4 引擎调用）"""
    return get_palace1_collector().get_anti_block_features()


def palace1_get_crawl_report() -> Dict[str, Any]:
    """获取抓取报告（供 L4 引擎调用）"""
    return get_palace1_collector().get_crawl_report()


def palace1_execute_crawl(url: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行抓取（供 L4 引擎调用）
    
    Returns:
        抓取结果字典
    """
    collector = get_palace1_collector()
    
    crawl_config = CrawlConfig(
        url=url,
        mode=CrawlMode(config.get("mode", "http_fast")),
        use_proxy=config.get("use_proxy", True),
        rotate_ip=config.get("rotate_ip", True),
        simulate_human=config.get("simulate_human", True),
        max_pages=config.get("max_pages", 100),
        timeout=config.get("timeout", 60)
    )
    
    result = collector.execute_crawl(crawl_config)
    collector.record_crawl(result, f"crawl_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    
    return {
        "success": result.success,
        "url": result.url,
        "mode": result.mode.value,
        "data_type": result.data_type.value,
        "pages_crawled": result.pages_crawled,
        "time_elapsed": result.time_elapsed,
        "ip_rotations": result.ip_rotations,
        "error": result.error
    }
