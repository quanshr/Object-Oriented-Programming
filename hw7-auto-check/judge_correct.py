import re
import sys


class maintainReq:
    def __init__(self, eleId, time):
        self.eleId = eleId
        self.time = time

    def __repr__(self):
        return '[' + str(self.time) + ']MAINTAIN-Elevator-' + str(self.eleId)


class passengerReq:
    def __init__(self, personId, fromFloor, toFloor, time):
        self.personId = personId
        self.fromFloor = fromFloor
        self.toFloor = toFloor
        self.time = time

    def __repr__(self):
        return '[' + str(self.time) + ']' + self.personId + '-FROM-' + self.fromFloor + '-TO-' + self.toFloor


class addEleReq:
    def __init__(self, eleId, fromFloor, capacity, moveTime, touchFloors, time):  # 这里是构造器传的参数
        self.eleId = eleId
        self.fromFloor = fromFloor
        self.capacity = capacity
        self.moveTime = moveTime
        self.touchFloors = touchFloors
        self.time = time  # self.xxx 这个xxx才是属性名

    def getTouchFloors(self) -> list:  # 依据可达性掩码属性 拿到可达楼层列表
        realFloors = []
        for i in range(0, 11):
            if ((int(self.touchFloors) >> i) & 1) != 0:
                realFloors.append(i + 1)
        return realFloors

    def __repr__(self):
        return '[' + str(self.time) + ']ADD-Elevator-' + str(self.eleId) + \
            '-' + str(self.fromFloor) + '-' + str(self.capacity) + '-' + str(self.moveTime) + '-' + str(
                self.touchFloors)


class openStdout:
    def __init__(self, floor, eleId, time):
        self.floor = floor
        self.eleId = eleId
        self.time = time

    def __repr__(self):
        return '[' + str(self.time) + ']OPEN-' + self.floor + '-' + self.eleId


class closeStdout:
    def __init__(self, floor, eleId, time):
        self.floor = floor
        self.eleId = eleId
        self.time = time

    def __repr__(self):
        return '[' + str(self.time) + ']CLOSE-' + self.floor + '-' + self.eleId


class inStdout:
    def __init__(self, personId, floor, eleId, time):
        self.personId = personId
        self.floor = floor
        self.eleId = eleId
        self.time = time

    def __repr__(self):
        return '[' + str(self.time) + ']IN-' + self.personId + '-' + self.floor + '-' + self.eleId


class outStdout:
    def __init__(self, personId, floor, eleId, time):
        self.personId = personId
        self.floor = floor
        self.eleId = eleId
        self.time = time

    def __repr__(self):
        return '[' + str(self.time) + ']OUT-' + self.personId + '-' + self.floor + '-' + self.eleId


class arriveStdout:
    def __init__(self, floor, eleId, time):
        self.floor = floor
        self.eleId = eleId
        self.time = time

    def __repr__(self):
        return '[' + str(self.time) + ']ARRIVE-' + self.floor + '-' + self.eleId


class maintainAbleStout:
    def __init__(self, eleId, time):
        self.eleId = eleId
        self.time = time

    def __repr__(self):
        return '[' + str(self.time) + ']MAINTAIN_ABLE-' + self.eleId


class maintainAcStdout:
    def __init__(self, eleId, time):
        self.eleId = eleId
        self.time = time

    def __repr__(self):
        return '[' + str(self.time) + ']MAINTAIN_ACCEPT-' + self.eleId


