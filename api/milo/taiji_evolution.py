"""
太极自我进化引擎

让米珞能够：
1. 自我感知瓶颈
2. 自我优化组队和任务管理
3. 自我进化提升

核心原理：
- 阴阳平衡 → 资源均衡优化
- 五行相生 → 能力增强循环
- 五行相克 → 制衡纠偏
- 中宫调度 → 协调全局
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


# ==================== 进化类型 ====================

class EvolutionType(Enum):
    """进化类型"""
    BALANCE = "balance"        # 阴阳平衡优化
    GENERATION = "generation"  # 相生增强
    CONTROL = "control"        # 相克制衡
    STRUCTURE = "structure"    # 结构优化
    CAPABILITY = "capability"  # 能力增强


@dataclass
class EvolutionRecord:
    """进化记录"""
    timestamp: str
    type: EvolutionType
    before: Dict[str, Any]
    after: Dict[str, Any]
    improvement: float
    reason: str


# ==================== 自我感知 ====================

class SelfPerception:
    """自我感知引擎"""
    
    def __init__(self):
        self.history: List[Dict] = []
    
    def sense_bottlenecks(self, system_state: Dict) -> List[Dict]:
        """
        感知系统瓶颈
        
        Returns:
            [{type, severity, location, suggestion}, ...]
        """
        bottlenecks = []
        
        # 1. 阴阳失衡检测
        balance = system_state.get("balance", 1.0)
        if balance < 0.3:
            bottlenecks.append({
                "type": "阴阳失衡",
                "severity": "critical",
                "location": "全局",
                "suggestion": "激活阴卦宫位，平衡负载",
                "metric": balance,
            })
        elif balance < 0.5:
            bottlenecks.append({
                "type": "阴阳轻度失衡",
                "severity": "warning",
                "location": "局部",
                "suggestion": "调整任务分配",
                "metric": balance,
            })
        
        # 2. 宫位过载检测
        palace_loads = system_state.get("palace_loads", {})
        for palace_id, load in palace_loads.items():
            if load > 0.9:
                bottlenecks.append({
                    "type": "宫位过载",
                    "severity": "critical",
                    "location": f"{palace_id}宫",
                    "suggestion": "分流任务或升级能力",
                    "metric": load,
                })
        
        # 3. 中轴健康检测
        axis_health = system_state.get("axis_health", 1.0)
        if axis_health < 0.5:
            bottlenecks.append({
                "type": "中轴断裂",
                "severity": "high",
                "location": "159中轴",
                "suggestion": "修复数据流→控制→生态链条",
                "metric": axis_health,
            })
        
        # 4. 支撑强度检测
        support_strength = system_state.get("support_strength", 0)
        if support_strength < 0.2:
            bottlenecks.append({
                "type": "支撑不足",
                "severity": "medium",
                "location": "258三角",
                "suggestion": "加强质量→控制→营销协作",
                "metric": support_strength,
            })
        
        # 5. 能力空缺检测
        capabilities = system_state.get("capabilities", {})
        missing = [cap for cap, available in capabilities.items() if not available]
        if missing:
            bottlenecks.append({
                "type": "能力缺失",
                "severity": "medium",
                "location": missing,
                "suggestion": "安装或开发缺失能力",
                "metric": len(missing),
            })
        
        return bottlenecks
    
    def sense_opportunities(self, system_state: Dict) -> List[Dict]:
        """
        感知进化机会
        
        基于相生路径发现增强机会
        """
        opportunities = []
        
        # 相生路径: 3→6→9→7→4→8→3
        generation_path = [3, 6, 9, 7, 4, 8]
        palace_loads = system_state.get("palace_loads", {})
        
        # 找相生链条中的强化机会
        for i in range(len(generation_path) - 1):
            p1, p2 = generation_path[i], generation_path[i + 1]
            load1 = palace_loads.get(p1, 0)
            load2 = palace_loads.get(p2, 0)
            
            # 如果前一个宫位活跃，后一个空闲 → 传递机会
            if load1 > 0.5 and load2 < 0.3:
                opportunities.append({
                    "type": "相生传递",
                    "from": p1,
                    "to": p2,
                    "potential": load1 - load2,
                    "suggestion": f"{p1}宫可向{p2}宫传递任务",
                })
        
        # 阴阳互补机会
        yin_active = sum(v for k, v in palace_loads.items() if k in [2, 4, 9, 7])
        yang_active = sum(v for k, v in palace_loads.items() if k in [6, 3, 1, 8])
        
        if yang_active > yin_active * 2:
            opportunities.append({
                "type": "阴阳激活",
                "target": "阴卦",
                "suggestion": "激活坤巽离兑，承接阳卦溢出任务",
            })
        elif yin_active > yang_active * 2:
            opportunities.append({
                "type": "阴阳激活",
                "target": "阳卦",
                "suggestion": "激活乾震坎艮，承接阴卦溢出任务",
            })
        
        return opportunities
    
    def record_state(self, state: Dict):
        """记录状态用于趋势分析"""
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "state": state,
        })
        
        # 保留最近100条
        if len(self.history) > 100:
            self.history = self.history[-100:]


# ==================== 自我优化 ====================

class SelfOptimizer:
    """自我优化引擎"""
    
    def __init__(self):
        self.evolution_records: List[EvolutionRecord] = []
    
    def optimize_balance(self, 
                         bottlenecks: List[Dict], 
                         current_teams: Dict[str, List[int]]) -> Dict[str, Any]:
        """
        优化阴阳平衡
        
        Returns:
            {adjustments: [...], new_teams: {...}}
        """
        adjustments = []
        new_teams = current_teams.copy()
        
        # 找阴阳失衡瓶颈
        for b in bottlenecks:
            if b["type"] == "阴阳失衡":
                # 找过载的阳卦宫位
                yang_overload = [k for k, v in b.get("details", {}).items() 
                                if k in [6, 3, 1, 8] and v > 0.7]
                
                # 找空闲的阴卦宫位
                yin_idle = [k for k, v in b.get("details", {}).items()
                           if k in [2, 4, 9, 7] and v < 0.3]
                
                # 重新分配
                for yang in yang_overload:
                    if yin_idle:
                        yin = yin_idle.pop(0)
                        adjustments.append({
                            "type": "负载转移",
                            "from": yang,
                            "to": yin,
                            "reason": "阴阳平衡优化",
                        })
                        
                        # 更新组队
                        for scene, team in new_teams.items():
                            if yang in team and yin not in team:
                                new_teams[scene] = team + [yin]
        
        return {
            "adjustments": adjustments,
            "new_teams": new_teams,
        }
    
    def optimize_generation(self,
                           opportunities: List[Dict],
                           current_tasks: List[Dict]) -> Dict[str, Any]:
        """
        优化相生循环
        
        增强能力传递链条
        """
        enhancements = []
        
        for opp in opportunities:
            if opp["type"] == "相生传递":
                enhancements.append({
                    "type": "链条增强",
                    "path": f"{opp['from']}→{opp['to']}",
                    "action": f"让{opp['from']}宫带动{opp['to']}宫",
                    "expected_improvement": opp["potential"],
                })
        
        return {
            "enhancements": enhancements,
        }
    
    def optimize_control(self,
                         bottlenecks: List[Dict],
                         current_tasks: List[Dict]) -> Dict[str, Any]:
        """
        优化相克制衡
        
        建立检查点和纠偏机制
        """
        controls = []
        
        # 相克关系用于制衡
        control_relations = [
            (3, 6, "技术制约监控"),
            (6, 9, "监控制约生态"),
            (9, 7, "生态制约验收"),
            (7, 4, "验收制约品牌"),
            (4, 8, "品牌制约营销"),
            (8, 1, "营销制约采集"),
            (1, 3, "采集制约技术"),
        ]
        
        for b in bottlenecks:
            if b["type"] == "宫位过载":
                palace_id = int(b["location"][0])
                
                # 找能制约它的宫位
                for p1, p2, desc in control_relations:
                    if p1 == palace_id:
                        controls.append({
                            "type": "制衡介入",
                            "controller": p2,
                            "target": palace_id,
                            "mechanism": desc,
                            "action": f"{p2}宫检查{palace_id}宫输出",
                        })
        
        return {
            "controls": controls,
        }
    
    def evolve_structure(self,
                         bottlenecks: List[Dict],
                         opportunities: List[Dict]) -> Dict[str, Any]:
        """
        进化系统结构
        
        调整组队模式、优化流程
        """
        evolution = {
            "new_patterns": [],
            "deprecated_patterns": [],
            "recommended_complexity": None,
        }
        
        # 根据瓶颈严重程度推荐复杂度
        critical_count = sum(1 for b in bottlenecks if b["severity"] == "critical")
        if critical_count > 2:
            evolution["recommended_complexity"] = 8  # 全模态
        elif critical_count > 0:
            evolution["recommended_complexity"] = 5  # 小圆
        else:
            evolution["recommended_complexity"] = 3  # 三角
        
        # 推荐新的组队模式
        for opp in opportunities:
            if opp["type"] == "阴阳激活":
                evolution["new_patterns"].append({
                    "pattern": "阴阳激活模式",
                    "target": opp["target"],
                    "config": f"优先调度{opp['target']}宫位",
                })
        
        return evolution
    
    def record_evolution(self, record: EvolutionRecord):
        """记录进化历史"""
        self.evolution_records.append(record)
        
        # 保存到文件
        with open("/tmp/taiji_evolution.json", "a") as f:
            f.write(json.dumps({
                "timestamp": record.timestamp,
                "type": record.type.value,
                "improvement": record.improvement,
                "reason": record.reason,
            }) + "\n")


# ==================== 自我进化 ====================

class SelfEvolution:
    """自我进化引擎"""
    
    def __init__(self):
        self.perception = SelfPerception()
        self.optimizer = SelfOptimizer()
        self.evolution_count = 0
    
    def evolve(self, system_state: Dict) -> Dict[str, Any]:
        """
        执行一次进化循环
        
        Returns:
            {
                bottlenecks: [...],
                opportunities: [...],
                optimizations: {...},
                evolution: {...},
                actions: [...]
            }
        """
        # 1. 自我感知
        bottlenecks = self.perception.sense_bottlenecks(system_state)
        opportunities = self.perception.sense_opportunities(system_state)
        self.perception.record_state(system_state)
        
        # 2. 自我优化
        balance_opt = self.optimizer.optimize_balance(bottlenecks, {})
        generation_opt = self.optimizer.optimize_generation(opportunities, [])
        control_opt = self.optimizer.optimize_control(bottlenecks, [])
        structure_evo = self.optimizer.evolve_structure(bottlenecks, opportunities)
        
        # 3. 生成行动建议
        actions = self._generate_actions(
            bottlenecks, opportunities, 
            balance_opt, generation_opt, control_opt, structure_evo
        )
        
        # 4. 记录进化
        if actions:
            self.evolution_count += 1
            self.optimizer.record_evolution(EvolutionRecord(
                timestamp=datetime.now().isoformat(),
                type=EvolutionType.STRUCTURE,
                before={"balance": system_state.get("balance", 0)},
                after={"actions": len(actions)},
                improvement=len(actions) / max(len(bottlenecks), 1),
                reason=f"发现{len(bottlenecks)}个瓶颈，{len(opportunities)}个机会",
            ))
        
        return {
            "bottlenecks": bottlenecks,
            "opportunities": opportunities,
            "optimizations": {
                "balance": balance_opt,
                "generation": generation_opt,
                "control": control_opt,
            },
            "evolution": structure_evo,
            "actions": actions,
            "evolution_count": self.evolution_count,
        }
    
    def _generate_actions(self, 
                          bottlenecks: List[Dict],
                          opportunities: List[Dict],
                          balance_opt: Dict,
                          generation_opt: Dict,
                          control_opt: Dict,
                          structure_evo: Dict) -> List[Dict]:
        """生成具体行动建议"""
        actions = []
        
        # 从瓶颈生成行动
        for b in bottlenecks:
            if b["severity"] == "critical":
                actions.append({
                    "priority": 1,
                    "type": "紧急修复",
                    "action": b["suggestion"],
                    "target": b["location"],
                })
        
        # 从机会生成行动
        for opp in opportunities[:3]:  # 限制数量
            actions.append({
                "priority": 2,
                "type": "机会利用",
                "action": opp["suggestion"],
                "target": opp.get("from", opp.get("target")),
            })
        
        # 从优化生成行动
        for adj in balance_opt.get("adjustments", [])[:3]:
            actions.append({
                "priority": 3,
                "type": "平衡调整",
                "action": f"从{adj['from']}宫转移到{adj['to']}宫",
                "target": f"{adj['from']}→{adj['to']}",
            })
        
        # 从进化生成行动
        for pattern in structure_evo.get("new_patterns", []):
            actions.append({
                "priority": 4,
                "type": "模式进化",
                "action": pattern["config"],
                "target": pattern["target"],
            })
        
        # 按优先级排序
        actions.sort(key=lambda x: x["priority"])
        
        return actions
    
    def auto_improve(self, 
                     system_state: Dict,
                     auto_apply: bool = False) -> Dict[str, Any]:
        """
        自动改进
        
        Args:
            system_state: 当前系统状态
            auto_apply: 是否自动应用改进
        
        Returns:
            进化结果
        """
        result = self.evolve(system_state)
        
        if auto_apply:
            # 自动应用优先级最高的行动
            for action in result["actions"][:3]:
                if action["priority"] == 1:
                    self._apply_action(action)
        
        return result
    
    def _apply_action(self, action: Dict):
        """应用行动（实际执行）"""
        # 这里可以接入实际的执行逻辑
        # 例如：调整组队、重新分配任务、激活宫位等
        print(f"[进化] 执行: {action['action']} @ {action['target']}")


# ==================== 进化报告 ====================

def generate_evolution_report(evolution_result: Dict) -> str:
    """生成进化报告"""
    lines = []
    lines.append("═" * 50)
    lines.append("太极自我进化报告")
    lines.append("═" * 50)
    lines.append("")
    
    # 瓶颈分析
    lines.append("🔍 瓶颈分析:")
    for b in evolution_result.get("bottlenecks", []):
        lines.append(f"  - [{b['severity']}] {b['type']}: {b['suggestion']}")
    
    lines.append("")
    
    # 机会发现
    lines.append("💡 进化机会:")
    for o in evolution_result.get("opportunities", []):
        lines.append(f"  - {o['type']}: {o['suggestion']}")
    
    lines.append("")
    
    # 行动建议
    lines.append("🎯 行动建议:")
    for a in evolution_result.get("actions", []):
        lines.append(f"  - P{a['priority']} {a['type']}: {a['action']}")
    
    lines.append("")
    lines.append("═" * 50)
    
    return "\n".join(lines)


# ==================== 示例用法 ====================

if __name__ == "__main__":
    print("=== 太极自我进化引擎 ===\n")
    
    engine = SelfEvolution()
    
    # 模拟系统状态
    system_state = {
        "balance": 0.25,  # 阴阳失衡
        "axis_health": 0.6,
        "support_strength": 0.1,
        "palace_loads": {
            1: 0.9,  # 数据采集过载
            2: 0.0,  # 产品质量空闲
            3: 0.7,  # 技术团队忙碌
            4: 0.0,  # 品牌战略空闲
            5: 0.3,  # 中控正常
            6: 0.95, # 物联监控过载
            7: 0.0,  # 法务框架空闲
            8: 0.0,  # 营销客服空闲
            9: 0.1,  # 行业生态低负载
        },
        "capabilities": {
            "agent-browser": True,
            "video-summary": True,
            "mcp-server": False,  # 缺失
            "auto-code": False,   # 缺失
        },
    }
    
    # 执行进化
    result = engine.evolve(system_state)
    
    # 生成报告
    report = generate_evolution_report(result)
    print(report)
    
    print(f"\n进化次数: {result['evolution_count']}")
    print(f"发现瓶颈: {len(result['bottlenecks'])}个")
    print(f"发现机会: {len(result['opportunities'])}个")
    print(f"行动建议: {len(result['actions'])}条")