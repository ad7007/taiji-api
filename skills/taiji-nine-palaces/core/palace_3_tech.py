#!/usr/bin/env python3
"""
3 宫 - 技术团队核心

职责：
1. 技能安装（skillhub/clawhub）
2. 代码执行
3. 脚本运行
4. 依赖管理

自动组队：3宫开发 → 7宫测试 → 5宫交付
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class TechResult:
    """技术操作结果"""
    success: bool
    action: str  # install/run/test
    target: str  # skill/script/command
    output: Optional[str] = None
    error: Optional[str] = None
    metadata: Dict = field(default_factory=dict)
    executed_at: datetime = field(default_factory=datetime.now)


class Palace3Tech:
    """
    3 宫 - 技术团队
    
    使用示例:
        tech = Palace3Tech()
        
        # 安装技能
        result = tech.install_skill("some-skill")
        
        # 运行脚本
        result = tech.run_script("python3 script.py")
        
        # 执行命令
        result = tech.execute("ls -la")
    """
    
    def __init__(self):
        self.palace_id = 3
        self.palace_name = "技术团队"
        
        # 技能目录
        self.skills_dir = Path("/root/.openclaw/workspace/skills")
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        
        # 操作历史
        self.history: List[TechResult] = []
        
        # 支持的包管理器
        self.package_managers = {
            "pip": ["pip", "pip3"],
            "npm": ["npm"],
            "pnpm": ["pnpm"]
        }
    
    # ========== 技能安装 ==========
    
    def install_skill(self, skill_name: str,
                     source: str = "skillhub",
                     version: Optional[str] = None) -> TechResult:
        """
        安装技能
        
        Args:
            skill_name: 技能名称
            source: 来源 (skillhub/clawhub)
            version: 版本号
        
        Returns:
            TechResult
        """
        try:
            # 构建安装命令
            if source == "skillhub":
                cmd = ["skillhub", "install", skill_name]
            elif source == "clawhub":
                cmd = ["clawhub", "install", skill_name]
            else:
                raise ValueError(f"未知的技能源: {source}")
            
            if version:
                cmd.extend(["--version", version])
            
            # 执行安装
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                tech_result = TechResult(
                    success=True,
                    action="install",
                    target=skill_name,
                    output=result.stdout,
                    metadata={
                        "source": source,
                        "version": version,
                        "command": " ".join(cmd)
                    }
                )
            else:
                tech_result = TechResult(
                    success=False,
                    action="install",
                    target=skill_name,
                    output=result.stdout,
                    error=result.stderr or "安装失败",
                    metadata={"command": " ".join(cmd)}
                )
        
        except FileNotFoundError:
            # 尝试手动安装
            tech_result = self._manual_install(skill_name, source)
        except Exception as e:
            tech_result = TechResult(
                success=False,
                action="install",
                target=skill_name,
                error=str(e)
            )
        
        self.history.append(tech_result)
        return tech_result
    
    def _manual_install(self, skill_name: str, source: str) -> TechResult:
        """手动安装技能（从 Git 克隆）"""
        try:
            # 尝试从 GitHub 克隆
            git_url = f"https://github.com/{skill_name}.git"
            
            result = subprocess.run(
                ["git", "clone", git_url, str(self.skills_dir / skill_name.split("/")[-1])],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return TechResult(
                    success=True,
                    action="install",
                    target=skill_name,
                    output="手动安装成功（Git 克隆）",
                    metadata={"method": "git_clone", "url": git_url}
                )
            else:
                return TechResult(
                    success=False,
                    action="install",
                    target=skill_name,
                    error="手动安装失败，请检查技能名称"
                )
        except Exception as e:
            return TechResult(
                success=False,
                action="install",
                target=skill_name,
                error=f"手动安装失败: {str(e)}"
            )
    
    # ========== 代码执行 ==========
    
    def run_script(self, script_path: str,
                   args: Optional[List[str]] = None,
                   cwd: Optional[str] = None,
                   timeout: int = 60) -> TechResult:
        """
        运行脚本
        
        Args:
            script_path: 脚本路径
            args: 参数列表
            cwd: 工作目录
            timeout: 超时时间（秒）
        
        Returns:
            TechResult
        """
        # 检测脚本类型
        script_type = self._detect_script_type(script_path)
        
        # 构建命令
        cmd = [script_path]
        if args:
            cmd.extend(args)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd
            )
            
            tech_result = TechResult(
                success=result.returncode == 0,
                action="run",
                target=script_path,
                output=result.stdout,
                error=result.stderr if result.returncode != 0 else None,
                metadata={
                    "script_type": script_type,
                    "args": args,
                    "returncode": result.returncode
                }
            )
        
        except subprocess.TimeoutExpired:
            tech_result = TechResult(
                success=False,
                action="run",
                target=script_path,
                error=f"执行超时（{timeout}秒）"
            )
        except Exception as e:
            tech_result = TechResult(
                success=False,
                action="run",
                target=script_path,
                error=str(e)
            )
        
        self.history.append(tech_result)
        return tech_result
    
    def execute(self, command: str,
               timeout: int = 60,
               cwd: Optional[str] = None) -> TechResult:
        """
        执行命令
        
        Args:
            command: 命令字符串
            timeout: 超时时间（秒）
            cwd: 工作目录
        
        Returns:
            TechResult
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd
            )
            
            tech_result = TechResult(
                success=result.returncode == 0,
                action="execute",
                target=command,
                output=result.stdout,
                error=result.stderr if result.returncode != 0 else None,
                metadata={"returncode": result.returncode}
            )
        
        except subprocess.TimeoutExpired:
            tech_result = TechResult(
                success=False,
                action="execute",
                target=command,
                error=f"执行超时（{timeout}秒）"
            )
        except Exception as e:
            tech_result = TechResult(
                success=False,
                action="execute",
                target=command,
                error=str(e)
            )
        
        self.history.append(tech_result)
        return tech_result
    
    # ========== 依赖管理 ==========
    
    def install_dependency(self, package: str,
                          manager: str = "pip") -> TechResult:
        """
        安装依赖包
        
        Args:
            package: 包名
            manager: 包管理器 (pip/npm/pnpm)
        
        Returns:
            TechResult
        """
        if manager not in self.package_managers:
            return TechResult(
                success=False,
                action="install_dep",
                target=package,
                error=f"不支持的包管理器: {manager}"
            )
        
        try:
            pm_cmd = self.package_managers[manager][0]
            
            if manager == "pip":
                cmd = [pm_cmd, "install", package]
            else:
                cmd = [pm_cmd, "install", package]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            tech_result = TechResult(
                success=result.returncode == 0,
                action="install_dep",
                target=package,
                output=result.stdout,
                error=result.stderr if result.returncode != 0 else None,
                metadata={"manager": manager}
            )
        
        except Exception as e:
            tech_result = TechResult(
                success=False,
                action="install_dep",
                target=package,
                error=str(e)
            )
        
        self.history.append(tech_result)
        return tech_result
    
    def check_dependency(self, package: str) -> bool:
        """检查依赖是否已安装"""
        try:
            result = subprocess.run(
                ["pip", "show", package],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except:
            return False
    
    # ========== 工具方法 ==========
    
    def _detect_script_type(self, script_path: str) -> str:
        """检测脚本类型"""
        ext = Path(script_path).suffix.lower()
        
        type_map = {
            ".py": "python",
            ".sh": "bash",
            ".js": "javascript",
            ".ts": "typescript",
            ".rb": "ruby",
            ".go": "go"
        }
        
        return type_map.get(ext, "unknown")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取操作统计"""
        if not self.history:
            return {"total": 0, "success": 0, "failed": 0}
        
        success_count = sum(1 for r in self.history if r.success)
        
        by_action = {}
        for r in self.history:
            action = r.action
            if action not in by_action:
                by_action[action] = {"total": 0, "success": 0}
            by_action[action]["total"] += 1
            if r.success:
                by_action[action]["success"] += 1
        
        return {
            "total": len(self.history),
            "success": success_count,
            "failed": len(self.history) - success_count,
            "success_rate": success_count / len(self.history),
            "by_action": by_action
        }


# ========== 全局实例 ==========

_tech_instance = None

def get_tech() -> Palace3Tech:
    """获取全局技术团队实例"""
    global _tech_instance
    if _tech_instance is None:
        _tech_instance = Palace3Tech()
    return _tech_instance


# ========== 快捷函数 ==========

def install_skill(skill_name: str, **kwargs) -> TechResult:
    """快捷函数：安装技能"""
    return get_tech().install_skill(skill_name, **kwargs)

def run_script(script_path: str, **kwargs) -> TechResult:
    """快捷函数：运行脚本"""
    return get_tech().run_script(script_path, **kwargs)

def execute(command: str, **kwargs) -> TechResult:
    """快捷函数：执行命令"""
    return get_tech().execute(command, **kwargs)


# ========== 测试 ==========

if __name__ == "__main__":
    print("=== 3 宫技术团队测试 ===\n")
    
    tech = Palace3Tech()
    
    # 测试1: 检查依赖
    print("1. 检查依赖:")
    has_pip = tech.check_dependency("pip")
    print(f"   pip 已安装: {has_pip}")
    
    # 测试2: 执行命令
    print("\n2. 执行命令:")
    result = tech.execute("echo 'Hello from 3宫'")
    print(f"   成功: {result.success}")
    print(f"   输出: {result.output.strip() if result.output else ''}")
    
    # 测试3: 执行Python
    print("\n3. 执行 Python:")
    result = tech.execute("python3 -c 'print(1+1)'")
    print(f"   成功: {result.success}")
    print(f"   输出: {result.output.strip() if result.output else ''}")
    
    # 测试4: 统计
    print("\n4. 操作统计:")
    stats = tech.get_stats()
    print(f"   总计: {stats['total']}")
    print(f"   成功率: {stats['success_rate']:.1%}")
    
    print("\n=== 3 宫就绪 ===")