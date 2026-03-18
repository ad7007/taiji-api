#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3 宫 - 技术团队 · 模型分配专家
Palace 3 - Technical Team · Model Allocator

核心能力:
1. 模型成本感知（API Token vs Zero Token）
2. 任务 - 模型匹配
3. 优先级驱动分配
4. 多模型负载均衡

灵感来源：OpenClaw Zero Token 项目
- 浏览器自动化接管网页会话
- 零成本调用 Claude/DeepSeek/GPT/Gemini
- API Token 模式 与 Zero Token 模式 并行
"""

from enum import Enum
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


# ========== 枚举定义 ==========

class ModelProvider(Enum):
    """模型提供商"""
    CLAUDE = "claude"
    DEEPSEEK = "deepseek"
    GPT = "gpt"
    GEMINI = "gemini"
    QWEN = "qwen"
    ZHIPU = "zhipu"


class AccessMode(Enum):
    """访问模式"""
    API_TOKEN = "api_token"      # 传统 API 调用（付费）
    ZERO_TOKEN = "zero_token"    # 浏览器自动化（免费）


class TaskComplexity(Enum):
    """任务复杂度"""
    SIMPLE = 1      # 简单任务（聊天、查询）
    MEDIUM = 2      # 中等任务（摘要、分类）
    COMPLEX = 3     # 复杂任务（推理、分析）
    EXPERT = 4      # 专家任务（代码、创作）


# ========== 数据模型 ==========

@dataclass
class ModelCapability:
    """模型能力描述"""
    provider: ModelProvider
    model_name: str
    access_mode: AccessMode
    strengths: List[str]  # 擅长领域
    cost_level: int  # 1-5（1=免费，5=昂贵）
    speed_level: int  # 1-5（1=慢，5=快）
    quality_level: int  # 1-5（1=低，5=高）


@dataclass
class ModelAllocation:
    """模型分配结果"""
    model: str
    provider: ModelProvider
    access_mode: AccessMode
    reason: str
    estimated_cost: float
    estimated_time: float


# ========== 3 宫模型分配器 ==========

class Palace3ModelAllocator:
    """
    3 宫模型分配专家
    
    核心逻辑:
    1. 根据任务类型匹配模型能力
    2. 根据优先级选择访问模式（API Token vs Zero Token）
    3. 根据成本预算优化分配
    4. 支持多模型负载均衡
    """
    
    # 模型能力库
    MODEL_CAPABILITIES = {
        # Qwen 系列（当前默认）
        "qwen3.5-plus": ModelCapability(
            provider=ModelProvider.QWEN,
            model_name="qwen3.5-plus",
            access_mode=AccessMode.API_TOKEN,
            strengths=["推理", "代码", "分析", "创作"],
            cost_level=3,
            speed_level=4,
            quality_level=5
        ),
        "qwen3.5": ModelCapability(
            provider=ModelProvider.QWEN,
            model_name="qwen3.5",
            access_mode=AccessMode.API_TOKEN,
            strengths=["通用", "快速响应"],
            cost_level=2,
            speed_level=5,
            quality_level=4
        ),
        
        # Claude 系列（Zero Token 支持）
        "claude-sonnet": ModelCapability(
            provider=ModelProvider.CLAUDE,
            model_name="claude-sonnet",
            access_mode=AccessMode.ZERO_TOKEN,  # ✅ 支持浏览器自动化
            strengths=["创作", "对话", "分析"],
            cost_level=1,  # Zero Token = 免费
            speed_level=4,
            quality_level=5
        ),
        "claude-opus": ModelCapability(
            provider=ModelProvider.CLAUDE,
            model_name="claude-opus",
            access_mode=AccessMode.API_TOKEN,
            strengths=["复杂推理", "代码", "专业领域"],
            cost_level=5,
            speed_level=3,
            quality_level=5
        ),
        
        # DeepSeek 系列（Zero Token 支持）
        "deepseek-chat": ModelCapability(
            provider=ModelProvider.DEEPSEEK,
            model_name="deepseek-chat",
            access_mode=AccessMode.ZERO_TOKEN,  # ✅ 支持浏览器自动化
            strengths=["代码", "推理", "数学"],
            cost_level=1,  # Zero Token = 免费
            speed_level=4,
            quality_level=4
        ),
        
        # GPT 系列（Zero Token 支持）
        "gpt-4o": ModelCapability(
            provider=ModelProvider.GPT,
            model_name="gpt-4o",
            access_mode=AccessMode.ZERO_TOKEN,  # ✅ 支持浏览器自动化
            strengths=["通用", "多模态", "创作"],
            cost_level=1,  # Zero Token = 免费
            speed_level=4,
            quality_level=5
        ),
        
        # Gemini 系列（Zero Token 支持）
        "gemini-pro": ModelCapability(
            provider=ModelProvider.GEMINI,
            model_name="gemini-pro",
            access_mode=AccessMode.ZERO_TOKEN,  # ✅ 支持浏览器自动化
            strengths=["多模态", "长文本", "分析"],
            cost_level=1,  # Zero Token = 免费
            speed_level=4,
            quality_level=4
        ),
        
        # 🆕 本地模型支持（Ollama）
        "ollama/llama3": ModelCapability(
            provider=ModelProvider.OLLAMA,
            model_name="llama3",
            access_mode=AccessMode.LOCAL,  # 本地运行
            strengths=["通用", "快速", "隐私"],
            cost_level=0,  # 免费
            speed_level=5,
            quality_level=4
        ),
        "ollama/mistral": ModelCapability(
            provider=ModelProvider.OLLAMA,
            model_name="mistral",
            access_mode=AccessMode.LOCAL,
            strengths=["代码", "推理"],
            cost_level=0,
            speed_level=5,
            quality_level=4
        ),
        "ollama/qwen": ModelCapability(
            provider=ModelProvider.OLLAMA,
            model_name="qwen",
            access_mode=AccessMode.LOCAL,
            strengths=["中文", "通用"],
            cost_level=0,
            speed_level=5,
            quality_level=4
        ),
    }
    
    # 任务类型 → 推荐模型
    TASK_MODEL_MAPPING = {
        "video_process": {
            "default": "qwen3.5-plus",
            "zero_token": "gemini-pro",  # 多模态支持
            "priority_override": {1: "qwen3.5-plus", 2: "qwen3.5-plus", 3: "gemini-pro", 4: "gemini-pro"}
        },
        "file_download": {
            "default": "qwen3.5",  # 简单任务
            "zero_token": "deepseek-chat",
            "priority_override": {}
        },
        "data_analysis": {
            "default": "qwen3.5-plus",
            "zero_token": "claude-sonnet",  # 分析能力强
            "priority_override": {1: "qwen3.5-plus", 2: "claude-sonnet", 3: "claude-sonnet", 4: "deepseek-chat"}
        },
        "skill_install": {
            "default": "qwen3.5",
            "zero_token": "deepseek-chat",  # 代码能力强
            "priority_override": {}
        },
        "content_create": {
            "default": "qwen3.5-plus",
            "zero_token": "claude-sonnet",  # 创作能力强
            "priority_override": {1: "qwen3.5-plus", 2: "claude-sonnet", 3: "gpt-4o", 4: "gpt-4o"}
        },
        "monitoring": {
            "default": "qwen3.5",
            "zero_token": "gemini-pro",
            "priority_override": {}
        },
        "legal_compliance": {
            "default": "qwen3.5-plus",
            "zero_token": "claude-sonnet",
            "priority_override": {}
        },
        "general": {
            "default": "qwen3.5",
            "zero_token": "gpt-4o",
            "priority_override": {}
        }
    }
    
    # 成本估算（元/千 token）
    COST_ESTIMATES = {
        "qwen3.5-plus": 0.004,
        "qwen3.5": 0.002,
        "claude-sonnet": 0.0,  # Zero Token
        "claude-opus": 0.015,
        "deepseek-chat": 0.0,  # Zero Token
        "gpt-4o": 0.0,  # Zero Token
        "gemini-pro": 0.0  # Zero Token
    }
    
    def __init__(self, prefer_zero_token: bool = True):
        """
        初始化 3 宫模型分配器
        
        Args:
            prefer_zero_token: 是否优先使用 Zero Token 模式（免费）
        """
        self.prefer_zero_token = prefer_zero_token
        self.allocation_history: List[Dict[str, Any]] = []
    
    def allocate_model(
        self,
        task_type: str,
        priority: int = 3,
        budget: float = 0.0,
        complexity: TaskComplexity = TaskComplexity.MEDIUM
    ) -> ModelAllocation:
        """
        分配模型
        
        Args:
            task_type: 任务类型
            priority: 优先级 (1=CRITICAL, 2=HIGH, 3=MEDIUM, 4=LOW)
            budget: 成本预算（0=免费优先）
            complexity: 任务复杂度
        
        Returns:
            ModelAllocation 分配结果
        """
        # 1. 获取任务类型配置
        task_config = self.TASK_MODEL_MAPPING.get(task_type, self.TASK_MODEL_MAPPING["general"])
        
        # 2. 检查优先级覆盖
        if priority in task_config.get("priority_override", {}):
            model_name = task_config["priority_override"][priority]
            access_mode = self.MODEL_CAPABILITIES[model_name].access_mode
            return self._create_allocation(model_name, access_mode, f"优先级{priority}覆盖")
        
        # 3. 根据预算和偏好选择模式
        if self.prefer_zero_token or budget <= 0:
            # 优先 Zero Token（免费）
            model_name = task_config.get("zero_token", task_config["default"])
            access_mode = AccessMode.ZERO_TOKEN
            reason = "Zero Token 模式（浏览器自动化，免费）"
        else:
            # 使用 API Token（付费，质量更高）
            model_name = task_config["default"]
            access_mode = AccessMode.API_TOKEN
            reason = "API Token 模式（付费，质量保证）"
        
        # 4. 复杂度调整
        if complexity == TaskComplexity.EXPERT:
            # 专家任务升级到更强模型
            if access_mode == AccessMode.ZERO_TOKEN:
                model_name = "claude-sonnet"  # 免费中最强
            else:
                model_name = "qwen3.5-plus"  # 付费中最强
            reason += " - 专家任务升级"
        
        return self._create_allocation(model_name, access_mode, reason)
    
    def _create_allocation(
        self,
        model_name: str,
        access_mode: AccessMode,
        reason: str
    ) -> ModelAllocation:
        """创建分配结果"""
        cap = self.MODEL_CAPABILITIES.get(model_name)
        if not cap:
            return ModelAllocation(
                model=model_name,
                provider=ModelProvider.QWEN,
                access_mode=access_mode,
                reason="模型不存在，使用默认",
                estimated_cost=0.0,
                estimated_time=1.0
            )
        
        cost_per_1k = self.COST_ESTIMATES.get(model_name, 0.002)
        estimated_tokens = 2000  # 假设平均 2k tokens
        
        return ModelAllocation(
            model=model_name,
            provider=cap.provider,
            access_mode=access_mode,
            reason=reason,
            estimated_cost=cost_per_1k * (estimated_tokens / 1000),
            estimated_time=1.0 / cap.speed_level * 5  # 速度等级转换
        )
    
    def get_model_capabilities(self, provider: Optional[ModelProvider] = None) -> List[Dict[str, Any]]:
        """获取模型能力列表"""
        result = []
        for name, cap in self.MODEL_CAPABILITIES.items():
            if provider and cap.provider != provider:
                continue
            result.append({
                "model": name,
                "provider": cap.provider.value,
                "access_mode": cap.access_mode.value,
                "strengths": cap.strengths,
                "cost_level": cap.cost_level,
                "speed_level": cap.speed_level,
                "quality_level": cap.quality_level
            })
        return result
    
    def compare_modes(self, task_type: str) -> Dict[str, Any]:
        """
        比较 API Token vs Zero Token 模式
        
        Returns:
            对比结果
        """
        config = self.TASK_MODEL_MAPPING.get(task_type, self.TASK_MODEL_MAPPING["general"])
        
        api_model = config["default"]
        zero_model = config.get("zero_token", api_model)
        
        api_cap = self.MODEL_CAPABILITIES.get(api_model)
        zero_cap = self.MODEL_CAPABILITIES.get(zero_model)
        
        return {
            "task_type": task_type,
            "api_token": {
                "model": api_model,
                "provider": api_cap.provider.value if api_cap else "unknown",
                "cost_level": api_cap.cost_level if api_cap else 3,
                "quality_level": api_cap.quality_level if api_cap else 4,
                "estimated_cost": self.COST_ESTIMATES.get(api_model, 0.002) * 2  # 假设 2k tokens
            },
            "zero_token": {
                "model": zero_model,
                "provider": zero_cap.provider.value if zero_cap else "unknown",
                "cost_level": zero_cap.cost_level if zero_cap else 1,
                "quality_level": zero_cap.quality_level if zero_cap else 4,
                "estimated_cost": 0.0
            },
            "recommendation": "优先使用 Zero Token 模式，质量要求高时使用 API Token"
        }
    
    def record_allocation(self, allocation: ModelAllocation, task_id: str):
        """记录分配历史"""
        self.allocation_history.append({
            "task_id": task_id,
            "model": allocation.model,
            "provider": allocation.provider.value,
            "access_mode": allocation.access_mode.value,
            "reason": allocation.reason,
            "estimated_cost": allocation.estimated_cost,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_cost_report(self) -> Dict[str, Any]:
        """生成成本报告"""
        if not self.allocation_history:
            return {"message": "暂无分配记录"}
        
        total_cost = sum(a["estimated_cost"] for a in self.allocation_history)
        zero_token_count = sum(1 for a in self.allocation_history if a["access_mode"] == "zero_token")
        api_token_count = len(self.allocation_history) - zero_token_count
        
        return {
            "total_tasks": len(self.allocation_history),
            "zero_token_tasks": zero_token_count,
            "api_token_tasks": api_token_count,
            "total_estimated_cost": total_cost,
            "savings": api_token_count * 0.004 - total_cost,  # 假设 API Token 平均 0.004 元/千 token
            "zero_token_ratio": zero_token_count / len(self.allocation_history) if self.allocation_history else 0
        }


# ========== 导出给 L4 引擎使用 ==========

# 全局 3 宫分配器实例
_palace3_allocator: Optional[Palace3ModelAllocator] = None


def get_palace3_allocator() -> Palace3ModelAllocator:
    """获取 3 宫分配器单例"""
    global _palace3_allocator
    if _palace3_allocator is None:
        _palace3_allocator = Palace3ModelAllocator(prefer_zero_token=True)
    return _palace3_allocator


def palace3_allocate_model(
    task_type: str,
    priority: int = 3,
    budget: float = 0.0
) -> Dict[str, Any]:
    """
    3 宫模型分配入口（供 L4 引擎调用）
    
    Returns:
        分配结果字典
    """
    allocator = get_palace3_allocator()
    allocation = allocator.allocate_model(task_type, priority, budget)
    allocator.record_allocation(allocation, f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    
    return {
        "model": allocation.model,
        "provider": allocation.provider.value,
        "access_mode": allocation.access_mode.value,
        "reason": allocation.reason,
        "estimated_cost": allocation.estimated_cost,
        "estimated_time_seconds": allocation.estimated_time
    }


def palace3_get_capabilities() -> List[Dict[str, Any]]:
    """获取模型能力列表（供 L4 引擎调用）"""
    return get_palace3_allocator().get_model_capabilities()


def palace3_compare_modes(task_type: str) -> Dict[str, Any]:
    """比较两种模式（供 L4 引擎调用）"""
    return get_palace3_allocator().compare_modes(task_type)


def palace3_get_cost_report() -> Dict[str, Any]:
    """获取成本报告（供 L4 引擎调用）"""
    return get_palace3_allocator().get_cost_report()
