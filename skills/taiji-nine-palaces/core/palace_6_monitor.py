#!/usr/bin/env python3
"""
6 宫 - 质量监控核心

职责：
1. 系统健康监控
2. 自动备份
3. 告警通知
4. 日志管理

自动组队：6宫监控 → 9宫生态 → 5宫交付
"""

import os
import sys
import json
import subprocess
import psutil
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field


@dataclass
class MonitorResult:
    """监控结果"""
    success: bool
    check_type: str  # health/backup/alert/log
    message: str
    data: Dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


class Palace6Monitor:
    """
    6 宫 - 质量监控
    
    使用示例:
        monitor = Palace6Monitor()
        
        # 健康检查
        result = monitor.health_check()
        
        # 创建备份
        result = monitor.create_backup()
        
        # 检查告警
        alerts = monitor.check_alerts()
    """
    
    def __init__(self):
        self.palace_id = 6
        self.palace_name = "质量监控"
        
        # 备份目录
        self.backup_dir = Path("/root/.openclaw/backups")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # 监控历史
        self.history: List[MonitorResult] = []
        
        # 告警阈值
        self.thresholds = {
            "cpu_percent": 80.0,      # CPU使用率上限
            "memory_percent": 85.0,   # 内存使用率上限
            "disk_percent": 90.0,     # 磁盘使用率上限
            "load_average": 4.0       # 负载上限
        }
        
        # 备份保留天数
        self.backup_retention_days = 30
    
    # ========== 健康监控 ==========
    
    def health_check(self) -> MonitorResult:
        """
        系统健康检查
        
        Returns:
            MonitorResult 包含各项健康指标
        """
        try:
            # CPU 使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # 内存使用
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # 磁盘使用
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            # 系统负载
            load_avg = os.getloadavg()[0] if hasattr(os, 'getloadavg') else 0
            
            # 进程数
            process_count = len(psutil.pids())
            
            # 判断健康状态
            is_healthy = (
                cpu_percent < self.thresholds["cpu_percent"] and
                memory_percent < self.thresholds["memory_percent"] and
                disk_percent < self.thresholds["disk_percent"]
            )
            
            health_data = {
                "cpu_percent": cpu_percent,
                "memory_percent": memory_percent,
                "memory_available_gb": memory.available / (1024**3),
                "disk_percent": disk_percent,
                "disk_free_gb": disk.free / (1024**3),
                "load_average": load_avg,
                "process_count": process_count,
                "is_healthy": is_healthy
            }
            
            result = MonitorResult(
                success=is_healthy,
                check_type="health",
                message="系统健康" if is_healthy else "系统异常，请检查",
                data=health_data
            )
        
        except Exception as e:
            result = MonitorResult(
                success=False,
                check_type="health",
                message=f"健康检查失败: {str(e)}"
            )
        
        self.history.append(result)
        return result
    
    # ========== 自动备份 ==========
    
    def create_backup(self, 
                     source_dir: Optional[str] = None,
                     backup_name: Optional[str] = None) -> MonitorResult:
        """
        创建备份
        
        Args:
            source_dir: 源目录（默认备份 workspace）
            backup_name: 备份名称
        
        Returns:
            MonitorResult
        """
        # 默认备份 workspace
        if source_dir is None:
            source_dir = "/root/.openclaw/workspace"
        
        # 生成备份名称
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = backup_name or f"backup_{timestamp}"
        
        source_path = Path(source_dir)
        backup_path = self.backup_dir / backup_name
        
        try:
            if not source_path.exists():
                raise FileNotFoundError(f"源目录不存在: {source_dir}")
            
            # 创建备份
            shutil.copytree(source_path, backup_path)
            
            # 获取备份大小
            backup_size = sum(
                f.stat().st_size 
                for f in backup_path.rglob('*') 
                if f.is_file()
            )
            
            result = MonitorResult(
                success=True,
                check_type="backup",
                message=f"备份成功: {backup_name}",
                data={
                    "backup_path": str(backup_path),
                    "backup_size_mb": backup_size / (1024**2),
                    "file_count": len(list(backup_path.rglob('*'))),
                    "source_dir": source_dir
                }
            )
        
        except Exception as e:
            result = MonitorResult(
                success=False,
                check_type="backup",
                message=f"备份失败: {str(e)}"
            )
        
        self.history.append(result)
        return result
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """列出所有备份"""
        backups = []
        
        for backup_path in self.backup_dir.iterdir():
            if backup_path.is_dir():
                stat = backup_path.stat()
                size = sum(
                    f.stat().st_size 
                    for f in backup_path.rglob('*') 
                    if f.is_file()
                )
                
                backups.append({
                    "name": backup_path.name,
                    "path": str(backup_path),
                    "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "size_mb": size / (1024**2)
                })
        
        # 按创建时间降序排序
        backups.sort(key=lambda x: x["created_at"], reverse=True)
        
        return backups
    
    def clean_old_backups(self) -> MonitorResult:
        """清理旧备份"""
        try:
            cutoff_date = datetime.now() - timedelta(days=self.backup_retention_days)
            
            deleted_count = 0
            deleted_size = 0
            
            for backup_path in self.backup_dir.iterdir():
                if backup_path.is_dir():
                    stat = backup_path.stat()
                    created_time = datetime.fromtimestamp(stat.st_ctime)
                    
                    if created_time < cutoff_date:
                        # 计算大小
                        size = sum(
                            f.stat().st_size 
                            for f in backup_path.rglob('*') 
                            if f.is_file()
                        )
                        
                        # 删除
                        shutil.rmtree(backup_path)
                        deleted_count += 1
                        deleted_size += size
            
            result = MonitorResult(
                success=True,
                check_type="backup",
                message=f"清理完成: 删除 {deleted_count} 个旧备份",
                data={
                    "deleted_count": deleted_count,
                    "freed_space_mb": deleted_size / (1024**2),
                    "retention_days": self.backup_retention_days
                }
            )
        
        except Exception as e:
            result = MonitorResult(
                success=False,
                check_type="backup",
                message=f"清理失败: {str(e)}"
            )
        
        self.history.append(result)
        return result
    
    # ========== 告警检查 ==========
    
    def check_alerts(self) -> List[Dict[str, Any]]:
        """
        检查告警条件
        
        Returns:
            告警列表
        """
        alerts = []
        
        try:
            # CPU 告警
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > self.thresholds["cpu_percent"]:
                alerts.append({
                    "level": "WARNING",
                    "type": "cpu",
                    "message": f"CPU 使用率过高: {cpu_percent:.1f}%",
                    "value": cpu_percent,
                    "threshold": self.thresholds["cpu_percent"]
                })
            
            # 内存告警
            memory = psutil.virtual_memory()
            if memory.percent > self.thresholds["memory_percent"]:
                alerts.append({
                    "level": "WARNING",
                    "type": "memory",
                    "message": f"内存使用率过高: {memory.percent:.1f}%",
                    "value": memory.percent,
                    "threshold": self.thresholds["memory_percent"]
                })
            
            # 磁盘告警
            disk = psutil.disk_usage('/')
            if disk.percent > self.thresholds["disk_percent"]:
                alerts.append({
                    "level": "ERROR",
                    "type": "disk",
                    "message": f"磁盘使用率过高: {disk.percent:.1f}%",
                    "value": disk.percent,
                    "threshold": self.thresholds["disk_percent"]
                })
        
        except Exception as e:
            alerts.append({
                "level": "ERROR",
                "type": "check_failed",
                "message": f"告警检查失败: {str(e)}"
            })
        
        return alerts
    
    # ========== 日志管理 ==========
    
    def get_recent_logs(self, 
                       log_dir: str = "/var/log",
                       lines: int = 100) -> Dict[str, str]:
        """
        获取最近日志
        
        Args:
            log_dir: 日志目录
            lines: 行数
        
        Returns:
            日志内容字典
        """
        logs = {}
        log_path = Path(log_dir)
        
        try:
            for log_file in log_path.glob("*.log"):
                if log_file.is_file():
                    try:
                        with open(log_file, 'r', errors='ignore') as f:
                            # 读取最后 N 行
                            all_lines = f.readlines()
                            logs[log_file.name] = ''.join(all_lines[-lines:])
                    except:
                        pass
        except Exception as e:
            logs["error"] = str(e)
        
        return logs
    
    # ========== 统计 ==========
    
    def get_stats(self) -> Dict[str, Any]:
        """获取监控统计"""
        if not self.history:
            return {"total": 0, "backups": 0, "health_checks": 0}
        
        backups = [r for r in self.history if r.check_type == "backup" and r.success]
        health_checks = [r for r in self.history if r.check_type == "health"]
        
        return {
            "total": len(self.history),
            "backups": len(backups),
            "health_checks": len(health_checks),
            "backup_count": len(self.list_backups())
        }


