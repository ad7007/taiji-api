#!/bin/bash
# 免费内容生成工作流

# 1. 配音生成
generate_audio() {
    local text="$1"
    local output="$2"
    edge-tts --voice zh-CN-XiaoxiaoNeural --text "$text" --write-media "$output"
}

# 2. 转录
transcribe() {
    local audio="$1"
    local output_dir="$2"
    whisper "$audio" --model tiny --language zh --output_dir "$output_dir" --output_format txt
}

# 3. 视频合成(FFmpeg)
synthesize_video() {
    local audio="$1"
    local image="$2"
    local output="$3"
    ffmpeg -loop 1 -i "$image" -i "$audio" -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest "$output"
}

echo "免费内容生成工作流已就绪"
echo "1. generate_audio '文本' 输出.mp3"
echo "2. transcribe 音频.mp3 输出目录"
echo "3. synthesize_video 音频.mp3 图片.png 输出.mp4"
