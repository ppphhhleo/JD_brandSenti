import csv


def price_sort():
    names = []
    prices = []
    brands = []
    emotion_scores = []

    with open('name_price_brand_emotion.csv', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        next(csv_reader)
        for row in csv_reader:
            names.append(row[0])
            prices.append(row[1])
            brands.append(row[2])
            emotion_scores.append(row[3])

    new_prices = [] # 字符型价格转换为浮点型价格 存储在此
    for i in range(len(prices)):
        new_prices.append(float(prices[i].strip('元')))

    # 对价格升序，三个空列表实现存储对应价格下的商品名称、品牌和情感值
    sorted_new_prices = sorted(new_prices)
    names_1 = []
    brands_1 = []
    emotion_scores_1 = []
    # print(sorted(new_prices))

    for i in range(len(sorted_new_prices)):
        for j in range(len(new_prices)):
            if(sorted_new_prices[i] == new_prices[j]):
                names_1.append(names[j])
                brands_1.append(brands[j])
                emotion_scores_1.append(emotion_scores[j])
                new_prices[j] = ''


    # 按价格升序写入文件
    with open('price_sort.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['名称', '价格', '品牌', '情感值（评估好评率）'])
        for i in range(len(names_1)):
            writer.writerow([names_1[i], sorted_new_prices[i], brands_1[i], emotion_scores_1[i]])

