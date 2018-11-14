#coding=utf-8
import os
import jieba
import sys
import re
import time
import jieba.posseg as pseg

sys.path.append("../")
jieba.load_userdict("../samples/dicts/smalldict.txt") # 加载自定义分词词典

'''
title：利用结巴分词进行文本语料处理：单文本处理器、批量文件处理器
    1 首先对文本进行遍历查找
    2 创建原始文本的保存结构
    3 对原文本进行结巴分词和停用词处理
    4 对预处理结果进行标准化格式，并保存原文件结构路径
'''

'''
分词.词性标注以及去停用词
stopwordspath： 停用词路径
dealpath：中文数据预处理文件的路径
savepath：中文数据预处理结果的保存路径
'''
def cutTxtWord(dealpath,savepath,stopwordspath):
    stopwords = {}.fromkeys([ line.rstrip() for line in open(stopwordspath,"r",encoding='utf-8')]) # 停用词表
    with open(dealpath,"r",encoding='utf-8') as f:
        txtlist=f.read() # 读取待处理的文本
    words =pseg.cut(txtlist) # 带词性标注的分词结果
    cutresult=""# 获取去除停用词后的分词结果
    for word, flag in words:
        if word not in stopwords:
            cutresult += word+"/"+flag+" " #去停用词
            getFlag(cutresult,savepath) #


'''
分词.词性标注以及去停用词
stopwordspath： 停用词路径
read_folder_path ：中文数据预处理文件的路径
write_folder_path ：中文数据预处理结果的保存路径
filescount=300 #设置文件夹下文件最多多少个
'''

def cutFileWord(read_folder_path,write_folder_path,stopwordspath):
    # 停用词表
    stopwords = {}.fromkeys([ line.rstrip() for line in open(stopwordspath,"r",encoding='utf-8')])
    # 获取待处理根目录下的所有类别
    folder_list = os.listdir(read_folder_path)
    # 类间循环
    for folder in folder_list:
        #某类下的路径
        new_folder_path = os.path.join(read_folder_path, folder)

        # 创建保存文件目录
        path=write_folder_path+folder #保存文件的子文件
        isExists=os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            print(path+' 创建成功')
        else: pass
        save_folder_path = os.path.join(write_folder_path, folder)#某类下的保存路径
        print('--> 请稍等，正在处理中...')

        # 类内循环
        files = os.listdir(new_folder_path)
        j = 1
        for file in files:
            if j > len(files): break
            dealpath = os.path.join(new_folder_path, file) #处理单个文件的路径
            with open(dealpath,"r",encoding='utf-8') as f:
                txtlist=f.read()
                # python 过滤中文、英文标点特殊符号
                # txtlist1 = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "",txtlist)
            words =pseg.cut(txtlist) # 带词性标注的分词结果
            cutresult="" # 单个文本：分词后经停用词处理后的结果
            for word, flag in words:
                if word not in stopwords:
                    cutresult += word+"/"+flag+" " #去停用词
            savepath = os.path.join(save_folder_path,file)
            getFlag(cutresult,savepath)
            j += 1

'''
做词性筛选
cutresult：str类型，初切分的结果
savepath： 保存文件路径
'''
def getFlag(cutresult,savepath):
    txtlist=[] #过滤掉的词性后的结果
    #词列表为自己定义要过滤掉的词性
    cixing=["/x","/zg","/uj","/ul","/e","/d","/uz","/y"]
    for line in cutresult.split('\n'):
        line_list2=re.split('[ ]', line)
        line_list2.append("\n") # 保持原段落格式存在
        line_list=line_list2[:]
        for segs in line_list2:
            for K in cixing:
                if K in segs:
                    line_list.remove(segs)
                    break
                else:
                    pass
        txtlist.extend(line_list)

    # 去除词性标签
    resultlist=txtlist[:]
    flagresult=""
    for v in txtlist:
        if "/" in v:
            slope=v.index("/")
            letter=v[0:slope]+" "
            flagresult+= letter
        else:
            flagresult+= v
    standdata(flagresult,savepath)
'''
标准化处理，去除空行，空白字符等。
flagresult:筛选过的结果
'''
def standdata(flagresult,savepath):
    f2=open(savepath,"w",encoding='utf-8')
    for line in flagresult.split('\n'):
        if len(line)>=2:
            line_clean="/ ".join(line.split())
            lines=line_clean+" "+"\n"
            f2.write(lines)
        else: pass
    f2.close()


if __name__ == '__main__' :
    t1=time.time()


    # 测试单个文件
    dealpath="../Database/SogouC/FileTest/1.txt"
    savepath="../Database/SogouCCut/FileTest/1.txt"

    stopwordspath='../Database/stopwords/CH_stopWords.txt'
    stopwordspath1='../Database/stopwords/HG_stopWords.txt' # 哈工大停用词表

    # 批量处理文件夹下的文件
    # rfolder_path = '../Database/SogouC/Sample/'
    rfolder_path = '../Database/SogouC/FileNews/'
    # 分词处理后保存根路径
    wfolder_path = '../Database/SogouCCut/'

    # 中文语料预处理器
    # cutTxtWord(dealpath,savepath,stopwordspath) # 单文本预处理器
    cutFileWord(rfolder_path,wfolder_path,stopwordspath) # 多文本预处理器


    t2=time.time()
    print("中文语料语处理完成，耗时："+str(t2-t1)+"秒。") #反馈结果
