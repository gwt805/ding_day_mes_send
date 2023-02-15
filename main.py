import sys
import requests
from loguru import logger

'''
Author: gwt
摸鱼人日历: vvhan
argv[1]: ann_team
argb[2]: algorithm
'''

def ann_team_tip_mes():
    res = requests.post(
        f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={sys.argv[1]}",
        json={
            "msgtype": "news",
            "news": {
                "articles": [
                    {
                        "title": "钉钉乐 温馨提示",
                        "description": "每批次开始验收时, 及时填写开始验收时间\r每批次结束验收时, 及时填写结束验收时间",
                        "url": "https://api.vvhan.com/api/moyu",
                        "picurl": "https://api.vvhan.com/api/moyu"
                    }
                ]
            }
        }
    )
    logger.info(f"企微机器人-ESS填写-消息状态: {res.json()}")
def algorithm_tip_mes():
    res = requests.post(
        f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={sys.argv[2]}",
        json={
            "msgtype": "news",
            "news": {
                "articles": [
                    {
                        "title": "钉钉乐 温馨提示",
                        "description": "规则文档有版本更新时\r    请及时同步到标注规范汇总表\r        文档链接在群公告",
                        "url": "https://api.vvhan.com/api/moyu",
                        "picurl": "https://api.vvhan.com/api/moyu"
                    }
                ]
            }
        }
    )
    logger.info(f"企微机器人-规则文档提示-消息状态: {res.json()}")

if __name__ == "__main__":
    ann_team_tip_mes()
    algorithm_tip_mes()
