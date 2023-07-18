import os
import random


def copyFile(goalFile, copiedFile):
    with open(copiedFile, 'r') as file:
        temp = file.read()
    with open(goalFile, 'w') as file:
        file.write(temp)


def main():
    testCount = input('scan the number of tests: ')
    for i in range(int(testCount)):
        os.system('python dataBuilder.py')
        print('data' + str(i) + ' have got and test is going')
        copyFile('datas/data' + str(i) + '.txt', 'stdin.txt')
        os.system('.\\datainput_student_win64.exe | java -jar code.jar > stdout.txt')
        copyFile('outputs/output' + str(i) + '.txt', 'stdout.txt')

        if i == 0:
            model = 'w'
        else:
            model = 'a'
        with open('log.txt', model) as file:
            file.write('test data' + str(i) + ':\n')

        os.system('python judge_correct.py >> log.txt')
        print('test' + str(i) + ' have finished')

# 在自动评测机中运行main.py 让数据写入文件stdin.txt中
# os.system('python main.py')
# 调投喂包运行代码跑出结果, 输出到stdout.txt
# os.system('.\datainput_student_win64.exe | java -jar code.jar > stdout.txt')
# isRight = judgeCorrect()
# judgeCorrect()


if __name__ == '__main__':
    main()


