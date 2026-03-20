#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3-技术团队宫 - 代码管理、自动化脚本、智能模型路由
Palace 3 - Tech Team & Code Management

特点：
- 根据任务类型自动切换最优百炼模型
- 仅在请求报告时才生成，避免浪费 token
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
import sys

sys.path.insert(0, '/root/.openclaw/workspace/skills/taiji-nine-palaces')

from palace_base import PalaceBase
from bailian_client import BailianClient
from model_router import ModelRouter, TaskType


class Palace3Tech(PalaceBase):
    """
    3-技术团队宫
    
    职责:
    - 代码生成与审查
    - Git 项目管理
    - 自动化脚本
    - 技术文档
    
    技能:
    - github: 代码管理
    - python-executor: 代码执行
    - bailian: 智能模型路由
    
    模型策略:
    - 简单问答 → qwen-turbo
    - 代码生成 → qwen-coder
    - 代码审查 → qwen-max
    - 技术文档 → qwen-plus
    """
    
    def __init__(self):
        super().__init__(
            palace_id=3,
            palace_name="3-技术团队",
            element="木"
        )
        self.skills = ["github", "python-executor", "bailian"]
        self.capabilities = {
            "code_generate": "代码生成",
            "code_review": "代码审查",
            "git_manage": "Git 管理",
            "auto_script": "自动化脚本",
            "tech_doc": "技术文档",
            "debug_help": "调试帮助",
        }
        
        # 百炼客户端（自动路由）
        self.llm_client = BailianClient()
        
        # 代码目录
        self.code_dir = Path("/root/.openclaw/workspace/code")
        self.code_dir.mkdir(parents=True, exist_ok=True)
        
        # 报告缓存（避免重复生成）
        self.report_cache: Dict[str, Dict] = {}
        
        # 任务日志（不生成报告，只记录关键信息）
        self.task_log_path = Path("/root/.openclaw/workspace/logs/tech_tasks.jsonl")
        self.task_log_path.parent.mkdir(parents=True, exist_ok=True)
    
    def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行宫位动作"""
        self._log(f"执行动作：{action}")
        
        action_map = {
            "code_generate": self.code_generate,
            "code_review": self.code_review,
            "git_manage": self.git_manage,
            "auto_script": self.auto_script,
            "tech_doc": self.tech_doc,
            "debug_help": self.debug_help,
            "generate_report": self.generate_report,  # 仅请求时生成报告
        }
        
        if action not in action_map:
            return {"success": False, "error": f"未知动作：{action}"}
        
        try:
            self.update_load(0.3)
            result = action_map[action](**params)
            
            # 记录任务日志（轻量级，不生成报告）
            self._log_task(action, params, result)
            
            self.update_load(0.7)
            return result
        except Exception as e:
            self.update_load(0.2)
            return {"success": False, "error": str(e)}
    
    def code_generate(self, description: str, language: str = "python", 
                      framework: str = None, generate_report: bool = False) -> Dict[str, Any]:
        """
        代码生成
        
        Args:
            description: 代码功能描述
            language: 编程语言
            framework: 框架（可选）
            generate_report: 是否生成报告（默认 False，避免浪费）
        """
        self._log(f"生成代码：{language} - {description[:50]}...")
        
        # 构建提示词
        prompt = self._build_code_prompt(description, language, framework)
        
        # 自动选择模型（代码生成用 qwen-coder）
        context = {"task_type": "code_generation", "language": language}
        result = self.llm_client.generate(prompt, context)
        
        if not result.get("success"):
            return result
        
        # 保存代码
        code_content = result["content"]
        code_file = self._save_code(code_content, language, description)
        
        response = {
            "success": True,
            "message": f"代码已生成：{code_file}",
            "code_file": str(code_file),
            "model": result["model_info"]["selected_model"],
            "cost": result["model_info"]["estimated_cost"],
        }
        
        # 仅当请求时才生成报告
        if generate_report:
            response["report"] = self._generate_code_report(description, code_content, result)
        
        return response
    
    def code_review(self, code: str, review_type: str = "full", 
                    generate_report: bool = False) -> Dict[str, Any]:
        """
        代码审查
        
        Args:
            code: 待审查代码
            review_type: 审查类型（performance/security/style/full）
            generate_report: 是否生成报告（默认 False）
        """
        self._log(f"代码审查：{review_type} - {len(code)} 字符")
        
        # 构建审查提示词
        prompt = self._build_review_prompt(code, review_type)
        
        # 自动选择模型（代码审查用 qwen-max）
        context = {"task_type": "code_review", "review_type": review_type}
        result = self.llm_client.generate(prompt, context)
        
        if not result.get("success"):
            return result
        
        response = {
            "success": True,
            "message": f"审查完成：{review_type}",
            "review": result["content"],
            "model": result["model_info"]["selected_model"],
            "cost": result["model_info"]["estimated_cost"],
        }
        
        # 仅当请求时才生成报告
        if generate_report:
            response["report"] = self._generate_review_report(code, result["content"], result)
        
        return response
    
    def git_manage(self, action: str, repo_path: str, **kwargs) -> Dict[str, Any]:
        """
        Git 管理
        
        Args:
            action: git 动作（status/commit/push/pull/branch）
            repo_path: 仓库路径
        """
        self._log(f"Git 操作：{action} - {repo_path}")
        
        import subprocess
        
        try:
            cmd = ["git", "-C", repo_path, action]
            if "message" in kwargs:
                cmd.extend(["-m", kwargs["message"]])
            if "branch" in kwargs:
                cmd.append(kwargs["branch"])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def auto_script(self, task_description: str, 
                    generate_report: bool = False) -> Dict[str, Any]:
        """
        生成自动化脚本
        
        Args:
            task_description: 任务描述
            generate_report: 是否生成报告（默认 False）
        """
        self._log(f"生成自动化脚本：{task_description[:50]}...")
        
        prompt = f"""请生成一个 Python 自动化脚本来完成以下任务：

