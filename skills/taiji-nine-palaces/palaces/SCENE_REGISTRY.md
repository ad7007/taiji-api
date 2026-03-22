# 太极九宫 Scene 注册表

---
version: 2.0.0
updated: 2026-03-19
---

- Scene 总览

所有宫位声明的场景，用于自动组队匹配。

***

- 场景注册表

-- 1宫 - 数据采集（内置 Agent Browser）

```yaml
scene:download:
  palace: 1
  description: 文件下载
  keywords: ["下载", "download"]
  flow: [1, 7, 5]
  tools: [agent-browser, yt-dlp, wget]
    
scene:scrape:
  palace: 1
  description: 网页抓取
  keywords: ["抓取", "爬取", "scrape"]
  flow: [1, 3, 7, 5]
  tools: [agent-browser, playwright]
    
scene:transcribe:
  palace: 1
  description: 视频/音频转录
  keywords: ["转录", "视频总结", "音频转文字"]
  flow: [1, 3, 7, 5]
  tools: [agent-browser, yt-dlp, whisper]

scene:browser:
  palace: 1
  description: 浏览器自动化
  keywords: ["打开网页", "点击", "填写", "登录", "截图"]
  flow: [1, 7, 5]
  tools: [agent-browser]
```

-- 2宫 - 产品质量

```yaml
scene:quality_check:
  palace: 2
  description: 质量检查
  keywords: ["质量", "检查", "质检"]
  flow: [1, 2, 7, 5]
```

-- 3宫 - 技术团队

```yaml
scene:code:
  palace: 3
  description: 代码开发
  keywords: ["代码", "开发", "写代码"]
  flow: [3, 7, 5]
    
scene:debug:
  palace: 3
  description: 问题调试
  keywords: ["调试", "debug", "修bug"]
  flow: [3, 7, 5]
```

-- 4宫 - 品牌战略

```yaml
scene:competitive:
  palace: 4
  description: 竞品分析
  keywords: ["竞品", "竞争分析"]
  flow: [1, 4, 7, 5]
  tools: [agent-browser]
```

-- 9宫 - 行业生态

```yaml
scene:research:
  palace: 9
  description: 行业研究
  keywords: ["行业", "研究"]
  flow: [1, 9, 7, 5]
  tools: [agent-browser]
```

***

- 自动组队算法

```python
def auto_group(user_message: str) -> tuple[str, list[int]]:
    """根据用户消息自动匹配场景和组队"""
    
    for scene_id, scene_data in SCENES.items():
        keywords = scene_data["keywords"]
        
        for keyword in keywords:
            if keyword in user_message:
                return scene_id, scene_data["flow"]
    
    return "scene:dispatch", [5]
```

***

- 使用示例

```python
# "帮我下载这个视频"
scene, flow = auto_group("帮我下载这个视频")
# → scene:transcribe, [1, 3, 7, 5]

# "打开这个网页并截图"
scene, flow = auto_group("打开网页截图")
# → scene:browser, [1, 7, 5]

# "分析竞品定价"
scene, flow = auto_group("分析竞品定价")
# → scene:competitive, [1, 4, 7, 5]
```