import os
from werkzeug.utils import secure_filename

from app.services.stt import execute_one
from app.services.wav2pinyin import get_pinyin_from_audio
from app.services.ai_service import get_correction_suggestions
from app.services.tts import generate_tts_audio
from app.services.convert_audio import convert_audio

UPLOAD_FOLDER = 'uploads'

def process_audio(audio_file):
    try:
        # 确保 uploads 目录存在
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # 保存音频文件到本地
        filename = secure_filename(audio_file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        audio_file.save(file_path)
        print(f"Audio saved to {file_path}")

        # 将音频转换为 wav 格式
        # file_path = convert_audio(file_path,file_path)
        # print(F"音频格式转换完成，保存路径：{file_path}")

        # 调用语音转文字服务
        text = execute_one(file_path)
        print(F"语音转文字：{text}")
        # 转换为拼音
        pinyin = get_pinyin_from_audio(file_path)
        print(F"拼音：{pinyin}")
        # 获取修正建议
        suggestions = get_correction_suggestions(pinyin, text)

        # 转换修正建议为语音
        speech_url = generate_tts_audio(suggestions)

        return {
            'text': text,
            'pinyin': pinyin,
            'suggestions': suggestions,
            'speech_url': speech_url
        }
    except Exception as e:
        # 处理异常情况
        return {
            'error': str(e)
        }