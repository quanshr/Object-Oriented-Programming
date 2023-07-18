'''
Author: ltt
Date: 2023-03-03 10:42:22
LastEditors: ltt
LastEditTime: 2023-03-06 09:35:46
FilePath: Std.py
'''
import sympy
from . import base

def calcStd(path):
    def trans(s: str):
        (pre, expr) = s.split("=")
        pre = pre.strip()
        name = pre.split("(")[0]
        argv = pre.split("(")[1][:-1].split(",")
        return (name, tuple(argv), sympy.sympify(base.preprocess(expr[::])))
    data: list[str] = []
    with open(path, "r") as f:
        data = f.readlines()
    n = int(data[0])
    funcs = {}
    for i in range(1, n+1):
        (name, argv, expr) = trans(data[i])
        funcs[name] = sympy.Lambda(argv, expr)
    return sympy.sympify(base.preprocess(data[n+1]), locals=funcs)