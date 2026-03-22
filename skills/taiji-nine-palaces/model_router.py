#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百炼模型智能路由器
Bailian Model Router - Auto-select optimal model for each task
"""

from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
import json
import os


class TaskType(Enum):
    """任务类型"""
    SIMPLE_QA = "simple_qa"           # 简单问答
    CREATIVE_WRITING = "creative"      # 创意写作
    CODE_GENERATION = "code"           # 代码生成
    CODE_REVIEW = "code_review"        # 代码审查
    DATA_ANALYSIS = "analysis"         # 数据分析
    LONG_CONTEXT = "long_context"      # 长文本处理
    MULTI_STEP = "multi_step"          # 多步推理
    TRANSLATION = "translation"        # 翻译
    SUMMARIZATION = "summarization"    # 摘要
    CLASSIFICATION = "classification"  # 分类


class ModelTier(Enum):
    """模型层级"""
    FAST = "fast"      # 快速/低成本
    BALANCED = "balanced"  # 平衡
    PREMIUM = "premium"    # 高端/复杂任务


@dataclass
class BailianModel:
    """百炼模型定义"""
    model_id: str
    name: str
    tier: ModelTier
    max_tokens: int
    context_window: int
    cost_per_1k: float  # 每 1K tokens 成本（元）
    strengths: List[str]
    best_for: List[TaskType]


# 多模型配置（百炼 + 智谱 + DeepSeek）
# 注意：kimi2.5 是默认主模型，用于对话和简单问答
BAILIAN_MODELS = {
    # 智谱 AI（免费优先）
    "glm-4-flash": BailianModel(
        model_id="glm-4-flash",
        name="智谱 GLM-4-Flash",
        tier=ModelTier.FAST,
        max_tokens=8000,
        context_window=32000,
        cost_per_1k=0.0,  # 免费！
        strengths=["免费", "速度快", "中文优化"],
        best_for=[TaskType.SIMPLE_QA, TaskType.CREATIVE_WRITING, TaskType.SUMMARIZATION],
    ),
    "glm-4-air": BailianModel(
        model_id="glm-4-air",
        name="智谱 GLM-4-Air",
        tier=ModelTier.BALANCED,
        max_tokens=8000,
        context_window=32000,
        cost_per_1k=0.0,  # 免费！
        strengths=["免费", "平衡性能", "中文优秀"],
        best_for=[TaskType.CREATIVE_WRITING, TaskType.DATA_ANALYSIS],
    ),
    # DeepSeek（免费高性能）
    "deepseek-chat": BailianModel(
        model_id="deepseek-chat",
        name="DeepSeek Chat",
        tier=ModelTier.BALANCED,
        max_tokens=8000,
        context_window=32000,
        cost_per_1k=0.0,  # 免费！
        strengths=["免费", "接近 GPT-4", "中文优秀"],
        best_for=[TaskType.CREATIVE_WRITING, TaskType.MULTI_STEP],
    ),
    "deepseek-coder": BailianModel(
        model_id="deepseek-coder",
        name="DeepSeek Coder",
        tier=ModelTier.PREMIUM,
        max_tokens=8000,
        context_window=32000,
        cost_per_1k=0.0,  # 免费！
        strengths=["免费", "代码专用", "接近 GPT-4 Code"],
        best_for=[TaskType.CODE_GENERATION, TaskType.CODE_REVIEW],
    ),
    # 百炼模型（备用）
    "qwen-turbo": BailianModel(
        model_id="qwen-turbo",
        name="通义千问-Turbo",
        tier=ModelTier.FAST,
        max_tokens=8000,
        context_window=32000,
        cost_per_1k=0.002,
        strengths=["速度快", "成本低", "简单任务"],
        best_for=[TaskType.CLASSIFICATION, TaskType.TRANSLATION],
    ),
    "qwen-plus": BailianModel(
        model_id="qwen-plus",
        name="通义千问-Plus",
        tier=ModelTier.BALANCED,
        max_tokens=8000,
        context_window=32000,
        cost_per_1k=0.008,
        strengths=["平衡性能", "通用任务", "性价比高"],
        best_for=[TaskType.CREATIVE_WRITING, TaskType.SUMMARIZATION, TaskType.DATA_ANALYSIS],
    ),
    "qwen-max": BailianModel(
        model_id="qwen-max",
        name="通义千问-Max",
        tier=ModelTier.PREMIUM,
        max_tokens=8000,
        context_window=32000,
        cost_per_1k=0.04,
        strengths=["复杂推理", "代码能力", "高质量输出"],
        best_for=[TaskType.CODE_GENERATION, TaskType.CODE_REVIEW, TaskType.MULTI_STEP],
    ),
    "qwen-long": BailianModel(
        model_id="qwen-long",
        name="通义千问-Long",
        tier=ModelTier.PREMIUM,
        max_tokens=8000,
        context_window=200000,  # 200K 超长上下文
        cost_per_1k=0.06,
        strengths=["超长文本", "文档分析", "多文档处理"],
        best_for=[TaskType.LONG_CONTEXT, TaskType.SUMMARIZATION],
    ),
    "qwen-coder": BailianModel(
        model_id="qwen-coder",
        name="通义千问-Coder",
        tier=ModelTier.PREMIUM,
        max_tokens=8000,
        context_window=32000,
        cost_per_1k=0.04,
        strengths=["代码生成", "代码审查", "调试"],
        best_for=[TaskType.CODE_GENERATION, TaskType.CODE_REVIEW],
    ),
}


class ModelRouter:
    """
    模型路由器
    
    根据任务特征自动选择最优模型，平衡成本与性能
    默认对话使用 kimi2.5，专业任务使用百炼模型
    """
    
    def __init__(self, api_key: str = None, default_model: str = "kimi2.5"):
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.default_model = default_model  # kimi2.5 用于日常对话
        self.model_history: List[Dict] = []
        
        # 任务类型到模型层级的映射规则
        self.routing_rules = {
            TaskType.SIMPLE_QA: ModelTier.FAST,
            TaskType.CLASSIFICATION: ModelTier.FAST,
            TaskType.TRANSLATION: ModelTier.FAST,
            TaskType.CREATIVE_WRITING: ModelTier.BALANCED,
            TaskType.SUMMARIZATION: ModelTier.BALANCED,
            TaskType.DATA_ANALYSIS: ModelTier.BALANCED,
            TaskType.CODE_GENERATION: ModelTier.PREMIUM,
            TaskType.CODE_REVIEW: ModelTier.PREMIUM,
            TaskType.MULTI_STEP: ModelTier.PREMIUM,
            TaskType.LONG_CONTEXT: ModelTier.PREMIUM,
        }
        
        # 特殊任务类型：对话使用 kimi2.5
        self.conversation_model = "kimi2.5"
    
    def classify_task(self, prompt: str, context: Dict[str, Any] = None) -> TaskType:
        """
        根据提示词分类任务类型
        
        优先级顺序：
        1. 代码相关（最高优先级）
        2. 翻译
        3. 长文本
        4. 多步推理
        5. 创意写作
        6. 摘要
        7. 分类
        8. 数据分析
        9. 对话/问候
        10. 默认简单问答
        """
        prompt_lower = prompt.lower()
        prompt_length = len(prompt)
        
        # 1. 代码相关（最高优先级）
        code_keywords = ["代码", "code", "function", "def ", "import ", "class ", "编程", "debug", "python", "javascript"]
        if any(kw in prompt_lower for kw in code_keywords):
            if "review" in prompt_lower or "检查" in prompt_lower or "优化" in prompt_lower or "审查" in prompt_lower:
                return TaskType.CODE_REVIEW
            return TaskType.CODE_GENERATION
        
        # 2. 翻译相关
        translation_keywords = ["翻译", "translate", "翻译成", "to english", "to chinese"]
        if any(kw in prompt_lower for kw in translation_keywords):
            return TaskType.TRANSLATION
        
        # 3. 长文本
        if prompt_length > 10000:
            return TaskType.LONG_CONTEXT
        
        # 4. 多步推理
        reasoning_keywords = ["推理", "reasoning", "分析", "analyze", "比较", "compare", 
                             "为什么", "why", "如何", "how to", "步骤", "step"]
        if any(kw in prompt_lower for kw in reasoning_keywords):
            return TaskType.MULTI_STEP
        
        # 5. 创意写作
        creative_keywords = ["写文章", "write", "创作", "创意的", "creative", "故事", "story"]
        if any(kw in prompt_lower for kw in creative_keywords):
            return TaskType.CREATIVE_WRITING
        
        # 6. 摘要
        summary_keywords = ["摘要", "summary", "总结", "summarize", "概述", "overview"]
        if any(kw in prompt_lower for kw in summary_keywords):
            return TaskType.SUMMARIZATION
        
        # 7. 分类
        classification_keywords = ["分类", "classify", "标签", "tag", "类别", "category"]
        if any(kw in prompt_lower for kw in classification_keywords):
            return TaskType.CLASSIFICATION
        
        # 8. 数据分析
        analysis_keywords = ["分析", "analyze", "数据", "data", "统计", "statistics"]
        if any(kw in prompt_lower for kw in analysis_keywords):
            return TaskType.DATA_ANALYSIS
        
        # 9. 对话/问候（使用 kimi2.5）
        conversation_keywords = ["你好", "hello", "hi", "早上好", "下午好", "晚上好", 
                                "在吗", "help", "请问", "帮我", "介绍一下"]
        if any(kw in prompt_lower for kw in conversation_keywords):
            return TaskType.SIMPLE_QA
        
        # 10. 默认简单问答（使用 kimi2.5）
        return TaskType.SIMPLE_QA
    
    def select_model(self, task_type: TaskType, context: Dict[str, Any] = None) -> BailianModel:
        """
        根据任务类型选择模型（免费优先策略）
        
        选择逻辑：
        1. 优先使用免费模型（智谱/DeepSeek）
        2. 对话/简单问答 → kimi2.5 或 glm-4-flash
        3. 代码生成 → deepseek-coder
        4. 代码审查 → glm-4-air 或 deepseek-chat
        5. 其他任务 → 根据层级选择免费模型
        """
        # 对话和简单问答优先使用智谱 GLM-4-Flash（免费）
        if task_type == TaskType.SIMPLE_QA:
            # 优先免费模型
            return BAILIAN_MODELS.get("glm-4-flash", BailianModel(
                model_id="kimi2.5",
                name="Kimi 2.5",
                tier=ModelTier.BALANCED,
                max_tokens=8000,
                context_window=128000,
                cost_per_1k=0.012,
                strengths=["长文本处理", "对话理解", "通用任务"],
                best_for=[TaskType.SIMPLE_QA],
            ))
        
        # 代码生成使用 DeepSeek-Coder（免费，接近 GPT-4 Code）
        if task_type == TaskType.CODE_GENERATION:
            return BAILIAN_MODELS.get("deepseek-coder", BAILIAN_MODELS.get("glm-4-flash"))
        
        # 代码审查使用 DeepSeek-Chat 或 GLM-4-Air（免费）
        if task_type == TaskType.CODE_REVIEW:
            return BAILIAN_MODELS.get("deepseek-chat", BAILIAN_MODELS.get("glm-4-air"))
        
        # 创意写作使用 GLM-4-Flash 或 DeepSeek-Chat（免费）
        if task_type == TaskType.CREATIVE_WRITING:
            return BAILIAN_MODELS.get("glm-4-flash", BAILIAN_MODELS.get("deepseek-chat"))
        
        # 摘要使用 GLM-4-Flash（免费）
        if task_type == TaskType.SUMMARIZATION:
            return BAILIAN_MODELS.get("glm-4-flash")
        
        # 多步推理使用 DeepSeek-Chat（免费，接近 GPT-4）
        if task_type == TaskType.MULTI_STEP:
            return BAILIAN_MODELS.get("deepseek-chat", BAILIAN_MODELS.get("glm-4-air"))
        
        # 确定目标层级
        target_tier = self.routing_rules.get(task_type, ModelTier.BALANCED)
        
        # 获取同层级模型
        candidate_models = [
            model for model in BAILIAN_MODELS.values()
            if model.tier == target_tier
        ]
        
        # 如果没有同层级模型，降级或升级
        if not candidate_models:
            if target_tier == ModelTier.FAST:
                candidate_models = [m for m in BAILIAN_MODELS.values() if m.tier == ModelTier.BALANCED]
            elif target_tier == ModelTier.PREMIUM:
                candidate_models = [m for m in BAILIAN_MODELS.values() if m.tier == ModelTier.BALANCED]
            else:
                candidate_models = list(BAILIAN_MODELS.values())
        
        # 根据任务类型筛选最佳匹配
        best_matches = [
            model for model in candidate_models
            if task_type in model.best_for
        ]
        
        if best_matches:
            # 选择成本最低的
            selected = min(best_matches, key=lambda m: m.cost_per_1k)
        else:
            # 选择层级内成本最低的
            selected = min(candidate_models, key=lambda m: m.cost_per_1k)
        
        # 检查上下文长度
        if context and "prompt_length" in context:
            if context["prompt_length"] > selected.context_window:
                # 选择更大上下文的模型
                for model in sorted(candidate_models, key=lambda m: m.context_window, reverse=True):
                    if model.context_window >= context["prompt_length"]:
                        selected = model
                        break
        
        return selected
    
    def route(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        完整路由流程
        
        Returns:
            包含模型选择结果的字典
        """
        # 分类任务
        task_type = self.classify_task(prompt, context)
        
        # 选择模型
        model = self.select_model(task_type, context)
        
        # 记录历史
        result = {
            "task_type": task_type.value,
            "selected_model": model.model_id,
            "model_name": model.name,
            "tier": model.tier.value,
            "estimated_cost": self._estimate_cost(prompt, model),
            "reason": self._generate_reason(task_type, model),
            "alternatives": self._get_alternatives(task_type),
        }
        
        self.model_history.append(result)
        
        return result
    
    def _estimate_cost(self, prompt: str, model: BailianModel) -> float:
        """估算成本"""
        # 简单估算：每 100 字符≈15 tokens
        tokens = len(prompt) * 15 / 100
        return round(tokens * model.cost_per_1k / 1000, 6)
    
    def _generate_reason(self, task_type: TaskType, model: BailianModel) -> str:
        """生成选择理由"""
        return f"任务类型：{task_type.value}，选择{model.name}（{model.tier.value}层级），优势：{', '.join(model.strengths[:2])}"
    
    def _get_alternatives(self, task_type: TaskType) -> List[str]:
        """获取替代模型"""
        alternatives = [
            model.model_id for model in BAILIAN_MODELS.values()
            if task_type in model.best_for and model.model_id != self.default_model
        ]
        return alternatives[:2]
    
    def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """获取模型信息"""
        if model_id not in BAILIAN_MODELS:
            return None
        
        model = BAILIAN_MODELS[model_id]
        return {
            "model_id": model.model_id,
            "name": model.name,
            "tier": model.tier.value,
            "max_tokens": model.max_tokens,
            "context_window": model.context_window,
            "cost_per_1k": model.cost_per_1k,
            "strengths": model.strengths,
            "best_for": [t.value for t in model.best_for],
        }
    
    def list_models(self) -> List[Dict[str, Any]]:
        """列出所有可用模型"""
        return [self.get_model_info(model_id) for model_id in BAILIAN_MODELS]
    
    def get_history(self, limit: int = 10) -> List[Dict]:
        """获取路由历史"""
        return self.model_history[-limit:]
    
    def get_cost_summary(self) -> Dict[str, Any]:
        """获取成本统计"""
        if not self.model_history:
            return {"total_cost": 0, "total_requests": 0}
        
        total_cost = sum(r.get("estimated_cost", 0) for r in self.model_history)
        
        model_counts = {}
        for r in self.model_history:
            model = r.get("selected_model", "unknown")
            model_counts[model] = model_counts.get(model, 0) + 1
        
        return {
            "total_cost": round(total_cost, 4),
            "total_requests": len(self.model_history),
            "avg_cost_per_request": round(total_cost / len(self.model_history), 6),
            "model_distribution": model_counts,
        }


