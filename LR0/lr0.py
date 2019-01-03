number = 1


class Lr0:
    def __init__(self):
        self.__lr0 = {}
        self.__clo = {}  # 闭包
        self.__nterminal = []
        self.__dfa = ''
        self.__analyze = {}
        self.__beg = ''

        self.ipt()  # 输入文法
        self.all_clo()  # 求闭包
        self.initDfa()  # 初始化Dfa
        self.createAllDfa(self.__dfa, [])  # 求Dfa
        self.createAnalyze(self.__dfa, [])

    def ipt(self):
        num = int(input("请输入你想输入几个文法"))
        print("请输入文法 S-A|null")
        for i in range(num):
            item = input()
            index = item.find('-')
            if i == 0:
                self.__beg = item[0:index] + "'"
                self.__lr0[item[0:index] + "'"] = item[0:index]
                self.__nterminal.append(item[0:index] + "'")
            self.__lr0[item[0:index]] = item[index + 1:]
            self.__nterminal.append(item[0:index])

    def all_clo(self):  # 求每个非终结符的闭包
        for key in self.__lr0:
            for item in self.__lr0[key].split('|'):
                if key not in self.__clo or key + "-" + item not in self.__clo[key]:
                    self.clo(key, key, item)

    def clo(self, key, beg, item):  # 求单个非终结符的闭包
        if key not in self.__clo:
            self.__clo[key] = [beg + "-" + item]
        else:
            self.__clo[key].append(beg + "-" + item)
        item = self.deal_str(item)
        index = 0
        try:
            while item[index] in self.__nterminal:
                for val in self.__lr0[item[index]].split('|'):
                    if item[index] + "-" + val not in self.__clo[key]:
                        self.clo(key, item[index], val)
                index += 1
        except:
            pass

    def deal_str(self, s):  # 提取每个字符串中的非终结符和终结符
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
                if lst[index + 1] == 'u' and lst[index + 2] == 'l' and lst[index + 3] == 'l':
                    lst[index] = 'null'
                    del lst[index + 1]
                    del lst[index + 1]
                    del lst[index + 1]
            except:
                pass
        return lst

    def initDfa(self):
        nterminal = list(self.__lr0.keys())
        self.__dfa = Dfa(Item(nterminal[0] + '-' + self.__lr0[nterminal[0]], 0), 0, 0, self.get_nterminal(),
                         self.get_clo())

    def createNewDfa(self, item, number):  # 根据每一条产生式创建一个dfa
        val = item.val
        pointIndex = item.pointIndex
        index = val.find('-')
        end = val[index + 1:]
        # print("end=",list(end))
        if end == 'null':
            return end[pointIndex], Dfa(Item(val[:index+1], 0), number, 1, self.get_nterminal(), self.get_clo())
        end = self.deal_str(end)
        # print(val)
        # print(pointIndex)
        # print(len(end))
        if pointIndex == len(end):
            return
        if pointIndex == len(end) - 1:
            return end[pointIndex], Dfa(Item(val, pointIndex + 1), number, 1, self.get_nterminal(), self.get_clo())
        else:
            return end[pointIndex], Dfa(Item(val, pointIndex + 1), number, 0, self.get_nterminal(), self.get_clo())

    def createAllDfa(self, before, already):
        global number
        for idx, item in enumerate(before.allItem):
            try:
                go, dfa = self.createNewDfa(item, number)
            except:
                continue
            number += 1
            if dfa.status == 1:
                same = self.findSame(dfa, self.__dfa)
                if same.allItem == ['']:
                    before.nextVal.append(go)
                    before.next.append(dfa)
                else:
                    before.nextVal.append(go)
                    before.next.append(same)
            else:
                same = self.findSame(dfa, self.__dfa)
                # print(same.allItem)
                if same.allItem == ['']:
                    if go in before.nextVal:
                        index = before.nextVal.index(go)
                        before.next[index] = before.next[index] + dfa
                    else:
                        before.nextVal.append(go)
                        before.next.append(dfa)
                else:
                    # for newitem in same.allItem:
                    #     print(newitem.val)
                    # number -= 1
                    if go not in before.nextVal:
                        before.nextVal.append(go)
                        before.next.append(same)
        for item in before.next:
            if item.status != 1 and item.number not in already:
                already.append(item.number)
                self.createAllDfa(item, already)

    def findSame(self, newDfa, dfa):
        # print("123123")
        already = []
        DfaLst = []
        already.append(dfa.number)
        DfaLst.append(dfa)
        while len(DfaLst) != 0:
            # print(len(DfaLst))
            if newDfa == DfaLst[0]:
                return DfaLst[0]
            for item in DfaLst[0].next:
                if item.number not in already:
                    # print(already)
                    # print(item.number)
                    DfaLst.append(item)
                    already.append(item.number)
            del DfaLst[0]
        return Dfa('', 0, 0, '', '')

    def createAnalyze(self, dfa, already):
        temp = dfa
        already.append(temp.number)
        if temp.next != []:
            for index, item in enumerate(temp.next):
                if temp.number not in self.__analyze:
                    self.__analyze[temp.number] = {temp.nextVal[index]: item.number}
                else:
                    self.__analyze[temp.number][temp.nextVal[index]] = item.number
                if item.number not in already:
                    self.createAnalyze(item, already)
        else:
            self.__analyze[temp.number] = {'reduce':temp.allItem[0].val}


    def printDfa(self, dfa, already):
        temp = dfa
        # print("number:", temp.number)
        # print("status:", temp.status)
        # for item in temp.allItem:
        #     print(item)
        already.append(temp.number)
        if temp.next != []:
            for index, item in enumerate(temp.next):
                print(temp.number, "(", temp.nextVal[index], ") ->")
                print("number:", item.number)
                print("status:", item.status)
                for val in item.allItem:
                    print(val)
                if item.number not in already:
                    self.printDfa(item, already)
                # elif item.number == temp.number:
                #     print("number:", item.number)
                #     print("status:", item.status)
                #     for val in item.allItem:
                #         print(val)

    def DealWidth(self, ipt):
        print("%20s %20s %20s"%("analyzeStack", "input", "action"))
        analyzeStack = ['$', '0']
        ipt = list(ipt)
        ipt = ipt + ['$']
        while analyzeStack[1] != self.__beg:
            if 'reduce' in self.__analyze[int(analyzeStack[-1])]:
                reduce = self.__analyze[int(analyzeStack[-1])]['reduce']
                print("%20s %20s %20s"%("".join(analyzeStack), "".join(ipt), "reduce "+reduce))
                index = reduce.find('-')
                beg = reduce[0:index]
                end = reduce[index+1:]
                end = self.deal_str(end)
                while len(end) != 0:
                    if end[-1] == analyzeStack[-2]:
                        del end[-1]
                        del analyzeStack[-1]
                        del analyzeStack[-1]
                    else:
                        print("%20s %20s %20s"%("".join(analyzeStack), "".join(ipt), "Error!"))
                        return
                temp = int(analyzeStack[-1])
                analyzeStack.append(beg)
                # print(beg)
                # print(self.__beg)
                if beg == self.__beg:
                    print("%20s %20s %20s" % ("".join(analyzeStack), "".join(ipt), "Accept"))
                    return
                analyzeStack.append(str(self.__analyze[temp][beg]))
            elif ipt[0] in self.__analyze[int(analyzeStack[-1])]:
                print("%20s %20s %20s"%("".join(analyzeStack), "".join(ipt), "shift"))
                temp = int(analyzeStack[-1])
                analyzeStack.append(ipt[0])
                analyzeStack.append(str(self.__analyze[temp][ipt[0]]))
                del ipt[0]
            else:
                print("%20s %20s %20s"%("".join(analyzeStack), "".join(ipt), "Error!"))
                return



    def get_lr0(self):
        return self.__lr0

    def get_nterminal(self):
        return self.__nterminal

    def get_clo(self):
        return self.__clo

    def get_dfa(self):
        return self.__dfa

    def get_analyze(self):
        return self.__analyze


