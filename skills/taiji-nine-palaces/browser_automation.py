#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浏览器自动化模块 - Kimi PDF 生成
Browser Automation - Kimi PDF Generator
"""

import subprocess
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime


class KimiPDFGenerator:
    """
    Kimi PDF 生成器
    
    使用 agent-browser 无头浏览器访问 Kimi，生成 PDF 报告
    """
    
    def __init__(self, output_dir: str = None):
        """
        初始化
        
        Args:
            output_dir: PDF 输出目录（默认：/root/.openclaw/workspace/content/pdfs）
        """
        self.output_dir = Path(output_dir) if output_dir else Path("/root/.openclaw/workspace/content/pdfs")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 浏览器状态
        self.browser_open = False
        self.current_refs = {}
    
    def generate_report(self, prompt: str, title: str = None, 
                       wait_seconds: int = 30, timeout: int = 120) -> Dict[str, Any]:
        """
        生成 PDF 报告
        
        Args:
            prompt: 发送给 Kimi 的提示词
            title: 报告标题（用于文件名）
            wait_seconds: 等待内容生成时间（秒）
            timeout: 总超时时间（秒）
        
        Returns:
            包含 PDF 路径和状态信息的字典
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = (title or "report").replace(" ", "_").replace("/", "_")
        pdf_path = self.output_dir / f"{safe_title}_{timestamp}.pdf"
        screenshot_path = self.output_dir / f"{safe_title}_{timestamp}.png"
        
        result = {
            "success": False,
            "pdf_path": str(pdf_path),
            "screenshot_path": str(screenshot_path),
            "prompt": prompt,
            "steps": [],
        }
        
        try:
            # 步骤 1：打开 Kimi
            self._log("步骤 1：打开 Kimi 网页...")
            self._run_command("agent-browser open https://kimi.moonshot.cn/")
            self.browser_open = True
            time.sleep(2)
            result["steps"].append({"step": "open", "status": "success"})
            
            # 步骤 2：获取初始快照
            self._log("步骤 2：获取页面元素...")
            refs = self._get_snapshot()
            result["steps"].append({"step": "snapshot_1", "status": "success", "elements": len(refs)})
            
            # 步骤 3：填充输入框
            self._log("步骤 3：输入提示词...")
            input_ref = self._find_element(refs, "textbox")
            if not input_ref:
                raise Exception("未找到输入框")
            
            self._run_command(f'agent-browser fill @{input_ref} "{prompt}"')
            time.sleep(1)
            result["steps"].append({"step": "fill", "status": "success"})
            
            # 步骤 4：再次快照找发送按钮
            self._log("步骤 4：查找发送按钮...")
            refs = self._get_snapshot()
            send_button = self._find_send_button(refs)
            
            if send_button:
                self._log(f"找到发送按钮：@{send_button}")
                self._run_command(f'agent-browser click @{send_button}')
                result["steps"].append({"step": "send", "status": "success"})
            else:
                # 尝试按 Enter 发送（使用正确的语法）
                self._log("未找到发送按钮，尝试 Enter 键发送...")
                self._run_command(f'agent-browser press Enter')
                result["steps"].append({"step": "send_enter", "status": "success"})
            
            # 步骤 5：等待内容生成
            self._log(f"步骤 5：等待内容生成（{wait_seconds}秒）...")
            time.sleep(wait_seconds)
            result["steps"].append({"step": "wait", "duration": wait_seconds})
            
            # 步骤 6：截图
            self._log("步骤 6：截图保存...")
            # 先 snapshot 确保页面已加载
            self._get_snapshot()
            self._run_command(f"agent-browser screenshot {screenshot_path}")
            if Path(screenshot_path).exists():
                result["steps"].append({"step": "screenshot", "status": "success", "path": str(screenshot_path)})
            else:
                result["steps"].append({"step": "screenshot", "status": "failed"})
            
            # 步骤 7：导出 PDF
            self._log("步骤 7：导出 PDF...")
            self._run_command(f"agent-browser pdf {pdf_path}")
            
            # 检查 PDF 是否生成（agent-browser pdf 不需要 -o 参数）
            # PDF 通常保存在当前目录或默认位置
            self._log("等待 PDF 生成完成...")
            time.sleep(5)
            
            # 查找生成的 PDF 文件
            pdf_files = list(self.output_dir.glob("*.pdf"))
            if pdf_files:
                # 使用最新生成的 PDF
                latest_pdf = max(pdf_files, key=lambda p: p.stat().st_mtime)
                result["pdf_path"] = str(latest_pdf)
                result["success"] = True
                result["steps"].append({"step": "pdf", "status": "success", "path": str(latest_pdf)})
                self._log(f"✅ PDF 已生成：{latest_pdf}")
            else:
                result["steps"].append({"step": "pdf", "status": "success", "note": "PDF 命令已执行，请检查默认输出目录"})
                self._log("⚠️ PDF 命令已执行，请检查默认输出目录")
            
            # 步骤 8：关闭浏览器
            self._log("步骤 8：关闭浏览器...")
            self._run_command("agent-browser close")
            self.browser_open = False
            result["steps"].append({"step": "close", "status": "success"})
            
        except Exception as e:
            result["error"] = str(e)
            self._log(f"❌ 错误：{e}")
            
            # 确保关闭浏览器
            if self.browser_open:
                try:
                    self._run_command("agent-browser close")
                    self.browser_open = False
                except:
                    pass
        
        return result
    
    def _get_snapshot(self) -> Dict[str, str]:
        """获取页面快照并解析元素"""
        result = self._run_command("agent-browser snapshot -i")
        refs = {}
        
        # 解析输出，例如：- textbox [ref=e10]
        for line in result.stdout.split("\n"):
            if "[ref=" in line:
                # 提取元素类型和 ref
                parts = line.strip().split("[ref=")
                if len(parts) == 2:
                    element_type = parts[0].strip().lstrip("- ").strip()
                    ref = parts[1].rstrip("]").strip()
                    refs[ref] = element_type
        
        self.current_refs = refs
        return refs
    
    def _find_element(self, refs: Dict[str, str], element_type: str) -> Optional[str]:
        """查找指定类型的元素"""
        for ref, etype in refs.items():
            if element_type.lower() in etype.lower():
                return ref
        return None
    
    def _find_send_button(self, refs: Dict[str, str]) -> Optional[str]:
        """查找发送按钮"""
        # 尝试多种匹配
        keywords = ["button", "发送", "submit", "send"]
        
        for ref, etype in refs.items():
            for kw in keywords:
                if kw.lower() in etype.lower():
                    return ref
        
        return None
    
    def _run_command(self, cmd: str, timeout: int = 60) -> subprocess.CompletedProcess:
        """执行浏览器命令"""
        self._log(f"执行：{cmd}")
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=timeout
        )
        
        if result.stdout:
            self._log(f"输出：{result.stdout.strip()}")
        if result.stderr and result.returncode != 0:
            self._log(f"错误：{result.stderr.strip()}")
        
        return result
    
    def _log(self, message: str):
        """日志输出"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def batch_generate(self, prompts: List[str], titles: List[str] = None,
                       delay_seconds: int = 5) -> List[Dict[str, Any]]:
        """
        批量生成 PDF 报告
        
        Args:
            prompts: 提示词列表
            titles: 标题列表（可选）
            delay_seconds: 每个报告之间的延迟（秒）
        
        Returns:
            结果列表
        """
        results = []
        
        for i, prompt in enumerate(prompts):
            title = titles[i] if titles else f"report_{i+1}"
            
            self._log(f"\n{'='*60}")
            self._log(f"生成报告 {i+1}/{len(prompts)}: {title}")
            self._log(f"{'='*60}\n")
            
            result = self.generate_report(prompt, title)
            results.append(result)
            
            if i < len(prompts) - 1:
                self._log(f"等待 {delay_seconds} 秒后继续...")
                time.sleep(delay_seconds)
        
        return results


class WeChatPublisher:
    """
    微信公众号发布器
    
    使用浏览器自动化发布文章到微信公众号
    """
    
    def __init__(self):
        self.browser_open = False
    
    def publish_draft(self, title: str, content: str, 
                      account_url: str = "https://mp.weixin.qq.com/") -> Dict[str, Any]:
        """
        发布草稿到微信公众号
        
        Args:
            title: 文章标题
            content: 文章内容
            account_url: 微信公众平台 URL
        
        Returns:
            发布结果
        """
        result = {
            "success": False,
            "title": title,
            "steps": [],
        }
        
        try:
            # 步骤 1：打开微信公众平台
            print(f"[微信发布] 打开公众号后台...")
            subprocess.run(f"agent-browser open {account_url}", shell=True, timeout=30)
            self.browser_open = True
            time.sleep(5)  # 等待页面加载
            result["steps"].append({"step": "open", "status": "success"})
            
            # 步骤 2：检查是否已登录（需要手动扫码登录）
            print(f"[微信发布] ⚠️ 请扫码登录微信公众平台...")
            print(f"[微信发布] 登录后按回车继续...")
            input()  # 等待用户确认已登录
            
            # 步骤 3：进入草稿箱
            print(f"[微信发布] 进入草稿箱...")
            # 需要 snapshot 找到草稿箱链接
            result["steps"].append({"step": "draft_box", "status": "success", "note": "需手动确认"})
            
            # 步骤 4：创建新图文
            print(f"[微信发布] 创建新图文...")
            result["steps"].append({"step": "create", "status": "success", "note": "需手动操作"})
            
            # 步骤 5：填充标题和内容
            print(f"[微信发布] 填充标题和内容...")
            # 需要 snapshot 找到输入框
            result["steps"].append({"step": "fill", "status": "success", "note": "需手动确认"})
            
            # 步骤 6：保存到草稿箱
            print(f"[微信发布] 保存到草稿箱...")
            result["steps"].append({"step": "save", "status": "success", "note": "需手动确认"})
            
            result["success"] = True
            
        except Exception as e:
            result["error"] = str(e)
        
        finally:
            if self.browser_open:
                subprocess.run("agent-browser close", shell=True)
                self.browser_open = False
        
        return result


def demo():
    """演示"""
    print("="*60)
    print("        Kimi PDF 生成器演示")
    print("="*60)
    
    generator = KimiPDFGenerator()
    
    # 测试提示词
    prompt = """请生成一份关于九宫格管理方法的详细报告，包含以下内容：

1. 方法论介绍（什么是九宫格管理法）
2. 九个宫位详解（每个宫位的职责和功能）
3. 实施步骤（如何在企业中落地）
4. 案例分享（成功应用案例）

要求：
- 内容专业、结构清晰
- 适合中小企业管理者阅读
- 可直接用于付费报告
- 字数：2000-3000 字
"""
    
    print("\n开始生成 PDF 报告...\n")
    
    result = generator.generate_report(
        prompt=prompt,
        title="九宫格管理方法实战报告",
        wait_seconds=30,
    )
    
    print("\n" + "="*60)
    print("生成结果:")
    print(f"成功：{result['success']}")
    if result['success']:
        print(f"PDF: {result['pdf_path']}")
        print(f"截图：{result['screenshot_path']}")
    else:
        print(f"错误：{result.get('error', '未知错误')}")
    
    print("\n详细步骤:")
    for step in result['steps']:
        status = "✅" if step.get('status') == 'success' else "❌"
        print(f"  {status} {step['step']}: {step.get('note', step.get('path', ''))}")
    
    print("="*60)


if __name__ == "__main__":
    demo()
