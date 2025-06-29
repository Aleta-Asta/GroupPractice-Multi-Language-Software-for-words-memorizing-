from random import randint, random, shuffle
from time import time

import pandas as pd
from random import sample  # TODO 7
import matplotlib.pyplot as plt  # TODO 后续统计图表可能会使用，也可能不用

# TODO Warning fixed 1: 使用相对路径,不然在不同机器下运行的情况会有所差别,由于存储路径不同可能出现不能运行的情况.下面将对应数据保存至文件夹"Data"中
dt0 = pd.read_excel('Data/data.xlsx', index_col=0)
dt1 = pd.read_excel('Data/data.xlsx', sheet_name='Sheet1')
df1 = dt1
dt2 = pd.read_excel('Data/record.xlsx', index_col=0, sheet_name='Sheet1')
df2 = dt2
dt3 = pd.read_excel('Data/review.xlsx', index_col=0, sheet_name='Sheet1')
df3 = dt3
dt4 = pd.read_excel('Data/book.xlsx', index_col=0, sheet_name='Sheet1')
df4 = dt4


# 选择难度(从而实现对df1的替换)
def choose_level():
    n = int(input('请选择题目难度：(输入阿拉伯数字)\n'))
    df = dt0[dt0['level'] == n]
    return df


# 题目记录
class record_ac:
    def __init__(self, ac=0, wa=0):
        self.ac = ac  # 答对题目数
        self.wa = wa  # 答错题目数
        self.time = []  # 耗时

    def add_ac(self, t):
        self.ac += 1
        self.time.append(t)

    def add_wa(self, t):
        self.wa += 1
        self.time.append(t)


# 选取语言
def choose_language():
    mainlanguage = input('请输入主语言：')
    studylanguage = input('请输入学习语言：')
    return mainlanguage, studylanguage


# TODO Syntactic Sugar: Python 有内置的直接生成对应随机整数的函数 randint(a, b) 范围是 [a, b], 无需使用C++风格随机整数
# TODO new
# 生成一个随机浮点数
def generate_random_float(n):
    return random() * n


# 选取一个随机单词
def choose_word(n):
    id0 = generate_random_float(n)
    id00 = int(id0)
    # id00 = randint(0, n)
    word = df1.iloc[id00]
    id1 = int(word['id'])
    record1 = int(df2.iloc[id00]['star'])
    # if id0 <= id1 and id0 >= id1 - 1 + record1 / 3:
    # TODO 3 简化链式比较,使用Python风格的比较方式
    if id1 >= id0 >= id1 - 1 + record1 / 3:
        return word
    else:
        return choose_word(n)


# 生成题目 返回问题 选项 答案
def generate_question(word, mainlanguage, studylanguage, n):
    # i = min(int(random() * 3), 2)  # 随机选择题目类型
    # TODO 4 使用 Python 风格随机数可以提高效率
    i = randint(0, 2)
    letters = ['A', 'B', 'C', 'D']
    if i == 0:
        question = f"{word[mainlanguage]}的{studylanguage}是什么？"
        answer = word[studylanguage]
        # 先获取所有可能的选项，排除正确答案
        all_options = df1[studylanguage].tolist()
        all_options = [opt for opt in all_options if opt != answer]
        # 随机选取3个不重复的干扰项
        selection = [all_options[randint(0, len(all_options) - 1)] for _ in range(3)]
        # 防止抽到重复项
        selection = list(set(selection))
        while len(selection) < 3:
            opt = all_options[randint(0, len(all_options) - 1)]
            if opt not in selection:
                selection.append(opt)
        selection.append(answer)
        shuffle(selection)
        selection0 = {}
        for ii in range(4):
            selection0[letters[ii]] = selection[ii]
            if selection[ii] == answer:
                answer = letters[ii]
        return question, selection0, answer, i
    elif i == 1:
        question = f"{word[studylanguage]}的{mainlanguage}是什么？"
        answer = word[mainlanguage]
        all_options = df1[mainlanguage].tolist()
        all_options = [opt for opt in all_options if opt != answer]
        selection = [all_options[randint(0, len(all_options) - 1)] for _ in range(3)]
        selection = list(set(selection))
        while len(selection) < 3:
            opt = all_options[randint(0, len(all_options) - 1)]
            if opt not in selection:
                selection.append(opt)
        selection.append(answer)
        shuffle(selection)
        selection0 = {}
        for ii in range(4):
            selection0[letters[ii]] = selection[ii]
            if selection[ii] == answer:
                answer = letters[ii]
        return question, selection0, answer, i
    elif i == 2:
        end = True
        chosetotal = 0
        answer = 'B'
        word0 = ""
        while end:
            id0 = randint(0, n - 1)
            w = df1.iloc[id0][studylanguage]
            if w == word[studylanguage]:
                answer = 'A'
                word0 = w
                end = False
            else:
                chosetotal += 1
                if chosetotal >= n:
                    word0 = w
                    end = False
        question = f"判断{word[mainlanguage]}的{studylanguage}是否为{word0}？"
        return question, {'A': '是', 'B': '否'}, answer, i


