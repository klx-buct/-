class LL1():
    def __init__(self):
        self._ll1 = [] # 文法
        self._ll1dict = {} #  文法字典结构
        self._nterminal = [] #  非终结符
        self._beg = '' #  文法的开始符号
        self._first = {} #  first集合
        self._follow = {} #  follow集合
        self._analyze = {} #  分析表
        self.input_ll1()

    def input_ll1(self): #  输入文法
        num = int(input("请输入你想输入几个文法"))
        print("请输入文法(A-a|E|null)")
        for i in range(num):
            self._ll1.append(input())
            index = self._ll1[-1].index('-')
            self._ll1dict[self._ll1[-1][0:index]] = self._ll1[-1][index+1:]
            if i == 0:
                self._beg = self._ll1[-1][0:index]

    def get_ll1(self):
        return self._ll1

    def get_ll1dict(self):
        return self._ll1dict

    def get_first(self):
        return self._first

    def get_follow(self):
        return self._follow

    def get_analyze(self):
        return self._analyze

    def get_beg(self):
        return self._beg

    def remove_common_recursion(self, exp): # 消除一般左递归
        flag = -1
        index = exp.index('-')
        nterminal = exp[:index]
        left_exp = exp[index+1:]
        left_exp = left_exp.split('|')
        X = ''
        Y = ''
        for x in left_exp:
            length = len(nterminal)
            if nterminal in x[0:length]:
                flag = 1
                X += x[length:] + nterminal + "'|"
            else:
                Y += x + nterminal + "'|"
        if flag == -1:
            return
        X = X[:-1]
        Y = Y[:-1]
        self._ll1dict[nterminal+"'"] = X + "|null"
        self._nterminal = list(set(self._nterminal + [nterminal+"'"]))
        self._ll1dict[nterminal] = Y

    def replace(self, terminal): #  代替产生式中的非终结符
        res = ''
        for x in (self._ll1dict[terminal]).split('|'):
            if x == '':
                print(self._ll1dict[terminal], "terminal = ", terminal)
            temp = self.get_nterminal(x)
            print(x)
            if temp == -1:
                res = res + x + '|'
                continue
            if temp == 1:
                for s in (self._ll1dict[x]).split('|'):
                    res = res + s + '|'
                continue
            # print(temp)
            if self.num(terminal) > self.num(temp[0]):
                for s in (self._ll1dict[temp[0]]).split('|'):
                    if s == 'null':
                        res = res + temp[1] + '|'
                    else:
                        res = res + s + temp[1] + '|'
            else:
                res = res + x + '|'
        res = res[:-1]
        self._ll1dict[terminal] = res
        self.remove_common_recursion(terminal + '-' + res)

    def get_nterminal(self, part): #  得到产生式中的非终结符
        if part == '' or part[0] not in self._nterminal:
            return -1
        position = 0
        while True:
            if len(part) == 1:
                return 1
            if part[position+1] == "'":
                position += 1
            else:
                break
        return part[0:position+1], part[position+1:]

    def terminal(self): # 返回所有非终结符
        return self._nterminal

    def num(self, nterminal): #  返回非终结符的位置，作为大小判断
        return self._nterminal.index(nterminal)

    def remove_indirect_recursion(self): #  消除间接左递归
        nterminal = []
        for s in reversed(self._ll1):
            index = s.index('-')
            nterminal.append(s[:index])
        self._nterminal += nterminal
        # print(terminal)
        for s in nterminal:
            temp = self._ll1dict[s]
            self.replace(s)
            # print(temp, self._ll1dict[s])
            while self._ll1dict[s] != temp:
                temp = self._ll1dict[s]
                self.replace(s)

    def init_fstflw(self): #  初始化first和follow集合
        # print(self._nterminal)
        for key in self._nterminal:
            self._first[key] = []
            self._follow[key] = []
        self._follow[self._beg] = ['$']
        # print("first: ",self._first)
        # print("follow: ",self._follow)

    def deal_str(self, s): #  提取每个字符串中的非终结符和终结符
        lst = list(s)
        try:
            while True:
                index = lst.index("'")
                lst[index - 1] = lst[index - 1] + "'"
                del lst[index]
        except:
            pass
        if 'n' in lst:
            index = lst.index('n')
            try:
                if lst[index+1]=='u' and lst[index+2]=='l' and lst[index+3]=='l':
                    lst[index] = 'null'
                    del lst[index+1]
                    del lst[index+1]
                    del lst[index+1]
            except:
                pass
        return lst

    def first(self): #  求first集合
        judge = 0 # 求出所有first集合后是否需要再一次重新遍历
        for key in self._ll1dict:
            addnull = 1 # 是否添加空到first集合
            lst = self._ll1dict[key].split('|')
            for item in lst:
                nitem = self.deal_str(item)
                for i in nitem:
                    if i not in self._nterminal:
                        # print("not terminal")
                        # print("i = ", i, "key = ", key)
                        addnull = 0
                        temp = self._first[key]
                        self._first[key] = list(set(self._first[key] + [i]))
                        self._first[key].sort()
                        temp.sort()
                        if self._first[key] != temp:
                            judge = 1
                        break
                    else:
                        temp = self._first[key]
                        if 'null' in self._first[i]:
                            add = list(self._first[i])
                            add.remove('null')
                            self._first[key] = list(set(self._first[key] + add))
                            # self._first[key].remove('null')
                            # print("key = ", key)
                            # print("temp = ", temp)
                            # print("first[key] = ", self._first[key])
                        else:
                            self._first[key] = list(set(self._first[key] + self._first[i]))
                            self._first[key].sort()
                            temp.sort()
                            if self._first[key] != temp:
                                judge = 1
                            addnull = 0
                            # print("key = ", key)
                            # print("temp = ", temp)
                            # print("first[key] = ", self._first[key])
                            break
                        self._first[key].sort()
                        temp.sort()
                        if self._first[key] != temp:
                            judge = 1
            if addnull:
                self._first[key] += ['null']
        if judge:
            # print("sucess")
            self.first()

    def follow(self): #  求follow集合
        judge = 0
        for key in self._ll1dict: #  求每个非终结符的follow集
            for item in self._ll1dict:  #  从每个产生式右边找对应的key
                for i in self._ll1dict[item].split('|'):
                    lst = self.deal_str(i)
                    # print("lst = ",lst)
                    for index, aim in enumerate(lst):
                        if aim == key:
                            nindex = index
                            while True:
                                if nindex == len(lst) - 1:
                                    temp = self._follow[key]
                                    self._follow[key] = list(set(self._follow[key] + self._follow[item]))
                                    # print("key = ",key,"   ", self._follow[item])
                                    temp.sort()
                                    self._follow[key].sort()
                                    if temp != self._follow[key]:
                                        # print("temp = ", temp)
                                        # print("follow = ", self._follow[key])
                                        judge = 1
                                    break
                                elif lst[nindex+1] not in self._nterminal:
                                    # print(lst[nindex+1])
                                    temp = self._follow[key]
                                    self._follow[key] = list(set(self._follow[key] + [lst[nindex+1]]))
                                    temp.sort()
                                    self._follow[key].sort()
                                    if temp != self._follow[key]:
                                        # print("temp = ", set(temp))
                                        # print("follow = ", set(self._follow[key]))
                                        judge = 1
                                    break
                                else:
                                    temp = self._follow[key]
                                    self._follow[key] = list(set(self._follow[key] + self._first[lst[nindex+1]]))
                                    if 'null' in self._follow[key]:
                                        self._follow[key].remove('null')
                                    else:
                                        temp.sort()
                                        self._follow[key].sort()
                                        if temp != self._follow[key]:
                                            # print("temp = ", set(temp))
                                            # print("follow = ", set(self._follow[key]))
                                            judge = 1
                                        break
                                    temp.sort()
                                    self._follow[key].sort()
                                    if temp != self._follow[key]:
                                        # print("temp = ", set(temp))
                                        # print("follow = ", set(self._follow[key]))
                                        judge = 1
                                nindex += 1
        if judge:
            self.follow()

    def analyze(self): #  求分析表
        self._ll1.clear()
        index = 0
        for key in self._ll1dict:
            for item in self._ll1dict[key].split('|'):
                self._ll1.append(str(index)+': '+key+'->'+item)
                index += 1
        for item in self._nterminal: #  初始化分析表
            self._analyze[item] = {}
        index = 0
        for key in self._ll1dict:
            for item in self._ll1dict[key].split('|'):
                nitem = self.deal_str(item)
                for lth, val in enumerate(nitem):
                    if val in self._nterminal:
                        if 'null' not in self._first[val]:
                            for i in self._first[val]:
                                self._analyze[key][i] = index
                        else:
                            if lth == len(item) - 1:
                                for i in self._follow[key]:
                                    self._analyze[key][i] = index
                            else:
                                for i in self._first[val]:
                                    if i != 'null':
                                        self._analyze[key][i] = index
                            break
                    else:
                        if val != 'null':
                            self._analyze[key][val] = index
                            break
                        else:
                            # print("isokkkkkkkkkkkkkkkkkkkkkkkkkkkk")
                            # print(lth)
                            # print(len(nitem))
                            # print(item)
                            if lth == len(nitem) - 1:
                                # print('isok')
                                for i in self._follow[key]:
                                    self._analyze[key][i] = index
                            break
                # while True:
                #   if nitem[0] in self._nterminal:
                #     for i in self._first[nitem[0]]:
                #       self._analyze[key][i] = index
                #     break
                #   elif nitem[0] == 'null':
                #     if len(nitem) == 1:
                #       for i in self._follow[key]:
                #         self._analyze[key][i] = index
                #       break
                #     else:
                #       del nitem[0]
                #   else:
                #     self._analyze[key][nitem[0]] = index
                #     break
                index += 1

    def commonFactor(self, key, Str): #  提取公因子
        lst = Str.split('|')
        common = ''
        other = ''
        for i in range(len(lst) - 1):
            aim = self.deal_str(lst[i])
            # print("aim = ", aim)
            if i != 0:
                other = "".join(lst[:i])+'|'
            for item in lst[i:]:
                temp = self.deal_str(item)
                if  temp[0] == aim[0]:
                    common = common + "".join(temp[1:]) + '|'
                else:
                    other = other + "".join(temp) + '|'
                    # print("other=", other)
            judge = "".join(aim[1:])+'|'
            # print("judge =",judge)
            # print("common = ", common)
            if common != judge:
                self._nterminal.append(key+"'")
                # print(self._nterminal)
                if other == '':
                    # print(key, "->", aim[0]+key+"'")
                    self._ll1dict[key] = aim[0]+key+"'"
                else:
                    self._ll1dict[key] = aim[0]+key+"'"+"|"+other[:-1]
                    # print(key, "->", aim[0]+key+"'"+"|"+other[:-1])
                self._ll1dict[key+"'"] = common[:-1]
                # print(key+"'", "->", common[:-1])
                # print(key, "->", common)
                # print(key, "->", other[:-1])
                if other == '':
                    self.commonFactor(key, aim[0]+key+"'")
                else:
                    self.commonFactor(key, aim[0]+key+"'"+"|"+other[:-1])
                self.commonFactor(key+"'", common[:-1])
                break
            else:
                common = ''

