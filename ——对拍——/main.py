'''
Author: ltt
Date: 2023-02-25 15:29:32
LastEditors: ltt
LastEditTime: 2023-03-04 13:04:49
FilePath: main.py
'''

import sys, os, sympy

from core import base
from core.gobal import Gobal
from core.core import Checker, Comparator
from core.generator import generate


def main(argv):
    base.init_setting(os.path.join(os.getcwd(), "setting.json"))
    base.test_env()

    checkers: list[Checker] = []
    for (name, project) in Gobal.projects.items():
        checker = Checker(name, project)
        checkers.append(checker)

    for i in range(1000):
        path = os.path.join(Gobal.input, f"test_{i}.in")
        generate(path, 50)
        comparator = Comparator(checkers, path, True)
        comparator.print_result()

    for path in base.list_files(Gobal.input, ".in"):
        comparator = Comparator(checkers, path)
        comparator.print_result()


if __name__ == "__main__":
    main(sys.argv)
