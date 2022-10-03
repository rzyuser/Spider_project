import re
import xlwt
from selenium import webdriver
from selenium.webdriver.common.by import By

# Excel 表格初始化
workbook = xlwt.Workbook(encoding='utf-8')
worksheet = workbook.add_sheet('山西省疫情数据')
worksheet.write(0, 0, '日期')
worksheet.write(0, 1, '新增确诊病例')
worksheet.write(0, 2, '隔离治疗病例')
worksheet.write(0, 3, '疑似病例')

# 初始化参数
driver = webdriver.Chrome()


def get_a(li):
    a = []
    # 将页面内的A标签href属性和时间放到a 数组里
    for index in range(len(li)):
        ti = li[index].find_element_by_xpath(f'//*[@id="container"]/div[3]/div[3]/div[3]/ul/li[{index+1}]/a[2]').text
        if ti.find('新型冠状病') != -1:  # 如果该超链接指向的是疫情文章就装入到a数组
            href = li[index].find_element(By.TAG_NAME, "a").get_attribute('href')
            time = li[index].find_element(By.TAG_NAME, "span").text
            a.append({'time': time, 'a': href})
    return a


def get_page(i):
    driver.get(url='https://wjw.shanxi.gov.cn/xwzx/wjyw/index_' + str(i + 1) + '.shtml')  # 拼接页面url
    ul = driver.find_element(By.XPATH, '//*[@id="container"]/div[3]/div[3]/div[3]/ul')
    # ul = driver.find_element(By.XPATH, '//div[@class="demo-right"]/ul/li')
    li = ul.find_elements(By.TAG_NAME, 'li')
    return li


def page(start, end):
    row = 1  # Excel表行数 起始位置为1
    for i in range(start, end):  # 默认抓取前46页内容
        li = get_page(i)
        # print(li)
        # 获取当前页面所有跟新冠相关的a标签
        a = get_a(li)
        print(a)
        # 遍历a数组一个一个访问超链接
        for j in range(len(a)):
            driver.get(a[j]['a'])
            # p = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/div/p[1]')
            p = driver.find_element_by_xpath('//*[@id="container"]/div[3]/div[2]/div[2]/div[2]/div/div[1]/div/div | //*[@id="container"]/div[3]/div[2]/div[2]/div[2]/div/div[1]/div')
            print(a[j]['time'] + ":")
            sr = p.text
            print(sr)
            # 正则表达 格式化
            add = re.compile('山西省新增本地新冠肺炎确诊病例(.*?)例')
            apart = re.compile('现有在院隔离治疗病例(.*?)例')
            suspect = re.compile('现有疑似病例(.*?)例')
            ax = add.findall(sr)
            b = apart.findall(sr)
            c = suspect.findall(sr)
            # Excel 写表头
            worksheet.write(row, 0, a[j]['time'])
            # 对三个数组进行特判
            if len(ax):
                print("新增：" + ax[0])
                worksheet.write(row, 1, ax[0])
            else:
                print("新增：" + "0")
                worksheet.write(row, 1, '0')
            if len(b):
                print("隔离治疗：" + b[0])
                worksheet.write(row, 2, b[0])
            else:
                print("隔离治疗：" + "0")
                worksheet.write(row, 2, '0')
            if len(c):
                print("疑似：" + c[0])
                worksheet.write(row, 3, c[0])
            else:
                print("疑似：" + "0")
                worksheet.write(row, 3, '0')
            row += 1
            # 保存
            workbook.save('./山西省新冠数据.xlsx')
            print("成功")


if __name__ == '__main__':
    start_page = 0
    end_page = 20
    page(start_page,end_page)