def main():
    ll1 = LL1()
    ll1dict = dict(ll1.get_ll1dict())
    for key in ll1dict:
        ll1.commonFactor(key, ll1dict[key])
    ll1dict = ll1.get_ll1dict()
    print("提取公因子后的产生式为：")
    for key in ll1dict:
        print(key,"->",ll1dict[key])
    ll1.remove_indirect_recursion()
    ll1.init_fstflw()
    ll1.first()
    ll1.follow()
    ll1dict = ll1.get_ll1dict()
    print("消除递归后的产生式为：")
    for key in ll1dict:
        print(key,"->",ll1dict[key])
    first = ll1.get_first()
    print("first集合为：")
    for key in first:
        print("first(",key,")=",first[key])
    follow = ll1.get_follow()
    print("follow集合为：")
    for key in follow:
        print("follow(",key,")=",follow[key])
    ll1.analyze()
    actionList = {}
    print("分析表为：")
    _ll1 = ll1.get_ll1()
    for item in _ll1:
        index = item.find(':')
        index2 = item.find('>')
        actionList[item[0:index]] = item[index2+1:]
        print(item)
    # print(actionList)
    analyze = ll1.get_analyze()
    for key in analyze:
        print(key,": ",analyze[key])
    Str = input("请输入一个分析串")
    ipt = ll1.deal_str(Str)
    ipt.append('$')
    print("%20s %15s %10s"%("analyzeStack","input","action"))
    analyzeStack = [ll1.get_beg()]
    analyzeStack.append('$')
    while True:
        # ipt = "".join(lst)
        atop = analyzeStack[0]
        itop = ipt[0]
        # print(atop)
        # print(itop)
        # if (atop == '$' and itop != '$') or (atop != '$' and itop == '$'):
        #     action = 'Error!'
        #     print("%20s %15s %10s"%("".join(analyzeStack), "".join(ipt), action))
        #     break
        if atop == '$' and itop == '$':
            action = 'Accept'
            print("%20s %15s %10s"%("".join(analyzeStack), "".join(ipt), action))
            break
        elif atop == itop:
            action = 'matching'
            print("%20s %15s %10s"%("".join(analyzeStack), "".join(ipt), action))
            del ipt[0]
            del analyzeStack[0]
        else:
            if itop in analyze[atop]:
                number = str(analyze[atop][itop])
                action = atop + '->' + actionList[number]
                print("%20s %15s %10s"%("".join(analyzeStack), "".join(ipt), action))
                del analyzeStack[0]
                # print(actionList)
                if actionList[number] != 'null':
                    temp = ll1.deal_str(actionList[number])
                    analyzeStack = temp + analyzeStack
            else:
                action = 'Error!'
                print("%20s %15s %10s"%("".join(analyzeStack), "".join(ipt), action))
                break

if __name__ == '__main__':
    main()