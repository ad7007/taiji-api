#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
五行循环战略分析引擎
Five Elements Strategic Analysis Engine

通过五行相生相克循环，实现：
- 金：收集系统运行数据
- 水：分析问题根因与趋势
- 木：生成战略改进方案
- 火：实施路径规划
- 土：沉淀战略洞察报告
"""

from typing import Dict, List, Any
from datetime import datetime


class FiveElementsStrategicAnalyzer:
    """
    五行循环战略分析器
    
    相生分析路径：
    金 (数据采集) → 水 (问题洞察) → 木 (方案设计) → 火 (执行规划) → 土 (战略沉淀)
    """
    
    def __init__(self):
        self.analysis_history = []
        self.strategic_insights = []
        
    def run_full_cycle_analysis(self, system_data: Dict) -> Dict[str, Any]:
        """
        运行完整的五行循环分析
        
        Args:
            system_data: 包含九宫格各宫位运行状态的数据
            
        Returns:
            战略分析报告
        """
        print("\n" + "="*60)
        print("五行循环战略分析启动".center(60))
        print("="*60)
        
        # 1. 金：采集数据
        print("\n【金·采集】收集系统运行数据...")
        collected_data = self._collect_system_metrics(system_data)
        
        # 2. 水：洞察问题
        print("\n【水·洞察】分析问题与趋势...")
        problems_and_trends = self._analyze_problems_and_trends(collected_data)
        
        # 3. 木：生成方案
        print("\n【木·生长】生成战略改进方案...")
        strategic_plans = self._generate_strategic_plans(problems_and_trends)
        
        # 4. 火：规划路径
        print("\n【火·发散】规划实施路径...")
        implementation_paths = self._plan_implementation_paths(strategic_plans)
        
        # 5. 土：沉淀报告
        print("\n【土·承载】沉淀战略洞察报告...")
        strategic_report = self._create_strategic_report(
            collected_data, problems_and_trends, strategic_plans, implementation_paths
        )
        
        # 记录分析历史
        self.analysis_history.append({
            "timestamp": datetime.now().isoformat(),
            "report": strategic_report
        })
        
        print("\n" + "="*60)
        print("分析完成".center(60))
        print("="*60)
        
        return strategic_report
    
    def _collect_system_metrics(self, data: Dict) -> Dict:
        """金：收集系统指标"""
        metrics = {
            "palace_loads": {},
            "balance_status": {},
            "task_statistics": {},
            "resource_utilization": {}
        }
        
        # 收集九宫格负载
        for palace_id in range(1, 10):
            if str(palace_id) in data.get("palaces", {}):
                palace_data = data["palaces"][str(palace_id)]
                metrics["palace_loads"][palace_id] = {
                    "load": palace_data.get("load", 0),
                    "tasks": palace_data.get("task_count", 0),
                    "efficiency": palace_data.get("efficiency", 1.0)
                }
        
        # 收集阴阳平衡状态
        balance_pairs = data.get("balance_pairs", {})
        for pair_name, pair_data in balance_pairs.items():
            if isinstance(pair_data, dict):
                metrics["balance_status"][pair_name] = pair_data.get("balance", 1.0)
            else:
                # 如果直接是数值
                metrics["balance_status"][pair_name] = pair_data
        
        # 收集任务统计
        metrics["task_statistics"] = {
            "total": data.get("total_tasks", 0),
            "completed": data.get("completed_tasks", 0),
            "in_progress": data.get("in_progress_tasks", 0),
            "blocked": data.get("blocked_tasks", 0)
        }
        
        # 收集资源利用率
        metrics["resource_utilization"] = data.get("resources", {})
        
        print(f"   ✓ 收集了 {len(metrics['palace_loads'])} 个宫位的数据")
        print(f"   ✓ 任务总数：{metrics['task_statistics']['total']}")
        
        return metrics
    
    def _analyze_problems_and_trends(self, metrics: Dict) -> Dict:
        """水：分析问题与趋势"""
        analysis = {
            "imbalanced_pairs": [],
            "overloaded_palaces": [],
            "underutilized_palaces": [],
            "bottlenecks": [],
            "trends": []
        }
        
        # 分析阴阳失衡
        for pair_name, balance in metrics["balance_status"].items():
            if balance < 0.7:
                analysis["imbalanced_pairs"].append({
                    "pair": pair_name,
                    "severity": "高" if balance < 0.5 else "中",
                    "balance": balance
                })
        
        # 分析宫位过载
        for palace_id, palace_data in metrics["palace_loads"].items():
            if palace_data["load"] > 0.8:
                analysis["overloaded_palaces"].append({
                    "palace": palace_id,
                    "load": palace_data["load"],
                    "impact": "严重" if palace_data["load"] > 0.9 else "中等"
                })
            elif palace_data["load"] < 0.3 and palace_data["efficiency"] > 0.8:
                analysis["underutilized_palaces"].append({
                    "palace": palace_id,
                    "load": palace_data["load"],
                    "potential": "高"
                })
        
        # 识别瓶颈
        if metrics["task_statistics"]["blocked"] > metrics["task_statistics"]["completed"]:
            analysis["bottlenecks"].append("任务阻塞率过高")
        
        if len(analysis["imbalanced_pairs"]) >= 2:
            analysis["bottlenecks"].append("多处阴阳失衡")
        
        # 趋势分析
        if analysis["imbalanced_pairs"]:
            analysis["trends"].append("系统内部矛盾加剧，需及时调节")
        
        if analysis["overloaded_palaces"]:
            analysis["trends"].append("资源分配不均，可能影响整体效率")
        
        print(f"   ✓ 发现 {len(analysis['imbalanced_pairs'])} 组失衡")
        print(f"   ✓ 发现 {len(analysis['overloaded_palaces'])} 个过载宫位")
        print(f"   ✓ 识别 {len(analysis['bottlenecks'])} 个瓶颈")
        
        return analysis
    
    def _generate_strategic_plans(self, analysis: Dict) -> List[Dict]:
        """木：生成战略方案"""
        plans = []
        
        # 针对阴阳失衡的方案
        for imbalance in analysis["imbalanced_pairs"]:
            plans.append({
                "type": "balance_restoration",
                "priority": "高" if imbalance["severity"] == "高" else "中",
                "target": f"恢复 {imbalance['pair']} 的阴阳平衡",
                "actions": [
                    f"分析 {imbalance['pair']} 的负载差异",
                    "重新分配任务优先级",
                    "必要时进行资源倾斜"
                ],
                "expected_outcome": "平衡度提升至 0.8 以上"
            })
        
        # 针对过载宫位的方案
        for overload in analysis["overloaded_palaces"]:
            plans.append({
                "type": "load_balancing",
                "priority": "高" if overload["impact"] == "严重" else "中",
                "target": f"减轻 {overload['palace']}-宫负载",
                "actions": [
                    "转移部分任务到其他宫位",
                    "优化该宫位的工作流程",
                    "考虑增加资源投入"
                ],
                "expected_outcome": "负载降至 0.7 以下"
            })
        
        # 针对瓶颈的方案
        for bottleneck in analysis["bottlenecks"]:
            plans.append({
                "type": "bottleneck_resolution",
                "priority": "高",
                "target": f"解决瓶颈：{bottleneck}",
                "actions": [
                    "成立专项小组攻关",
                    "引入外部资源支持",
                    "优化相关流程"
                ],
                "expected_outcome": "瓶颈消除，系统流畅运行"
            })
        
        print(f"   ✓ 生成 {len(plans)} 个战略方案")
        
        return plans
    
    def _plan_implementation_paths(self, plans: List[Dict]) -> List[Dict]:
        """火：规划实施路径"""
        paths = []
        
        # 按优先级排序
        high_priority = [p for p in plans if p["priority"] == "高"]
        medium_priority = [p for p in plans if p["priority"] == "中"]
        
        # 短期路径（立即执行）
        paths.append({
            "phase": "短期 (1-3 天)",
            "focus": "紧急问题处理",
            "plans": high_priority[:3],  # 最多 3 个
            "resources_needed": "跨宫位协调",
            "success_criteria": "关键问题解决 50% 以上"
        })
        
        # 中期路径（本周内）
        paths.append({
            "phase": "中期 (1 周)",
            "focus": "系统性优化",
            "plans": high_priority[3:] + medium_priority[:2],
            "resources_needed": "中宫统筹资源",
            "success_criteria": "阴阳平衡度平均达 0.75 以上"
        })
        
        # 长期路径（本月内）
        paths.append({
            "phase": "长期 (1 月)",
            "focus": "机制建设",
            "plans": medium_priority[2:],
            "resources_needed": "持续投入",
            "success_criteria": "建立自动平衡机制"
        })
        
        print(f"   ✓ 规划 {len(paths)} 个实施阶段")
        
        return paths
    
    def _create_strategic_report(self, metrics: Dict, analysis: Dict, 
                                  plans: List[Dict], paths: List[Dict]) -> Dict:
        """土：创建战略报告"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "executive_summary": self._generate_executive_summary(metrics, analysis),
            "current_state": {
                "overall_health": self._calculate_overall_health(metrics),
                "key_metrics": metrics,
                "critical_issues": len(analysis["imbalanced_pairs"]) + len(analysis["overloaded_palaces"])
            },
            "strategic_plans": plans,
            "implementation roadmap": paths,
            "recommendations": self._generate_recommendations(analysis),
            "next_review_date": self._calculate_next_review_date(analysis)
        }
        
        print(f"   ✓ 生成战略报告")
        print(f"   ✓ 整体健康度：{report['current_state']['overall_health']}")
        
        return report
    
    def _generate_executive_summary(self, metrics: Dict, analysis: Dict) -> str:
        """生成执行摘要"""
        health = self._calculate_overall_health(metrics)
        
        summary = f"系统当前整体健康度为 {health}。\n"
        
        if health >= 0.8:
            summary += "系统运行良好，阴阳基本平衡。\n"
        elif health >= 0.6:
            summary += "系统存在一定问题，需要关注。\n"
        else:
            summary += "系统问题较多，建议立即干预。\n"
        
        if analysis["imbalanced_pairs"]:
            summary += f"发现 {len(analysis['imbalanced_pairs'])} 组阴阳失衡，"
        
        if analysis["overloaded_palaces"]:
            summary += f"{len(analysis['overloaded_palaces'])} 个宫位负载过高。"
        
        return summary
    
    def _calculate_overall_health(self, metrics: Dict) -> float:
        """计算整体健康度 (0-1)"""
        if not metrics["balance_status"]:
            return 1.0
        
        # 平衡度占比 60%
        avg_balance = sum(metrics["balance_status"].values()) / len(metrics["balance_status"])
        
        # 负载合理性占比 40%
        loads = [p["load"] for p in metrics["palace_loads"].values()]
        avg_load = sum(loads) / len(loads) if loads else 0
        load_score = 1.0 - abs(avg_load - 0.5) * 2  # 理想负载是 0.5
        
        return round(avg_balance * 0.6 + load_score * 0.4, 2)
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """生成建议"""
        recommendations = []
        
        if analysis["imbalanced_pairs"]:
            recommendations.append("建议优先处理阴阳失衡问题，防止系统内部矛盾加剧")
        
        if analysis["overloaded_palaces"]:
            recommendations.append("需要对过载宫位进行减负，避免单点故障")
        
        if analysis["underutilized_palaces"]:
            recommendations.append("可考虑将部分任务转移到利用率不足的宫位")
        
        if not recommendations:
            recommendations.append("系统运行良好，继续保持当前状态")
        
        return recommendations
    
    def _calculate_next_review_date(self, analysis: Dict) -> str:
        """计算下次审查日期"""
        from datetime import timedelta
        
        # 根据问题严重程度决定审查频率
        critical_issues = len(analysis["imbalanced_pairs"]) + len(analysis["overloaded_palaces"])
        
        if critical_issues >= 3:
            days = 1  # 每天审查
        elif critical_issues >= 1:
            days = 3  # 每 3 天审查
        else:
            days = 7  # 每周审查
        
        next_date = datetime.now() + timedelta(days=days)
        return next_date.strftime("%Y-%m-%d")


