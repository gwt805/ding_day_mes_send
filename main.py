'''
Author: gwt
Date: 2022-08-26
Describe: 每天定时推送消息

Markdown 字体颜色
<font color="#660000">深红色文字</font>

内容:
    现在是 xxxx-xx-xx 星期x
    今日天气 : 多云
    当前温度 : xx℃
    最低温   : xx℃
    最高温   : xx℃
    今日彩虹屁 : xxxxx
    今日段子 : xxxx
    <font color="#660000">xxxx</font>
'''
from dingtalkchatbot.chatbot import DingtalkChatbot
from datetime import datetime, timedelta
import requests
import time
import urllib
import hmac
import hashlib
import base64
import random
import os
import re


city = os.getenv('CITYS') # 最少写2个城市
webhook_url = os.getenv("WEBHOOK")
qian_key = os.getenv("QIAN")
anno = os.getenv("ANNOS") # 非人人适用，可注释掉

nowtime = datetime.utcnow() + timedelta(hours=8)  # 东八区时间
today = str(nowtime.year) + "-" +str(nowtime.month) + "-" + str(nowtime.day) +" " + str(nowtime.hour) + ":" + str(nowtime.minute) + ":" + str(nowtime.second)  # 今天的日期


def random_color():
    color_code = "0123456789ABCDEF"
    color_str = "#"
    for num in range(6):
        color_str += random.choice(color_code)
    return color_str


def get_weather():
    weather_list = []
    for ct in city.split(","):
        url = f"https://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city={ct}&needMoreData=true&pageNo=1&pageSize=1"
        res = requests.get(url).json()
        if res is None:
            return None
        weather = res["data"]["list"][0]
        weather_list.append({ct: [weather["weather"], weather["temp"],
                            weather["low"], weather["high"]]})  # 天气，温度， 最低温，最高温
    return weather_list


def get_week_day():
    week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    week_day = week_list[datetime.date(datetime.strptime(today, "%Y-%m-%d %H:%M:%S")).weekday()]
    return week_day


def get_caihongpi():
    pi = requests.get("https://api.shadiao.pro/chp").json()["data"]["text"]
    duanzi_html = requests.get(
        "http://www.yduanzi.com/?utm_source=https://shadiao.pro").text
    kaishi = re.search("<span id='duanzi-text'>", duanzi_html).span()[1]
    end = re.search("</span>", duanzi_html).span()[0]
    duanzi = duanzi_html[kaishi:end]
    return pi, duanzi

"""
为 "None"时 不用'，'
非 "None"时, 只有1条或2条数据时最后需要加上 '，'
eg1: 123，
eg2: 123，456，
eg3: 123,456,789
"""
def get_annos():  # 非人人适用，可注释掉
    if anno != "None":
        tmp = ""
        anno_split = anno.split("，")
        if len(anno_split) != 2:
            for idx in anno_split:
                tmp += f"\n<font color={random_color()}>{idx}</font>\n"
        else:
            tmp += f"\n<font color={random_color()}>{anno_split[0]}</font>\n"
        return tmp
    else:
        return f"\n<font color={random_color()}>Author休假中,上班后同步...</font>"

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
            tmp += f"### {k}\n<font color={random_color()}>天气: {v[0]}&nbsp;&nbsp;&nbsp;当前温度: {v[1]}℃&nbsp;&nbsp;&nbsp;最低温: {v[2]}℃&nbsp;&nbsp;&nbsp;最高温: {v[3]}℃</font>\n***\n"
    tmp += f"### 今日彩虹屁\n<font color={random_color()}>{pi}</font>\n***\n### 今日段子\n<font color={random_color()}>{duanzi}</font>\n***\n### 验收情况\n"
    msg_text = f"### 现在是&nbsp;&nbsp;<font color={random_color()}>{today}</font>&nbsp;&nbsp;<font color={random_color()}>{get_week_day()}</font>\n***\n"
    msg_text += tmp + get_annos() # get_annos() 非人人适用，可注释掉
    msg.send_markdown(title="钉钉乐温馨提示", text=msg_text, is_at_all=False)


if __name__ == "__main__":
    main()
