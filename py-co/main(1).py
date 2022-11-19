import tkinter
from tkinter import *
from pypinyin import lazy_pinyin, Style
from fuzzywuzzy import process
import logging
import time
import datetime
import sys

import re #正则表达式，进行文字匹配
from bs4 import BeautifulSoup#网页解析，获取数据
import urllib.request,urllib.error #制定URL，获取网页数据
import xlwt #进行excel操作
import pymysql
class App:
    def __init__(self, win):
        win.title('Project_2')
        # win.geometry('600x500')
        win.config(background="white")
        # 创建一个容器来包括其他控件
        frame = Frame(win)

        filename = 'cities.txt'
        with open(filename, 'r', encoding='utf-8') as file_object:
            lines = file_object.readlines()

        class LoggerBox(Text):

            def write(self, message):
                self.insert("end", message)

        def getentry():
            global strings
            strings = entry.get()  # 获取Entry的内容

        def get_city_py(a):
            style = Style.FIRST_LETTER
            k = lazy_pinyin(a, style=style)
            strk = '拼音首字母：'
            for letter in k:
                strk += letter.upper()
                strk += ' '
            return strk

        def calc():
            result = get_city_py(strings)
            # 将计算的结果显示在Label控件上
            results = process.extract(strings, lines, limit=2)
            result += "\n城市一: " + str(results[0][0]) + " 匹配度:" + str(results[0][1]) + "%"
            result += "\n城市二: " + str(results[1][0]) + " 匹配度:" + str(results[1][1]) + "%"
            label.config(text=result)

        def showtime():
            label1.config(text="Download progress:" + "▋" * i)

        label1 = Label(frame, width=60)
        for i in range(1, 35):
            showtime()
            label1.pack_forget()
            label1.pack()
            sys.stdout.flush()
            time.sleep(0.02)

        labelf = Label(frame, text="输入你要查找的城市")
        labelf.pack()
        # 创建一个Label控件
        label = Label(frame, width=60, height=8, padx=10, pady=15, borderwidth=10, relief="sunken")
        # 创建一个Entry控件
        entry = Entry(frame, width=30)
        # 读取用户输入的表达式
        expression = StringVar()
        entry["textvariable"] = expression
        button01 = Button(frame, text='获取信息', command=getentry)
        button01.pack()

        button1 = Button(frame, text="查找", command=calc)
        frame.pack()
        # Entry控件位于窗体的上方
        entry.pack()
        # Label控件位于窗体的左方
        label.pack(side="left", fill=tkinter.BOTH)
        # Button控件位于窗体的右方
        button1.pack(side="right")


        Button(win, text="LOGGER", command=self.btn_command, bg='black', fg='white').pack()

        streamHandlerBox = LoggerBox(win, width=50, height=5)
        streamHandlerBox.pack()
        self.log1 = logging.getLogger('log1')
        self.log1.setLevel(logging.INFO)
        handler = logging.StreamHandler(streamHandlerBox)
        self.log1.addHandler(handler)

    def btn_command(self):

        now = datetime.datetime.now()
        self.log1.info(f"LoggerBox:{now}")


if __name__ == "__main__":
    win = Tk()
    app = App(win)
    # 开始程序循环
    win.mainloop()
