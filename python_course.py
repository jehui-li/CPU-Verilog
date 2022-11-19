from pypinyin import lazy_pinyin, Style
import argparse
from fuzzywuzzy import process
import logging
import sys
import time
from tqdm import tqdm
#输入城市中文，返回对应汉语拼音首字母
def getStrAllAplha(str):
    initial=''.join(lazy_pinyin(str, style=Style.FIRST_LETTER))
    return initial.upper()
#模糊匹配
def vLook():
    #对txt文件进行读取（将城市名放入list并返回）
    filename = args.cityfile
    with open(filename, 'r', encoding='utf-8') as file_object:
        lines = file_object.readlines()
    #模糊匹配
    results = process.extract(str, lines, limit = 3)
    print(f"查找到城市1：{results[0][0]} 匹配度：{results[0][1]}%")
    print(f"查找到城市2：{results[1][0]} 匹配度：{results[1][1]}%")
    print(f"查找到城市3：{results[2][0]} 匹配度：{results[2][1]}%")   

#写日志
def log():
    logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.DEBUG,filename=args.logfile,
                    filemode='w')
    logging.debug("This is a debug log.")
    logging.info("This is a info log.")
    logging.warning("This is a warning log.")
    logging.error("This is a error log.")
    logging.critical("This is a critical log.")

#加载进度条
def progress_bar():
    _output = sys.stdout
    #使用tqdm库
    for i in tqdm(range(100), desc='Processing'):
        # 这里的second只是作为工作量的一种代替
        _second = 0.05
        # 模拟业务的消耗时间
        time.sleep(_second)
       # 将标准输出一次性刷新
        _output.flush()

if __name__ == '__main__':
    #参数解析
    parser = argparse.ArgumentParser(description="Parses command.")
    parser.add_argument("-i", "--cityfile", help="input city file.")
    parser.add_argument("-l", "--logfile", help="output to logfile.")
    args = parser.parse_args()
    
    print("请输出城市名：",end = "")
    str = input()
    progress_bar()
    print("城市名的大写字母：",end = "")
    print(getStrAllAplha(str).upper())
    vLook()
    log()
