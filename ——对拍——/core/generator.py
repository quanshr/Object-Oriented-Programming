"""
Author: ltt
Date: 2023-03-04 10:50:15
LastEditors: ltt
LastEditTime: 2023-03-06 10:38:17
FilePath: generator.py
"""

import random
import subprocess

from . import base, makecheck
from .gobal import Gobal


def generate(path, num=10):
    if random.randint(0, 1) == 1:
        makecheck.generate(path, num)
    else:
        with open(path, "w") as f:
            pass
        for _ in range(num):
            success = False
            while not success:
                try:
                    base.run(["java", "-jar", Gobal.generator, ">>", path])
                except subprocess.TimeoutExpired as e:
                    continue
                success = True
                # retult = result.replace("\r\n", "\n")
                # f.writelines(result.split('\n'))
                # f.write('\n')
