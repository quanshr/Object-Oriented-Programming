'''
Author: ltt
Date: 2023-02-25 15:22:39
LastEditors: ltt
LastEditTime: 2023-03-06 16:44:54
FilePath: core.py
'''
import sympy, os, platform, subprocess, random, math

from . import base, Std
from .gobal import Gobal

class Checker:
    def __init__(self, name: str, project: dict) -> None:
        self.name: str = name
        self.src: str = os.path.join(Gobal.testPath, project["src"])
        self.MainClassPath: str = os.path.join(self.src, project["MainClass"].replace('.', '/')) + ".java"
        self.output: str = os.path.join(Gobal.output, "bin", self.name)
        self.exe: str = project["MainClass"]
        base.mkdir(self.output)
            
        self.compile()
    
    def compile(self) -> None:
        base.run([Gobal.javac, "-encoding", "UTF-8", "-cp", '"'+self.src+'"', "-d", '"'+self.output+'"', '"'+self.MainClassPath+'"'])
        
    def run(self, inputFile: str):
        print("test--" + self.name)
        return base.run([Gobal.java, "-cp", '"'+self.output+'"', '"'+self.exe+'"', '<', inputFile]).strip()
    
class Comparator:
    def __init__(self, checkers: list[Checker], path: str, delete = False) -> None:
        self.checkers = checkers
        self.delete = delete
        (filepath, filename) = os.path.split(path)
        (name, suffix) = os.path.splitext(filename)
        self.output: str = os.path.join(Gobal.output, name+".json")
        single: str = os.path.join(Gobal.temp, f"single_{filename}")
        self.ans: list[dict] = []
        with open(path, "r") as f:
            print(f"file: {filename}")
            line = 0
            group = 0
            data = f.readlines()
            while (line < len(data)):
                row = data[line].strip()
                if (row == ""):
                    line += 1
                    continue
                try : 
                    n = int(row)
                except:
                    print("data error")
                    return
                line += 1
                with open(single, "w") as w:
                    w.write(str(n)+"\n")
                    for _ in range(n+1):
                        w.write(data[line])
                        line += 1
                group += 1
                ret: dict[str, str] = {}
                try :
                    std = Std.calcStd(single)
                except :
                    print("data error")
                    continue
                with open(single, "r") as single_data:
                    ret["input"]: str = "".join(single_data.readlines())
                    input:str = ret["input"]
                    if (len(input) > 100):
                        print("data too long")
                        continue
                    print(f"checking-{group}: \n{input}")
                ret["std"]: str = str(std.expand())
                for checker in checkers:
                    try:
                        out = checker.run(os.path.join(Gobal.input, single))
                        if (len(out) > 1000) :
                            ret[checker.name]: str = "output too long"
                            continue
                    except RuntimeError as e:
                        ret[checker.name]: str = "RE"
                        continue
                    except subprocess.TimeoutExpired as e:
                        ret[checker.name]: str = "TLE"
                        continue
                    try:
                        tran_out = sympy.sympify(out)
                    except Exception as e:
                        ret[checker.name]: str = "SyntaxError " + out
                    if equals(std,tran_out):
                        if (not Gobal.display["hide"]):
                            ret[checker.name] = "Accepted " + out
                    else:
                        ret[checker.name]: str = out
                if (not Gobal.display["hide"] or (len(ret) != 2)):
                    self.ans.append(ret)
        if ((len(self.ans) == 0) and self.delete):
            os.remove(path)
        os.remove(single)
        
    def print_result(self):
        if (len(self.ans) == 0):
            print("All Accepted")
        else:
            print(base.dump_json(self.output, self.ans))
    
def equals(a, b):
    for _ in range(20):
        x = random.random() * 50
        y = random.random() * 50
        z = random.random() * 50
        # print(a.evalf(subs={"x":x, "y":y, "z":z}),"-",b.evalf(subs={"x":x, "y":y, "z":z}))
        if not math.isclose(a.evalf(subs={"x":x, "y":y, "z":z}), b.evalf(subs={"x":x, "y":y, "z":z}), rel_tol=1e-8):
            return False
    return True