def demo_strategic_analysis():
    """演示战略分析"""
    analyzer = FiveElementsStrategicAnalyzer()
    
    # 模拟系统数据
    mock_data = {
        "palaces": {
            "1": {"load": 0.3, "task_count": 5, "efficiency": 0.9},
            "2": {"load": 0.6, "task_count": 8, "efficiency": 0.85},
            "3": {"load": 0.9, "task_count": 15, "efficiency": 0.7},
            "6": {"load": 0.4, "task_count": 6, "efficiency": 0.8},
        },
        "balance_pairs": {
            "team_process": 0.95,
            "tech_quality": 0.44,  # 失衡
            "product_data": 0.75,
            "monitor_eco": 0.88
        },
        "total_tasks": 50,
        "completed_tasks": 30,
        "in_progress_tasks": 15,
        "blocked_tasks": 5,
        "resources": {"cpu": 0.65, "memory": 0.72}
    }
    
    report = analyzer.run_full_cycle_analysis(mock_data)
    
    print("\n" + "="*60)
    print("战略分析报告摘要".center(60))
    print("="*60)
    print(report["executive_summary"])
    print("\n建议:")
    for rec in report["recommendations"]:
        print(f"  • {rec}")
    print(f"\n下次审查日期：{report['next_review_date']}")
    print("="*60)


if __name__ == "__main__":
    demo_strategic_analysis()
