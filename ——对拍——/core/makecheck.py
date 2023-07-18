'''
Author: ltt
Date: 2023-02-26 21:02:23
LastEditors: ltt
LastEditTime: 2023-03-06 10:46:18
FilePath: makecheck.py
'''


def generate(path, testnum=10):
    import random
    TERMS = 2
    FACTORS = 2
    VARS = ["", "y", "z", "x"]
    FUNCNUM = 3
    NORMALS = 3
    FUNCNAME = ["", "f", "g", "h"]
    TRIFUNC = ["sin", "cos"]
    funcNormal = [0, 0, 0, 0]
    with open(path, "w", encoding="utf-8") as fout:
        def setIndex():
            index = random.randint(0, 4)
            fout.write("**")
            # print("**",end = "")
            fout.write(str(index))
            # print(str(index),end = "")

        def setSigned():
            sign = random.randint(1, 2)
            if sign == 1:
                fout.write("-")
                # print("-",end = "")
            else:
                fout.write("+")
                # print("+",end = "")

        def exprFactor(vars, dep, yn=0):
            for i in range(1, termsOut + 1):
                setSigned()
                factors = random.randint(1, FACTORS)
                for j in range(1, factors + 1):
                    if j != 1:
                        fout.write("*")
                        # print("*", end = "")
                    type = random.randint(1, 8)
                    while ((type == 3 or type == 4 or type >= 5) and dep > 2) or (
                            type >= 5 and (funcNum == 0 or yn == 0)):
                        type = random.randint(1, 8)
                    if type == 1:
                        setSigned()
                        # print('0'*leadingzero,end="")
                        fout.write(str(random.randint(0, 20)))
                        # print(str(random.randint(0,20)),end = "")
                    if type == 2:
                        var = random.randint(1, vars)
                        fout.write(VARS[var])
                        # print(VARS[var],end = "")
                        setIndex()
                    if type == 3:
                        fout.write("(")
                        # print("(",end = "")
                        exprFactor(vars, max(dep + 1, 2), yn)
                        fout.write(")")
                        # print(")",end = "")
                        setIndex()
                    if type == 4:
                        fout.write(TRIFUNC[random.randint(0, 1)])
                        fout.write("((")
                        exprFactor(vars, max(dep + 1, 2), yn)
                        fout.write("))")
                        setIndex()
                    if type >= 5:
                        func = random.randint(1, funcNum)
                        fout.write(FUNCNAME[func])
                        fout.write("(")
                        for k in range(1, funcNormal[func] + 1):
                            if k != 1:
                                fout.write(",")
                            fout.write("(")
                            exprFactor(vars, max(dep + 1, 2), 0)
                            fout.write(")")
                        fout.write(")")

        while testnum != 0:
            testnum = testnum - 1
            termsOut = random.randint(1, TERMS)
            funcNum = random.randint(0, FUNCNUM)
            fout.write(str(funcNum))
            # print(str(funcNum))
            fout.write("\n")
            for i in range(1, funcNum + 1):
                fout.write(FUNCNAME[i] + "(")
                vars = random.randint(1, NORMALS)
                funcNormal[i] = vars
                for j in range(1, vars + 1):
                    if j != 1:
                        fout.write(",")
                    fout.write(VARS[j])
                fout.write(")=")
                exprFactor(vars, 2, 0)
                fout.write("\n")

            exprFactor(3, 0, 1)

            fout.write("\n")
    # print("")
