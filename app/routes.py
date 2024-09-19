import requests
from flask import Blueprint, request, jsonify
from app.services.audio_processing import process_audio
import subprocess

api = Blueprint('api', __name__)

UPLOAD_FOLDER = 'uploads'  # 定义上传文件夹


@api.route('/upload-audio', methods=['POST'])
def upload_audio():
    audio_file = request.files['audio']
    print("Received audio file:", audio_file)
    result = process_audio(audio_file)
    return jsonify(result)


@api.route('/getJson', methods=['POST'])
def getJson():
    # 定义接口 URL
    url = 'http://127.0.0.1:5000/upload-audio'

    audio_file = request.files['audio']

    audio_file.save('upload.wav')

    def convert_to_asrt_standard(input_file, output_file):
        """
        将上传的wav文件转换为ASRT标准格式文件。

        :param input_file: 输入音频文件路径
        :param output_file: 输出音频文件路径
        """
        try:
            # 使用ffmpeg进行转换
            command = [
                'E:\\soft\\ffmpeg-2024-09-12-git-504c1ffcd8-essentials_build\\bin\\ffmpeg.exe',  # 使用绝对路径
                '-i', input_file,
                '-map_metadata', '-1',
                '-fflags', '+bitexact',
                '-acodec', 'pcm_s16le',
                '-ac', '1',
                '-ar', '16000',
                '-y',
                output_file
            ]
            subprocess.run(command, check=True)
            print(f"音频文件已转换为ASRT标准格式，保存路径：{output_file}")
        except subprocess.CalledProcessError as e:
            print(f"转换音频文件时出错: {e}")

    # 转换上传的音频文件
    converted_file_path = 'converted.wav'
    convert_to_asrt_standard('upload.wav', converted_file_path)

    # 定义音频文件路径
    audio_file_path = converted_file_path

    # 创建一个包含音频文件的 FormData
    files = {'audio': open(audio_file_path, 'rb')}

    # 发送 POST 请求
    response = requests.post(url, files=files)
    print(response.json())
    return response.json()