from bs4 import BeautifulSoup
from lxml import html
import xml
import requests
import re
import pymysql

def getCode():

    # 建立数据库连接
    conn=pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='123456',
        db='school',
        charset='utf8'
    )

    # 获取游标
    cursor=conn.cursor()

    # 创建表
    cursor.execute("drop table if exists school_code")
    creat = 'create table school_code (no int,schoolName varchar(20), code varchar(20))'
    cursor.execute(creat)




    url = "https://www.icourse163.org/university/view/all.htm#/"
    htmlData = requests.get(url)
    soup = BeautifulSoup(htmlData.text, 'lxml')
    data = soup.select('#g-body > div > div.g-flow > div.u-usitys.f-cb > a')

    no = 1#序号

    for item in data:
        name = re.findall(r'<img alt="(.*)" class="".*',str(item))
        code = re.findall('/university/(.*)',item.get('href'))
        insert = "insert into school_code values ("+ str(no) +", '"+str(*name)+"', '"+str(*code)+"')"
        cursor.execute(insert)
        no = no + 1


    conn.commit()
    cursor.close()
    conn.close()

if __name__=="__main__":
    getCode()