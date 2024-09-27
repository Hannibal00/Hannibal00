# -*- coding:utf-8 -*-
from sys import argv
import random
import time
from fractions import Fraction
import tkinter as tk
import tkinter.messagebox
window = tk.Tk()
window.title("计算器")
window.geometry("400x600")
# 消息处理函数
def show_info(context):
    tk.messagebox.showinfo(title="信息", message=context)

def show_warning(context):
    tk.messagebox.showwarning(title="警告", message=context)

def show_error(context):
    tk.messagebox.showerror(title="错误", message=context)
class exercise:
    def __init__(self, account=100, range=10):
        self.account = account
        self.range = range

    # 生成题目
    def makeExe(self):
        localtime = time.asctime(time.localtime(time.time()))
        # 清理文件内容
        with open("Exercise.txt", 'w') as exercise_file:
            exercise_file.write("题目数量 ： " + str(self.account) + "\t时间 ：" + localtime + "\n")
            exercise_file.close()
        with open("Answer.txt", 'w') as Answer_file:
            Answer_file.close()

        que_order = 0
        repeat = testRepeat()
        makeQue = randomMake(repeat, self.range)
        # 生成account道题
        while que_order < self.account:
            choose2_3 = 2 + random.randint(0, 1)
            # 两个数的运算题生成
            if choose2_3 == 2:
                makeQue.question_2bits(que_order + 1)
            # 三个数的运算题生成
            elif choose2_3 == 3:
                makeQue.question_3bits(que_order + 1)
            que_order = que_order + 1

    # 核对答案
    def confirmExe(self, exeFile, userFile):
        corrctQue = []  # 记录用户的错题和对题
        wrongQue = []
        try:
            with open(exeFile) as exeFile:  # 读取题目文件
                with open(userFile) as userFile:  # 读取用户文件
                    orderLine = 1  # 记录核对的第几道题
                    lineExe = exeFile.__next__()
                    fracAcc = fracHandle()
                    for lineExe in exeFile:  # 遍历题目
                        lineExe = lineExe.strip()
                        div = lineExe.split(" ")
                        # 两个数的题目
                        if len(div) == 5:
                            frac1 = fracAcc.strToFrac(div[1])
                            frac2 = fracAcc.strToFrac(div[3])
                            rightAnswer = fracAcc.fracAccount(frac1, frac2, div[2])
                            rightAnswer = fracAcc.fracToStr(rightAnswer)
                        # 三个数
                        elif len(div) == 7:
                            # 如果式子中有括号
                            if '(' in lineExe:
                                for locate in range(7):
                                    # 如果式子中有括号
                                    if '(' in div[locate]:
                                        # 如果括号在左边
                                        if locate == 1:
                                            leftFrac = fracAcc.strToFrac(div[1].replace("(", ""))
                                            rightFrac = fracAcc.strToFrac(div[3].replace(")", ""))
                                            thirdFrac = fracAcc.strToFrac(div[5])
                                            firstSum = fracAcc.fracAccount(leftFrac, rightFrac, div[2])
                                            rightAnswer = fracAcc.fracToStr(
                                                fracAcc.fracAccount(firstSum, thirdFrac, div[4]))
                                        else:
                                            leftFrac = fracAcc.strToFrac(div[3].replace("(", ""))
                                            rightFrac = fracAcc.strToFrac(div[5].replace(")", ""))
                                            thirdFrac = fracAcc.strToFrac(div[1])
                                            firstSum = fracAcc.fracAccount(leftFrac, rightFrac, div[4])
                                            rightAnswer = fracAcc.fracToStr(
                                                fracAcc.fracAccount(thirdFrac, firstSum, div[2]))
                            # 如果式子没括号
                            else:
                                leftFrac = fracAcc.strToFrac(div[1])
                                rightFrac = fracAcc.strToFrac(div[3])
                                thirdFrac = fracAcc.strToFrac(div[5])
                                if (div[2] == '+' or div[2] == '-') and (div[4] == '*' or div[4] == "÷"):
                                    firstSum = fracAcc.fracAccount(rightFrac, thirdFrac, div[4])
                                    rightAnswer = fracAcc.fracToStr(fracAcc.fracAccount(leftFrac, firstSum, div[2]))
                                else:
                                    firstSum = fracAcc.fracAccount(leftFrac, rightFrac, div[2])
                                    rightAnswer = fracAcc.fracToStr(fracAcc.fracAccount(firstSum, thirdFrac, div[4]))
                        else:
                            show_info("题目出错。")
                        try:
                            userAnswer = userFile.__next__().split(' ', 2)
                            # 如果用户答案还存在的话
                            if userAnswer[0] != '\n':
                                if (userAnswer[1].strip() == rightAnswer.strip()):
                                    corrctQue.append(orderLine)
                                else:
                                    wrongQue.append(orderLine)
                            # 用户答案已空
                            else:
                                show_info("同学，你第" + str(orderLine) + "题未完成。")
                                wrongQue.append(orderLine)
                            orderLine = orderLine + 1
                        except StopIteration:
                            show_info("同学，你第" + str(orderLine) + "题未完成。")
                            wrongQue.append(orderLine)
                            orderLine = orderLine + 1

                    show_info("批卷完毕，答题情况如下：")
                    show_info("Correct: " + str(len(corrctQue)))
                    show_info(str(corrctQue))
                    show_info("Wrong: " + str(len(wrongQue)))
                    show_info(str(wrongQue))

                    # 答题情况写入Grade.txt
                    with open("Grade.txt", 'w') as grade_file:
                        grade_file.write("Correct: " + str(len(corrctQue)))
                        grade_file.write(str(corrctQue) + '\n')
                        grade_file.write("Wrong: " + str(len(wrongQue)))
                        grade_file.write(str(wrongQue) + '\n')
        except FileNotFoundError:
            show_info("找不到文件！请重新输入！")

    def confirm_4bit(self):
        self

