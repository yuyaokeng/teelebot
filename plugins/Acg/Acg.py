# -*- coding:utf-8 -*-
from teelebot import Bot
from threading import Timer
import requests

bot = Bot()

def Acg(message):
    chat_id = message["chat"]["id"]
    message_id = message["message_id"]
    text = message["text"]
    prefix = "acg"

    if text[1:len(prefix)+1] == prefix:
        img = acg_img()
        caption = str(one_said())
        if img != False and caption != False:
            status = bot.sendChatAction(chat_id, "typing")
            status = bot.sendPhoto(chat_id=chat_id, photo=img, caption=caption, parse_mode="HTML", reply_to_message_id=message_id)
        else:
            status = bot.sendChatAction(chat_id, "typing")
            status = bot.sendMessage(chat_id=chat_id, text="获取失败，请重试!", parse_mode="HTML", reply_to_message_id=message_id)
            timer = Timer(15, timer_func, args=[chat_id, status["message_id"]])
            timer.start()
    else:
        status = bot.sendChatAction(chat_id, "typing")
        status = bot.sendMessage(chat_id=chat_id, text="指令错误，请检查!", parse_mode="HTML", reply_to_message_id=message_id)
        timer = Timer(15, timer_func, args=[chat_id, status["message_id"]])
        timer.start()


def acg_img():
    url = "https://v1.alapi.cn/api/acg"
    with requests.post(url=url, verify=False) as req:
        if not req.status_code == requests.codes.ok:
            return False
        elif type(req.content) == bytes:
            return req.content
        else:
            return False

def one_said():
    url = "http://api.guaqb.cn/v1/onesaid/"
    with requests.post(url, verify=False) as req:
        if not req.status_code == requests.codes.ok:
            return False
        else:
            return req.text


def timer_func(chat_id, message_id):
    status = bot.deleteMessage(chat_id=chat_id, message_id=message_id)
