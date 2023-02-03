'''
Author: gwt
Date: 2022-08-26
Describe: 每天定时推送消息

Markdown 字体颜色
<font color="#660000">深红色文字</font>

'''
from dingtalkchatbot.chatbot import DingtalkChatbot
from datetime import datetime, timedelta
import time
import urllib
import hmac
import hashlib
import base64
import random
import sys

nowtime = datetime.utcnow() + timedelta(hours=8)  # 东八区时间
today = str(nowtime.year) + "-" +str(nowtime.month) + "-" + str(nowtime.day) +" " + str(nowtime.hour) + ":" + str(nowtime.minute) + ":" + str(nowtime.second)  # 今天的日期


def random_color():
    color_code = "0123456789ABCDEF"
    color_str = "#"
    for num in range(6):
        color_str += random.choice(color_code)
    return color_str


def get_week_day():
    week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    week_day = week_list[datetime.date(datetime.strptime(today, "%Y-%m-%d %H:%M:%S")).weekday()]
    return week_day

def main():
    webhook_addres = sys.argv[1]
    timestamp = str(round(time.time() * 1000))

    secret = sys.argv[2]  # 替换成你的签
    secret_enc = secret.encode("utf-8")
    string_to_sign = "{}\n{}".format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode("utf-8")
    hmac_code = hmac.new(secret_enc, string_to_sign_enc,
                         digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

    webhook = f"{webhook_addres}&timestamp={timestamp}&sign={sign}"
    msg = DingtalkChatbot(webhook)

    msg_text = f"### 现在是&nbsp;&nbsp;<font color={random_color()}>{today}</font>&nbsp;&nbsp;<font color={random_color()}>{get_week_day()}</font>\n***\n"
    msg_text += f"<font color={random_color()}>规则文档有版本更新时,请及时同步到标注规范汇总表</font>\n<font color={random_color()}>文档链接在群公告</font>"
    res = msg.send_markdown(title="钉钉乐温馨提示", text=msg_text, is_at_all=False)
    print(res)

if __name__ == "__main__":
    main()
