from selenium import webdriver
from time import sleep
import csv

def brand():
    # 读取data.csv中的信息
    names = []
    hrefs = []
    prices = []
    with open('data.csv', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        for row in csv_reader:  # 将csv 文件中的数据保存到birth_data中
            if(row[-1] != '网址'):
                hrefs.append(row[-1])
            if(row[0] != '名称'):
                names.append(row[0])
            if(row[1] != '价格'):
                prices.append(row[1])


    # 对每个网址爬取评论并写入文件
    for i in range(len(hrefs)):
        fullhref = hrefs[i] + '#none'
        browser = webdriver.Chrome()  # 需要使用chrome的调用驱动chormedrive导入script目录
        try:
            browser.get(fullhref)  # 控制浏览器跳转到这个网页
            brand = browser.find_elements_by_xpath("//div[@class='p-parameter']/ul[@id='parameter-brand']")
            print(brand[0].text.replace("品牌： ", ''))
            with open('brand.csv', 'a', newline='', encoding='utf-8') as csvfile:
                new_list = [names[i], prices[i], brand[0].text.replace("品牌： ", '')]
                writer = csv.writer(csvfile)
                writer.writerow(new_list)
        finally:
            browser.close()