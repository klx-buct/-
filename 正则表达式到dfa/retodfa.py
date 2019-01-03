from graphviz import Digraph


class State(object):  # nfa dfa的起始和终止状态
    """docstring for State"""
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Node(object):  # nfa的每个状态
    """docstring for Node"""
    def __init__(self):
        self.name = -1
        self.next = []
        self.val = []


class Nfa(object):  # nfa
    """docstring for nfa"""
    def __init__(self):
        self.__num = 0  # nfa的状态数
        self.__stack = []  # 构造nfa的栈
        self.__re = ''  # 正则表达式
        self.__symbol = ('|', '·', '*', '(', ')')  # 符号元组
        self.flag = []  # 判断nfa的图是否遍历完全

    def get_stack(self):  # 返回nfa栈
        return self.__stack

    def get_num(self):  # 返回状态数
        return self.__num

    def init(self, val):
        start = Node()
        start.name = self.__num
        self.__num = self.__num + 1
        end = Node()
        end.name = self.__num
        self.__num = self.__num + 1
        start.next.append(end)
        start.val.append(val)
        self.__stack.append(State(start, end))  # 初始化一个状态

    def operation(self, op):  # 传入的参数为操作符('|', '·', '*')
        if op == '|':
            start = Node()
            start.name = self.__num
            self.__num = self.__num + 1
            end = Node()
            end.name = self.__num
            self.__num = self.__num + 1
            start.next.append(self.__stack[-2].start)
            start.val.append("null")
            start.next.append(self.__stack[-1].start)
            start.val.append("null")
            self.__stack[-2].end.next.append(end)
            self.__stack[-2].end.val.append("null")
            self.__stack[-1].end.next.append(end)
            self.__stack[-1].end.val.append("null")
            self.__stack.pop()
            self.__stack.pop()
            self.__stack.append(State(start, end))
            # printnfa(start)
            # print("\n")
            # flag.clear()
            # for i in range(len(start.next)):
            #     print(start.name, start.val[i], start.next[i].name)
        elif op == '*':
            start = Node()
            start.name = self.__num
            self.__num = self.__num + 1
            end = Node()
            end.name = self.__num
            self.__num = self.__num + 1
            start.next.append(self.__stack[-1].start)
            start.val.append("null")
            self.__stack[-1].end.next.append(self.__stack[-1].start)
            self.__stack[-1].end.val.append("null")
            self.__stack[-1].end.next.append(end)
            self.__stack[-1].end.val.append("null")
            start.next.append(end)
            start.val.append("null")
            self.__stack.pop()
            self.__stack.append(State(start, end))
            # printnfa(start)
            # print("\n")
            # flag.clear()
            # for i in range(len(start.next)):
            #     print(start.name, start.val[i], start.next[i].name)
        elif op == '·':
            start = Node()
            start.name = self.__num
            self.__num = self.__num + 1
            end = Node()
            end.name = self.__num
            self.__num = self.__num + 1
            start.next.append(self.__stack[-2].start)
            start.val.append("null")
            self.__stack[-2].end.next.append(self.__stack[-1].start)
            self.__stack[-2].end.val.append("null")
            self.__stack[-1].end.next.append(end)
            self.__stack[-1].end.val.append("null")
            self.__stack.pop()
            self.__stack.pop()
            self.__stack.append(State(start, end))
            # printnfa(start)
            # print("\n")
            # self.__stack.clear()
            # for i in range(len(start.next)):
            #     print("·",start.name, start.val[i], start.next[i].name)#构造正则表达式的nfa  # 构造nf

    def create_nfa(self):
        for i in range(len(self.__re)):
            if(self.__symbol.count(self.__re[i]) == 0):
                self.init(self.__re[i])
            else:
                self.operation(self.__re[i])  # 构建nfa

    def input_re(self):  # 输入正则表达式
        self.__re = input("请输入正则表达式")
        self.__re = list(self.__re)

    def reverse_re(self):
        length = len(self.__re)
        i = 0
        res = []  # 结果
        symbol_stack = []  # 符号栈
        while i != length - 1:
            if (self.__symbol.count(self.__re[i]) == 0 or self.__symbol.index(self.__re[i]) == 2 or self.__symbol.index(self.__re[i]) == 4) and (self.__symbol.count(self.__re[i+1]) == 0 or self.__symbol.index(self.__re[i+1]) == 3):
                self.__re.insert(i+1, '·')
                length = length + 1
            i = i + 1
        # print(Re)

        for i in range(len(self.__re)):
            if self.__symbol.count(self.__re[i]) == 0:
                res.append(self.__re[i])
                temp = 0
            elif self.__re[i] != '(' and self.__re[i] != ')':
                temp = 1
                while temp == 1:
                    if len(symbol_stack) == 0 or symbol_stack[-1] == '(':
                        symbol_stack.append(self.__re[i])
                        temp = 0
                    elif self.__symbol.index(self.__re[i]) > self.__symbol.index(symbol_stack[-1]):
                        symbol_stack.append(self.__re[i])
                        temp = 0
                    else:
                        res.append(symbol_stack[-1])
                        symbol_stack.pop()
            else:
                if self.__re[i] == '(':
                    symbol_stack.append(self.__re[i])
                else:
                    while symbol_stack[-1] != '(':
                        res.append(symbol_stack[-1])
                        symbol_stack.pop()
                    symbol_stack.pop()
        for i in range(len(symbol_stack)):
            res.append(symbol_stack[-1])
            symbol_stack.pop()
        self.__re = list(res)
        # print("逆波兰化后的Re为", "".join(self.__re))  # 正则表达式逆波兰化

    def print_nfa(self, start):
        if len(self.flag) != self.__num:
            if self.flag.count(start.name) == 0:
                self.flag.append(start.name)
                for i in range(len(start.next)):
                    print(start.name, start.val[i], start.next[i].name)
                    if self.flag.count(start.next[i].name) == 0:
                        self.print_nfa(start.next[i])
        return 0  # 输出nfa


