import random
import sys

nowTime = 0.2
maxEleNum = 6
elevatorList = ['1', '2', '3', '4', '5', '6']
allFloors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
elevators = []
isMaintainInit = 0
isStrong = 1


class Elevator:
    def __init__(self, eleId, accessFloor):
        self.eleId = eleId
        self.accessFloor = accessFloor  # 可达性列表


def removeElevators(eleId):  # 删除电梯列表中id为eleId的某个电箱元素
    global elevators
    for elevator in elevators:
        if elevator.eleId == eleId:
            elevators.remove(elevator)
            break


def isAllAccessIfRemove(eleId) -> bool:  # 判断将一个已有的电梯删掉后是否还可达
    global elevators
    # spList = elevators
    # removeElevators(eleId)

    newList = []
    for entry in elevators:
        if entry.eleId != eleId:
            newList.append(entry)
    graph = getGraphFromEle(newList)
    # 判断graph是不是全图连通, 只需要判断其中一个点 是否可以到达其它所有点即可, 是则全图连通
    isAccess = isAllAccess(graph, 11)
    # 复原电梯列表
    # elevators = spList
    # print(str(eleId) + '->' + str(isAccess))
    return isAccess


def isAllAccess(graph, nodeCn) -> bool:
    # 判断一个图是不是全部连通的图
    visited = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 记录某个点是否可到达
    queue = [1]
    visited[1] = 1
    while len(queue) != 0:
        curNode = queue[0]
        queue = queue[1:]  # 出队
        for nextNode in graph[curNode]:  # 遍历当前节点连结着的其它节点
            if visited[nextNode] != 1:
                visited[nextNode] = 1
                queue.append(nextNode)
    return 0 not in visited[0:nodeCn + 1]


def getGraphFromEle(eleList):  # 传进来一个电梯对象列表
    graph = [0]  # [0, [...], [...], ...]
    for i in range(1, 12):  # 1->11
        graph.append([])
        for elevator in eleList:
            if i in elevator.accessFloor:
                graph[i].extend(elevator.accessFloor)
        graph[i] = list(set(graph[i]))
    return graph


def isNoInitEle() -> bool:
    for i in range(1, 7):
        if str(i) in elevatorList:
            return False
    return True


def getData(minFloor, maxFloor):  # 该函数捏一条条的数据并写入stdin.txt文件中
    global isMaintainInit
    with open('stdin.txt', 'w') as file1:
        global isStrong
        isStrong = random.randint(0,1)
        isMaintainInit = random.randint(0, 2)
        reqCount = random.randint(70, 80)  # 随机生成需求条目数量
        i = 1
        isTotal = False
        addReqCn = 0
        maintainReqCn = 0
        personReqCn = 0
        floorModel = random.randint(0, 1)  # 0 -> 完全随机楼层需求  1 -> 楼层密集需求
        dirMode = random.randint(0, 4)  # 0 -> 随机方向 1,2 -> 上升密集  3,4 -> 下降密集
        centralFloor = random.randint(1, 11)  # 随机生成密集的中心楼层
        while i <= reqCount:
            ranNum = random.randint(1, 100)
            if len(elevatorList) <= 2:
                morePossible = 8
            elif len(elevatorList) <= 4:
                morePossible = 4
            else:
                morePossible = 0
            if isMaintainInit == 0:
                morePossibleMain = 0
            elif isMaintainInit == 1:
                morePossibleMain = 25
            else:
                morePossibleMain = 50  # 若没维护完就70的概率维护一个旧电梯
            # morePossibleMain = 100
            if isNoInitEle():
                morePossibleMain = 0  # 没有旧电梯的话不管强不强都不加了
            # 上面计算概率增值
            if isStrong == 1 and not isTotal:
                if i <= 6:
                    dataLine = '[0.2]MAINTAIN-Elevator-' + str(i)
                    elevatorList.remove(str(i))
                    removeElevators(i)
                elif not isAllAccess(getGraphFromEle(elevators), 11):
                    dataLine = getAddRequest()
                else:
                    isTotal = True
                    continue
            elif ranNum <= 10 + morePossible:  # 加 加电梯 操作
                dataLine = getAddRequest()
            elif ranNum <= 20 + morePossibleMain and len(elevatorList) > 1:  # 加 维护 操作
                dataLine = getMaintainRequest()
                if dataLine == 'null':
                    i += 1
                    continue
                personReqCn += 1
            else:  # 加 常规 请求
                # 确定楼层
                if floorModel == 0:
                    if dirMode == 0:
                        dataLine = getPersonRequest(i, minFloor, maxFloor, 0)
                    elif dirMode <= 2:  # 上升密集, 上升的概率大
                        if random.randint(1, 10) <= 7:
                            dataLine = getPersonRequest(i, minFloor, maxFloor, 1)
                        else:
                            dataLine = getPersonRequest(i, minFloor, maxFloor, -1)
                    else:  # 下降密集, 下降的概率大
                        if random.randint(1, 10) <= 7:
                            dataLine = getPersonRequest(i, minFloor, maxFloor, -1)
                        else:
                            dataLine = getPersonRequest(i, minFloor, maxFloor, 1)
                else:  # 起始楼层密集
                    # 先确定起始楼层范围
                    leftFloor = centralFloor - 2
                    if leftFloor < 1:
                        leftFloor = 1
                    rightFloor = centralFloor + 2
                    if rightFloor > 11:
                        rightFloor = 11
                    # 确定方向
                    if dirMode == 0:
                        dataLine = getPersonRequest(i, leftFloor, rightFloor, 0)
                    elif dirMode <= 2:  # 上升密集, 上升的概率大
                        if random.randint(1, 10) <= 7:
                            if random.randint(1, 100) <= 15:
                                dataLine = getPersonRequest(i, minFloor, maxFloor, 1)
                            else:
                                dataLine = getPersonRequest(i, leftFloor, rightFloor, 1)
                        else:
                            if random.randint(1, 100) <= 15:
                                dataLine = getPersonRequest(i, minFloor, maxFloor, -1)
                            else:
                                dataLine = getPersonRequest(i, leftFloor, rightFloor, -1)
                    else:  # 下降密集, 下降的概率大
                        if random.randint(1, 10) <= 7:
                            if random.randint(1, 100) <= 15:
                                dataLine = getPersonRequest(i, minFloor, maxFloor, -1)
                            else:
                                dataLine = getPersonRequest(i, leftFloor, rightFloor, -1)
                        else:
                            if random.randint(1, 100) <= 15:
                                dataLine = getPersonRequest(i, minFloor, maxFloor, 1)
                            else:
                                dataLine = getPersonRequest(i, leftFloor, rightFloor, 1)
            file1.write(dataLine)
            file1.write('\n')
            i += 1


