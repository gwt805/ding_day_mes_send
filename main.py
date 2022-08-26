'''
Author: gwt
Date: 2022-08-26
Describe: 每天定时推送消息

Markdown 字体颜色
<font color="#660000">深红色文字</font>

内容:
    今日天气 : 多云
    当前温度 : 34
    <font color="#660000">洗脑</font>
'''
from dingtalkchatbot.chatbot import DingtalkChatbot
import requests
import time
import urllib
import hmac
import hashlib
import base64
import random
import os
import re


city = os.getenv('CITYS')
webhook_url = os.getenv("WEBHOOK")
qian_key = os.getenv("QIAN")


def random_color():
    color_code = "0123456789ABCDEF"
    color_str = "#"
    for num in range(6):
        color_str += random.choice(color_code)
    return color_str


def get_weather():
    weather_list = []
    for ct in city.split(","):
        url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + ct
        res = requests.get(url).json()
        if res is None:
            return None
        weather = res['data']['list'][0]
        weather_list.append({ct: [weather["weather"], weather["temp"],
                            weather["low"], weather["high"]]})  # 天气，温度， 最低温，最高温
    return weather_list


def get_caihongpi():
    pi = requests.get("https://api.shadiao.pro/chp").json()["data"]["text"]
    duanzi_html = requests.get(
        "http://www.yduanzi.com/?utm_source=https://shadiao.pro").text
    kaishi = re.search("<span id='duanzi-text'>", duanzi_html).span()[1]
    end = re.search("</span>", duanzi_html).span()[0]
    duanzi = duanzi_html[kaishi:end]
    return pi, duanzi


def main():
    pi, duanzi = get_caihongpi()
    webhook_addres = webhook_url
    timestamp = str(round(time.time() * 1000))

    secret = qian_key  # 替换成你的签
    secret_enc = secret.encode("utf-8")
    string_to_sign = "{}\n{}".format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode("utf-8")
    hmac_code = hmac.new(secret_enc, string_to_sign_enc,
                         digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

    webhook = f"{webhook_addres}&timestamp={timestamp}&sign={sign}"
    msg = DingtalkChatbot(webhook)
    tmp = ""
    for t in get_weather():
        for k, v in t.items():
            tmp += f"### {k}\n<font color={random_color()}>天气: {v[0]} &nbsp;&nbsp;&nbsp;&nbsp;温度: {v[1]}&nbsp;&nbsp;&nbsp;&nbsp;最低温: {v[2]}&nbsp;&nbsp;&nbsp;&nbsp;最高温: {v[3]}</font>\n***\n"
    tmp += f"### 今日彩虹屁\n<font color={random_color()}>{pi}</font>\r***\n### 今日段子\n<font color={random_color()}>{duanzi}</font>"
    msg_text = f"***\n"
    msg_text += tmp
    msg.send_markdown(title="钉钉乐温馨提示", text=msg_text, is_at_all=False)


if __name__ == "__main__":
    main()
