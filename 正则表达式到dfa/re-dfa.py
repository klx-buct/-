from graphviz import Digraph


stack = []  # 储存nfa的栈
flag = []  # 判断图是否遍历完全
symbol = ('|', '·', '*', '(', ')')  # 符号元组
temp = []  # 求闭包时判断是否遍历重复结点
_name = 0  # 求当前结点的数字编号


class State(object):  # nfa的起始和终止状态
    """docstring for State"""
    def __init__(self, start, end):
        self.start = start
        self.end = end


class nfa():  # nfa的每个状态信息
    """docstring for retonfa"""
    def __init__(self):
        self.name = -1
        self.next = []
        self.val = []


def Clear():  # 清空flag标志列表
    flag.clear()


def initnfa(val):  # 初始化一个nfa
    global _name
    start = nfa()
    start.name = _name
    _name = _name + 1
    end = nfa()
    end.name = _name
    _name = _name + 1
    start.next.append(end)
    start.val.append(val)
    stack.append(State(start, end))
    # for i in range(len(start.next)):
    #     print(start.name, start.val[i], start.next[i].name)
    # print(start.name, end.name)


def stnfa(op):  # 构造nfa
    global _name
    if op == '|':
        start = nfa()
        start.name = _name
        _name = _name + 1
        end = nfa()
        end.name = _name
        _name = _name + 1
        start.next.append(stack[-2].start)
        start.val.append("null")
        start.next.append(stack[-1].start)
        start.val.append("null")
        stack[-2].end.next.append(end)
        stack[-2].end.val.append("null")
        stack[-1].end.next.append(end)
        stack[-1].end.val.append("null")
        stack.pop()
        stack.pop()
        stack.append(State(start, end))
        # printnfa(start)
        # print("\n")
        flag.clear()
        # for i in range(len(start.next)):
        #     print(start.name, start.val[i], start.next[i].name)
    elif op == '*':
        start = nfa()
        start.name = _name
        _name = _name + 1
        end = nfa()
        end.name = _name
        _name = _name + 1
        start.next.append(stack[-1].start)
        start.val.append("null")
        stack[-1].end.next.append(stack[-1].start)
        stack[-1].end.val.append("null")
        stack[-1].end.next.append(end)
        stack[-1].end.val.append("null")
        start.next.append(end)
        start.val.append("null")
        stack.pop()
        stack.append(State(start, end))
        # printnfa(start)
        # print("\n")
        flag.clear()
        # for i in range(len(start.next)):
        #     print(start.name, start.val[i], start.next[i].name)
    elif op == '·':
        start = nfa()
        start.name = _name
        _name = _name + 1
        end = nfa()
        end.name = _name
        _name = _name + 1
        start.next.append(stack[-2].start)
        start.val.append("null")
        stack[-2].end.next.append(stack[-1].start)
        stack[-2].end.val.append("null")
        stack[-1].end.next.append(end)
        stack[-1].end.val.append("null")
        stack.pop()
        stack.pop()
        stack.append(State(start, end))
        # printnfa(start)
        # print("\n")
        flag.clear()
        # for i in range(len(start.next)):
        #     print("·",start.name, start.val[i], start.next[i].name)#构造正则表达式的nfa  # 构造nfa