def getPersonRequest(num, minFloor, maxFloor, direction):  # 得到一条数据
    ans = ''
    ans += str(getTime())
    ans += str(getRequest(num, minFloor, maxFloor, direction))
    return str(ans)


def getTime():  # 返回一个 [浮点时间]
    global nowTime
    # 1/ 4 的概率时间不增, 其他的概率时间随机增长
    randNum = random.randint(1, 4)  # 随机生成一个[1, 8]区间内的整数
    if randNum != 1:  # 需要加的时候才加时间, 否则不执行if 直接原时间返回
        randNum = random.randint(1, 4)  # 随机加时间的幅度: 小 中 挡, 概率比为: 5:3
        if randNum <= 3:  # 小幅度
            nowTime += random.uniform(0, 0.2)
        else:
            nowTime += random.uniform(0.2, 0.7)

    return '[' + str(nowTime) + ']'


def getRequest(num, minFloor, maxFloor, direction):  # 这里的需求生成不设计换乘  dir = 0 随机方向
    ans = ''
    # 加乘客id
    ans += str(num)
    floors = random.sample(list(range(minFloor, maxFloor + 1)), 2)  # 取两个不同的楼层
    lessFloor = min(floors)
    moreFloor = max(floors)
    if direction == 1:
        floors[0] = lessFloor
        floors[1] = moreFloor
    elif direction == -1:
        floors[0] = moreFloor
        floors[1] = lessFloor
    # 加起始楼层
    ans += '-FROM-' + str(floors[0]) + '-'
    # 加目标楼层, 这个楼层和起始楼层不可相同
    # toFloor = random.randint()
    ans += 'TO-' + str(floors[1])
    return ans


def getMaintainRequest():  # 得到一条随机维护现有电梯的指令
    global elevatorList
    global elevators
    stillAccessEle = []
    # print('here')
    # print(elevators)
    for elevator in elevators:  # 挑一个不破坏全图性的维护
        # print(elevator.eleId)
        # print('can jia pan duan->' + str(elevator.eleId))
        if isAllAccessIfRemove(elevator.eleId):
            # print(elevator.eleId)
            stillAccessEle.append(elevator.eleId)
    if len(stillAccessEle) == 0:
        return 'null'
    # 根据强化程度,1->50的概率维护一个旧电梯, 2->90的概率维护一个旧电梯
    # initEleList = []
    # for entry in stillAccessEle:
    #     if entry <= 6:
    #         initEleList.append(entry)  # 可去电梯中的初始电梯列表
    #
    # if isMaintainInit != 0:
    #     if len(initEleList) != 0:
    #         maintainId = random.sample(initEleList, 1)[0]  # 返回的是一个列表, 所以需要拿来[0]
    #     else:

    maintainId = random.sample(stillAccessEle, 1)[0]  # 返回的是一个列表, 所以需要拿来[0]
    elevatorList.remove(str(maintainId))
    removeElevators(int(maintainId))  # 删掉电梯对象列表中的某个id的电梯
    return getTime() + 'MAINTAIN-Elevator-' + str(maintainId)


def getAddRequest():  # 得到加id不同于之间有过的电梯的请求, 返回一个字符串
    global maxEleNum
    global elevatorList
    global elevators
    ans = ''
    ans += getTime()
    # 不会加id 1-6的请求
    eleId = maxEleNum + 1
    maxEleNum = maxEleNum + 1
    fromFloor = random.randint(1, 11)
    capacity = random.randint(3, 8)
    moveTimeFloat = float(random.randint(2, 6)) / 10.0
    ans = ans + 'ADD-Elevator-' + str(eleId) + '-' + str(fromFloor) + '-' + str(capacity) + '-' + str(moveTimeFloat)
    # 加上一个掩码
    reList = getAccessFloor()
    accessFloor = reList[0]
    ans = ans + '-' + str(accessFloor)
    elevatorList.append(str(eleId))
    elevators.append(Elevator(eleId, reList[1]))
    return ans


def getAccessFloor() -> list:  # 随机生成一个可达3个及以上楼层的电梯
    accessCn = random.randint(3, 11)  # 能到 最少3个 最多11个楼层
    # 000 0000 0000
    # 1-11号位置随机找accessCn个位置
    floorList = random.sample(range(1, 12), accessCn)
    ans = 0
    for bit in floorList:
        ans += pow(int(2), bit - 1)
    return [ans, floorList]


# 初始化电梯列表
for i in range(1, 7):
    elevators.append(Elevator(i, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]))
getData(1, 11)
