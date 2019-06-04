from tkinter import *
from tkinter.messagebox import showinfo


# 阮沛钧看这里就行了
# 调用方法在这个方法里  jin是 金额选项 0 为否  zhi是 职务选项 0 为否
# 只要返回职务正确形式的String即可  每行 以\n结束
def getmesage():
    user = user_text.get()  # 庭审过程
    jin = v.jine
    zhi = getzhi()
    print(jin)
    print(zhi)
    # 调用方法  传入 1.庭审过程 2.金额选项 3，职务选项
    result = '最终传入\n xxxxx\n'

    showinfo(title='最终结果', message=result)



#界面函数
#子元看这里
#该函数 共设置了 2个选项 1 个确认 注释有写 适当添加背景 调整大小即可

class View(Tk):
    jine=0
    def __init__(self):
        Tk.__init__(self)
        # 总界面
        self.title("案件相似度量模型")
        #界面大小
        self.geometry('400x220+400+100')
        # 金额选项
        L = ['考虑金额相似','不考虑金额相似']
        self.vS = StringVar(master=self)
        self.vS.set(L[1])

        self.oS = OptionMenu(self,self.vS,*L, command=self.cbOption)
        self.oS.place(x=40,y=80,width=120)


    def cbOption(self,wert):
        if wert=='考虑金额相似' :
            self.jine=1
        else:
            self.jine=0


def getzhi():
    wert=aS.get()
    if wert == '考虑职务相似':
        return 1
    else:
        return 0
#职务选项
v = View()
T = ['考虑职务相似', '不考虑职务相似']
aS = StringVar()
aS.set(T[1])
qS = OptionMenu(v,aS, *T )
qS.place(x=220, y=80, width=120)

#庭审输入框
l1 = Label(v, text="庭审过程文本：")  # 标签
l1.pack()  # 指定包管理器放置组件
user_text = Entry()  # 创建文本框
user_text.pack()







Button(v, text="寻找相似文本", command=getmesage).place(x=150,y=150,anchor='nw')#将模块的左上方固定在坐标（10，100）上
v.mainloop()
