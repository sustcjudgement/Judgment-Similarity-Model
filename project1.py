# -!- coding: utf-8 -!-
import synonyms.jieba as jieba
import openpyxl
import re


def distinguish(s):
    result = ""
    li = separate(s)
    temp = "0"
    sign2 = 0
    s = []
    for i in range(0, len(li)):
        x = re.search(r'(^[1-9]([0-9]+)?(\.[0-9]{1,9})?$)|(^(0){1}$)|(^[0-9]\.[0-9]([0-9])?$)', li[i])
        if x:
            lent = len(li)
            if i + 2 > lent:
                continue
            else:
                if "元" in li[i + 1]:
                    a = x.group()
                    if sign2 == 1:
                        s.append(float(a))
                        s.append(li[i + 1])
                    if "-" in temp or temp == "0":
                        temp = a + li[i + 1]
                    else:
                        b = separate(str(temp))
                        if b[1] == li[i + 1]:
                            temp = str(float(b[0]) + float(a)) + b[1]
                        else:
                            if "万元" in b[1]:
                                temp = str(float(b[0]) * 10000 + float(a)) + li[i + 1]
                            else:
                                temp = str(float(b[0]) + float(a) * 10000) + b[1]
        elif "。" in li[i]:
            temp = "-" + temp
            sign2 = 0
        elif "送" in li[i] or "收" in li[i] or "好处费" in li[i] or "赃款" in li[i]:
            sign2 = 1
    i = 0
    total = [0, "元"]
    while i <= len(s) - 2:
        if s[i + 1] == total[1]:
            total[0] = max(s[i], total[0])
        elif "万元" in s[i + 1]:
            if total[0] >= float(s[i]) * 10000:
                i = i + 2
                continue
            else:
                total[0] = s[i]
                total[1] = s[i + 1]
        elif "万元" in total[1]:
            if total[0] >= float(s[i]) * 10000:
                i = i + 2
                continue
            else:
                total[0] = s[i]
                total[1] = s[i + 1]
        i = i + 2
    result = str(str(total[0]) + str(total[1]))
    return result  # 返回金额


def separate(s):
    seg_list = list(jieba.cut(s, cut_all=False))
    return seg_list