# 答对题目
def success(word, score):
    id0 = int(word['id'])
    record1 = int(df2.iloc[id0]['star'])
    if record1 < 3:
        df2.at[id0, 'star'] = record1 + 1
        df1.at[id0, 'star'] = record1 + 1
    else:
        df2.at[id0, 'star'] = 3
        df1.at[id0, 'star'] = 3
        df2.at[id0, 'pass'] = 1
        global df3
        if id0 not in df3.index:
            df3.loc[id0] = df1.iloc[id0]
        df3.to_excel('Data/review.xlsx', index=True)
    df1.to_excel('Data/data.xlsx', index=True)
    df2.to_excel('Data/record.xlsx', index=True)
    score += int(word['level'])


# 答错题目
def fail(word, m, s):
    # id0 = int(word['id'])
    generate_question(word, m, s, len(df1))
    df3.loc[len(df3)] = word
    df3.to_excel('Data/review.xlsx', index=True)


# 添加到收藏本中
def add_book(word):
    if word['id'] not in df4['id']:
        df4.loc[len(df4)] = word
        df4.to_excel('Data/book.xlsx', index=True)


# 样例输出
def sample_output():
    # l = choose_language().split() # TODO 6 Bug-fixed: choose_language() 返回一个(str, str)元组而非一个长字符串,这里无需 split 下面直接用就好
    crt = choose_language()  # TODO 编译器报错模糊变量名,为避免以后弄混我将其改为 crt = current 表示临时借用的变量名
    with open('Data/output.txt', 'w', encoding='utf-8') as f:
        for i in range(10):
            result = generate_question(choose_word(len(df1)), crt[0], crt[1], len(df1))
            f.write(str(result))
            f.write('\n')


# 复习单词
def review_words(num):  # TODO 8 这里的形参 nn 是什么? 我暂时将其设定为了函数内参数,似乎是对于一个单词生成的题的个数,那么按照熟练度默认设为3暂且
    nn = 3
    global df3
    if len(df3) == 0:
        re = "没有需要复习的单词。"
        return re
    elif num > len(df3):
        re0 = "复习单词数超过可复习单词数，已将复习单词数修改为可复习单词最大数。"
        num = len(df3)
        return re0, review_words(num)  # TODO 我把 nn 改为类内变量此处便无需传入，否则参数缺少且无缺省值导致报错
    else:
        re_lst = []
        language = ['Chinese', 'English', 'Japanese']
        mainlanguage, studylanguage = sample(language, 2)  # TODO 7 报错 'function' 中找不到 'sample' 的原因其实是我们引用库的时候
        # TODO 7 写了 from random import random 这个时候 random = random.random, 想引用 random.sample 会引发名词空间冲突的同时也没有导入这个函数
        for i in range(num):
            word = df3.iloc[i]
            for j in range(nn):  # TODO 这里nn暂时是 0 ,我们需要核实其含义后再行改正。另外此变量的引用仅在此出现一次,若不重要可改为常数,也可以受外边传入实参使用.
                # TODO 5 Bug fixed: re is string type, use += instead of list-style .append method
                # TODO 5-2 看起来 re 想要返回的不是一个字符串,而是类似返回一些类似 TODO* 风格的能给四个变量赋值的内容,于是我们写成list或者元组都可以
                # todo 5-3 我又确认了一下,这里应该是希望返回一个很多个题的列表,每个元素是返回值的四元组,因此先初始化一个列表,为了避免变量及其类型混淆,改个名字
                # re.append(generate_question(word, mainlanguage, studylanguage, len(df4))
                re_lst.append(generate_question(word, mainlanguage, studylanguage, len(df4)))  # 这里最后会返回一个4元组,按照我们在 TODO* 中的方式赋值即可使用
        return re_lst


# 主函数
def main():
    global df1, df2, df3, df4
    print("欢迎使用单词学习系统！")
    mainlanguage, studylanguage = choose_language()
    record = record_ac()
    n = len(df1)
    t0 = time()
    while True:
        word = choose_word(n)
        question, selection, answer, i = generate_question(word, mainlanguage, studylanguage, n) # TODO*
        print(question)
        for key in selection:
            print(f"{key}: {selection[key]}")
        user_answer = input("请输入你的答案（A/B/C/D）：").strip().upper()
        if user_answer == answer:
            t = time()
            record.add_ac(t - t0)
            success(word, record.ac)
            print("答对了！")
        else:
            t = time()
            record.add_wa(t - t0)
            fail(word, mainlanguage, studylanguage)
            print(f"答错了，正确答案是：{answer}")
        bt = input("是否将此单词添加到收藏本？(y/n): ").strip().lower()
        if bt == 'y':
            add_book(word)
        cont = input("是否继续？(y/n): ").strip().lower()
        if cont != 'y':
            break
    print(f"答对题目数: {record.ac}, 答错题目数: {record.wa}, 耗时: {record.time}")


if __name__ == "__main__":
    main()
    # sample_output()  # Uncomment to generate sample output
    # review_words(5, 3)  # Uncomment to review words, adjust numbers as needed
