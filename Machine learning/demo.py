import time
import torch
import numpy as np
from train_eval import train, init_network
from importlib import import_module
import argparse
from tqdm import tqdm
import os
import torch
import numpy as np
import pickle as pkl
from utils import DatasetIterater
import torch.nn.functional as F
MAX_VOCAB_SIZE = 10000  # 词表长度限制
UNK, PAD = '<UNK>', '<PAD>'  # 未知字，padding符号
def build_vocab(file_path, tokenizer, max_size, min_freq):
    vocab_dic = {}
    with open(file_path, 'r', encoding='UTF-8') as f:
        for line in tqdm(f):
            lin = line.strip()
            if not lin:
                continue
            content = lin.split('\t')[0]
            for word in tokenizer(content):
                vocab_dic[word] = vocab_dic.get(word, 0) + 1
        vocab_list = sorted([_ for _ in vocab_dic.items() if _[1] >= min_freq], key=lambda x: x[1], reverse=True)[:max_size]
        vocab_dic = {word_count[0]: idx for idx, word_count in enumerate(vocab_list)}
        vocab_dic.update({UNK: len(vocab_dic), PAD: len(vocab_dic) + 1})
    return vocab_dic

def build_dataset1(config, ues_word,path):
    if ues_word:
        tokenizer = lambda x: x.split(' ')  # 以空格隔开，word-level
    else:
        tokenizer = lambda x: [y for y in x]  # char-level
    if os.path.exists(config.vocab_path):
        vocab = pkl.load(open(config.vocab_path, 'rb'))
    else:
        vocab = build_vocab(config.train_path, tokenizer=tokenizer, max_size=MAX_VOCAB_SIZE, min_freq=1)
        pkl.dump(vocab, open(config.vocab_path, 'wb'))
    #print(f"Vocab size: {len(vocab)}")
    def load_dataset1(path, pad_size=32):
        contents = []
        data = pd.read_csv(path)
        contents1 = data['评论']
        for content in contents1:
            label = 1
            words_line = []
            token = tokenizer(content)
            seq_len = len(token)
            if pad_size:
                if len(token) < pad_size:
                    token.extend([PAD] * (pad_size - len(token)))
                else:
                    token = token[:pad_size]
                    seq_len = pad_size
            # word to id
            for word in token:
                words_line.append(vocab.get(word, vocab.get(UNK)))
            contents.append((words_line, int(label), seq_len))
        return contents  # [([...], 0), ([...], 1), ...]
    return vocab,load_dataset1(path, config.pad_size)
model_name_list = ['TextCNN','TextRNN','TextRCNN']
for model_name in model_name_list:
    x = import_module('models.' + model_name)
    dataset = 'online_shopping_10_cats'  # 数据集
    print(model_name)
    # 搜狗新闻:embedding_SougouNews.npz, 腾讯:embedding_Tencent.npz, 随机初始化:random
    embedding = 'embedding_SougouNews.npz'
    embedding = 'random'
    config = x.Config(dataset, embedding)
    from utils import build_dataset, build_iterator, get_time_dif
    keyword = "笔记本电脑.csv"
    import pandas as pd
    data = pd.read_csv('./product-o/c.csv')
    product_ID = (data['ID'])
    print(product_ID)
    score_set = []
    sum1 = 0
    #for id in product_ID:
    for a in range(2):
        path = './product-o/25361143529.csv'
        #path = './product-o/' + str(id) +'评论.csv'
        vocab, texts = build_dataset1(config, False,path)
        data_iter = DatasetIterater(texts, len(texts), config.device)
        config.n_vocab = len(vocab)
        model = x.Model(config).to(config.device)
        model.load_state_dict(torch.load("./online_shopping_10_cats/saved_dict/"+model_name+".ckpt"))
        sum = 0
        for texts, labels in data_iter: # 依次读取评论 和 标签
            print(texts)
            print(labels)
            outputs = model(texts)
            print(outputs)
            ot = F.softmax(outputs,dim=1)
            sum = 0
            for sc in ot:
                sum += sc[1]  # 累计
            print(sum)
            print(str(float(sum / len(labels))))
            score_set.append(float(sum / len(labels)))
    #print(len(score_set))
    data = pd.read_csv('./product/'+keyword)
    data[model_name] = score_set
    data.to_csv('./product/'+keyword)