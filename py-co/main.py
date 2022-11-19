import requests
import parsel
import sqlite3

id = 1


con = sqlite3.connect("test.db")

cur = con.cursor()
sql = "create table lianjia0(page int, title TEXT NOT NULL, address TEXT NOT NULL, introduce TEXT NOT NULL, tags TEXT NOT NULL,totalPrise TEXT NOT NULL, unitPrice TEXT NOT NULL)"

con.commit()
con.close()

con = sqlite3.connect("test.db")
cur = con.cursor()
res = cur.execute("select * from lianjia0")
for r in res.fetchall():
    print(r)
test = "select * from lianjia0"
cur.execute(test)
des = cur.description
print(des)
for page in range(1, 101):

    print(f"+++++++++++正在抓取第{page}页数据++++++++++++++")
    url = f'https://sy.lianjia.com/ershoufang/pg{page}/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
               'like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42'}

    response = requests.get(url=url, headers=headers)
    html_data = response.text
    # print(html_data)

    selector = parsel.Selector(html_data)
    lis = selector.css('.clear.LOGCLICKDATA')

    for li in lis:
        title = li.css('.title a::text').get()

        address = li.css('.positionInfo a::text').getall()
        address = '- '.join(address)

        introduce = li.css('.houseInfo::text').get()   # 介绍
        star = li.css('.followInfo::text').get()    # 关注

        tags = li.css('.tag span::text').getall()    # 标签
        tags = ','.join(tags)

        totalPrise = li.css('.priceInfo .totalPrice span::text').get() + '万'
        unitPrice = li.css('.unitPrice span::text').get()




        print(id, page, title, address, introduce, tags, totalPrise, unitPrice, sep='****')
        string = "insert into lianjia0 values(%d, %d,'%s','%s','%s','%s','%s','%s')"%\
              (id, page, title, address, introduce, tags, totalPrise, unitPrice)
        id += 1
        cur.execute(string)
        con.commit()


        # with open('lianjia2.csv', mode='a', encoding='utf-8', newline='') as f:
        #     csv_write = csv.writer(f)
        #     csv_write.writerow([title, address, introduce, tags, totalPrise, unitPrice])
        #



