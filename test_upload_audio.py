import requests

# 定义接口 URL
url = 'http://127.0.0.1:5000/upload-audio'

# 定义音频文件路径
audio_file_path = 'recorded.wav'

# 创建一个包含音频文件的 FormData
files = {'audio': open(audio_file_path, 'rb')}

# 发送 POST 请求
response = requests.post(url, files=files)

# 打印响应
print(response.status_code)
print(response.json())