class Dfa:
    def __init__(self, item, number, status, nterminal, clo):
        self.number = number
        self.next = []
        self.nextVal = []
        self.allItem = [item]
        self.status = status
        self.addOther(nterminal, clo, [])

    def append(self, item):
        self.allItem.append(item)

    def addOther(self, nterminal, clo, already):
        judge = 0
        if self.allItem == ['']:
            return
        for item in self.allItem:
            index = item.val.find('-')
            temp = item.val[index + 1:]
            if item.pointIndex == len(temp):
                continue
            if temp[item.pointIndex] in nterminal and temp[item.pointIndex] not in already:
                already.append(temp[item.pointIndex])
                for val in clo[temp[item.pointIndex]]:

                    idt = val.find('-')
                    print("val", val[idt+1:])
                    print("end", val[:idt+1])
                    if val[idt+1:] == 'null':
                        print("end", val[:idt + 1])
                        val = val[:idt + 1]
                        # val = val[:idt+1]
                        self.status = 1
                    if Item(val, 0) not in self:
                        judge = 1
                        self.append(Item(val, 0))
        if judge:
            self.addOther(nterminal, clo, already)

    def __contains__(self, val):
        for item in self.allItem:
            if item.val == val.val and item.pointIndex == val.pointIndex:
                return True
        return False

    def __add__(self, dfa):
        # print(dfa.allItem)
        if dfa.allItem != ['']:
            # print("length=",len(dfa.allItem))
            for index, item in enumerate(dfa.allItem):
                if item not in self.allItem:
                    self.allItem.append(item)
        return self

    def __eq__(self, dfa):
        # for item in self.allItem:
        #     print(item.val, item.pointIndex)
        # print("----------------")
        # for item in dfa:
        #     print(item.val, item.pointIndex)
        # if self.allItem[0].val == 'A-d':
        # print("----------beg-------")
        # print(self.allItem[0].val, self.allItem[0].pointIndex)
        # print("-------------------------")
        # for item in dfa.allItem:
        #     print(item.val, item.pointIndex)
        # print("--------end-------------")
        count = 0
        for item in self.allItem:
            for item2 in dfa.allItem:
                if item.val == item2.val and item.pointIndex == item2.pointIndex:
                    count += 1
                    break
        if count == len(self.allItem):
            return  True
        else:
            return False


    def intersection(self, dfa):
        if dfa.allItem != ['']:
            return dfa
        else:
            return self


