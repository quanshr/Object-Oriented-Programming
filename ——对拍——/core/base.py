"""
Author: ltt
Date: 2023-02-25 15:54:12
LastEditors: ltt
LastEditTime: 2023-02-26 18:15:10
FilePath: base.py
"""
import subprocess, json, os, platform, sympy, re

from .gobal import Gobal


def run(command, desc=None, errdesc=None):
    """调用命令"""
    if desc is not None:
        print(desc)

    result = subprocess.run(' '.join(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, timeout=5.0)

    if result.returncode != 0:
        message = f"""{errdesc or 'Error running command'}.
Command: {' '.join(command)}
Error code: {result.returncode}
stdout: {result.stdout.decode(encoding="gb2312", errors="ignore") if len(result.stdout) > 0 else '<empty>'}
stderr: {result.stderr.decode(encoding="gb2312", errors="ignore") if len(result.stderr) > 0 else '<empty>'}
"""
        raise RuntimeError(message)
    return result.stdout.decode(encoding="utf8", errors="ignore")


def load_json(path: str) -> None:
    with open(path, "r") as f:
        return json.load(f)


def dump_json(path, out):
    ret = json.dumps(out, sort_keys=False,
                     indent=4, separators=(',', ': '))
    with open(path, "w") as dump_file:
        dump_file.write(ret)
    return ret


def list_files(path: str, extension: str = ""):
    """
    遍历 path 目录下所有文件名以 extension 结尾的文件，返回文件名称列表
    例: list_files('src', '.v')
    """
    result = []
    for path, dirs, files in os.walk(os.path.join(path)):
        for file in files:
            if file.endswith(extension):
                result.append(os.path.join(path, file))
    return result


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def test_env():
    mkdir(Gobal.output)
    mkdir(Gobal.input)
    mkdir(Gobal.temp)
    pass


def preprocess(input: str):
    def trim(matched):
        return str(int(matched.group()))

    return re.sub(r'\d+', trim, input)


def init_setting(path: str):
    load_json(path)
    suffix = ""
    if platform.system() == 'Windows':
        suffix = ".exe"
    Gobal.java: str = '"' + os.path.join(Gobal.setting["java.home"], "bin", "java" + suffix) + '"'
    Gobal.javac: str = '"' + os.path.join(Gobal.setting["java.home"], "bin", "javac" + suffix) + '"'
    Gobal.testPath: str = os.path.join(Gobal.setting["testPath"])
    Gobal.projects: dict = Gobal.setting["projects"]
    Gobal.generator: str = Gobal.setting["generator"]
    Gobal.cwd: str = os.getcwd()
    Gobal.output: str = os.path.join(Gobal.cwd, Gobal.setting["output"])
    Gobal.input: str = os.path.join(Gobal.cwd, Gobal.setting["input"])
    Gobal.temp: str = os.path.join(Gobal.cwd, Gobal.setting["temp"])
    Gobal.display: dict = Gobal.setting["display"]


def parseArgv(argv):
    pass


if __name__ == "__main__":
    print(preprocess("-1 + x ** 233 - z ** 06 +y"))
