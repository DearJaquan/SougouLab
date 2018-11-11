
import os
import jieba

'''从samples文件夹中读取所有样本文件'''
def listdir(path, list_name):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        else:
            list_name.append(file_path)

list_name = []
listdir('../samples/', list_name)

'''去停用词'''
def get_stop_words():
    path = "stop_words"
    file = open(path, 'rb').read().decode('utf-8').split('\r\n')
    return set(file)

def rm_stop_words(word_list):
    word_list = list(word_list)
    stop_words = get_stop_words()
    # 这个很重要，注意每次pop之后总长度是变化的
    for i in range(word_list.__len__())[::-1]:
        # 去停用词
        if word_list[i] in stop_words:
            word_list.pop(i)
        #  去数字
        elif word_list[i].isdigit():
            word_list.pop(i)
    return word_list

def rm_word_freq_so_little(dictionary, freq_thred):
    small_freq_ids = [tokenid for tokenid, docfreq in dictionary.dfs.items() if docfreq < freq_thred ]
    dictionary.filter_tokens(small_freq_ids)
    dictionary.compactify()


for path in list_name[0:2]:
    print(path)

    file = open(path, 'rb').read().decode('utf-8').split('\n')
    class_count = 0
    for text in file:
        # 打标签
        class_count = class_count + 1

        content = text
        # 分词
        word_list = list(jieba.cut(content, cut_all=False))
        # 去停用词
        word_list = rm_stop_words(word_list)

        dictionary.add_documents([word_list])

        '''
        转化成词袋
        gensim包中的dic实际相当于一个map
        doc2bow方法，对没有出现过的词语，在dic中增加该词语
        如果dic中有该词语，则将该词语序号放到当前word_bow中并且统计该序号单词在该文本中出现了几次
        '''
        word_bow = dictionary.doc2bow(word_list)
        bow.append(word_bow)