#!/usr/bin/python

import schedule
import smtplib
import requests
from lxml import etree
import re
from datetime import datetime
from datetime import date
import logging
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time
from threading import Thread

one_punch_man = 'https://www.mkzhan.com/214236/'
one_piece = 'https://www.manhuabei.com/manhua/haizeiwang/'
classname = 'update-time'

receivers = ['494939649@qq.com']

# 0 black 1 red 2 green 3 yellow 4blue 5purple 6cyan(青色) 7white


def front_color(text, color): return f'\33[38;5;{str(color)}m{text}\33[0m'
def background_color(text, color): return f'\33[48;5;{str(color)}m{text}\33[0m'

# get comic page by url


def get_page(url):
    page = requests.get(url)
    return page.text


# get string contains update info
# xpath or classname must be choosen
def parse_update_time_info(page, xpath=None, classname=None):
    s = etree.HTML(page)
    if(xpath is not None):
        return s.xpath(xpath)
    elif classname is not None:
        result_array = s.xpath(f'//span[@class="{classname}"]/text()')
        if(len(result_array) == 0):
            raise Exception('there are no update info in this html page')
        if(len(result_array) > 1):
            logging.info('there are more than one update info')
            return result_array[0]
        else:
            return result_array[0]

# get update time for string with update info


def extract_date(string, split='.') -> re.Match:
    date_str = (
        re.search(r'[0-9]{4}'+split+'[0-9]{1,2}'+split+'[0-9]{1,2}', string)).group(0)
    return datetime.strptime(date_str, f'%Y{split}%m{split}%d')


def send_email(subject):
    sender = 'poorguy_tech@163.com'
    receivers = ['poorguy_tech@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    password = 'xxx'

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText('我试试发邮件都不行的吗', 'plain', 'utf-8')
    message['From'] = Header(sender, 'utf-8')   # 发送者
    message['To'] = Header(receivers[0], 'utf-8')        # 接收者
    message['Subject'] = Header(subject, 'utf-8')

    # smtp code xxx
    try:
        smtpObj = smtplib.SMTP_SSL('smtp.163.com', 465)
        smtpObj.login(sender, password)
        smtpObj.sendmail(sender, receivers, message.as_string())
    except smtplib.SMTPException as e:
        logging.error("Error: 无法发送邮件")
        logging.error(e)


def get_one_punch_man_update():
    # one punch man update
    page = get_page(one_punch_man)
    update_info = (parse_update_time_info(page, None, classname=classname))
    print(update_info)

    today_date_time = datetime.strptime(str(date.today()), '%Y-%m-%d')
    update_date_time = (extract_date(update_info))
    if(today_date_time == update_date_time):
        print(front_color(
            f'these is update for ONE PUNCH MAN, click to watch: {one_punch_man}', 2))
        send_email(
            f'these is update for ONE PUNCH MAN, click to watch: {one_punch_man}')
    else:
        print(front_color(f'there is no update for ONE PUNCH MAN', 1))


def get_one_piece_update():
    # one piece update
    one_piece_page = get_page(one_piece)
    one_piece_update_info = (parse_update_time_info(
        one_piece_page, None, classname='zj_list_head_dat'))
    print(one_piece_update_info)
    today_date_time = datetime.strptime(str(date.today()), '%Y-%m-%d')
    if(extract_date(one_piece_update_info, split='-') == today_date_time):
        print(front_color(
            f'these is update for ONE PIECE, click to watch: {one_piece}', 2))
        send_email(
            f'these is update for ONE PUNCH MAN, click to watch: {one_punch_man}')
    else:
        print(front_color(f'there is no update for ONE PIECE', 1))


def job():
    get_one_punch_man_update()
    get_one_piece_update()

# def loop():
#     logging.info('loop start...')
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

if __name__ == '__main__':
    job()
    # schedule.every().day.at('13:15').do(job)
    # thread=Thread(target=loop)
    # thread.setDaemon(True)
    # thread.start()
    # logging.info('main process end. loop running in background')
    
