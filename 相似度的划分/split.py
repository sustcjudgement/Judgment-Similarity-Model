# encoding=utf-8
# import synonyms.jieba.posseg as psg
import jieba
import jieba.posseg as psg
jieba.load_userdict("family.txt")
jieba.load_userdict("finance.txt")
jieba.load_userdict("law.txt")
jieba.load_userdict("place.txt")
# jieba.load_userdict("vocab.txt")


# 对新判决文本的处理
def split_text(name, text):
    '''

    :param name: 被告名字
    :param text: 庭审过程
    :return: 返回分词结果
    '''
    global result  # 与被告有关
    global money_result  # 收受 受贿
    global sum_money_result  # 收受总数

    global get_money_result  # 骗取  贪污

    global get_sum_money_result  # 收受总数

    result = ""
    money_result = ""
    get_money_result = ""
    sum_money_result = ""
    get_sum_money_result = ""
    text_point = text
    text1 = jieba.cut(text)

    text = str(",".join(text1)).replace("，、", "")
    text = str(text).replace("，,", "")
    text = str(text).replace("、,", "")
    text = str(text).replace("。,", "")
    text = str(text).replace("；,", "")
    text = str(text).replace("：", "")
    text = str(text).replace(".", "")

    text_point = str(text_point).replace("、", "")
    text_point = str(text_point).replace("；", "")
    text_point = str(text_point).replace("：", "")
    text_point = str(text_point).replace(".", "")

    text = psg.cut(text)

    all = [(x.word, x.flag) for x in text if
           x.flag == "v" or x.flag == "vn" or x.flag == "n" or x.flag == "an" or x.flag == "nr" or
           x.flag == "ns" or x.flag == "nt" or x.flag == "m" or x.flag == "q" or x.flag == "t" or x.flag == "tg"]

    point = 0
    lenth = len(text_point)
    txt = ""

    sum_money_result_1 = ""  # 收受总数

    return_money_result = ""  # 收了就退
    another_return_money_result = ""  # 案发才退

    add_flag = 0  # 被告人名出现
    add_flag_2 = 0  # 一句话结束

    money = 0
    get_money = 0
    sum_money = 0
    return_money = 0
    another_return_money = 0
    for t in range(len(all)):
        message = all.pop(0)
        world = message[0]
        length = len(world)
        ty = message[1]
        if point + length > lenth:
            break
        while 1:
            if text_point[point] == '，':
                point += 1
                txt += " "
            if text_point[point] == '。':
                add_flag_2 = 1
                point += 1
                txt += " "
            if ty == 't' or t == 'tg':  #
                break
            # 对逗号和句号分格

            # 读取法院意见获取金额
            if world == name or world == "被告人":  # 判断句子中是否出现被告人 出现则认定相关
                add_flag = 1
                break
            if ty == 'nr':  # 去除人名字
                break
            if ty == 'ns':  # 去除地名
                break
            if world == "收受" or world == "索取":
                money = 1
            if world == "骗取" or world == "侵吞" or world == "占有":
                get_money = 1
            if world == "共计":
                sum_money = 1

            if money == 1:
                if ty == 'm':
                    sum_money = 0

                    if sum_money == 1:
                        sum_money_result = world
                    else:
                        money_result += world
            if get_money == 1:
                if ty == 'm':
                    get_money = 0
                    if sum_money == 1:
                        get_sum_money_result = world
                    else:
                        get_money_result += world

            # 精简庭审过程
            if add_flag == 1 and add_flag_2 == 1:
                add_flag = 0
                add_flag_2 = 0
                result += txt
                txt = ""

            new_str = text_point[point:point + length]
            if new_str == world:
                if ty == 'm':
                    point += length
                    break
                txt += new_str
                txt += ty
                txt += " "
                point += length
                break
            else:
                point += 1
                txt += " "
    return sum_money_result
