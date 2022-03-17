
from selenium import webdriver
from time import sleep
import csv

def comment_con():
    # 读取data.csv中的网址信息
    hrefs = []
    with open('data.csv', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        next(csv_reader)  # 跳过标题
        for row in csv_reader:  # 将csv 文件中的数据保存到birth_data中
            if(row[-1] != '网址'):
                hrefs.append(row[-1])
    print(hrefs)



    # 对每个网址爬取评论并写入文件
    for href in hrefs:
        print(href)
        fullhref = href + '#none'
        browser = webdriver.Chrome()  # 需要使用chrome的调用驱动chormedrive导入script目录
        try:

            browser.get(fullhref)  # 控制浏览器跳转到这个网页
            # 获取商品评论按钮
            button = browser.find_element_by_xpath("//li[@clstag='shangpin|keycount|product|shangpinpingjia_1']")
            button.click()  # 控制按钮进行点击
            sleep(10)  # 等待网页加载，防止网页加载过慢

            with open('comment_con.csv', 'a', newline='', encoding='utf-8') as csvfile:  # 新建并打开comment_con.csv文件
                writer = csv.writer(csvfile)
                list_href = [href]
                writer.writerow(list_href)
                comment_count = 0
                for n in range(5):  # 进行5次循环 即找5页评论
                    m = n + 1
                    print(m)
                    lis = browser.find_elements_by_xpath("//p[@class='comment-con']")  # 获取评论
                    for i in range(len(lis)):
                        if (comment_count < 50):
                            writer.writerow([lis[i].text])
                            comment_count = comment_count + 1
                        else:
                            break
                    button2 = browser.find_element_by_class_name("ui-pager-next")  # 获取下一页按钮
                    print(button2.text)
                    sleep(1)
                    print("第%d页" % m)
                    # button2.click()
                    button2.send_keys("\n")
                    sleep(5)

        finally:
            browser.close()