def scanData(stdin, stdout):
    # 把文件中的内容以对象列表的形式读入变量
    with open('stdin.txt', 'r') as f1:
        tempInput = f1.readlines()
        for entry in tempInput:
            elements = re.split(r"[\[\]\s-]+", entry)
            if str(entry).find('MAINTAIN') != -1:  # find方法, 找到的话返回索引, 没找到的话返回-1
                stdin.append(maintainReq(elements[4], float(elements[1])))
            elif str(entry).find('ADD') != -1:
                stdin.append(
                    addEleReq(elements[4], elements[5], elements[6], int(float(elements[7]) * 1000),
                              elements[8], elements[1]))
            elif str(entry).find('FROM') != -1:
                stdin.append(passengerReq(elements[2], elements[4], elements[6], float(elements[1])))
            else:
                print('fix: ' + str(entry))
                print('error input!!')
                return False

    with open('stdout.txt', 'r') as f2:
        tempInput = f2.readlines()
        for entry in tempInput:
            elements = re.split(r"[\[\]\s-]+", entry)
            if str(entry).find('IN-') != -1:
                stdout.append(inStdout(elements[3], elements[4], elements[5], float(elements[1])))
            elif str(entry).find('OUT-') != -1:
                stdout.append(outStdout(elements[3], elements[4], elements[5], float(elements[1])))
            elif str(entry).find('ARRIVE-') != -1:
                stdout.append(arriveStdout(elements[3], elements[4], float(elements[1])))
            elif str(entry).find('OPEN-') != -1:
                stdout.append(openStdout(elements[3], elements[4], float(elements[1])))
            elif str(entry).find('CLOSE-') != -1:
                stdout.append(closeStdout(elements[3], elements[4], float(elements[1])))
            elif str(entry).find('ABLE-') != -1:
                stdout.append(maintainAbleStout(elements[3], float(elements[1])))
            elif str(entry).find('ACCEPT-') != -1:
                stdout.append(maintainAcStdout(elements[3], float(elements[1])))
            else:
                # continue  # 加上这个continue就能开启忽略输出中的调试信息的模式
                print('fix: ' + str(entry))
                print('error output: cannot identified!!')
                return False
    return True


def isTimeUp(stdout) -> bool:  # -> bool 仅仅是增加可读性, 返回任意东西都不会有语法错误
    lastTime = 0
    for entry in stdout:
        if entry.time < lastTime:
            print('lastTime: ' + str(lastTime))
            print('thisTime: ' + str(entry.time))
            print('error: time is not up up and up!!')
            return False
        lastTime = entry.time
    return True


