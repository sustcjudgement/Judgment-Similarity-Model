# -*- coding: utf-8 -*-
import numpy as np
import math
import simple_tfidf
import synonyms
import time



class simhash:
    def __init__(self, content, list, reverse=True, word=False, type=False):
        '''

        :param content: 处理后的文本
        :param list: idf文本库内容
        '''
        self.tf_idf, self.keylist, self.weight_list = self.get_tf_idf(content, list, reverse=reverse, word=word,
                                                                      type=type)
        self.simhash = self.simhash()

    def __str__(self):
        return str(self.simhash)

    def get_tf_idf(self, content, list, reverse=True, word=False, type=False):
        '''
                :param reverse: 为True则倒序排序，为False则顺序排序
                :param word: 为True则考虑词跨度，为False则不考虑
                :param type: 为True则考虑词性，为False则不考虑
                :return:
                '''
        tf_idf = simple_tfidf.tf_idf(content=content, list=list)
        tf_idf.count_tf_idf(reverse=reverse, word=word, type=type)
        count = 20  # 20 if len(tf_idf.tf_idf) >= 20 else 15
        keylist = []
        weight_list = []
        for word in tf_idf.tf_idf:
            if count < 0:
                break
            keylist.append(word[0])
            weight_list.append(word[1])
            count -= 1
        return tf_idf.tf_idf, keylist, weight_list

    def simhash(self):
        keyList = []
        count = 20  # if len(self.tf_idf) >= 20 else 15
        if len(self.tf_idf) < 20:  # 如果提取出的关键词少于10个
            return '00', None
        for j in self.tf_idf:
            word, weight = j[0], j[1]
            if count < 0:
                break
            feature = self.string_hash(word)
            temp = []
            for i in feature:
                if i == '1':
                    temp.append(weight)
                else:
                    temp.append(-weight)
            keyList.append(temp)
            count -= 1
        list1 = np.sum(np.array(keyList), axis=0)
        sim = ''
        for i in list1:
            if i > 0:
                sim = sim + '1'
            else:
                sim = sim + '0'
        return sim

    def string_hash(self, source):
        if source == "":
            return 0
        else:
            x = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** 128 - 1
            for c in source:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(source)
            if x == -1:
                x = -2
            x = bin(x).replace('0b', '').zfill(64)[-64:]

            return str(x)

    def hammingDis(self, com):
        t1 = '0b' + self.simhash
        t2 = '0b' + com.simhash
        n = int(t1, 2) ^ int(t2, 2)
        i = 0
        while n:
            n &= (n - 1)
            i += 1
        return i

    def count_cos(self, com):
        lis1 = self.simhash
        if not isinstance(com, str):  # 如果传进来的是simhash对象
            lis2 = com.simhash
        else:
            lis2 = com
        len_a = 0
        for i in range(len(lis1)):
            if lis1[i] == '1':
                len_a += 1
        len_a = math.sqrt(len_a)
        len_b = 0
        for i in range(len(lis2)):
            if lis2[i] == '1':
                len_b += 1
        len_b = math.sqrt(len_b)
        len_dot = 0
        for i in range(len(lis1)):
            if lis1[i] == '1' and lis2[i] == '1':
                len_dot += 1
        return len_dot / (len_a * len_b + 1)

    def matrix_dis(self, keys):
        start = time.time()
        keys = keys[:20]
        sim, k = 0, 1
        matrix = dict()
        x_max = np.max(self.weight_list)
        x_min = np.min(self.weight_list)
        count_list = dict()
        for i in range(len(self.keylist)):
            count_list[i] = (self.weight_list[i] - x_min) / (x_max - x_min)
        start2 = time.time()
        for i in range(len(self.keylist)):
            for j in range(len(keys)):
                start3 = time.time()
                matrix[(i, j)] = synonyms.compare(self.keylist[i], keys[j], seg=False) * (1 + count_list[i])
                # print(time.time()-start3)
        # print(time.time()-start2)
        while matrix:
            max_couple = max(matrix, key=matrix.get)
            i, j = max_couple[0], max_couple[1]
            k += 1
            simil = matrix.get(max_couple)
            sim += simil  # if simil > 0.2 else 0
            for t1 in range(len(keys)):
                if (i, t1) in matrix:
                    matrix.pop((i, t1))
            for t2 in range(len(self.keylist)):
                if t2 != i and (t2, j) in matrix:
                    matrix.pop((t2, j))
        # print("total compare time", time.time() - start)
        return sim / k

    # def matrix_dis_self(self, keys, W2V):
    #     start = time.time()
    #     keys = keys[:20]
    #     sim, k = 0, 1
    #     matrix = dict()
    #     x_max = np.max(self.weight_list)
    #     x_min = np.min(self.weight_list)
    #     count_list = dict()
    #     for i in range(len(self.keylist)):
    #         count_list[i] = (self.weight_list[i] - x_min) / (x_max - x_min)
    #     start2 = time.time()
    #     for i in range(len(self.keylist)):
    #         for j in range(len(keys)):
    #             start3 = time.time()
    #             matrix[(i, j)] = W2V.similarity(self.keylist[i], keys[j]) * (1 + count_list[i])
    #             # print(time.time()-start3)
    #     # print(time.time()-start2)
    #     while matrix:
    #         max_couple = max(matrix, key=matrix.get)
    #         i, j = max_couple[0], max_couple[1]
    #         k += 1
    #         simil = matrix.get(max_couple)
    #         sim += simil  # if simil > 0.2 else 0
    #         for t1 in range(len(keys)):
    #             if (i, t1) in matrix:
    #                 matrix.pop((i, t1))
    #         for t2 in range(len(self.keylist)):
    #             if t2 != i and (t2, j) in matrix:
    #                 matrix.pop((t2, j))
    #     # print("total compare time", time.time() - start)
    #     return sim / k
