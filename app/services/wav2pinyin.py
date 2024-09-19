import subprocess
import asrt_sdk
import numpy as np
from scipy.io import wavfile
from scipy.signal import resample

# 配置ASRT服务的主机、端口和协议
HOST = '127.0.0.1'
PORT = '20001'
PROTOCOL = 'http'
SUB_PATH = ''

# 获取语音识别实例
speech_recognizer = asrt_sdk.get_speech_recognizer(HOST, PORT, PROTOCOL)
speech_recognizer.sub_path = SUB_PATH


# def convert_audio_format_with_ffmpeg(input_path: str, output_path: str):
#     """
#     使用 ffmpeg 将音频文件转换为指定的格式:
#     单声道、16kHz采样率、PCM编码
#     :param input_path: 输入音频文件路径
#     :param output_path: 输出音频文件路径
#     """
#     command = [
#         'ffmpeg',
#         '-i', input_path,   # 输入文件
#         '-ac', '1',         # 单声道
#         '-ar', '16000',     # 采样率 16kHz
#         '-acodec', 'pcm_s16le',  # PCM 16-bit Signed Integer
#         '-map_metadata', '-1',  # 移除元数据
#         '-fflags', '+bitexact',  # 确保无误差复制
#         output_path  # 输出文件
#     ]
#
#     subprocess.run(command, check=True)


def convert_sample_rate(input_filename, output_filename, target_rate=16000):
    """
    使用 scipy 将音频文件的采样率转换为目标采样率。

    :param input_filename: 输入音频文件路径
    :param output_filename: 输出音频文件路径
    :param target_rate: 目标采样率
    """
    sample_rate, data = wavfile.read(input_filename)
    num_samples = int(data.shape[0] * target_rate / sample_rate)
    resampled_data = resample(data, num_samples)

    # 写入新的WAV文件
    wavfile.write(output_filename, target_rate, resampled_data.astype(np.int16))


def get_pinyin_from_audio(audio_file_path):
    """
    将音频文件转换为拼音序列。

    :param audio_file_path: 音频文件路径
    :return: 拼音序列
    """
    # 转换音频格式并确保符合要求
    converted_filename = "converted.wav"
    # convert_audio_format_with_ffmpeg(audio_file_path, converted_filename)

    # 读取转换后的WAV文件
    wave_data = asrt_sdk.read_wav_datas(converted_filename)

    # 分段处理音频数据
    max_length = 512000  # 最大允许的字节长度
    segments = [wave_data.str_data[i:i + max_length] for i in range(0, len(wave_data.str_data), max_length)]

    # 识别每个分段
    results = []
    for segment in segments:
        result = speech_recognizer.recognite_speech(
            segment,
            wave_data.sample_rate,
            wave_data.channels,
            wave_data.byte_width
        )
        results.append(result)

    # 合并结果并返回拼音序列
    merged_result = [pinyin for result in results for pinyin in result.result]

    # 打印每个分段的结果
    for i, result in enumerate(results):
        print(f"分段 {i + 1} 声学模型识别响应:", result)
        print(f"分段 {i + 1} 声学模型识别结果（拼音序列）:", result.result)

    # 打印合并后的结果
    print("合并后的拼音序列:", merged_result)

    return merged_result