任务：{task_description}

要求：
1. 代码完整可运行
2. 包含必要的错误处理
3. 添加注释说明关键步骤
4. 遵循 Python 最佳实践

脚本：
"""
        
        context = {"task_type": "code_generation", "script_type": "automation"}
        result = self.llm_client.generate(prompt, context)
        
        if not result.get("success"):
            return result
        
        # 保存脚本
        script_file = self.code_dir / f"auto_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        script_file.write_text(result["content"], encoding="utf-8")
        
        response = {
            "success": True,
            "message": f"脚本已生成：{script_file}",
            "script_file": str(script_file),
            "model": result["model_info"]["selected_model"],
            "cost": result["model_info"]["estimated_cost"],
        }
        
        # 仅当请求时才生成报告
        if generate_report:
            response["report"] = self._generate_script_report(task_description, result["content"], result)
        
        return response
    
    def tech_doc(self, topic: str, content_type: str = "api", 
                 generate_report: bool = False) -> Dict[str, Any]:
        """
        生成技术文档
        
        Args:
            topic: 文档主题
            content_type: 文档类型（api/tutorial/guide/readme）
            generate_report: 是否生成报告（默认 False）
        """
        self._log(f"生成技术文档：{topic} - {content_type}")
        
        prompt = self._build_doc_prompt(topic, content_type)
        
        # 技术文档用 qwen-plus（平衡性能与成本）
        context = {"task_type": "creative_writing", "doc_type": content_type}
        result = self.llm_client.generate(prompt, context)
        
        if not result.get("success"):
            return result
        
        # 保存文档
        doc_file = self.code_dir / f"doc_{topic.replace(' ', '_')}.md"
        doc_file.write_text(result["content"], encoding="utf-8")
        
        response = {
            "success": True,
            "message": f"文档已生成：{doc_file}",
            "doc_file": str(doc_file),
            "model": result["model_info"]["selected_model"],
            "cost": result["model_info"]["estimated_cost"],
        }
        
        # 仅当请求时才生成报告
        if generate_report:
            response["report"] = self._generate_doc_report(topic, result["content"], result)
        
        return response
    
    def debug_help(self, error_message: str, code_snippet: str = "", 
                   generate_report: bool = False) -> Dict[str, Any]:
        """
        调试帮助
        
        Args:
            error_message: 错误信息
            code_snippet: 相关代码片段
            generate_report: 是否生成报告（默认 False）
        """
        self._log(f"调试帮助：{error_message[:100]}...")
        
        prompt = f"""请帮我分析以下错误并提供解决方案：

错误信息：
{error_message}

相关代码：
{code_snippet if code_snippet else "（无）"}

