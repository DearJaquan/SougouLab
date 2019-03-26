# -*- coding:utf-8 -*-

import os
import sys
import re
import pandas as pd

"""
该脚本目前只做了最简单的特殊符号处理。

"""

df = pd.read_csv('data/chinatax_qa.csv', delimiter=';').dropna()

# 去掉一些特殊符号【爬虫网页数据残渣】
df = df.replace(regex="[&]\w*[;]", value="")

# ===============这里可以按knowledge_id拆分文件===============
q_2 = df[df["knowledge_id"] == 3]
q_2.to_csv("data/knowledge_q_3.txt",
           index = 0,
           header = 0,
           columns=["knowledge_q"])

# ===============这里不拆分文件===============
# 整个knowledge_q文本数据放在一个文件中
df.to_csv("data/knowledge_q.txt",
          index = 0,
          header = 0,
          columns = ["knowledge_q"])

