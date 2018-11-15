from urllib import request #负责网络请求和响应
from bs4 import BeautifulSoup #负责解析html
import pymysql
import json
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}
def start():
    req = request.Request("https://bj.lianjia.com/ershoufang/rs/",headers=headers)
    resp = request.urlopen(req)
    soup = BeautifulSoup(resp, "lxml")
    totalPage = int(json.loads(soup.select("div.page-box.house-lst-page-box")[0].attrs.get("page-data",None)).get("totalPage",0))
    #for curPage in range(1,totalPage+1):
    for curPage in range(1,1+1):
        req = request.Request("https://bj.lianjia.com/ershoufang/pg{page}/".format(page=curPage),headers=headers)
        resp = request.urlopen(req)
        soup = BeautifulSoup(resp, "lxml")
        for n in soup.select("div.info.clear"):
            url = n.select("div.title > a")[0].attrs.get("href",None)
            if url is not None:
                parse(url);
def parse(url):
    req = request.Request(url,headers=headers)
    resp = request.urlopen(req)
    soup = BeautifulSoup(resp,"lxml")
    direction = soup.select("div.base > div.content li")[6].contents[1]
    district = soup.select("div.areaName > span.info a")[1].string
    elevator = soup.select("div.base > div.content li")[11].contents[1]
    floor = soup.select("div.base > div.content li")[1].contents[1]
    garden = soup.select("div.communityName a")[0].string
    layout = soup.select("div.base > div.content li")[0].contents[1]
    price = soup.select("span.total")[0].string
    region = soup.select("div.areaName > span.info a")[0].string
    renovation = soup.select("div.base > div.content li")[8].contents[1]
    size = soup.select("div.base > div.content li")[2].contents[1]
    year = soup.select("div.houseInfo > div.area > div.subInfo")[0].string
    info={
        "direction":direction,
        "district":district,
        "elevator":elevator,
        "floor":floor,
        "garden":garden,
        "layout":layout,
        "price":price,
        "region":region,
        "renovation":renovation,
        "size":size,
        "year":year
    }
    print(info)

    print(direction,district,elevator,floor,garden,layout,price,region,renovation,size,year,sep="|")
    save_mysql(info)
#打开数据库连接
conn = pymysql.connect(host="192.168.0.10",user="root",password="123",db="test",charset="utf8")
# 使用cursor()方法获取操作游标
cur = conn.cursor()
def save_mysql(info):
    sql = '''
    insert into tb_info (direction,district,elevator,floor,garden,layout,price,region,renovation,size,year)
    values(%(direction)s,%(district)s,%(elevator)s,%(floor)s,%(garden)s,%(layout)s,%(price)s,%(region)s,%(renovation)s,%(size)s,%(year)s)
    '''
    # 使用execute方法执行SQL语句
    cur.execute(sql,info)
    conn.commit()
# ch = pymysql.Connection('192.168.0.10')
# table = ch.table("tb_info")
start()
cur.close()
conn.close()
#producer.close()
# ch.close()