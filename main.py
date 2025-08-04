import streamlit as st
from pydub import AudioSegment, utils
import io
import tempfile
import os
from pydub.utils import which

st.set_page_config(page_title="🎵 TuneCutter - 音频片段裁剪器")
st.title("🎵 TuneCutter - 音频片段裁剪器")

ffmpeg_path = which("ffmpeg")
manual_ffmpeg = False

if ffmpeg_path:
    st.success(f"✅ 检测到系统 ffmpeg: `{ffmpeg_path}`")
else:
    st.warning("⚠️ 未检测到系统 ffmpeg，请手动选择 ffmpeg.exe 所在路径")
    manual_ffmpeg = True
    ffmpeg_path_input = st.text_input("📁 请输入 ffmpeg.exe 完整路径，例如：`E:\\ffmpeg\\bin\\ffmpeg.exe`")

    if os.path.isfile(ffmpeg_path_input) and ffmpeg_path_input.lower().endswith("ffmpeg.exe"):
        ffmpeg_path = ffmpeg_path_input
        st.success("✅ 已手动设置 ffmpeg 路径")
    else:
        st.stop()

AudioSegment.converter = ffmpeg_path
utils.get_encoder_name = lambda: ffmpeg_path

uploaded_file = st.file_uploader("📤 上传一首音频文件（mp3 或 wav）", type=["mp3", "wav"])

def to_ms(time_str):
    try:
        if ':' in time_str:
            minutes, seconds = map(int, time_str.split(':'))
            return (minutes * 60 + seconds) * 1000
        return int(float(time_str) * 1000)
    except:
        return -1

if uploaded_file:
    audio_bytes = uploaded_file.read()
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes))

    st.audio(audio_bytes, format="audio/mp3")

    start_time = st.text_input("起始时间 (秒或 mm:ss)", "0:30")
    end_time = st.text_input("结束时间 (秒或 mm:ss)", "0:50")

    start_ms = to_ms(start_time)
    end_ms = to_ms(end_time)

    if st.button("🎧 裁剪并播放片段"):
        if 0 <= start_ms < end_ms <= len(audio):
            clip = audio[start_ms:end_ms]
            clip_bytes = io.BytesIO()
            clip.export(clip_bytes, format="mp3")
            clip_bytes.seek(0)
            st.audio(clip_bytes.getvalue(), format="audio/mp3")
        else:
            st.error("时间范围不合法或格式错误")

    if st.button("💾 导出裁剪片段"):
        if 0 <= start_ms < end_ms <= len(audio):
            clip = audio[start_ms:end_ms]
            clip_bytes = io.BytesIO()
            clip.export(clip_bytes, format="mp3")
            clip_bytes.seek(0)
            st.success("已裁剪完成")
            st.download_button(
                label="点击下载片段",
                data=clip_bytes,
                file_name="clip.mp3",
                mime="audio/mp3"
            )
        else:
            st.error("时间范围不合法或格式错误")
