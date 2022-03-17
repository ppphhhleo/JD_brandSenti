

from selenium import webdriver
import time
import csv
import brands
import comments_con
import comments_emotion
import name_price_brand_emotions
import price_sorts
import brand_merges
import price_level_final


def get_product(key):
    """搜索商品"""
    driver.find_element_by_css_selector('#key').send_keys(key)
    driver.find_element_by_css_selector('.button').click()  # click()点击


    driver.implicitly_wait(10)  # 隐式
    driver.maximize_window()  # 浏览器最大化



def drop_down():
    """懒加载, 模拟人去滚动鼠标向下浏览页面"""
    for x in range(1, 11, 2):
        time.sleep(0.5)
        j = x / 10
        js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % j
        driver.execute_script(js)


def parse_product():
    """解析商品数据"""
    lis = driver.find_elements_by_css_selector('.gl-warp.clearfix>li')
    count = 0
    for li in lis:
        try:
            name = li.find_element_by_css_selector('.p-name a em').text   # 商品的名字
            price = li.find_element_by_css_selector('.p-price strong i').text + '元'  # 商品的价格
            info = li.find_element_by_css_selector('.p-commit strong a').text   # 商品的评价数
            title = li.find_element_by_css_selector('.J_im_icon a').get_attribute('title')   # 商品的店铺
            web = li.find_element_by_css_selector('.p-img a').get_attribute('href')
            print(name, price, info, title, web)
            with open('data.csv', mode='a', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                # if count == 0:
                #     writer.writerow(['名称', '价格', '评价数', '店铺', '网址'])
                if ('万' in info):
                    count += 1
                    writer.writerow([name, price, info, title, web])
        except Exception as e:
            print(e)

def get_next():
    """找到下一页标签, 点击"""
    driver.find_element_by_css_selector('#J_bottomPage > span.p-num > a.pn-next > em').click()
    driver.implicitly_wait(10)

keyword = input('请输入你想要的搜索商品的关键字:')
driver = webdriver.Chrome()  # 创建一个浏览器对象
driver.get('https://www.jd.com/')

with open('data.csv', mode='a', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['名称', '价格', '评价数', '店铺', '网址'])
get_product(keyword)
for page in range(1, 5): # 可以设置爬取商品的页数
    drop_down()
    parse_product()
    get_next()
# 可自行分步骤调试
print('商品品牌')
brands.brand()
print('商品评论')
comments_con.comment_con()
print('评论情感极性')
comments_emotion.comment_emotion()
print('商品的情感值')
name_price_brand_emotions.name_price_brand_emotion()
print('价格排序')
price_sorts.price_sort()
print('同一价位品牌合并')
brand_merges.brand_merge()
print('同一价位品牌内部情感值排序')
price_level_final.price_level_finally()















