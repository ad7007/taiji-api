# 第2-5节课脚本合集

---

## 第2节课：环境搭建

**时长**: 15-20分钟

### 内容
1. Python环境配置
2. 太极系统安装
3. Hello World演示
4. 常见问题

```bash
# 安装命令
git clone https://gitee.com/miroeta/taiji-api.git
pip install -r requirements.txt
```

```python
# Hello World
from milo import Milo
milo = Milo()
print(milo.status())
```

---

## 第3节课：九宫协作原理

**时长**: 15-20分钟

### 内容
1. 1+8架构详解
2. 宫位职责分工
3. 自动组队机制
4. 实战演示

### 宫位表
| 宫位 | 职责 |
|------|------|
| 1宫 | 数据采集 |
| 3宫 | 技术开发 |
| 4宫 | 品牌战略 |
| 6宫 | 质量监控 |
| 7宫 | TDD验收 |
| 8宫 | 营销客服 |

---

## 第4节课：数据采集实战

**时长**: 15-20分钟

### 内容
1. 视频下载
2. 文件下载
3. 网页抓取
4. API采集

```python
from palace_1 import download_video, download_file, scrape_web

# 下载视频
result = download_video("https://v.douyin.com/xxx")

# 下载文件
result = download_file("https://example.com/data.json")

# 抓取网页
result = scrape_web("https://example.com")
```

---

## 第5节课：技术开发实战

**时长**: 15-20分钟

### 内容
1. 技能安装
2. 代码执行
3. 脚本自动化
4. 依赖管理

```python
from palace_3 import install_skill, execute

# 安装技能
result = install_skill("some-skill")

# 执行命令
result = execute("python3 script.py")
```

---

**第2-5节课脚本完成！**