# -*- coding:utf-8 -*-
'''
七月在线  julyEdu.com
note：视频代码采用python2.X
'''
import os
import sys
import jieba
import sklearn

stopwords_folder_path = '../samples/stopwords/'

# 词统计,【去重】
def make_word_set(words_file):
    print("生成样本集....")
    words_set = set()   #set()函数创建一个无序不重复元素集，可进行关系测试，删除重复数据，计算交、差、并集等
    with open(words_file, 'r', encoding = 'utf-8') as fp: # open()函数‘Open file and return a stream’
        for line in fp.readlines():
            word = line.strip()
            if len(word) > 0 and word not in words_set:    #去重
                words_set.add(word)
    print("样本集生成完毕")
    return words_set


# 文本处理，样本生成的过程
def text_processing(folder_path, test_size=0.2):
    folder_list = os.listdir(folder_path)
    data_list = []
    class_list = []

    # 遍历文件夹
    for folder in folder_list:
        new_folder_path = os.path.join(folder_path, folder)
        files = os.listdir(new_folder_path)
        # 读取文件
        # j=1
        for file in files:
            # if j >10:   #只取10个样本文件,以防内存爆炸
            #     break
            with open(os.path.join(new_folder_path, file), 'r') as  fp:
                raw = fp.read()
                # 结巴中文分词
                word_cut = jieba.cut(raw, cut_all=False)    #精确模式，返回的结构是一个可迭代的genertor
                word_list = list(word_cut)  #将genertor转化为list，unicode编码
                data_list.append(word_list) #训练集list
                class_list.append(folder.decode('utf-8'))   #类别
                # j += 1

    train_data_list, test_data_list, train_class_list, test_class_list = sklearn.cross_validation.train_test_split(
            data_list, class_list, data_list = class_list)  #sklearn划分训练集，测试集

    # 统计词频 【字典】
    all_words_dict = {}
    for word_list in train_data_list:
        for word in word_list:
            if all_words_dict.has_key(word):
                all_words_dict[word] += 1
            else:
                all_words_dict[word] = 1
    # 利用词频进行降序。内建函数sorted参数需为list
    all_words_tuple_list = sorted(all_words_dict.items(), key=lambda x: x[1], reverse=True)

    all_words_list = list(zip(*all_words_tuple_list)[0])
    return all_words_list, train_data_list, test_data_list,train_class_list, test_class_list

def words_dict(all_words_list, deleteN, stopwords_set=set()):
    # 选取特征词
    feature_words = []
    n = 1
    for t in range(deleteN, len(all_words_list), 1):
        if n> 1000: # feature_words的维度1000
            break

        if not all_words_list(t).isdigit() and all_words_list[t] not in stopwords_set and 1 < len(all_words_list[t]) < 5:
            feature_words.append(all_words_list[t])
            n += 1
    return feature_words
