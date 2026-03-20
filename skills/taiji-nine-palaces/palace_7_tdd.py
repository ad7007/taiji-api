#!/usr/bin/env python3
"""
7 宫 - 法务框架 · Red/Green TDD 节点

提供任务验收标准定义和绿灯检查能力。
5 宫调用此模块进行任务质量把控。
"""

import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

TAIJI_API_URL = "http://localhost:8000"

# 验收标准模板库
ACCEPTANCE_STANDARDS = {
    "video_process": {
        "standards": [
            {"name": "核心方法论", "required": True, "check": "必须提取视频核心观点"},
            {"name": "可行动建议", "required": True, "check": "必须有具体行动项"},
            {"name": "关键数据/案例", "required": True, "check": "必须引用视频中的数据或案例"},
            {"name": "结构清晰", "required": True, "check": "必须有清晰的标题和分段"},
            {"name": "时长匹配", "required": False, "check": "摘要长度与视频时长成正比"}
        ]
    },
    "video_summary": {
        "standards": [
            {"name": "核心方法论", "required": True, "check": "必须提取视频核心观点"},
            {"name": "可行动建议", "required": True, "check": "必须有具体行动项"},
            {"name": "关键数据/案例", "required": True, "check": "必须引用视频中的数据或案例"},
            {"name": "结构清晰", "required": True, "check": "必须有清晰的标题和分段"},
            {"name": "时长匹配", "required": False, "check": "摘要长度与视频时长成正比"}
        ]
    },
    "file_download": {
        "standards": [
            {"name": "文件完整性", "required": True, "check": "文件大小>0 且格式正确"},
            {"name": "命名规范", "required": True, "check": "文件名包含任务名和时间戳"},
            {"name": "落盘位置", "required": True, "check": "保存到指定目录"},
            {"name": "成功确认", "required": True, "check": "返回文件路径和大小"}
        ]
    },
    "data_analysis": {
        "standards": [
            {"name": "数据来源", "required": True, "check": "必须说明数据来源"},
            {"name": "分析方法", "required": True, "check": "必须说明使用的分析方法"},
            {"name": "核心洞察", "required": True, "check": "必须有 3 条以上洞察"},
            {"name": "可视化", "required": False, "check": "有图表辅助说明"}
        ]
    },
    "skill_install": {
        "standards": [
            {"name": "技能来源", "required": True, "check": "必须说明来自 skillhub 或 clawhub"},
            {"name": "版本信息", "required": True, "check": "必须记录版本号"},
            {"name": "依赖检查", "required": True, "check": "必须检查并安装依赖"},
            {"name": "功能验证", "required": True, "check": "必须执行基本功能测试"}
        ]
    }
}


class Palace7TDD:
    """7 宫 TDD 节点类"""
    
    def __init__(self, api_url: str = TAIJI_API_URL):
        self.api_url = api_url
        self.node_id = "7-tdd"
    
    def define_acceptance_criteria(
        self,
        task_type: str,
        requirements: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        定义任务验收标准
        
        Args:
            task_type: 任务类型 (video_summary, file_download, data_analysis, skill_install)
            requirements: 额外要求列表
        
        Returns:
            验收标准字典
        """
        # 获取基础模板
        base_standards = ACCEPTANCE_STANDARDS.get(task_type, {"standards": []})
        
        # 添加额外要求
        if requirements:
            for req in requirements:
                base_standards["standards"].append({
                    "name": f"自定义要求-{len(base_standards['standards'])+1}",
                    "required": True,
                    "check": req
                })
        
        # 记录到 API
        try:
            response = requests.post(
                f"{self.api_url}/api/zhengzhuan",
                json={"node_id": self.node_id, "value": 0.9},
                timeout=5
            )
            if response.status_code == 200:
                task_id = response.json().get("task_id", "unknown")
            else:
                task_id = "api_error"
        except Exception as e:
            task_id = f"error_{str(e)}"
        
        return {
            "task_type": task_type,
            "standards": base_standards["standards"],
            "defined_at": datetime.now().isoformat(),
            "task_id": task_id
        }
    
    def green_light_check(
        self,
        task_type: str,
        output: Any,
        standards: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        绿灯检查 - 对照验收标准验证输出
        
        Args:
            task_type: 任务类型
            output: 任务输出
            standards: 验收标准（如不提供则使用默认模板）
        
        Returns:
            检查结果 {"passed": bool, "reasons": [...]}
        """
        if not standards:
            standards = ACCEPTANCE_STANDARDS.get(task_type, {"standards": []})
        
        results = []
        failed_reasons = []
        
        for std in standards.get("standards", []):
            # 简单检查逻辑 - 实际应用中应根据 output 内容判断
            # 这里用输出长度作为代理指标
            output_str = str(output) if not isinstance(output, str) else output
            
            # 基本检查
            passed = len(output_str) > 50  # 简化检查
            
            # 特殊检查
            if std["name"] == "结构清晰" and "##" not in output_str:
                passed = False
            
            if std["name"] == "核心方法论" and any(kw in output_str for kw in ["核心", "方法", "关键"]):
                passed = True
            
            results.append({
                "name": std["name"],
                "passed": passed,
                "check": std["check"]
            })
            
            if not passed and std["required"]:
                failed_reasons.append(f"{std['name']}: {std['check']}")
        
        # 记录到 API
        try:
            response = requests.post(
                f"{self.api_url}/api/fanzhuan",
                json={"node_id": self.node_id},
                timeout=5
            )
        except:
            pass
        
        return {
            "passed": len(failed_reasons) == 0,
            "reasons": failed_reasons,
            "details": results,
            "checked_at": datetime.now().isoformat()
        }
    
    def red_light_confirm(self, task_description: str) -> Dict[str, Any]:
        """
        红灯确认 - 确认当前状态是失败的
        
        Args:
            task_description: 任务描述
        
        Returns:
            确认结果
        """
        # 红灯确认的逻辑：确认"现在没有完成任务"
        return {
            "confirmed": True,
            "message": f"红灯确认：任务未开始 - {task_description}",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_node_status(self) -> Dict[str, Any]:
        """获取节点状态"""
        try:
            response = requests.get(
                f"{self.api_url}/api/taiji/palace/7",
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
        except:
            pass
        
        return {
            "node_id": self.node_id,
            "status": "active",
            "type": "methodology"
        }


# 5 宫调用示例
if __name__ == "__main__":
    tdd = Palace7TDD()
    
    # 示例：定义视频摘要任务的验收标准
    print("=== 定义验收标准 ===")
    standards = tdd.define_acceptance_criteria(
        task_type="video_summary",
        requirements=["必须包含金句摘录"]
    )
    print(json.dumps(standards, indent=2, ensure_ascii=False))
    
    # 示例：绿灯检查
    print("\n=== 绿灯检查 ===")
    sample_output = """
    # 视频摘要
    
    ## 核心方法论
    Red/Green TDD 是核心...
    
    ## 可行动建议
    1. 先写测试
    2. 确认红灯
    3. 写实现
    """
    result = tdd.green_light_check("video_summary", sample_output, standards)
    print(json.dumps(result, indent=2, ensure_ascii=False))