class randomMake:
    def __init__(self, repeat, range):
        self.repeat = repeat
        self.range = range

    # 生成两个数的题目
    def question_2bits(self, order):
        while True:
            frac_Handle = fracHandle()
            sign = self.random_sign()
            numberList = []
            signList = []
            firstNum = self.random_frac()
            secondNum = self.random_frac()  # 生成两个分数

            question = ''
            rightAnswer = ''
            numberList.append(str(firstNum) + ',' + str(secondNum))  # 将生成的数字和符号放在字典同一个位置
            signList.append(sign)
            if (self.repeat.isRepeat(numberList, signList) == True):  # 检测此组数字和运算符是否重复
                rightAnswer = frac_Handle.fracAccount(firstNum, secondNum, sign)
                if rightAnswer != False:
                    rightAnswer = fracHandle.fracToStr(self, rightAnswer)
                    question = str(order) + ". " + frac_Handle.fracToStr(
                        firstNum) + " " + sign + " " + frac_Handle.fracToStr(
                        secondNum) + " ="
                else:
                    continue
            else:
                continue
            # 将问题写入 Exercise.txt中，将答案写入Answer.txt中
            with open("Exercise.txt", 'a') as exercise_file:
                exercise_file.write(question + "\n")
                exercise_file.close()
            with open("Answer.txt", 'a') as Answer_file:
                Answer_file.write(str(order) + ". " + rightAnswer + "\n")
                Answer_file.close()
            break

    # 生成三个数的题目
    def question_3bits(self, order):
        while True:
            frac_Handle = fracHandle()
            # 生成相应的数字和符号
            sign1 = self.random_sign()
            sign2 = self.random_sign()
            numberList = []
            signList = []
            firstNum = self.random_frac()
            secondNum = self.random_frac()
            thirdNum = self.random_frac()

            question = ''
            rightAnswer = ''
            numberList.append(str(firstNum) + ',' + str(secondNum) + ',' + str(thirdNum))
            signList.append(sign1 + ',' + sign2)
            if self.repeat.isRepeat(numberList, signList) == True:  # 检测是否重复
                brackets = random.randint(0, 2)  # 随机生成括号的位置
                # 不生成括号
                if (brackets == 0):
                    question = str(order) + ". " + frac_Handle.fracToStr(
                        firstNum) + " " + sign1 + " " + frac_Handle.fracToStr(
                        secondNum) + " " + sign2 + " " + frac_Handle.fracToStr(thirdNum) + " ="
                    # 如果前面是加号和减号而后面不是
                    if (sign1 == '+' or sign1 == '-') and (sign2 == '*' or sign2 == '÷'):
                        firstSum = frac_Handle.fracAccount(secondNum, thirdNum, sign2)
                        if firstSum != False:
                            rightAnswer = frac_Handle.fracAccount(firstNum, firstSum, sign1)
                            if rightAnswer != False:
                                rightAnswer = frac_Handle.fracToStr(rightAnswer)
                            else:
                                continue
                        else:
                            continue
                    # 其他情况
                    else:
                        firstSum = frac_Handle.fracAccount(firstNum, secondNum, sign1)
                        if firstSum != False:
                            rightAnswer = frac_Handle.fracAccount(firstSum, thirdNum, sign2)
                            if rightAnswer != False:
                                rightAnswer = frac_Handle.fracToStr(rightAnswer)
                            else:
                                continue
                        else:
                            continue
                # 左边加一个括号：
                elif (brackets == 1):  # 左边加括号
                    question = str(order) + ". (" + frac_Handle.fracToStr(
                        firstNum) + " " + sign1 + " " + frac_Handle.fracToStr(
                        secondNum) + ") " + sign2 + " " + frac_Handle.fracToStr(thirdNum) + " ="
                    firstSum = frac_Handle.fracAccount(firstNum, secondNum, sign1)
                    if firstSum != False:
                        rightAnswer = frac_Handle.fracAccount(firstSum, thirdNum, sign2)
                        if rightAnswer != False:
                            rightAnswer = frac_Handle.fracToStr(rightAnswer)
                        else:
                            continue
                    else:
                        continue
                # 右边加括号
                else:
                    question = str(order) + ". " + frac_Handle.fracToStr(
                        firstNum) + " " + sign1 + " (" + frac_Handle.fracToStr(
                        secondNum) + " " + sign2 + " " + frac_Handle.fracToStr(thirdNum) + ") ="

                    firstSum = frac_Handle.fracAccount(secondNum, thirdNum, sign2)
                    if firstSum != False:
                        rightAnswer = frac_Handle.fracAccount(firstNum, firstSum, sign1)
                        if rightAnswer != False:
                            rightAnswer = frac_Handle.fracToStr(rightAnswer)
                        else:
                            continue
                    else:
                        continue

                with open("Exercise.txt", 'a') as exercise_file:
                    exercise_file.write(question + "\n")
                    exercise_file.close()
                with open("Answer.txt", 'a') as Answer_file:
                    Answer_file.write(str(order) + ". " + rightAnswer + "\n")
                    Answer_file.close()
                break
            # 运算式子重复
            else:
                continue

    # 生成四个数的题目
    def question_4bits(self, order):
        signList = []
        numberList = []
        braLen = 0
        signLenth = 0
        mustSign = 0
        frac_handle = fracHandle()

        # 生成三个符号
        while (signLenth < 3):
            makeBra = random.randint(0, 3)
            # 生成左括号
            if mustSign == 1 or (makeBra > 1):
                signList.append(self.random_sign())
                signLenth = signLenth + 1
                mustSign = 0
            elif makeBra == 0:
                signList.append('(')
                braLen = braLen + 1
                mustSign = 1
            elif makeBra == 1:
                if braLen != 0:
                    signList.append(')')
                    braLen = braLen - 1
                    mustSign = 0
                else:
                    continue
        while braLen > 0:
            signList.append(')')
            braLen = braLen - 1
        for i in range(4):
            numberList.append(frac_handle.fracToStr(self.random_frac()))
        show_info(numberList)
        show_info(signList)
        numberNext = True
        question = str(order) + '. '
        n = 0
        i = 0
        while n < len(numberList) or i < len(signList):
            if n < len(numberList):
                number = numberList[n]
            if i < len(signList):
                sign = signList[i]
            if sign == '(':
                question += str(sign)
                i += 1
            elif numberNext == True:
                question += str(number)
                numberNext = False
                n += 1
                show_info(n)
            elif sign == ')':
                question += str(sign) + ' '
                i += 1
            else:
                question += ' ' + str(sign) + ' '
                numberNext = True
                i += 1
        show_info(question)

    # 随机生成符号
    def random_sign(self):
        randomSign = random.randint(0, 3)
        if randomSign == 0:
            sign = '+'
        elif randomSign == 1:
            sign = '-'
        elif randomSign == 2:
            sign = '*'
        else:
            sign = '÷'
        return sign

    # 随机生成分数
    def random_frac(self):
        while (True):
            numer = random.randint(0, self.range)  # 分子
            dno = random.randint(1, self.range)  # 分母
            Num = Fraction(numer, dno)
            if Num:
                break
        return Num

