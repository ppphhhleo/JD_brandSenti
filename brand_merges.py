import csv

def brand_merge():
    sorted_new_prices = []
    brands_1 = []
    emotion_scores_1 = []

    with open('price_sort.csv', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        next(csv_reader)
        for row in csv_reader:
            sorted_new_prices.append(float(row[1]))
            brands_1.append(row[2])
            emotion_scores_1.append(float(row[3]))

    counts = [0,0,0,0,0,0,0]

# 可以自行设置价位

    for i in range(len(sorted_new_prices)):
        if (sorted_new_prices[i] > 0 and sorted_new_prices[i] < 1000):
            counts[0]+=1
        elif (sorted_new_prices[i] >= 1000 and sorted_new_prices[i] < 2000):
            counts[1]+=1
        elif (sorted_new_prices[i] >= 2000 and sorted_new_prices[i] < 3000):
            counts[2]+=1
        elif (sorted_new_prices[i] >= 3000 and sorted_new_prices[i] < 4000):
            counts[3]+=1
        elif (sorted_new_prices[i] >= 4000 and sorted_new_prices[i] < 5000):
            counts[4]+=1
        elif (sorted_new_prices[i] >= 5000 and sorted_new_prices[i] < 6000):
            counts[5]+=1
        else:
            counts[6] += 1

    prices_level = []
    for i in range(len(counts)):
        for j in range(counts[i]):
            if i == 0:
                prices_level.append('0-1000')
            elif i == 1:
                prices_level.append('1000-2000')
            elif i == 2:
                prices_level.append('2000-3000')
            elif i == 3:
                prices_level.append('3000-4000')
            elif i == 4:
                prices_level.append('4000-5000')
            elif i == 5:
                prices_level.append('5000-6000')
            else:
                prices_level.append('>6000')


    brands_merge = []
    prices_level_merge = []
    emotion_scores_merge = []
    for i in range(len(counts)):
        j = sum(counts[0:i])
        # print(j)
        been_kandled_brands = []
        for h in range(counts[i]):
            if (brands_1[j+h] in been_kandled_brands):
                continue
            been_kandled_brands.append(brands_1[j + h])
            sum_scores = float(emotion_scores_1[j + h])
            number = 1
            for k in range(counts[i]):
                if (h != k and prices_level[j + h] == prices_level[j + k] and brands_1[j + h] == brands_1[j + k]):
                    sum_scores += float(emotion_scores_1[j + k])
                    number = number + 1

            brands_merge.append(brands_1[j + h])
            prices_level_merge.append(prices_level[j + h])
            emotion_scores_merge.append(sum_scores/number)
    print(len(prices_level_merge))
    print(len(brands_merge))
    print(len(emotion_scores_merge))
    # 按价格降序写入文件
    with open('price_level_sort_brand_merge.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['价位', '品牌', '情感值（评估好评率）'])
        for i in range(len(brands_merge)):
            writer.writerow([prices_level_merge[i], brands_merge[i], emotion_scores_merge[i]])

