import requests
from zhipuai import ZhipuAI
def get_correction_suggestions(pinyin, text):
    client = ZhipuAI(api_key="44f339ae59d2d206884a8eed3a4700cc.t967Qq0sLwVnaWOc")  # 请填写您自己的API Key
    response = client.chat.completions.create(
        model="glm-4-flash",  # 填写需要调用的模型编码
        messages=[
            {"role": "system", "content": """
            你是一个帮助我练习普通话的助手，你的任务是为依据机器识别的我的发音与语音识别得到的我说的话，给出我可能存在的发音问题，及如何修正的建议。你将得到如“['kai1', 'shi3', 'lu4', 'yin1']”的汉语拼音，其中每个拼音后面的数字代表4个声调。请注意无论是汉语拼音都是由机器识别而来，准确率不是很高。所以你不但要根据给出的信息，还需要知道容易出错词汇。
你给出的建议应该是有用的，可以是纠正出错的读音，给出这个读音的发音方式等等。但是请不要提及机器识别得到的汉语拼音。
当你要输出读音时，请输出正确格式的读音。如：“kāi shǐ lù yīn”
示例答案：“牛奶”的读音是“niú nǎi”，您要注意“牛”字的发音，读“niú”，发音时注意双唇拢圆，向前突出，舌尖抵住下齿背。“奶”字读“nǎi”，发音时先发“n”的音，然后舌尖抵住上齿龈，软腭下降，打开鼻腔通路，气流振动声带，从鼻腔通过发出“ǎi”的音。
            """
             },
            {"role": "user", "content": f"拼音序列：{pinyin}\n我想说的话：{text}"
            },
        ],
        stream=False,
    )
    # print(response)
    sugestion = response.choices[0].message.content
    # for chunk in response:
    #     print(chunk.choices[0].delta)
    return sugestion