# ========== 全局实例 ==========

_monitor_instance = None

def get_monitor() -> Palace6Monitor:
    """获取全局监控实例"""
    global _monitor_instance
    if _monitor_instance is None:
        _monitor_instance = Palace6Monitor()
    return _monitor_instance


# ========== 快捷函数 ==========

def health_check() -> MonitorResult:
    """快捷函数：健康检查"""
    return get_monitor().health_check()

def create_backup(**kwargs) -> MonitorResult:
    """快捷函数：创建备份"""
    return get_monitor().create_backup(**kwargs)

def check_alerts() -> List[Dict[str, Any]]:
    """快捷函数：检查告警"""
    return get_monitor().check_alerts()


# ========== 测试 ==========

if __name__ == "__main__":
    print("=== 6 宫质量监控测试 ===\n")
    
    monitor = Palace6Monitor()
    
    # 测试1: 健康检查
    print("1. 健康检查:")
    result = monitor.health_check()
    print(f"   健康状态: {'✅' if result.success else '❌'}")
    print(f"   CPU: {result.data.get('cpu_percent', 0):.1f}%")
    print(f"   内存: {result.data.get('memory_percent', 0):.1f}%")
    print(f"   磁盘: {result.data.get('disk_percent', 0):.1f}%")
    
    # 测试2: 告警检查
    print("\n2. 告警检查:")
    alerts = monitor.check_alerts()
    if alerts:
        for alert in alerts:
            print(f"   [{alert['level']}] {alert['message']}")
    else:
        print("   ✅ 无告警")
    
    # 测试3: 备份列表
    print("\n3. 备份列表:")
    backups = monitor.list_backups()
    print(f"   备份数量: {len(backups)}")
    for backup in backups[:3]:
        print(f"   - {backup['name']} ({backup['size_mb']:.1f}MB)")
    
    # 测试4: 统计
    print("\n4. 监控统计:")
    stats = monitor.get_stats()
    print(f"   总计: {stats['total']}")
    print(f"   备份数: {stats['backup_count']}")
    
    print("\n=== 6 宫就绪 ===")