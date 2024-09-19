#coding=utf-8

'''
requires Python 3.6 or later
pip install requests
'''
import base64
import json
import uuid
import requests

# 填写平台申请的appid, access_token以及cluster
# appid = "xxxx"
# access_token = "xxxx"
# cluster = "xxxx"

appid = "5783655432"    # 项目的 appid
access_token = "9ds8F7N7Qjal5PoxarEp8ctl32M3lvsN"    # 项目的 token
cluster = "volcano_tts"  # 请求的集群

voice_type = "BV700_V2_streaming"
host = "openspeech.bytedance.com"
api_url = f"https://{host}/api/v1/tts"

header = {"Authorization": f"Bearer;{access_token}"}

def generate_tts_audio(text, output_file="output.mp3"):
    """
    生成TTS音频文件
    :param text: 需要合成的文本
    :param output_file: 生成的音频文件路径
    :return: 生成的音频文件路径
    """
    request_json = {
        "app": {
            "appid": appid,
            "token": "access_token",
            "cluster": cluster
        },
        "user": {
            "uid": "388808087185088"
        },
        "audio": {
            "voice_type": voice_type,
            "encoding": "mp3",
            "speed_ratio": 1.0,
            "volume_ratio": 1.0,
            "pitch_ratio": 1.0,
        },
        "request": {
            "reqid": str(uuid.uuid4()),
            "text": text,
            "text_type": "plain",
            "operation": "query",
            "with_frontend": 1,
            "frontend_type": "unitTson"
        }
    }

    try:
        resp = requests.post(api_url, json.dumps(request_json), headers=header)
        resp_json = resp.json()
        print(f"resp body: \n{resp_json}")

        if "data" in resp_json:
            data = resp_json["data"]
            with open(output_file, "wb") as file_to_save:
                file_to_save.write(base64.b64decode(data))
            return output_file
        else:
            print("Error: No audio data received.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_tts():
    text = "字节跳动语音合成"
    output_file = "test_submit.mp3"
    result = generate_tts_audio(text, output_file)
    if result:
        print(f"Audio file saved to: {result}")
    else:
        print("Failed to generate audio file.")

if __name__ == '__main__':
    test_tts()