请提供：
1. 错误原因分析
2. 解决方案
3. 修复后的代码示例（如适用）
"""
        
        # 调试用 qwen-max（复杂推理）
        context = {"task_type": "multi_step", "debug": True}
        result = self.llm_client.generate(prompt, context)
        
        if not result.get("success"):
            return result
        
        response = {
            "success": True,
            "message": "调试分析完成",
            "analysis": result["content"],
            "model": result["model_info"]["selected_model"],
            "cost": result["model_info"]["estimated_cost"],
        }
        
        # 仅当请求时才生成报告
        if generate_report:
            response["report"] = self._generate_debug_report(error_message, result["content"], result)
        
        return response
    
    def generate_report(self, task_type: str, time_range: str = "today") -> Dict[str, Any]:
        """
        生成任务报告（仅当明确请求时）
        
        Args:
            task_type: 任务类型（code_generate/code_review/debug/all）
            time_range: 时间范围（today/week/month）
        """
        self._log(f"生成报告：{task_type} - {time_range}")
        
        # 从日志读取任务记录
        tasks = self._read_task_log(time_range)
        
        # 过滤任务类型
        if task_type != "all":
            tasks = [t for t in tasks if t.get("action") == task_type]
        
        if not tasks:
            return {
                "success": True,
                "message": "没有找到任务记录",
                "report": None,
            }
        
        # 生成汇总报告
        report = self._compile_report(tasks, task_type, time_range)
        
        return {
            "success": True,
            "message": f"报告已生成（{len(tasks)} 个任务）",
            "report": report,
        }
    
    # ========== 辅助方法 ==========
    
    def _build_code_prompt(self, description: str, language: str, framework: str) -> str:
        """构建代码生成提示词"""
        prompt = f"""请生成{language}代码来实现以下功能：

功能描述：
{description}
"""
        if framework:
            prompt += f"\n使用框架：{framework}"
        
        prompt += """

要求：
1. 代码完整可运行
2. 遵循最佳实践
3. 添加必要的注释
4. 包含错误处理

代码：
"""
        return prompt
    
    def _build_review_prompt(self, code: str, review_type: str) -> str:
        """构建代码审查提示词"""
        type_map = {
            "performance": "性能优化建议",
            "security": "安全漏洞检查",
            "style": "代码风格检查",
            "full": "全面审查（性能、安全、风格、可维护性）",
        }
        
        return f"""请对以下代码进行{type_map.get(review_type, '全面审查')}：

```python
{code}
```

请提供：
1. 发现的问题
2. 改进建议
3. 优化后的代码示例（如适用）
"""
    
    def _build_doc_prompt(self, topic: str, content_type: str) -> str:
        """构建文档生成提示词"""
        type_map = {
            "api": "API 参考文档",
            "tutorial": "教程",
            "guide": "使用指南",
            "readme": "README 文档",
        }
        
        return f"""请生成{type_map.get(content_type, '技术文档')}：

主题：{topic}

要求：
1. 结构清晰
2. 内容准确
3. 包含示例代码（如适用）
4. 适合目标读者

