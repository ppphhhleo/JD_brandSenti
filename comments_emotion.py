# -*- coding:utf-8 -*-
import pandas as pd
import jieba
import csv

def comment_emotion():
    # 读取data.csv中的网址信息
    global key, score, stopwords
    comments = []
    with open('comment_con.csv', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        # next(csv_reader)  # 跳过标题
        for row in csv_reader:  # 将csv 文件中的数据保存到列表中
            if('https' not in str(row)):
                comments.append(row[0])
    # 基于BosonNLP情感词典计算情感值

    # print(comments)
    count = 0 # 用于将标题写入文件
    #载入词典
    BosonNLP_dict = pd.read_table(r"BosonNLP_dict\BosonNLP_sentiment_score.txt", sep=" ", names=['key', 'score'])
    key = BosonNLP_dict['key'].values.tolist()
    score = BosonNLP_dict['score'].values.tolist()
    #载入停用词
    stopwords = open(r"BosonNLP_dict\baidu_stopwords.txt", 'r', encoding = 'utf-8').read().split('\n')

    #计算情感值并标记
    for i in range(len(comments)):
        print(comments[i])

        # 删除停用词
        for x in stopwords:
            if x in comments[i]:
                comments[i] = comments[i].strip(x)
        # jieba分词
        segs = jieba.lcut(comments[i], cut_all=False)  # 返回list
        # 计算得分
        score_list = []
        for x in segs:
            if x in key:
                score_list.append(score[key.index(x)])
        text_score =  sum(score_list)
        print("情感值：", round(text_score, 5))
        if text_score<0:
            print('机器标注情感倾向：消极\n')
            emotion = '消极'
        else:
            print('机器标注情感倾向：积极\n')
            emotion = '积极'
        with open('comment_emotion.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if (count == 0):
                writer.writerow(['评论', '情感值', '极性'])
                count = count + 1
            new_list = [comments[i], round(text_score, 5), emotion]
            writer.writerow(new_list)
