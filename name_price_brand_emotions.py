import csv

def name_price_brand_emotion():
    emotion_scores = []
    with open('comment_emotion.csv', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        next(csv_reader)
        for row in csv_reader:
            emotion_scores.append(row[1])
    print(len(emotion_scores))

    rounds = int(len(emotion_scores)/50) # 轮次

    sum_ave_list = [] # 存储每50个元素的和的平均值，这里需要根据爬取到的评论数量调整，如果爬取100条评论，则改成100

    for i in range(rounds):
        sum = 0.0 # 每50个元素的和
        for k in range(50):
            sum = sum + float(emotion_scores[50 * i + k])
        ave_score = sum / 50
        sum_ave_list.append(ave_score)
    print(sum_ave_list)

    names = []
    prices = []
    brands = []

    with open('brand.csv', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        for row in csv_reader:
            names.append(row[0])
            prices.append(row[1])
            brands.append(row[2])


    with open('name_price_brand_emotion.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['名称', '价格', '品牌', '情感值（衡量好评度）'])
        for i in range(len(names)):
            new_list = [names[i], prices[i], brands[i], sum_ave_list[i]]
            writer.writerow(new_list)