文档：
"""
    
    def _save_code(self, code: str, language: str, description: str) -> Path:
        """保存代码文件"""
        ext_map = {
            "python": "py",
            "javascript": "js",
            "typescript": "ts",
            "go": "go",
            "rust": "rs",
        }
        ext = ext_map.get(language.lower(), "txt")
        
        # 生成文件名
        safe_desc = description[:30].replace(" ", "_").replace("/", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"code_{safe_desc}_{timestamp}.{ext}"
        
        code_file = self.code_dir / filename
        code_file.write_text(code, encoding="utf-8")
        
        return code_file
    
    def _log_task(self, action: str, params: Dict, result: Dict):
        """记录任务日志（轻量级）"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "params_summary": {k: str(v)[:100] for k, v in params.items()},
            "success": result.get("success", False),
            "model": result.get("model", "unknown"),
            "cost": result.get("cost", 0),
        }
        
        # 追加到日志文件
        with open(self.task_log_path, "a", encoding="utf-8") as f:
            import json
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    
    def _read_task_log(self, time_range: str) -> List[Dict]:
        """读取任务日志"""
        import json
        
        tasks = []
        now = datetime.now()
        
        with open(self.task_log_path, "r", encoding="utf-8") as f:
            for line in f:
                task = json.loads(line)
                task_time = datetime.fromisoformat(task["timestamp"])
                
                # 过滤时间范围
                if time_range == "today":
                    if task_time.date() == now.date():
                        tasks.append(task)
                elif time_range == "week":
                    if (now - task_time).days <= 7:
                        tasks.append(task)
                elif time_range == "month":
                    if (now - task_time).days <= 30:
                        tasks.append(task)
        
        return tasks
    
    def _compile_report(self, tasks: List[Dict], task_type: str, time_range: str) -> Dict:
        """编译汇总报告"""
        # 统计
        total_tasks = len(tasks)
        success_count = sum(1 for t in tasks if t.get("success"))
        total_cost = sum(t.get("cost", 0) for t in tasks)
        
        # 模型分布
        model_dist = {}
        for t in tasks:
            model = t.get("model", "unknown")
            model_dist[model] = model_dist.get(model, 0) + 1
        
        report = {
            "summary": {
                "time_range": time_range,
                "task_type": task_type,
                "total_tasks": total_tasks,
                "success_rate": f"{success_count/total_tasks*100:.1f}%" if total_tasks > 0 else "0%",
                "total_cost": f"¥{total_cost:.4f}",
            },
            "model_distribution": model_dist,
            "tasks": tasks,
            "generated_at": datetime.now().isoformat(),
        }
        
        return report
    
    # ========== 报告生成方法（按需调用）==========
    
    def _generate_code_report(self, description: str, code: str, llm_result: Dict) -> Dict:
        """生成代码报告"""
        return {
            "type": "code_generation",
            "description": description,
            "model_used": llm_result["model_info"]["selected_model"],
            "cost": llm_result["model_info"]["estimated_cost"],
            "code_length": len(code),
        }
    
    def _generate_review_report(self, code: str, review: str, llm_result: Dict) -> Dict:
        """生成审查报告"""
        return {
            "type": "code_review",
            "code_length": len(code),
            "model_used": llm_result["model_info"]["selected_model"],
            "cost": llm_result["model_info"]["estimated_cost"],
            "review_length": len(review),
        }
    
    def _generate_script_report(self, task: str, script: str, llm_result: Dict) -> Dict:
        """生成脚本报告"""
        return {
            "type": "auto_script",
            "task": task,
            "model_used": llm_result["model_info"]["selected_model"],
            "cost": llm_result["model_info"]["estimated_cost"],
            "script_length": len(script),
        }
    
    def _generate_doc_report(self, topic: str, doc: str, llm_result: Dict) -> Dict:
        """生成文档报告"""
        return {
            "type": "tech_doc",
            "topic": topic,
            "model_used": llm_result["model_info"]["selected_model"],
            "cost": llm_result["model_info"]["estimated_cost"],
            "doc_length": len(doc),
        }
    
    def _generate_debug_report(self, error: str, analysis: str, llm_result: Dict) -> Dict:
        """生成调试报告"""
        return {
            "type": "debug_help",
            "error": error[:200],
            "model_used": llm_result["model_info"]["selected_model"],
            "cost": llm_result["model_info"]["estimated_cost"],
            "analysis_length": len(analysis),
        }
    
    def initialize(self) -> bool:
        """初始化"""
        super().initialize()
        self._log(f"技能：{', '.join(self.skills)}")
        self._log(f"代码目录：{self.code_dir}")
        self._log(f"模型路由：已启用（自动选择最优模型）")
        self._log(f"报告策略：按需生成（generate_report=True）")
        return True


if __name__ == "__main__":
    # 测试
    palace = Palace3Tech()
    palace.initialize()
    
    print("\n=== 测试功能 ===")
    
    # 代码生成（不生成报告）
    result = palace.execute("code_generate", {
        "description": "计算斐波那契数列",
        "language": "python",
        "generate_report": False,  # 默认不生成
    })
    print(f"代码生成：{result['message']}")
    print(f"模型：{result['model']}, 成本：¥{result['cost']:.6f}")
    
    # 代码审查（不生成报告）
    result = palace.execute("code_review", {
        "code": "def add(a,b): return a+b",
        "review_type": "style",
        "generate_report": False,
    })
    print(f"\n代码审查：{result['message']}")
    
    # 生成报告（明确请求时才生成）
    result = palace.execute("generate_report", {
        "task_type": "all",
        "time_range": "today",
    })
    print(f"\n任务报告：{result['message']}")
    
    # 状态
    status = palace.get_status()
    print(f"\n状态：{status}")