class Item:
    def __init__(self, val, pointIndex):
        self.val = val
        self.pointIndex = pointIndex

    def deal_str(self, s):  # 提取每个字符串中的非终结符和终结符
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
                if lst[index + 1] == 'u' and lst[index + 2] == 'l' and lst[index + 3] == 'l':
                    lst[index] = 'null'
                    del lst[index + 1]
                    del lst[index + 1]
                    del lst[index + 1]
            except:
                pass
        return lst

    def __str__(self):
        index = self.val.find('-')
        temp = self.deal_str(self.val[index + 1:])
        temp.insert(self.pointIndex, '.')
        return self.val[0:index] + "-" + "".join(temp)


def main():
    lr0 = Lr0()
    res = lr0.get_lr0()
    clo = lr0.get_clo()
    dfa = lr0.get_dfa()
    # print(dfa)
    # lr0.printDfa(dfa, [])

    # print(res)
    print("拓广文法为：")
    for key in res:
        print(key, "->", res[key])
    print("自动机为：")
    lr0.printDfa(dfa, [])
    print("分析表为：")
    analyze = lr0.get_analyze()
    for key in analyze:
        print(key, " ", analyze[key])
    Str = input("请输入待分析的字符串")
    print("分析过程为:")
    lr0.DealWidth(Str)
    # print("%20s %15s %10s"%("analyzeStack","input","action"))


if __name__ == "__main__":
    main()