def NRe(Re):  # 将正则表达式逆波兰化
    Re = list(Re)
    length = len(Re)
    i = 0
    N_Re = []  # 结果
    symbol_stack = []  # 符号栈
    while i != length - 1:
        if (symbol.count(Re[i]) == 0 or symbol.index(Re[i]) == 2 or symbol.index(Re[i]) == 4) and (symbol.count(Re[i+1]) == 0 or symbol.index(Re[i+1]) == 3):
            Re.insert(i+1, '·')
            length = length + 1
        i = i + 1
    # print(Re)

    for i in range(len(Re)):
        if symbol.count(Re[i]) == 0:
            N_Re.append(Re[i])
            temp = 0
        elif Re[i] != '(' and Re[i] != ')':
            temp = 1
            while temp == 1:
                if len(symbol_stack) == 0 or symbol_stack[-1] == '(':
                    symbol_stack.append(Re[i])
                    temp = 0
                elif symbol.index(Re[i]) > symbol.index(symbol_stack[-1]):
                    symbol_stack.append(Re[i])
                    temp = 0
                else:
                    N_Re.append(symbol_stack[-1])
                    symbol_stack.pop()
        else:
            if Re[i] == '(':
                symbol_stack.append(Re[i])
            else:
                while symbol_stack[-1] != '(':
                    N_Re.append(symbol_stack[-1])
                    symbol_stack.pop()
                symbol_stack.pop()
    for i in range(len(symbol_stack)):
        N_Re.append(symbol_stack[-1])
        symbol_stack.pop()
    print("逆波兰化后的Re为", "".join(N_Re))
    return N_Re


def printnfa(start):  # 输出nfa
    if len(flag) != _name:
        if flag.count(start.name) == 0:
            flag.append(start.name)
            for i in range(len(start.next)):
                print(start.name, start.val[i], start.next[i].name)
                if flag.count(start.next[i].name) == 0:
                    printnfa(start.next[i])
    return 0


def getclo(start, clo):  # 求每个状态的闭包
    Nclo(start, start.name, clo)
    if len(flag) != _name:
        if flag.count(start.name) == 0:
            flag.append(start.name)
            for i in range(len(start.next)):
                Nclo(start.next[i], start.next[i].name, clo)
                temp.clear()
                if flag.count(start.next[i].name) == 0:
                    getclo(start.next[i], clo)
    return 0


def Nclo(start, name, clo):  # 求单个状态的闭包
    if temp.count(start.name) == 0:
        for i in range(len(start.next)):
            if start.val[i] == "null":
                if clo[name].count(start.next[i].name) != 1:
                    clo[name].append(start.next[i].name)
                Nclo(start.next[i], name, clo)
            if clo[name].count(name) != 1:
                clo[name].append(name)
        temp.append(start.name)


def tantable(table, Re, start, Str):  # 求每个状态的状态转换表
    if len(flag) != _name:
        if flag.count(start.name) == 0:
            flag.append(start.name)
            for i in range(len(start.next)):
                if start.val[i] != "null":
                    if start.val[i] not in table[start.name]:
                        table[start.name][start.val[i]] = [start.next[i].name]
                    else:
                        table[start.name][start.val[i]].append(start.next[i].name)
                if flag.count(start.next[i].name) == 0:
                    tantable(table, Re, start.next[i], Str)


def getdfa(dfa, table, clo, statu):  # 得到dfa
    dfa[statu] = {}
    res = {}
    for i in range(len(statu)):
        for key in table[statu[i]]:
            for j in range(len(table[statu[i]][key])):
                if key not in res:
                    res[key] = clo[table[statu[i]][key][j]]
                else:
                    res[key] = res[key] + clo[table[statu[i]][key][j]]
    for key in res:
        dfa[statu][key] = tuple(set(res[key]))
        if tuple(set(res[key])) not in dfa:
            getdfa(dfa, table, clo, tuple(set(res[key])))


def num(tup, group):  # 判断元组所在分组
    for i in range(len(group)):
        if group[i].count(tup) == 1:
            return i


def move(str1, str2, group, dfa):  # 判断str1和str2是否是同一个分组
    if len(str2) != len(str1):
        return 0
    # print("dfa[str2] = ", str2)
    for key in dfa[str2]:
        if key not in dfa[str1]:
            return 0
        if num(dfa[str1][key], group) != num(dfa[str2][key], group):
            return 0
    return 1


