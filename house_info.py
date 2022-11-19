import random
import re  # 正则表达式
import time
import requests  # 请求数据
import pymysql  # 链接数据库
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter
import logging
import sys
import datetime
def get_data():
    for i in range(1, 51):
        print('正在爬取第%d页' % (i))
        # 爬取上海链家网租房信息
        baseurl = 'https://sh.lianjia.com/zufang/pg'
        url = baseurl + str(i) + '/#contentList'
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        print(url)
        response = requests.get(url, headers=header)
        html = response.text
        data_list = []
        if response.status_code == 200:
            # 单独提取每个小区的信息
            regex = re.compile('title="(.*?)">\n.*?([0-9.]+)㎡\n.*?<em>([0-9.]+)</em> 元/月', re.DOTALL)
            data = regex.findall(html)
            data = list(data)
            data_list.append(data)
        # 每次随机休息1-3秒
        time.sleep(random.randint(1, 3))
    return data_list

def process_data(data):
    res = []
    res_list = []
    for i in range(0, len(data)):
        res.append([data_list[0][i][0].split()[0][3:], data_list[0][i][2]])
        res_list.append([data_list[0][i][0].split()[0][:2],
                         data_list[0][i][0].split()[0][3:],
                         data_list[0][i][0].split()[1],
                         data_list[0][i][0].split()[2],
                         data_list[0][i][1],
                         data_list[0][i][2],
                         data_list[0][i][3]]
                        )
 
    return res, res_list

def store_data(data):
    # 连接数据库
    conn = pymysql.connect(
        user="root",
        port=3306,
        passwd="123456",
        db="cityhouse",
        host="127.0.0.1",
        charset='utf8'
    )
    if conn:
        print('数据库连接成功')
        error = 0
        try:
            cursor = conn.cursor()
            num = 0
            for item in data:
                print(item)
                num = num + 1
                x0 = str(item[0])
                x1 = str(item[1])
                x2 = str(item[2])
                x3 = str(item[3])
                x4 = str(item[4])
                x5 = str(item[5])
                x6 = str(item[6])
                insert_re = f'insert into house(quyu, xiaoqu,house_size,chaoxiang,huxing,lou_type,price) values (\'{x0}\',\'{x1}\',\'{x2}\',\'{x3}\',\'{x4}\',\'{x5}\',\'{x6}\')'
                print(insert_re)
                print(type(insert_re))
                cursor.execute(insert_re)
                conn.commit()
        except Exception as e:
            error = error + 1
        except UnicodeDecodeError as e:
            error = error + 1
        # 断开数据库连接
        conn.close()
    else:
        print('数据库连接失败')

class myGUI:
    def __init__(self, win):
        #标题，窗口大小，背景色，容器
        win.title('Project2_GUI')
        win.geometry('1000x500+300+30')
        win.config(background="white")
        frame = Frame(win)        

        #输入部分
        labelh = Label(frame, text="请输出城市名：")
        labelh.pack()
        '''
        def getentry():
            global strings
            strings = entry.get()
        '''
        entry = Entry(frame, width=20)
        expression = StringVar()#用户输入城市名
        entry["textvariable"] = expression#将城市名显示在Entry控件上
        entry.pack()
        button01 = Button(frame, text='确认', command=insert)
        button01.pack()
        #进度条
        def showtime():
            label1.config(text="Progressing:" + "▋" * i)
        label1 = Label(frame, width=500)
        for i in range(1, 35):
            showtime()
            label1.pack_forget()
            label1.pack()
            sys.stdout.flush()
            time.sleep(0.02)
            
        frame.pack()
        def insert():
    # 插入数据
            for item in data:
                print(item)
                num = num + 1
                x0 = str(item[0])
                x1 = str(item[1])
                x2 = str(item[2])
                x3 = str(item[3])
                x4 = str(item[4])
                x5 = str(item[5])
                x6 = str(item[6])
                insert_re = f'insert into rent(quyu, xiaoqu,house_size,chaoxiang,huxing,lou_type,rent) values (\'{x0}\',\'{x1}\',\'{x2}\',\'{x3}\',\'{x4}\',\'{x5}\',\'{x6}\')'
                info = []
                info.append([x0,x1,x2,x3,x4,x5,x6])
            for data in enumerate(info):
                table.insert('', END, values=data)  # 添加数据到末尾
            screenwidth = win.winfo_screenwidth()
            screenheight = win.winfo_screenheight()
            width = 1000
            height = 500
            x = int((screenwidth - width) / 2)
            y = int((screenheight - height) / 2)
            win.geometry('{}x{}+{}+{}'.format(width, height, x, y)) 

            tabel_frame = tkinter.Frame(win)
            tabel_frame.pack()

            xscroll = Scrollbar(tabel_frame, orient=HORIZONTAL)
            yscroll = Scrollbar(tabel_frame, orient=VERTICAL)

            columns = ['区域', '小区', '房子大小', '房子朝向', '户型', '价格', '楼层类型']
            table = ttk.Treeview(
                master=tabel_frame,  # 父容器
                height=10,  # 表格显示的行数,height行
                columns=columns,  # 显示的列
                xscrollcommand=xscroll.set,  # x轴滚动条
                yscrollcommand=yscroll.set,  # y轴滚动条
                )
            for column in columns:
                table.heading(column=column, text=column, anchor=CENTER,
                        command=lambda name=column:
                        messagebox.showinfo('', '{}描述信息~~~'.format(name)))  # 定义表头
            table.column(column=column, width=100, minwidth=100, anchor=CENTER, )  # 定义列
            xscroll.config(command=table.xview)
            xscroll.pack(side=BOTTOM, fill=X)
            yscroll.config(command=table.yview)
            yscroll.pack(side=RIGHT, fill=Y)
            table.pack(fill=BOTH, expand=True)
            insert()

        btn_frame = Frame()
        btn_frame.pack()
        Button(btn_frame, text='保存数据', bg='yellow', width=20, command=store_data).pack()


 


        Button(win, text="LOGGER", command=self.btn_command, bg='black', fg='white').pack()        
        class LoggerBox(Text):
            def write(self, message):
                self.insert("end", message)
        streamHandlerBox = LoggerBox(win, width=500, height=5)
        streamHandlerBox.pack()
        self.log1 = logging.getLogger('log1')
        self.log1.setLevel(logging.INFO)
        handler = logging.StreamHandler(streamHandlerBox)
        self.log1.addHandler(handler)
    def btn_command(self):
        now = datetime.datetime.now()
        self.log1.info(f"LoggerBox:{now}")

if __name__ == "__main__":
    data_list = get_data()
    res, res_list = process_data(data_list[0])
    store_data(res_list)  # 数据存入数据库
    win = Tk()
    my = myGUI(win)
    win.mainloop()