class fracHandle:
    def __init__(self):
        self

    # 分数变为字符串
    def fracToStr(self, fraction):
        numer = fraction.numerator
        denom = fraction.denominator
        if denom == 0:
            return False
        INT = int(numer / denom)
        LEFT = numer % denom
        if LEFT == 0 or denom >= numer:
            return str(Fraction(numer, denom))
        else:
            return str(INT) + '\'' + str(Fraction(LEFT, denom))

    # 字符串变为分数
    def strToFrac(self, string):
        # 如果是带分数
        if '\'' in string:
            fullFrac = string.split('\'')
            INT = int(fullFrac[0])
            NUMERATOR = int((fullFrac[1].split('/'))[0])
            DENOMINATOR = int((fullFrac[1].split('/'))[1])
            return Fraction((INT * DENOMINATOR + NUMERATOR), DENOMINATOR)
        elif '/' in string:
            NUMERATOR = int((string.split('/'))[0])
            DENOMINATOR = int((string.split('/'))[1])
            return Fraction(NUMERATOR, DENOMINATOR)
        else:
            return Fraction(int(string), 1)

    # 分数的计算
    def fracAccount(self, frac1, frac2, sign):
        if (sign == '+'):
            return frac1 + frac2
        elif (sign == '-'):
            if frac1 < frac2:
                return False
            else:
                return frac1 - frac2
        elif (sign == '*'):
            return frac1 * frac2
        else:
            if frac2 == 0:
                return False
            else:
                return frac1 / frac2

