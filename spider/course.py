from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC
import pymysql

browser = webdriver.Chrome()

wait = WebDriverWait(browser, 10)

def getCode(no):
    # 建立数据库连接
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='123456',
        db='school',
        charset='utf8'
    )

    # 获取游标
    cursor = conn.cursor()

    sql = 'select code from school_code where no=' + str(no)

    cursor.execute(sql)
    code = cursor.fetchall()
    code = str(*code[0])

    cursor.close()

    conn.close()

    return code

def saveCourse():

    code = getCode(1)

    url = 'https://www.icourse163.org/university/' + code + '#/c'
    print(url)
    browser.get(url)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#newCourseList > div > div.um-spoc-course-list_wrap > div')))

    html = browser.page_source
    print(html)
    # for item in course:
    #     print(item)

if __name__=="__main__":
    saveCourse()