class Dfa(object):  # dfa
    """docstring for Dfa"""
    def __init__(self, num):
        self.__dfagv = Digraph()
        self.__spdfagv = Digraph()
        self.__table = {}  # 每个状态的装换表
        self.__clo = {}  # 每个状态的闭包
        self.__num = num  # nfa的状态数
        self.flag = []  # 判断dfa是否遍历完
        self.temp = []  # 求闭包时避免重复遍历结点
        self.__dfa = {}  # 未化简的dfa
        self.__spdfa = {}  # 化简后的dfa
        self.__group = [[], []]  # dfa未化简时的各个分组
        self.__state = ''  # 化简后的dfa开始和结束状态
        for i in range(num):  # 初始化clo table
            self.__clo[i] = []
            self.__table[i] = {}

    def clear(self):  # 清除temp和flag
        self.flag.clear()
        self.temp.clear()

    def create_table(self, start):  # 构造table表
        if len(self.flag) != self.__num:
            if self.flag.count(start.name) == 0:
                self.flag.append(start.name)
                for i in range(len(start.next)):
                    if start.val[i] != "null":
                        if start.val[i] not in self.__table[start.name]:
                            self.__table[start.name][start.val[i]] = [start.next[i].name]
                        else:
                            self.__table[start.name][start.val[i]].append(start.next[i].name)
                    if self.flag.count(start.next[i].name) == 0:
                        self.create_table(start.next[i])

    def init_clo(self, start, name):  # 求编号为name的结点的闭包
        if self.temp.count(start.name) == 0:
            for i in range(len(start.next)):
                if start.val[i] == "null":
                    if self.__clo[name].count(start.next[i].name) != 1:
                        self.__clo[name].append(start.next[i].name)
                    self.init_clo(start.next[i], name)
                if self.__clo[name].count(name) != 1:
                    self.__clo[name].append(name)
            self.temp.append(start.name)

    def init_group(self, stack):  # 把含结束状态的结点和其他结点分成两个组
        for key in self.__dfa:
            if key.count(stack[0].end.name) != 1:
                self.__group[0].append(key)
            else:
                self.__group[1].append(key)

    def num(self, tup):  # 求当前元组所属组的编号
        for i in range(len(self.__group)):
            if self.__group[i].count(tup) == 1:
                return i

    def move(self, tup1, tup2):  # 判断当前两个元组是否在同一组
        if len(tup2) != len(tup1):
            return 0
        # print("dfa[str2] = ", str2)
        for key in self.__dfa[tup2]:
            if key not in self.__dfa[tup1]:
                return 0
            if self.num(self.__dfa[tup1][key]) != self.num(self.__dfa[tup2][key]):
                return 0
        return 1

    def divide(self, stu):  # 划分一个分组为多个分组
        self.temp = list(stu)
        new_stu = []
        while len(stu) != 0:
            if len(stu) == 1:
                break
            t = stu[1:]
            new_stu.append([stu[0]])
            for i in range(len(t)):
                if self.move(stu[0], t[i]):
                    new_stu[-1].append(t[i])
                    stu.remove(t[i])
            stu.remove(stu[0])
        if len(stu) == 1:
            new_stu.append([stu[0]])
        if new_stu[0] != self.temp:
            self.__group.remove(self.temp)
            for i in range(len(new_stu)):
                self.__group.append(new_stu[i])
            for i in range(len(new_stu)):
                self.divide(list(new_stu[i]))

    def create_group(self):  # 把group组分成多个组
        self.divide(list(self.__group[0]))
        self.divide(list(self.__group[1]))

    def create_clo(self, start):  # 构造clo表
        self.init_clo(start, start.name)
        if len(self.flag) != self.__num:
            if self.flag.count(start.name) == 0:
                self.flag.append(start.name)
                for i in range(len(start.next)):
                    self.init_clo(start.next[i], start.next[i].name)
                    self.temp.clear()
                    if self.flag.count(start.next[i].name) == 0:
                        self.create_clo(start.next[i])
        return 0

    def create_dfa(self, statu):  # 构造dfa
        self.__dfa[statu] = {}
        res = {}
        for i in range(len(statu)):
            for key in self.__table[statu[i]]:
                for j in range(len(self.__table[statu[i]][key])):
                    if key not in res:
                        res[key] = self.__clo[self.__table[statu[i]][key][j]]
                    else:
                        res[key] = res[key] + self.__clo[self.__table[statu[i]][key][j]]
        for key in res:
            self.__dfa[statu][key] = tuple(set(res[key]))
            if tuple(set(res[key])) not in self.__dfa:
                self.create_dfa(tuple(set(res[key])))

    def update_state(self, stack):  # 把dfa中多余状态去掉,记录新dfa开始和结束编号
        self.__spdfa = dict(self.__dfa)
        for i in range(len(self.__group)):
            for j in range(len(self.__group[i]) - 1):
                self.__spdfa.pop(self.__group[i][j])
        beg = -1
        end = -1
        for i in range(len(self.__group)):
            if beg != -1 and end != -1:
                break
            for j in range(len(self.__group[i])):
                if self.__group[i][j].count(stack[0].start.name) == 1:
                    beg = i
                    break
                if self.__group[i][j].count(stack[0].end.name) == 1:
                    end = i
                    break
        self.__state = State(beg, end)

    def dfa_stu(self, tup):  # 判断当前元组所属dfa编号
        for i in range(len(self.__group)):
            if self.__group[i].count(tup) == 1:
                return i

    def get_clo(self):  # 返回clo
        return self.__clo

    def get_table(self):  # 返回table
        return self.__table

    def get_dfa(self):  # 返回dfa
        return self.__dfa

    def get_group(self):  # 返回group
        return self.__group

    def print_dfa(self, stack):  #输出dfa
        dfastu = {}
        first = 0
        end = -1
        for key in self.__dfa:
            if key.count(stack[0].end.name) == 1:
                end = first
            dfastu[key] = first
            first = first + 1
        for key in self.__dfa:
            for key2 in self.__dfa[key]:
                # print(dfastu[key], "(", key2, ")", "->", dfastu[self.__dfa[key][key2]])
                one = dfastu[key]
                two = dfastu[self.__dfa[key][key2]]
                self.__dfagv.node(name=str(one), shape='circle')
                self.__dfagv.node(name=str(two), shape='circle')
                self.__dfagv.edge(str(one), str(two), str(key2))
        self.__dfagv.node(name='start', label='', color='white')
        self.__dfagv.edge('start', '0')
        self.__dfagv.node(name=str(end), shape='doublecircle')
        self.__dfagv.render('dfa.gv', cleanup="True", format='png')

    def print_spdfa(self):  # 输出化简后的dfa
        for key in self.__spdfa:
            for key2 in self.__spdfa[key]:
                # print(self.dfa_stu(key), "(", key2, ")", "->", self.dfa_stu(self.__spdfa[key][key2]))
                one = self.dfa_stu(key)
                two = self.dfa_stu(self.__dfa[key][key2])
                self.__spdfagv.node(name=str(one), shape='circle')
                self.__spdfagv.node(name=str(two), shape='circle')
                self.__spdfagv.edge(str(one), str(two), str(key2))
        self.__spdfagv.node(name='start',label='', color='white')
        self.__spdfagv.edge('start', str(self.__state.start))
        self.__spdfagv.node(name=str(self.__state.end), shape='doublecircle')
        self.__spdfagv.render('最小化dfa.gv',cleanup="True",format='png')


if __name__ == '__main__':
    nfa = Nfa()
    nfa.input_re()
    nfa.reverse_re()
    nfa.create_nfa()
    stack = nfa.get_stack()
    nfa.print_nfa(stack[0].start)
    num = nfa.get_num()
    dfa = Dfa(num)
    dfa.create_table(stack[0].start)
    dfa.clear()
    dfa.create_clo(stack[0].start)
    dfa.create_dfa(tuple(set(dfa.get_clo()[stack[0].start.name])))
    dfa.init_group(stack)
    dfa.create_group()
    dfa.update_state(stack)
    dfa.print_spdfa()
    print('\n')
    dfa.print_dfa(stack)
