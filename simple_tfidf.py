import re
import math
import chardet
import codecs


def fileencodeing(file_path):  # 判断文本的编码方式
    file = open(file_path, 'rb')
    buf = file.read(20)
    res = chardet.detect(buf)
    file.close()
    return res['encoding']


def convertencoding(file_path):  # 文本编码转换
    encoding = fileencodeing(file_path)
    if encoding != 'utf-8' and encoding != 'ascii':
        with codecs.open(file_path, 'r', encoding) as sourceFile:
            contents = sourceFile.read()
        with codecs.open(file_path, 'w', 'utf-8') as targetFile:
            targetFile.write(contents)


def judge(n):
    return len(n) > 2


def sperate(string):  # 将词语词性和中文分离
    return "".join(i for i in string if ord(i) < 256)


def load_stopwords(file_path):
    stopwords = []
    file = open(file_path, 'r')
    data = file.readlines()
    for word in data:
        stopwords.append(word.strip())
    return stopwords


class tf_idf:

    def __init__(self, content=None, list=None, iter_range=100):
        '''
        :param iter_range: 扫描文本库的文本数
        :param list: 文本库的内容
        :param content: 文本内容
        '''
        self.iter_range = iter_range
        self.tf = {}
        self.idf = {}
        self.tf_idf = {}
        self.content = content
        self.list = list
        self.word_dis = {}
        self.word_type = {}

    def count_tf(self):  # 计算文本的tf值
        self.tf.clear()
        length = len(self.content)  # 文本总词数
        for word in self.content:  # 统计词频
            if word in self.tf:
                self.tf[word] += 1
            else:
                self.tf[word] = 1
        for i in self.tf:
            tf = float(self.tf.get(i) / length)
            self.tf[i] = tf * 20

    def count_word_type(self):  # 获取词的词性,并提出词性，返回纯文本
        stopwords = load_stopwords('stopwords.txt')
        word_type = {}
        new_content = []
        content = self.content.split(' ')
        content = list(filter(None, content))  # 去除空字符
        for words in content:
            ty = sperate(words)
            if ty:  # 如果有词性
                word = words.split(ty)[0]
            else:
                word = words
            if len(word) < 2:
                continue
            if word in stopwords:
                continue
            new_content.append(word)  # 将词语添加到新的content中
            if word not in word_type:
                word_type[word] = ty
            else:
                continue
        content.clear()
        self.content = new_content
        self.word_type = word_type

    def open_file(self):  # 打开文本并保存在list中
        content_list = []
        for i in range(100, 100+self.iter_range):
            convertencoding('lib\\text{}.txt'.format(i))
            file = open('lib\\text{}.txt'.format(i), 'rb')
            content = file.read().decode()
            content_list.append(content)
            file.close()
        return content_list

    def count_idf(self):  # 计算文本的idf值
        self.idf.clear()
        if not self.list:
            content_list = self.open_file()
        else:
            content_list = self.list
        for word in self.tf:
            count = 0
            for i in content_list:
                if re.search(word, i):
                    count += 1
            idf = math.log10(self.iter_range / (count + 1))
            self.idf[word] = idf * 20

    def count_word_dis(self):  # 计算词跨度权重
        # 词跨度权重 = last-first+1 /sum
        word_dis = {}
        for word in self.content:
            last = 0
            if word in word_dis:  # 词语重复出现
                continue
            for i in range(len(self.content)):
                if word == self.content[i] and word not in word_dis:  # 如果是第一次出现
                    word_dis[word] = 2 - i
                elif word == self.content[i]:  # 如果已经出现过，更新最后出现的位置
                    last = i
            word_dis[word] = (word_dis[word] + last) / len(self.content)
        self.word_dis = word_dis

    def count_tf_idf(self, reverse=True, word=False, type=False):  # 计算文本的tf_idf值
        '''

        :param reverse: 为True则倒序排序，为False则顺序排序
        :param word: 为True则考虑词跨度，为False则不考虑
        :param type: 为True则考虑词性，为False则不考虑
        :return:
        '''
        self.count_word_type()
        if not self.tf:  # 如果tf为空
            self.count_tf()
        if not self.idf:  # 如果idf为空
            self.count_idf()
        if word:
            self.count_word_dis()
        idf = {}
        for words in self.tf:
            if word:
                idf[words] = float(self.tf.get(words)) * float(self.idf.get(words)) * float(self.word_dis.get(words))
            else:
                idf[words] = float(self.tf.get(words)) * float(self.idf.get(words))
        if type:
            for words in idf:
                if self.word_type.get(words) == 'n':
                    idf[words] *= 1.2
                elif self.word_type.get(words) == 'v':
                    idf[words] *= 0.6
        self.tf_idf = sorted(idf.items(), key=lambda x: x[1], reverse=reverse)
        # print(self.tf_idf[:21])
