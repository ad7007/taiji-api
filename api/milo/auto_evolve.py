"""
太极自动进化守护进程

每30秒执行一次：
1. 感知系统状态
2. 发现瓶颈和机会
3. 自动优化
4. 记录进化历史
"""

import time
import json
from datetime import datetime
from taiji_evolution import SelfEvolution

class AutoEvolutionDaemon:
    """自动进化守护进程"""
    
    def __init__(self, interval: int = 30):
        self.interval = interval
        self.evolution = SelfEvolution()
        self.running = False
        self.log_file = "/tmp/taiji_evolution.log"
        self.state_file = "/tmp/taiji_state.json"
    
    def get_current_state(self) -> dict:
        """获取当前系统状态"""
        # 从太极API获取真实状态
        import subprocess
        
        try:
            # 获取宫位负载
            result = subprocess.run(
                ["curl", "-s", "http://localhost:8000/api/taiji/palaces"],
                capture_output=True, text=True, timeout=5
            )
            data = json.loads(result.stdout) if result.returncode == 0 else {}
            
            palaces = data.get("palaces", {})
            palace_loads = {i: palaces.get(str(i), {}).get("load", 0) for i in range(1, 10)}
            
            # 计算阴阳平衡
            yang_load = sum(palace_loads.get(i, 0) for i in [6, 3, 1, 8])
            yin_load = sum(palace_loads.get(i, 0) for i in [2, 4, 9, 7])
            balance = min(yang_load, yin_load) / max(yang_load, yin_load, 0.01)
            
            return {
                "balance": balance,
                "palace_loads": palace_loads,
                "axis_health": 1.0,  # 简化计算
                "support_strength": yin_load / 4,  # 阴卦平均
                "capabilities": {
                    "agent-browser": True,
                    "video-summary": True,
                    "mcp-server": False,
                },
            }
        except Exception as e:
            # 默认状态
            return {
                "balance": 0.5,
                "palace_loads": {i: 0.1 for i in range(1, 10)},
                "axis_health": 1.0,
                "support_strength": 0.1,
                "capabilities": {},
            }
    
    def evolve_step(self):
        """执行一次进化步骤"""
        state = self.get_current_state()
        result = self.evolution.evolve(state)
        
        # 记录日志
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "balance": state["balance"],
            "bottlenecks": len(result["bottlenecks"]),
            "opportunities": len(result["opportunities"]),
            "actions": len(result["actions"]),
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        # 保存当前状态
        with open(self.state_file, "w") as f:
            json.dump({
                "state": state,
                "result": {
                    "bottlenecks": result["bottlenecks"],
                    "opportunities": result["opportunities"],
                    "actions": result["actions"][:5],  # 只保存前5个行动
                },
                "evolution_count": result["evolution_count"],
                "last_update": datetime.now().isoformat(),
            }, f, indent=2)
        
        return result
    
    def run(self):
        """运行守护进程"""
        self.running = True
        print(f"[太极自动进化] 启动，间隔 {self.interval}秒")
        
        while self.running:
            try:
                result = self.evolve_step()
                
                # 如果发现critical瓶颈，输出告警
                critical = [b for b in result["bottlenecks"] if b.get("severity") == "critical"]
                if critical:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️ 发现 {len(critical)} 个关键瓶颈")
                    for c in critical:
                        print(f"  - {c['type']}: {c['suggestion']}")
                
                # 如果发现进化机会
                if result["opportunities"]:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] 💡 发现 {len(result['opportunities'])} 个进化机会")
                
            except Exception as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ 错误: {e}")
            
            time.sleep(self.interval)
    
    def stop(self):
        """停止守护进程"""
        self.running = False
        print("[太极自动进化] 停止")


if __name__ == "__main__":
    daemon = AutoEvolutionDaemon(interval=30)
    try:
        daemon.run()
    except KeyboardInterrupt:
        daemon.stop()
