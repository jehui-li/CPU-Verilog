import tkinter
from tkinter import *
from pypinyin import lazy_pinyin, Style
import argparse
from fuzzywuzzy import process
import logging
import sys
import time
import datetime
from tqdm import tqdm

class myGUI:
    def __init__(self, root):
        #标题，窗口大小，背景色，容器
        root.title('Project2_GUI')
        root.geometry('500x500+300+30')
        root.config(background="blue")
        frame = Frame(root)        

        class LoggerBox(Text):
            def write(self, message):
                self.insert("end", message)

        #输入部分
        labelh = Label(frame, text="请输出城市名：")
        labelh.pack()
        def getentry():
            global strings
            strings = entry.get()
        entry = Entry(frame, width=20)
        expression = StringVar()#用户输入城市名
        entry["textvariable"] = expression#将城市名显示在Entry控件上
        entry.pack()
        button01 = Button(frame, text='确认', command=getentry)
        button01.pack()

        def showtime():
            label1.config(text="Download progress:" + "▋" * i)
        label1 = Label(frame, width=60)
        for i in range(1, 35):
            showtime()
            label1.pack_forget()
            label1.pack()
            sys.stdout.flush()
            time.sleep(0.02)

        #输入城市中文，返回对应汉语拼音首字母
        def getStrAllAplha(str):
            initial=''.join(lazy_pinyin(str, style=Style.FIRST_LETTER))
            return initial.upper()
        


        

        frame.pack()

        Button(root, text="LOGGER", command=self.btn_command, bg='black', fg='white').pack()
        streamHandlerBox = LoggerBox(root, width=50, height=5)
        streamHandlerBox.pack()
        self.log1 = logging.getLogger('log1')
        self.log1.setLevel(logging.INFO)
        handler = logging.StreamHandler(streamHandlerBox)
        self.log1.addHandler(handler)

    def btn_command(self):
        now = datetime.datetime.now()
        self.log1.info(f"LoggerBox:{now}")
def log():
    logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.DEBUG,filename=args.logfile,
                    filemode='w')
    logging.debug("This is a debug log.")
    logging.info("This is a info log.")
    logging.warning("This is a warning log.")
    logging.error("This is a error log.")
    logging.critical("This is a critical log.")

if __name__ == "__main__":
    #参数解析
    parser = argparse.ArgumentParser(description="Parses command.")
    parser.add_argument("-i", "--cityfile", help="input city file.")
    parser.add_argument("-l", "--logfile", help="output to logfile.")
    args = parser.parse_args()
    #对txt文件进行读取（将城市名放入list并返回）
    filename = args.cityfile
    with open(filename, 'r', encoding='utf-8') as file_object:
        lines = file_object.readlines()  

    root = Tk()
    my = myGUI(root)
    root.mainloop()