def isOneElevatorAccepted(stdin, stdout, eleId) -> bool:  # hw7新增, 只能在指定楼层开门
    # 给一段输出, 一个电梯id(需要保证这个电梯存在), 判断这个电梯id在这段的运行中是否合理(初末状态均为: 无人 + 关门)
    # 电梯要存在于系统中, 第一次出现的时间晚于ADD的时间
    personList = []
    curFloor = 1
    capacity = 6
    moveTime = 400
    lastCanArriveTime = 0
    lastOpenTime = 0
    doorState = 0  # 0->关门 1-> 开门 其他都错
    addEleTime = 0
    touchFloors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    isAcceptMaintain = False  # 刚开始没接受维修, 当输出扫到的话再置为真
    for entry in stdin:  # 确定初始楼层
        if str(entry).find('ADD-') != -1 and str(entry.eleId) == str(eleId):
            curFloor = entry.fromFloor
            moveTime = entry.moveTime
            capacity = entry.capacity
            addEleTime = entry.time
            touchFloors = entry.getTouchFloors()
    for entry in stdout:  # 只关注hw5中的, 不关注维护, 维护不合规范会有函数处理
        if re.search('-{}$'.format(eleId), str(entry)):  # 找到了这个电梯相关的条目
            if float(entry.time) < float(addEleTime):  # 还没加进来就出现了
                print('fix:' + str(entry))
                print('error: elevator' + str(eleId) + ' is not added but have come up')
                return False
            if str(entry).find('MAINTAIN_ACCEPT-') != -1:
                isAcceptMaintain = True
            if str(entry).find('ARRIVE-') != -1:
                if int(entry.floor) < 1 or int(entry.floor) > 11:
                    print('fix:' + str(entry))
                    print('error: elevator' + str(eleId) + ' want to upper than sky or lower than ground')
                    return False
                if str(doorState) == str(1):
                    print('fix:' + str(entry))
                    print('error: elevator' + str(eleId) + ' move but the door is open')
                    return False
                if entry.time - lastCanArriveTime < (float(moveTime) / 1000.0 - 0.05):
                    print('fix:' + str(entry))
                    print('error: elevator' + str(eleId) + ' move so fast')
                    return False
                if abs(int(entry.floor) - int(curFloor)) != 1:
                    print('fix:' + str(entry))
                    print(
                        'error: elevator' + str(eleId) + ' move buf floor is not changed or changed more than 1 floor')
                    return False
                lastCanArriveTime = entry.time
                curFloor = entry.floor
            if str(entry).find('OPEN-') != -1:
                lastOpenTime = entry.time
                if str(doorState) == str(1):
                    print('fix:' + str(entry))
                    print('error: elevator' + str(eleId) + ' open the door but the door has been open')
                    return False
                if str(entry.floor) != str(curFloor):
                    print('fix:' + str(entry))
                    print('error: elevator' + str(eleId) + ' open the door but skip floors ' +
                          str(entry.floor) + ' ' + str(curFloor))
                    return False
                if int(entry.floor) not in touchFloors:  # 虽然不在指定楼层, 但是如果是在维修的话那没事
                    if not isAcceptMaintain:
                        print('fix:' + str(entry))
                        print('error: elevator' + str(eleId) + ' open in a unavailable floor, cur->' +
                              str(curFloor) + ', but should in the floors->' + str(touchFloors))
                        return False
                doorState += 1
            if str(entry).find('IN-') != -1:  # 没有检测是否人在当前楼层
                if len(personList) >= int(capacity):
                    print('fix:' + str(entry))
                    print('error: elevator' + str(eleId) + ' more than capacity')
                    return False
                elif str(doorState) == str(0):
                    print('fix:' + str(entry))
                    print('error: elevator' + str(eleId) + ' door is not open but one want to in')
                    return False
                elif str(entry.floor) != str(curFloor):
                    print('fix:' + str(entry))
                    print('error: elevator' + str(eleId) + ' a person goes in but skip floors')
                    return False
                else:
                    personList.append(entry.personId)
            if str(entry).find('OUT-') != -1:
                if entry.personId not in personList:
                    print('fix:' + str(entry))
                    print('error: elevator' + str(eleId) + ' a no in ele person want to go out')
                    return False
                elif str(entry.floor) != str(curFloor):
                    print('fix:' + str(entry))
                    print('error: elevator' + str(eleId) + ' a person goes out but skip floors')
                    return False
                elif str(doorState) == str(0):
                    print('fix:' + str(entry))
                    print('error: elevator' + str(eleId) + ' door is not open but one want to out')
                    return False
                else:
                    personList.remove(entry.personId)
            if str(entry).find('CLOSE-') != -1:
                lastCanArriveTime = entry.time
                if str(doorState) == str(0):
                    print('fix:' + str(entry))
                    print('error: elevator' + str(eleId) + ' close the door but the door has been closed')
                    return False
                if (entry.time - lastOpenTime) < 0.36:  # 认为小于0.36就是开关门过快
                    print('fix:' + str(entry))
                    print('error: elevator' + str(eleId) + ' close the door so fast')
                    return False
                if str(entry.floor) != str(curFloor):
                    print('fix:' + str(entry))
                    print('error: elevator' + str(eleId) + ' close the door but skip floors')
                    return False
                if int(entry.floor) not in touchFloors:
                    if not isAcceptMaintain:
                        print('fix:' + str(entry))
                        print('error: elevator' + str(eleId) + ' close in a unavailable floor, cur->' +
                              str(curFloor) + ', but should in the floors->' + str(touchFloors))
                        return False
                doorState -= 1
    if str(doorState) != str(0):
        print('fix:' + str(entry))
        print('error: elevator' + str(eleId) + ' over but the door is open')
        return False
    if len(personList) != 0:
        print('fix:' + str(entry))
        print('error: elevator' + str(eleId) + ' over but elevator is not empty')
        return False
    return True


def isMaintainAccepted(stdin, stdout) -> bool:  # 日常维护逻辑是否合理
    for i, entry in enumerate(stdout):  # 保证 维护ABLE之前有且仅有一个对应的accept 未得到指令时不能维护 && 维护后不能调度
        if str(entry).find('MAINTAIN_ABLE-') != -1:
            acceptCn = 0
            if not isOneElevatorAccepted(stdin, stdout[0:i], entry.eleId):  # 同时保证人员进出的合理性: 此时电梯不能有人且是关门的
                return False
            for entry2 in stdout[0:i]:
                if bool(re.search(r"MAINTAIN_ACCEPT-{}$".format(entry.eleId), str(entry2))):
                    acceptCn += 1
            if acceptCn != 1:
                print('error: elevator' + str(entry.eleId) + ' too much accept or no accept before ABLE')
                return False

            for entry3 in stdout[i + 1:]:  # 后面不能出现此电梯号
                if bool(re.search(r"-{}$".format(entry.eleId), str(entry3))):
                    print('fix: ' + str(entry3))
                    print('error: elevator' + str(entry.eleId) + ' come up again after ABLE')
                    return False

    for i, entry in enumerate(stdout):  # 保证accept出现后能规范维护
        if str(entry).find('MAINTAIN_ACCEPT-') != -1:
            # 判断此后的输出逻辑
            maintainId = entry.eleId
            arriveCn = 0
            isAble = 0
            for entry2 in stdout[i:]:
                # 后面在这个号的电梯的able之前最多只能有两个arrive, 且必须出现able
                if str(entry2).find('MAINTAIN_ABLE-' + str(maintainId)) != -1:  # 找到了able
                    isAble = 1
                    break
                elif re.search(r"ARRIVE-[0-9]+-{}$".format(maintainId), str(entry2)):
                    arriveCn += 1
            if isAble == 0:
                print('error: elevator' + maintainId + ' after maintain: no MAINTAIN_ABLE is out !!')
                return False
            if arriveCn > 2:
                print('error: elevator' + maintainId + ' after maintain: arrive is too much !!')
                return False
    return True