def spdfa(dfa, group, stu):  # 简化dfa
    # print("stu = ", stu)
    temp = list(stu)
    Nstu = []
    # print("stu = ", stu, len(stu))
    while len(stu) != 0:
        if len(stu) == 1:
            break
        t = stu[1:]
        # print("t = ", t)
        Nstu.append([stu[0]])
        for i in range(len(t)):
            if move(stu[0], t[i], group, dfa):
                Nstu[-1].append(t[i])
                stu.remove(t[i])
        # print(stu)
        # print(stu[0])
        # print(group)
        # print(id(stu[0]))
        # if(len(group) >= 3):
        #     print(id(group[2][0]))
        stu.remove(stu[0])
        # print(group)
    if len(stu) == 1:
        Nstu.append([stu[0]])
    # print("Nstu[0] = ", Nstu[0])
    # print("temp = ", temp)
    if Nstu[0] != temp:
        # print("temp = ", temp)
        # print("Nstu = ", Nstu)
        group.remove(temp)
        # print("del = ", group)
        for i in range(len(Nstu)):
            group.append(Nstu[i])
        for i in range(len(Nstu)):
            # print("Nstu[i] = ", Nstu[i])
            # print("group = ", group)
            spdfa(dfa, group, list(Nstu[i]))


def getdfastu(dfa, group, tup):  # 把dfa的元组状态变成简单的数字
    for i in range(len(group)):
        if group[i].count(tup) == 1:
            return i


def updatestate(group):  # 更新State状态为dfa的起始和终止状态
    for i in range(len(group)):
        for j in range(len(group[i]) - 1):
            dfa.pop(group[i][j])
    beg = 0
    end = 0
    for i in range(len(group)):
        for j in range(len(group[i])):
            if group[i][j].count(stack[0].start.name) == 1:
                beg = i
                break
            if group[i][j].count(stack[0].end.name) == 1:
                end = i
                break
    return State(beg, end)


def printdfa(dfa, group, DFA, dfastu):  # 输出dfa
    for key in dfa:
        for key2 in dfa[key]:
            print(getdfastu(dfa, group, key), "(", key2, ")", "->", getdfastu(dfa, group, dfa[key][key2]))
            # if getdfastu(dfa, group, key) == dfastu.start:
            #     DFA.node(name='a',label='',color='white')
            #     DFA.node(name=getdfastu(dfa, group, key))
            # elif getdfastu(dfa, group, key) == dfastu.end:
            #     DFA.


if __name__ == '__main__':
    Re = input("请输入正则表达式")
    Re = NRe(Re)
    for i in range(len(Re)):
        if(symbol.count(Re[i]) == 0):
            initnfa(Re[i])
        else:
            stnfa(Re[i])
    print("nfa为：")
    printnfa(stack[0].start)
    print("开始状态为:", stack[0].start.name, "结束状态为：", stack[0].end.name)
    Clear()
    clo = {}
    table = {}
    for i in range(_name):
        clo[i] = []
        table[i] = {}
    Str = ["null"]
    tantable(table, Re, stack[0].start, Str)
    Clear()
    getclo(stack[0].start, clo)
    Clear()
    # print(clo)
    # print(table)
    dfa = {}
    res = []
    getdfa(dfa, table, clo, tuple(set(clo[stack[0].start.name])))
    dfastu = {}
    first = 0
    print(table)
    print(clo)
    # print(dfa)
    for key in dfa:
        if key.count(stack[0].end.name) == 1:
            dfastu[key] = repr(first) + "(END)"
        else:
            dfastu[key] = first
        first = first + 1
    # print(dfastu)
    # print(dfa)
    print("未化简的dfa为：")
    for key in dfa:
        for key2 in dfa[key]:
            print(dfastu[key], "(", key2, ")", "->", dfastu[dfa[key][key2]])
    group = [[], []]
    for key in dfa:
        if key.count(stack[0].end.name) != 1:
            group[0].append(key)
        else:
            group[1].append(key)
    # print(group)
    temp1 = list(group[0])
    temp2 = list(group[1])
    spdfa(dfa, group, temp1)
    spdfa(dfa, group, temp2)
    # print(group)
    print("化简后的dfa为：")
    DFA = Digraph()
    dfastu = updatestate(group)
    printdfa(dfa, group, DFA, dfastu)
    print("开始状态为：", dfastu.start, "结束状态为：", dfastu.end)