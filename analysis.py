# author : haohao
# date : 18-7-21
# file_name : analysis.py
"""
存在问题：
停用值没有进行训练
文字位置对匹配的加权没有考虑

整体结构：
使用jieba进行中文分词，TF-IDF进行相似度计算
"""
import jieba
import pymongo
from bson.objectid import ObjectId

from config import *
from gensim import corpora, models, similarities


client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def main():
    """
    模拟API输入的情况：
    1. 先通过下拉表单缩小搜索范围,选定范围n
    2. 选择喜欢的工作d
    3. 之后进行n中文档与d文档相似度的计算排序(TF-IDF)
    :return: 相似度的排序
    """
    input_doc = []
    test_doc = []

    all_doc = db[MONGO_TABLE].find({'place': '上海'})
    temp = list(all_doc)
    print(temp)
    for doc in temp:
        input_doc.append(doc['detail_index'])
    print(input_doc)
    print(len(input_doc))
    doc_test = db[MONGO_TABLE].find_one({'_id': ObjectId("5b532ccc5f627d4337de8042")})
    test_doc = doc_test['detail_index']
    print(test_doc)

    analysis(input_doc, test_doc)


def analysis(all_doc, doc_test):
    result = []
    all_doc_list = seperate(all_doc)
    print(all_doc_list)
    doc_test_list = seperate(doc_test)
    print(doc_test_list)
    result = get_similarity(all_doc_list, doc_test_list)
    return result


# 进行分词
def seperate(all_doc):
    all_doc_list = []
    if isinstance(all_doc, str):
        all_doc_list = [word for word in jieba.cut(all_doc)]
    elif isinstance(all_doc, list):
        for doc in all_doc:
            doc_list = [word for word in jieba.cut(doc)]
            all_doc_list.append(doc_list)
    return all_doc_list


def get_similarity(all_doc_list, doc_test_list):
    """
    1. 使用corpora.Dictionary（建立分词与编号的定义库）->使用dictionary.doc2bow(建立每个文档的分词-索引标号-数量 向量）
    2. 使用models.TfidfModel（通过分词-索引标号-数量 向量,建立TFidfModel,得到每个all_doc_vec的TF-IDF值）->剔除TF-IDF值较低的
    3. 通过文档的TF-IDF值建立相似度比较矩阵对象index,将测试文档的doc_test_vec代入index对象得到相似度值，并进行排序

    :param all_doc_list: 输入的文字
    :param doc_test_list: 需要测试相似度的样本文字
    :return:相关度排序
    """
    # 1.
    dictionary = corpora.Dictionary(all_doc_list)
    print(dictionary.keys())
    # 获取词的编号
    print(dictionary.token2id)
    # 编号与词之间的对应
    all_doc_vec = get_bag_of_words(dictionary, all_doc_list)
    doc_test_vec = get_bag_of_words(dictionary, doc_test_list)
    # 取二元组向量
    # 2.
    tfidf = models.TfidfModel(all_doc_vec)  # 得到TF-IDF模型

    doc_test_vec = eliminate_junk(tfidf, doc_test_vec)
    # 3.
    index = similarities.SparseMatrixSimilarity(tfidf[all_doc_vec], num_features=len(dictionary.keys()))
    sim = index[tfidf[doc_test_vec]]
    print("相似度:")
    print(sim)
    similarities_sort = sorted(enumerate(sim), key=lambda item: -item[1])
    print("相似度排序：")
    print(similarities_sort)
    return similarities_sort


def get_bag_of_words(dictionary, all_doc_list):
    corpus = []
    if isinstance(all_doc_list[0], str):
        corpus = dictionary.doc2bow(all_doc_list)
    elif isinstance(all_doc_list, list):
        corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]
    print("分词-索引-数量：")
    print(corpus)
    # 制作语料库二元组
    return corpus


def eliminate_junk(tfidf, doc_test_vec):
    """
        去除停用值,停用值：0.05
        """
    test_tfidf = tfidf[doc_test_vec]

    for i in test_tfidf:
        if i[1] < 0.05:
            for doc in doc_test_vec:
                # print(i[0])
                if doc[0] == int(i[0]):
                    print(doc)
                    doc_test_vec.remove(doc)
                    break
    print(doc_test_vec)
    print("测试文档中的词汇的TF-IDF值:")
    print(tfidf[doc_test_vec])  # 测试文档中的词汇的TF-IDF值
    return doc_test_vec


if __name__ == '__main__':
    main()