def isElevatorAccept(stdin, stdout) -> bool:  # 判断所有电梯的运行逻辑是否合理
    # 找到所有出现的电梯
    elevatorList = []
    for entry in stdout:
        if entry.eleId not in elevatorList:
            elevatorList.append(entry.eleId)
            if not isOneElevatorAccepted(stdin, stdout, entry.eleId):
                return False
    return True


def isOnePersonAccept(stdout, personEntry) -> bool:  # 传进输出以及这个人的请求
    curFloor = personEntry.fromFloor
    personId = personEntry.personId
    isOut = 1  # 描述是否在电梯外面
    numberInELe = -1
    floorInEle = -1
    for entry in stdout:
        # 找到所有和这个人有关的, 只有in or out
        if bool(re.search(r"IN-{}-[0-9]+-[0-9]+$".format(personId), str(entry))):  # 不考虑是否开门, 只管让进去, 别的函数会处理
            if isOut == 0:
                print('fix: ' + str(entry))
                print('error: elevator' + str(entry.eleId) + ' the person want to in but have been in')
                return False
            if str(curFloor) != str(entry.floor):  # 乘客的所在位置(curFloor)不在电梯的位置(entry.floor)
                print('fix: ' + str(entry))
                print('error: elevator' + str(entry.eleId) + ' the person want to in but skips floors: curFloor->' +
                      curFloor + ' eleFloor->' + entry.floor)
                return False
            isOut = 0
            numberInELe = entry.eleId
        elif bool(re.search(r"ARRIVE-[0-9]+-{}$".format(numberInELe), str(entry))):
            curFloor = entry.floor
        elif bool(re.search(r"OUT-{}-[0-9]+-[0-9]+$".format(personId), str(entry))):
            if isOut == 1:
                print('fix: ' + str(entry))
                print('error: elevator' + str(entry.eleId) + ' the person want to out but have been out')
                return False
            elif str(entry.eleId) != str(numberInELe):  # 出来的电梯id不等于所在的电梯id
                print('fix: ' + str(entry))
                print('error: elevator' + str(entry.eleId) + ' the person want to out from an error ele')
                return False
            elif str(entry.floor) != str(curFloor):
                print('fix: ' + str(entry))
                print('error: elevator' + str(entry.eleId) + ' the person want to out but the floor'
                                                             ' is error personCurFloor: ' + curFloor + ' eleCurFloor is ' + entry.floor)
                return False
            isOut = 1
            numberInELe = -1
    if str(curFloor) != str(personEntry.toFloor):
        print('error:' + ' the person->' + str(personId) + ' not to his goal floor')
        return False
    if isOut == 0:
        print('error:' + ' the person' + str(personId) + 'is in ele but process over')
        return False
    return True


def isPersonAccept(stdin, stdout) -> bool:  # 每个人的请求都满足 + 输出中不出现不存在的人
    personList = []
    # 每个人的请求都满足
    for entry in stdin:
        if str(entry).find('FROM-') != -1:  # 是人的请求
            if entry.personId not in personList:
                personList.append(entry.personId)
                if not isOnePersonAccept(stdout, entry):  # 逐个判断每个人是否符合逻辑
                    return False
    # 至此, 所有出现的乘客编号都已在personList中
    for entry in stdout:
        if (str(entry).find('IN-') != -1) and (entry.personId not in personList):
            print('fix: ' + str(entry))
            print('error: person->' + str(entry.personId) + ' is not exist')
            return False
        if (str(entry).find('OUT-') != -1) and (entry.personId not in personList):
            print('fix: ' + str(entry))
            print('error: person->' + str(entry.personId) + ' is not exist')
            return False
    return True


