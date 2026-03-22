#!/bin/bash
# web-file-downloader 下载文件处理脚本
# 处理Chrome临时下载文件并规范落盘

set -e

# 配置参数（可通过环境变量传入）
BASE_DIR="${OUTPUT_DIR:-~/Downloads}"
TASK_NAME="${TASK_NAME:-download}"
FILE_NAME="${FILE_NAME:-downloaded_file}"
WAIT_SECONDS="${WAIT_SECONDS:-2}"

# 清洗任务名，避免路径非法字符
safe_name=$(echo "$TASK_NAME" | tr '/:' '_' | tr -s ' ' '_' | sed 's/[^[:alnum:]_.-]/_/g')

# 当前时间（Asia/Shanghai）
now=$(TZ=Asia/Shanghai date +%Y%m%d_%H%M%S)
out_dir=$(eval echo "$BASE_DIR")/${safe_name}_${now}

# 创建输出目录
mkdir -p "$out_dir"
echo "输出目录: $out_dir"

# 等待下载完成
echo "等待下载完成 (${WAIT_SECONDS}s)..."
sleep "$WAIT_SECONDS"

# 取最新Chrome临时下载文件
temp_file=$(ls -t ~/Downloads/.com.google.Chrome.* 2>/dev/null | head -1)

# 安全检查
if [ -z "$temp_file" ]; then
    echo "错误：未发现Chrome临时下载文件"
    echo "请确认:"
    echo "  1. Chrome浏览器已正确配置"
    echo "  2. 下载确实已触发"
    echo "  3. 下载目录为默认的 ~/Downloads"
    exit 1
fi

# 验证临时文件存在且可读
if [ ! -f "$temp_file" ]; then
    echo "错误：临时文件不存在或不可读: $temp_file"
    exit 1
fi

echo "找到临时文件: $temp_file"

# 移动并重命名
mv "$temp_file" "$out_dir/$FILE_NAME"

# 验证结果
if [ -f "$out_dir/$FILE_NAME" ]; then
    echo "✓ 下载成功: $out_dir/$FILE_NAME"
    echo "文件大小: $(ls -lh "$out_dir/$FILE_NAME" | awk '{print $5}')"
else
    echo "错误：文件移动失败"
    exit 1
fi
