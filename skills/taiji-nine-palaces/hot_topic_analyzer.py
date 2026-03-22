#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多平台热点搜索与分析器
Hot Topic Analyzer - 抖音/视频号/小红书/B 站热点数据分析
"""

import subprocess
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import re


class HotTopicAnalyzer:
    """
    热点搜索与分析器
    
    支持平台：
    - 抖音热榜
    - 小红书热榜
    - B 站热榜
    - 微博热搜
    - 知乎热榜
    - 微信视频号
    
    功能：
    - 关键词搜索热点
    - 生成 TOP9 热点标题排名
    - 数据分析（热度/趋势/相关性）
    """
    
    def __init__(self, output_dir: str = None):
        """
        初始化
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = Path(output_dir) if output_dir else Path("/root/.openclaw/workspace/content/hot_topics")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 平台热榜 API（优先使用备用 API，避免 Jina 限流）
        self.platform_apis = {
            "douyin": {
                "name": "抖音热榜",
                "primary": "https://api.vvhan.com/api/hotlist/douyin",
                "backup": "https://uapis.cn/api.php?msg=douyin",
            },
            "xiaohongshu": {
                "name": "小红书热榜",
                "primary": "https://api.vvhan.com/api/hotlist/xiaohongshu",
                "backup": "https://uapis.cn/api.php?msg=xiaohongshu",
            },
            "bilibili": {
                "name": "B 站热榜",
                "primary": "https://api.vvhan.com/api/hotlist/bilibili",
                "backup": "https://uapis.cn/api.php?msg=bilibili",
            },
            "weibo": {
                "name": "微博热搜",
                "primary": "https://api.vvhan.com/api/hotlist/weibo",
                "backup": "https://uapis.cn/api.php?msg=weibo",
            },
            "zhihu": {
                "name": "知乎热榜",
                "primary": "https://api.vvhan.com/api/hotlist/zhihu",
                "backup": "https://uapis.cn/api.php?msg=zhihu",
            },
            "wechat_channels": {
                "name": "微信视频号",
                "primary": "kimi_search",  # 用 Kimi 搜索
                "backup": "manual",
            },
        }
        
        # 聚合 API（推荐）
        self.aggregator_apis = {
            "vvhan": "https://api.vvhan.com/api/hotlist/{platform}",
            "alapi": "https://v2.alapi.cn/api/tophub/get",  # 需要 token
            "uapis": "https://uapis.cn/api.php?msg={platform}",
        }
    
    def search_hot_topics(self, keyword: str, platforms: List[str] = None,
                          top_n: int = 9) -> Dict[str, Any]:
        """
        搜索热点话题
        
        Args:
            keyword: 搜索关键词
            platforms: 平台列表（默认全部）
            top_n: 返回 TOP N 个热点
        
        Returns:
            热点数据分析结果
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        result = {
            "success": False,
            "keyword": keyword,
            "timestamp": timestamp,
            "platforms": platforms or list(self.platform_apis.keys()),
            "top_topics": [],
            "analysis": {},
            "output_files": [],
        }
        
        try:
            # 1. 收集各平台热榜
            self._log(f"开始搜索关键词：{keyword}")
            all_topics = self._collect_hot_topics(result["platforms"])
            
            # 2. 筛选相关热点
            relevant_topics = self._filter_by_keyword(all_topics, keyword)
            
            # 3. 排序并取 TOP9
            top_topics = self._rank_topics(relevant_topics, top_n)
            
            # 4. 生成数据分析
            analysis = self._generate_analysis(top_topics, keyword)
            
            result["top_topics"] = top_topics
            result["analysis"] = analysis
            result["success"] = True
            
            # 5. 保存结果
            report_file = self._save_report(result)
            result["output_files"].append(str(report_file))
            
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def _collect_hot_topics(self, platforms: List[str]) -> List[Dict]:
        """收集各平台热榜"""
        all_topics = []
        
        for platform in platforms:
            self._log(f"收集 {platform} 热榜...")
            
            try:
                platform_data = self._fetch_platform_hotlist(platform)
                if platform_data:
                    all_topics.extend(platform_data)
            except Exception as e:
                self._log(f"❌ {platform} 失败：{e}")
        
        return all_topics
    
    def _fetch_platform_hotlist(self, platform: str) -> List[Dict]:
        """获取单个平台热榜"""
        api_config = self.platform_apis.get(platform)
        if not api_config:
            return []
        
        # 尝试主 API
        try:
            data = self._fetch_url(api_config.get("primary", ""))
            if data and self._is_valid_response(data):
                return self._parse_hotlist(data, platform)
        except:
            pass
        
        # 尝试备用 API
        if "backup" in api_config and api_config["backup"] not in ["manual", "kimi_search"]:
            try:
                data = self._fetch_url(api_config["backup"])
                if data and self._is_valid_response(data):
                    return self._parse_hotlist(data, platform)
            except:
                pass
        
        return []
    
    def _is_valid_response(self, data: str) -> bool:
        """检查响应是否有效"""
        if not data:
            return False
        if "SecurityCompromiseError" in data or "DDoS attack" in data:
            return False
        try:
            json_data = json.loads(data)
            return "data" in json_data or json_data.get("code") == 200
        except:
            return len(data) > 50
    
    def _fetch_url(self, url: str) -> Optional[str]:
        """获取 URL 内容"""
        if url.startswith("https://api."):
            # API 直接返回 JSON
            result = subprocess.run(
                f'curl -s --max-time 10 "{url}"',
                shell=True,
                capture_output=True,
                text=True,
                timeout=15
            )
            return result.stdout if result.returncode == 0 else None
        else:
            # Jina Reader
            result = subprocess.run(
                f'curl -s --max-time 10 "{url}"',
                shell=True,
                capture_output=True,
                text=True,
                timeout=15
            )
            return result.stdout if result.returncode == 0 else None
    
    def _parse_hotlist(self, data: str, platform: str) -> List[Dict]:
        """解析热榜数据"""
        topics = []
        
        try:
            # 尝试解析 JSON（API 返回）
            json_data = json.loads(data)
            
            if "data" in json_data:
                items = json_data["data"]
                for i, item in enumerate(items[:50], 1):
                    topics.append({
                        "platform": platform,
                        "rank": i,
                        "title": item.get("title", ""),
                        "hot_value": item.get("hot", item.get("hot_value", 0)),
                        "url": item.get("url", item.get("link", "")),
                        "raw_data": item,
                    })
        except:
            # 尝试解析 Markdown（Jina 返回）
            lines = data.strip().split("\n")
            rank = 1
            for line in lines:
                if line.strip() and rank <= 50:
                    topics.append({
                        "platform": platform,
                        "rank": rank,
                        "title": line.strip(),
                        "hot_value": 0,
                        "url": "",
                        "raw_data": {"text": line},
                    })
                    rank += 1
        
        return topics
    
    def _filter_by_keyword(self, topics: List[Dict], keyword: str) -> List[Dict]:
        """按关键词筛选热点"""
        filtered = []
        
        for topic in topics:
            title = topic.get("title", "").lower()
            keyword_lower = keyword.lower()
            
            # 计算相关性
            relevance = self._calculate_relevance(title, keyword_lower)
            
            if relevance > 0:
                topic["relevance"] = relevance
                filtered.append(topic)
        
        return filtered
    
    def _calculate_relevance(self, text: str, keyword: str) -> float:
        """计算相关性分数"""
        score = 0.0
        
        # 完全匹配
        if keyword in text:
            score += 1.0
        
        # 分词匹配
        keyword_words = keyword.split()
        for word in keyword_words:
            if word in text:
                score += 0.3
        
        # 关键词长度占比
        if len(keyword) > 2:
            overlap = len(set(keyword) & set(text)) / max(len(keyword), len(text))
            score += overlap * 0.5
        
        return min(score, 3.0)  # 最高 3 分
    
    def _rank_topics(self, topics: List[Dict], top_n: int) -> List[Dict]:
        """排序并取 TOP N"""
        # 综合评分 = 相关性 * 热度
        for topic in topics:
            hot_score = topic.get("hot_value", 0) / 1000000  # 归一化
            relevance = topic.get("relevance", 0)
            topic["composite_score"] = relevance * (1 + hot_score)
        
        # 排序
        sorted_topics = sorted(topics, key=lambda x: x.get("composite_score", 0), reverse=True)
        
        return sorted_topics[:top_n]
    
    def _generate_analysis(self, topics: List[Dict], keyword: str) -> Dict[str, Any]:
        """生成数据分析"""
        if not topics:
            return {"error": "无相关热点"}
        
        analysis = {
            "total_found": len(topics),
            "platform_distribution": {},
            "avg_relevance": sum(t.get("relevance", 0) for t in topics) / len(topics),
            "hotness_trend": "rising" if len(topics) > 5 else "stable",
            "top_platform": "",
            "recommendations": [],
        }
        
        # 平台分布
        for topic in topics:
            platform = topic.get("platform", "unknown")
            analysis["platform_distribution"][platform] = analysis["platform_distribution"].get(platform, 0) + 1
        
        # 最多热点的平台
        if analysis["platform_distribution"]:
            analysis["top_platform"] = max(analysis["platform_distribution"], key=analysis["platform_distribution"].get)
        
        # 生成建议
        if len(topics) >= 9:
            analysis["recommendations"].append(f"关键词'{keyword}'热度很高，建议快速跟进")
        if analysis["avg_relevance"] > 2.0:
            analysis["recommendations"].append("相关内容与关键词高度相关，适合深度创作")
        
        return analysis
    
    def _save_report(self, result: Dict) -> Path:
        """保存报告"""
        timestamp = result["timestamp"]
        keyword = result["keyword"].replace(" ", "_")
        
        report_file = self.output_dir / f"hot_topics_{keyword}_{timestamp}.md"
        
        # 生成 Markdown 报告
        content = self._generate_markdown_report(result)
        report_file.write_text(content, encoding="utf-8")
        
        return report_file
    
    def _generate_markdown_report(self, result: Dict) -> str:
        """生成 Markdown 报告"""
        lines = [
            f"# 热点数据分析报告",
            "",
            f"**关键词**: {result['keyword']}",
            f"**时间**: {result['timestamp']}",
            f"**平台**: {', '.join(result['platforms'])}",
            "",
            "---",
            "",
            f"## 🔥 TOP{len(result['top_topics'])} 热点标题排名",
            "",
        ]
        
        for i, topic in enumerate(result["top_topics"], 1):
            platform_name = self.platform_apis.get(topic["platform"], {}).get("name", topic["platform"])
            lines.append(f"**{i}. {topic['title']}**")
            lines.append(f"- 平台：{platform_name}")
            lines.append(f"- 排名：{topic['rank']}")
            lines.append(f"- 热度：{topic['hot_value']:,}" if topic['hot_value'] else "- 热度：N/A")
            lines.append(f"- 相关性：{topic.get('relevance', 0):.2f}")
            if topic.get("url"):
                lines.append(f"- 链接：{topic['url']}")
            lines.append("")
        
        # 数据分析
        analysis = result.get("analysis", {})
        lines.extend([
            "---",
            "",
            "## 📊 数据分析",
            "",
            f"- **相关热点总数**: {analysis.get('total_found', 0)}",
            f"- **平均相关性**: {analysis.get('avg_relevance', 0):.2f}",
            f"- **热度趋势**: {analysis.get('hotness_trend', 'unknown')}",
            f"- **最热平台**: {analysis.get('top_platform', 'unknown')}",
            "",
            "### 平台分布",
            "",
        ])
        
        for platform, count in analysis.get("platform_distribution", {}).items():
            platform_name = self.platform_apis.get(platform, {}).get("name", platform)
            lines.append(f"- {platform_name}: {count} 个")
        
        # 建议
        if analysis.get("recommendations"):
            lines.extend([
                "",
                "## 💡 建议",
                "",
            ])
            for rec in analysis["recommendations"]:
                lines.append(f"- {rec}")
        
        return "\n".join(lines)
    
    def _log(self, message: str):
        """日志输出"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")


def demo():
    """演示"""
    print("="*60)
    print("        热点搜索与分析器演示")
    print("="*60)
    
    analyzer = HotTopicAnalyzer()
    
    # 测试关键词
    test_keywords = [
        "AI 助手",
        "九宫格",
        "数字化转型",
    ]
    
    for keyword in test_keywords:
        print(f"\n搜索：{keyword}")
        result = analyzer.search_hot_topics(keyword, top_n=9)
        
        if result["success"]:
            print(f"✅ 找到 {len(result['top_topics'])} 个相关热点")
            print(f"报告：{result['output_files'][0]}")
            
            # 显示 TOP3
            print("\nTOP3 热点:")
            for i, topic in enumerate(result["top_topics"][:3], 1):
                print(f"  {i}. {topic['title']} ({topic.get('relevance', 0):.2f})")
        else:
            print(f"❌ 失败：{result.get('error')}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    demo()
