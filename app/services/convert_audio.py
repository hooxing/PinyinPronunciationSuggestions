import ffmpeg
def convert_audio(input_path, output_path):
    """
    使用 ffmpeg 将音频转换为指定格式
    - 单声道 (Mono)
    - 16kHz 采样率
    - PCM 编码 (16-bit Signed Integer)
    - 移除额外的元数据
    """
    try:
        (
            ffmpeg
            .input(input_path)
            .output(output_path,
                    ac=1,        # 单声道
                    ar=16000,    # 16kHz 采样率
                    acodec='pcm_s16le',  # PCM 编码
                    map_metadata=-1,     # 移除元数据
                    fflags='+bitexact')  # 精确处理音频
            .run(overwrite_output=True)
        )
        print(f"音频已成功转换并保存到 {output_path}")
    except ffmpeg.Error as e:
        print(f"ffmpeg 错误: {e.stderr}")
        raise Exception(f"音频转换失败: {e.stderr}")