def isFloorAccept(stdin, stdout) -> bool:  # 11层楼, 每层楼都始终符合服务要求
    for floor in range(1, 12):
        if not isOneFloorAccept(stdin, stdout, floor):
            return False
    return True


def isOneFloorAccept(stdin, stdout, floor) -> bool:
    # 只关注和这层楼有关的开关门信息
    onlyPickCn = 0
    serviceCn = 0
    isOnlyPick = False
    onlyPickEleList = []
    for i, entry in enumerate(stdout):
        if str(entry).find('CLOSE-' + str(floor) + '-') != -1:  # 找到了一条和这个楼层有关的开门信息
            if entry.eleId in onlyPickEleList:  # 这个在只开门列表里
                onlyPickCn -= 1
                onlyPickEleList.remove(entry.eleId)  # 关门后把这个正在 只开门 的电梯去除
            serviceCn -= 1
        if str(entry).find('OPEN-' + str(floor) + '-') != -1:  # 找到了一条和这个楼层有关的开门信息
            # 为isOnlyPick 赋一个正确的值
            personList0 = []  # 开门前电梯内的乘客集合
            personList1 = []  # 开门后电梯内的乘客集合
            for j, eleEntry in enumerate(stdout):
                if j > i and bool(re.search(r"CLOSE-[0-9]+-{}".format(entry.eleId), str(eleEntry))):  # 本条开门指令之后的第一条关门指令
                    break
                if bool(re.search(r"IN-[0-9]+-[0-9]+-{}".format(entry.eleId), str(eleEntry))):  # 寻找这个编号的电梯的 IN 信息
                    if j < i:  # 还没到这个开门信息
                        personList0.append(eleEntry.personId)
                    personList1.append(eleEntry.personId)  # 把进的这个人的id加入到电梯内乘客列表中
                if bool(re.search(r"OUT-[0-9]+-[0-9]+-{}".format(entry.eleId), str(eleEntry))):  # 寻找这个编号的电梯的 OUT 信息
                    if j < i:
                        personList0.remove(eleEntry.personId)
                    personList1.remove(eleEntry.personId)
            isOnlyPick = set(personList0).issubset(set(personList1))  # 前是后的子集, 说明是只接人
            if isOnlyPick:  # 只接人: 这个开门的电梯, 在开门前的乘客集合 是 开门后的乘客集合的子集
                onlyPickEleList.append(entry.eleId)
                onlyPickCn += 1
            serviceCn += 1
        if onlyPickCn > 2:
            print('fix: ' + str(entry))
            print('error: floor->' + str(floor) + ' onlyPickCount is more than 2')
            return False
        if serviceCn > 4:
            print('fix: ' + str(entry))
            print('error: floor->' + str(floor) + ' serviceCount is more than 4')
            return False
    return True


def main():
    stdin = []
    stdout = []
    if not scanData(stdin, stdout):  # 读入数据
        return
    if not isTimeUp(stdout):
        return
    if not isMaintainAccepted(stdin, stdout):
        return
    if not isElevatorAccept(stdin, stdout):
        return
    if not isPersonAccept(stdin, stdout):
        return
    if not isFloorAccept(stdin, stdout):
        return
    print('Accepted !!')
    return
    # res = '[2.8]ADD-Elevator-7-9-8-0.4\n'
    # list = re.split(r"[\[\]\s-]+", res)
    # print(list)
    #
    # res = '[ 2.700]42-FROM-5-TO-8\n'
    # list = re.split(r"[\[\]\s-]+", res)
    # print(list)
    #
    # res = '[5.1]MAINTAIN-Elevator-1\n'
    # list = re.split(r"[\[\]\s-]+", res)
    # stdin.append(maintainReq(3, 4.3123))
    # print(float('0.2') * 1000)
    # ['', '2.8', 'ADD', 'Elevator', '7', '9', '8', '0.4', '']
    # ['', '2.700', '42', 'FROM', '5', 'TO', '8', '']
    # ['', '5.1', 'MAINTAIN', 'Elevator', '1', '']

    # print(stdin[0].find('MAINTAIN'))
    # scanData(stdin, stdout)  # 传进去两个初始列表, 可以直接修改其值
    # print(stdin)
    # stdin = []
    # stdout = []
    # scanData(stdin, stdout)
    # with open('stdin.txt', 'r') as f1:
    #     temp = f1.readlines()
    #     # 判断类型
    #
    #     # new对象,加进列表
    #     print(stdin[0])
    #     print(stdin[1])
    #     print(stdin[2])


if __name__ == '__main__':
    main()
