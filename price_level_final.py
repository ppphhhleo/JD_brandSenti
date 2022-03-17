import csv

def price_level_finally():
    prices_level = []
    brands = []
    emotion_scores = []
    with open('price_level_sort_brand_merge.csv', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        next(csv_reader)
        for row in csv_reader:
            prices_level.append(row[0])
            brands.append(row[1])
            emotion_scores.append(float(row[2]))


    counts = [0,0,0,0,0,0,0]
# 价位可以自行设置
    for i in range(len(prices_level)):
        if (prices_level[i] == '0-1000'):
            counts[0]+=1
        elif (prices_level[i] == '1000-2000'):
            counts[1]+=1
        elif (prices_level[i] == '2000-3000'):
            counts[2]+=1
        elif (prices_level[i] == '3000-4000'):
            counts[3]+=1
        elif (prices_level[i] == '4000-5000'):
            counts[4]+=1
        elif (prices_level[i] == '5000-6000'):
            counts[5]+=1
        else:
            counts[6] += 1

    # print(counts)
    sort_emotion_score = []
    for i in range(len(counts)):
        j = sum(counts[0:i])
        # print(j)
        if(counts[i] == 1):
            sort_emotion_score.append(emotion_scores[j])
        else:
            emotion_score_tmp = sorted(emotion_scores[j:(j+counts[i])], reverse=True)
            # print(emotion_score_tmp)
            sort_emotion_score = sort_emotion_score + emotion_score_tmp
    print(len(sort_emotion_score))
    print(sort_emotion_score)

    prices_level_1 = []
    brands_1 = []
    for i in range(len(counts)):
        j = sum(counts[0:i])
        for h in range(counts[i]):
            for k in range(counts[i]):
                if (sort_emotion_score[j + h] == emotion_scores[j + k]):
                    prices_level_1.append(prices_level[j + k])
                    brands_1.append(brands[j + k])

    # 写入文件
    # 按价格降序写入文件
    with open('price_level_finally.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['价格', '品牌', '情感值（评估好评率）'])
        for i in range(len(sort_emotion_score)):
            writer.writerow([prices_level_1[i], brands_1[i], sort_emotion_score[i]])