def demo():
    """演示"""
    print("="*60)
    print("        百炼模型智能路由器演示")
    print("="*60)
    
    router = ModelRouter()
    
    # 测试用例
    test_cases = [
        ("你好，今天天气怎么样？", "简单问候"),
        ("请帮我翻译这句话到英文：你好世界", "翻译任务"),
        ("写一个 Python 函数计算斐波那契数列", "代码生成"),
        ("请检查这段代码的性能问题并优化", "代码审查"),
        ("帮我总结这篇文章的主要内容...", "摘要任务" * 100),  # 长文本
        ("分析这个数据集的趋势和模式", "数据分析"),
        ("写一篇关于 AI 未来的创意文章", "创意写作"),
        ("比较 Qwen 和 GPT 的优缺点", "多步推理"),
    ]
    
    print("\n【模型路由测试】\n")
    
    for prompt, description in test_cases:
        result = router.route(prompt)
        print(f"任务：{description}")
        print(f"  类型：{result['task_type']}")
        print(f"  模型：{result['model_name']} ({result['selected_model']})")
        print(f"  层级：{result['tier']}")
        print(f"  成本：¥{result['estimated_cost']:.6f}")
        print(f"  理由：{result['reason']}")
        print()
    
    # 显示模型列表
    print("\n【可用模型】\n")
    models = router.list_models()
    for model in models:
        print(f"{model['name']} ({model['model_id']})")
        print(f"  层级：{model['tier']} | 上下文：{model['context_window']:,} | 成本：¥{model['cost_per_1k']}/1K tokens")
        print(f"  优势：{', '.join(model['strengths'])}")
        print()
    
    # 成本统计
    print("\n【成本统计】\n")
    summary = router.get_cost_summary()
    print(f"总请求：{summary['total_requests']}")
    print(f"总成本：¥{summary['total_cost']:.4f}")
    print(f"平均成本：¥{summary['avg_cost_per_request']:.6f}/请求")
    print(f"模型分布：{summary['model_distribution']}")


if __name__ == "__main__":
    demo()