class testRepeat:
    def __init__(self):
        self.oldNumber = {}  # 已有的数字组合
        self.signDic = {}  # 已有的符号组合

    # 检测是否式子重复
    def isRepeat(self, numberList, signList):
        numberList.sort()
        signList.sort()
        if self.oldNumber:
            for key, value in self.oldNumber.items():
                if value == numberList and self.signDic[key] == signList:
                    return False
            self.oldNumber[key + 1] = numberList
            self.signDic[key + 1] = signList
        else:
            self.oldNumber[0] = numberList
            self.signDic[0] = signList
        return True

# 如果需要生成题目
def generateProblems():
    if (num_entry.get()) and (range_entry.get()):
        # 获取题目的数量和范围
        userRange = int(range_entry.get())
        userAccount = int(num_entry.get())
        mathExercise = exercise(userAccount, userRange)
        mathExercise.makeExe()
        show_info("四则计算题已生成完毕，请查看Exercise文件并完成题目")
    else:
        show_warning("请输入题目数量和数值范围")

def correctProblems():
    # 如果需要对答案
    if (problem_file.get()) and (answer_file.get()):
        mathExercise = exercise()
        exerciseFile = problem_file.get()  # 获取题目文件
        answerFile = answer_file.get()  # 获取用户需要核对的文件
        mathExercise.confirmExe(exerciseFile, answerFile)
        show_info("同学，您的答题情况已存入Grade.txt中")
    else:
        show_info("请输入题目数量和数值范围")

# 题目数量输入
tk.Label(window, text="题目数量:").pack(pady=5)
num_entry = tk.Entry(window)
num_entry.pack(pady=5)

# 数值范围输入
tk.Label(window, text="数值范围:").pack(pady=5)
range_entry = tk.Entry(window)
range_entry.pack(pady=5)

# 生成按钮
generate_button = tk.Button(window, text="生成题目", command=generateProblems)
generate_button.pack(pady=20)

# 题目文件
tk.Label(window, text="题目文件:").pack(pady=5)
problem_file = tk.Entry(window)
problem_file.pack(pady=5)

# 答案文件
tk.Label(window, text="答案文件:").pack(pady=5)
answer_file = tk.Entry(window)
answer_file.pack(pady=5)

# 生成按钮
grade_button = tk.Button(window, text="批阅题目", command=correctProblems)
grade_button.pack(pady=20)

#开启主循环
window.mainloop()

