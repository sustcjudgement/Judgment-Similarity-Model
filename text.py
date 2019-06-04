case_his = r'C:\Users\kingway\Desktop\判决书分词\tf_idf.txt'
predeal = open(case_his, 'r')
data = predeal.readlines()
for i in data:
    data = i.split(' ')
    print(data)
    data[1] = data[1].replace('\n', '')
    print(data)
