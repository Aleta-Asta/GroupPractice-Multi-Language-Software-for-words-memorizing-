from random import randint, random, shuffle, sample
from time import time
from datetime import datetime
# TODO 2: 使用datetime库获取当前时间,以便于后续数据记录
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文黑体
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
import os
# 设置工作目录为当前脚本所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# TODO Warning fixed 1: 使用相对路径,不然在不同机器下运行的情况会有所差别,由于存储路径不同可能出现不能运行的情况.下面将对应数据保存至文件夹"Data"中
class VocabularyLearningSystem:
    class RecordAC:
        def __init__(self):
            self.ac = 0  # 答对题目数
            self.wa = 0  # 答错题目数
            self.time = []  # 耗时记录
            self.is_correct = []  # 新增：记录每题正误
            self.data=datetime.today().strftime('%Y-%m-%d')  # 新增：记录数据生成时间

        def add_ac(self, t):
            self.ac += 1
            self.time.append(t)
            self.is_correct.append(True)  # 正确

        def add_wa(self, t):
            self.wa += 1
            self.time.append(t)
            self.is_correct.append(False)  # 错误

    def __init__(self):
        # 初始化数据
        self.df0 = pd.read_excel('Data/data.xlsx', index_col=0)
        self.df1 = pd.read_excel('Data/data.xlsx', sheet_name='Sheet1')
        self.df2 = pd.read_excel('Data/record.xlsx', index_col=0, sheet_name='Sheet1')
        self.df3 = pd.read_excel('Data/review.xlsx', index_col=0, sheet_name='Sheet1')
        self.df4 = pd.read_excel('Data/book.xlsx', index_col=0, sheet_name='Sheet1')
        self.df5 = pd.read_excel('Data/day_record.xlsx',index_col=0 ,sheet_name='Sheet1')
        self.mainlanguage = None
        self.studylanguage = None
        self.record = self.RecordAC()
        self.current_level_df = None

    def choose_level(self,n):
        """设置题目难度等级"""
        self.current_level_df = self.df0[self.df0['level'] == n]
        return self.current_level_df

    def set_languages(self):
        """设置学习语言"""
        self.mainlanguage = input('请输入主语言：')
        self.studylanguage = input('请输入学习语言：')

    def _choose_word(self):
        """内部方法：根据记忆曲线选择单词"""
        n = len(self.df1)
        id0 = n*random()
        id00 = int(id0)
        # id00 = randint(0, n)
        word = self.df1.iloc[id00]
        id1 = int(word['id'])
        record1 = int(self.df2.iloc[id00]['star'])
        # if id0 <= id1 and id0 >= id1 - 1 + record1 / 3:
        # TODO 3 简化链式比较,使用Python风格的比较方式
        if id1 >= id0 >= id1 - 1 + record1 / 3:
            return word
        else:
            return self._choose_word()

    def _generate_options(self, correct_answer, language):
        """生成选择题选项"""
        options = [correct_answer]
        while len(options) < 4:
            random_word = self.df1.sample(1).iloc[0]
            candidate = random_word[language]
            if candidate not in options:
                options.append(candidate)
        shuffle(options)
        return {
            'A': options[0],
            'B': options[1],
            'C': options[2],
            'D': options[3]
        }, chr(65 + options.index(correct_answer))

    def generate_question(self):
        """生成题目"""
        word = self._choose_word()
        question_type = randint(0, 2)

        if question_type == 0:  # 外译中
            question = f"{word[self.mainlanguage]}的{self.studylanguage}是什么？"
            options, answer = self._generate_options(word[self.studylanguage], self.studylanguage)
        elif question_type == 1:  # 中译外
            question = f"{word[self.studylanguage]}的{self.mainlanguage}是什么？"
            options, answer = self._generate_options(word[self.mainlanguage], self.mainlanguage)
        else:  # 判断题
            random_word = self.df1.sample(1).iloc[0]
            is_correct = random() > 0.5
            target_word = word if is_correct else random_word
            question = f"判断{target_word[self.mainlanguage]}的{self.studylanguage}是否为{word[self.studylanguage]}？"
            options = {'A': '是', 'C': '否'}
            answer = 'A' if is_correct else 'C'

        return question, options, answer, word

    def handle_correct_answer(self, word):
        """处理正确答案"""
        idx = word.name
        current_star = self.df2.loc[idx, 'star']
        if current_star < 3:
            self.df2.loc[idx, 'star'] += 1
        self._save_progress()

    def handle_wrong_answer(self, word):
        """处理错误答案"""
        idx = word.name
        new_row = self.df1.loc[[idx]]
        if self.df3.empty:
            self.df3 = new_row
        else:
            self.df3 = pd.concat([self.df3, new_row])
        self._save_progress()

    def _save_progress(self):
        """保存学习进度"""
        self.df1.to_excel('Data/data.xlsx', index=True)
        self.df2.to_excel('Data/record.xlsx', index=True)
        self.df3.to_excel('Data/review.xlsx', index=True)
        self.df4.to_excel('Data/book.xlsx', index=True)

    def add_to_book(self, word):
        """添加到收藏本"""
        if word.name not in self.df4.index:
            new_row = self.df1.loc[[word.name]]
            if self.df4.empty:
                self.df4 = new_row
            else:
                self.df4 = pd.concat([self.df4, new_row])
            self._save_progress()

    def review(self):
        """复习功能"""
        if self.df3.empty:
            print("没有需要复习的单词！")
            return

        for idx, row in self.df3.iterrows():
            print(f"\n复习单词：{row[self.mainlanguage]} - {row[self.studylanguage]}")
            # 可以在此处添加复习逻辑

    def show_stats(self):
        """显示学习统计"""
        total_time = sum(self.record.time)
        print(f"\n学习统计：")
        print(f"正确题目：{self.record.ac}题")
        print(f"错误题目：{self.record.wa}题")
        print(f"总耗时：{total_time:.2f}秒")
        print(f"平均答题时间：{total_time / len(self.record.time):.2f}秒")

    def update_day_stats(self):
        """更新每日统计"""
        today = datetime.today().strftime('%Y-%m-%d')
        if today not in self.df5.index:
            self.df5.loc[today] = [self.record.ac+self.record.wa,self.record.ac, self.record.wa ]
        else:
            self.df5.loc[today, 'ac'] += self.record.ac
            self.df5.loc[today, 'wa'] += self.record.wa
            self.df5.loc[today, 'total'] += self.record.ac + self.record.wa
        self.df5.to_excel('Data/day_record.xlsx', index=True)

    def show_day_stats(self):
        """显示每日统计折线图"""
        if self.df5.empty:
            print("暂无每日统计数据！")
            return
        df = self.df5.copy()
        df = df.sort_index()
        dates = df.index.tolist()
        ac = df['ac'].tolist()
        wa = df['wa'].tolist()
        total = [a + w for a, w in zip(ac, wa)]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, ac, marker='o', label='正确(ac)')
        plt.plot(dates, wa, marker='o', label='错误(wa)')
        plt.plot(dates, total, marker='o', label='总答题数')
        plt.xlabel('日期')
        plt.ylabel('题目数')
        plt.title('每日答题统计')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    def run(self):
        """主运行循环"""
        print("欢迎使用智能单词学习系统！")
        self.set_languages()
        n=int(input("请选择题目难度等级（1-3）："))
        self.choose_level(n)

        while True:
            start_time = time()
            question, options, answer, word = self.generate_question()
            print(f"\n题目：{question}")
            for k, v in options.items():
                print(f"{k}. {v}")
            user_input = input("请输入答案：").upper()
            time_used = time() - start_time
            if user_input == answer:
                self.record.add_ac(time_used)
                self.handle_correct_answer(word)
                print("✅ 正确！")
            else:
                self.record.add_wa(time_used)
                self.handle_wrong_answer(word)
                print(f"❌ 错误，正确答案是：{answer}")

            # 收藏功能
            if input("添加到收藏本？(y/n) ").lower() == 'y':
                self.add_to_book(word)

            # 复习提示
            if len(self.df3) >= 5:
                print("\n您有5个以上需要复习的单词！")
                self.review()

            if input("继续学习？(y/n) ").lower() != 'y':
                self.show_stats()
                break
        self.update_day_stats()
        # 绘图部分
        x = list(range(1, len(self.record.time) + 1))
        y = self.record.time
        is_correct = self.record.is_correct
        plt.figure(figsize=(8, 4))
        # 正确题目
        x_ac = [i+1 for i, c in enumerate(is_correct) if c]
        y_ac = [y[i] for i, c in enumerate(is_correct) if c]
        plt.scatter(x_ac, y_ac, color='green', label='正确', zorder=3)
        # 错误题目
        x_wa = [i+1 for i, c in enumerate(is_correct) if not c]
        y_wa = [y[i] for i, c in enumerate(is_correct) if not c]
        plt.scatter(x_wa, y_wa, color='red', label='错误', zorder=3)
        # 折线
        plt.plot(x, y, color='blue', alpha=0.5, zorder=2)
        plt.xlabel('题目序号')
        plt.ylabel('用时（秒）')
        plt.title('每题用时折线图')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        self.show_day_stats()


if __name__ == "__main__":
    system = VocabularyLearningSystem()
    system.run()
