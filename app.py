from flask import Flask
import openai
import xml.etree.ElementTree as ET

app = Flask(__name__)

# 这里需要替换为您自己的API Key
openai.api_key = "YOUR_API_KEY_HERE"


# 处理微信公众号的消息
@app.route('/', methods=['POST'])
def wechat():
    # 获取微信公众号的请求内容
    data = request.data.decode('utf-8')
    root = ET.fromstring(data)

    # 解析微信公众号的请求
    from_user = root.find('FromUserName').text
    to_user = root.find('ToUserName').text
    content = root.find('Content').text

    # 调用OpenAI的API来生成回复
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=content,
        max_tokens=60
    )

    # 构造回复消息
    reply = response.choices[0].text.strip()
    reply_xml = f"""
    <xml>
    <ToUserName><![CDATA[{from_user}]]></ToUserName>
    <FromUserName><![CDATA[{to_user}]]></FromUserName>
    <CreateTime>{int(time.time())}</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[{reply}]]></Content>
    </xml>
    """
    return reply_xml

if __name__ == '__main__':
    app.run()
