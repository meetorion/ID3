import linecache
import math
import sys
sys.setrecursionlimit(100000) #例如这里设置为十万
from graphviz import Digraph
g = Digraph('G', filename='final.gv')
#声明一个全局字典来存储编号(列号)和节点的映射关系cnt => row
cntToNode={}
# rowToName={'0':'Outlook', '1':'Temper.', '2':'Humidity', '3':'Windy'}
# nameToRow={'Outlook':'0', 'Temper.':'1', 'Humidity':'2', 'Windy':'3'}
rowToName = {}
nameToRow = {}
edgeVal = {} #存　u=>v 对应的边的值
nodeVal = {} #存节点u对应的值
#一个节点需要存储的信息有它的邻接节点的编号列表
cnt = 0
dict={}
hasSelected=[]

def solve():
    init(read("dna.data"))
    root = create(read("dna.data"))
    g.view()
    exam(root, read("dna.test"))

#测试通过
def read(filename):
    dataSet = []
    ans = []
    with open(filename, 'r+') as file:
        for line in file:
            tmp = list(line.split(' '))
            dataSet.append(tmp)
    for line in dataSet:
        val = line[-1][0]
        line = line[:-1]
        line.append(str(val))
        ans.append(line)
    return ans

def create(dataSet):
    uniqueLabel = set([example[-1] for example in dataSet])
    if len(uniqueLabel) == 1:
        return None
    entropy = cal(dataSet)
    #选出信息增益最大的特征　输入：数据集　输出特征所在列列号
    row = select(dataSet)
    global cnt
    cnt = cnt + 1
    ans = cnt
    global cntToNode
    cntToNode[cnt] = row
    global g
    g.node(str(cnt), label=rowToName[str(cntToNode[cnt])])
    nodeVal[cnt] = rowToName[str(cntToNode[cnt])]

    #根据列号分出子集并递归创建子树
    uniqueValue = set([example[row] for example in dataSet])
    if len(uniqueValue) <= 1:
        return None

    edgeValue = None
    for value in uniqueValue:
        subDataSet = splitDataSet(dataSet, value, row)
        tmp = create(subDataSet)
        if tmp == None:
            cnt = cnt + 1
            tmp = cnt
            label = subDataSet[0][-1]
            g.node(str(cnt), label='标签为：'+str(label))
            nodeVal[cnt] = str(label)
        else:
            g.node(str(tmp), label=rowToName[str(cntToNode[tmp])])
            nodeVal[tmp] = rowToName[str(cntToNode[tmp])]
        add_edge(ans, tmp, value)
    return ans

#测试通过
def cal(dataSet):
    labelCounts={}
    labelSum=len(dataSet)
    ans = 0
    for line in dataSet:
        label = line[-1]
        if label not in labelCounts:
            labelCounts[label] = 1
        else:
            labelCounts[label] += 1
    for label in labelCounts:
        pro = labelCounts[label]/labelSum
        ans -= pro * math.log(pro, 2)
    return ans

#测试通过
def select(dataSet):
    #每个特征划分
    best = 1000000
    ans = -1
    attrSum = len(dataSet[0]) - 1
    attrCounts = {}
    for i in range(attrSum):
        uniqueValue = set([example[i] for example in dataSet])
        curEntropy = 0
        for value in uniqueValue:
            sum = 0
            for line in dataSet:
                tmp = line[i]
                if value == tmp:
                    sum += 1
            subDataSet = splitDataSet(dataSet, value, i)
            pro = sum/len(dataSet)
            curEntropy += pro*cal(subDataSet)
        # print(curEntropy)
        if curEntropy < best:
            best = curEntropy
            ans = i
    return ans

#测试通过
def splitDataSet(dataSet, value, row):
    ans = []
    for line in dataSet:
        if line[row] == value:
            ans.append(line)
    return ans

def add_edge(u, v, value): #u ==> v 并且在边上写value
    if u not in dict:
        dict[u] = set()
        dict[u].add(v)
    else:
        dict[u].add(v)
    g.edge(str(u), str(v), label=str(value))
    edgeVal[str(u)+str(v)] = str(value)

def init(dataSet):
    numAttr = len(dataSet[0]) - 1
    for i in range(numAttr):
        rowToName[str(i)] = str(i)
        nameToRow[str(i)] = str(i)
def exam(root, dataSet): #输入：决策树的根节点编号，测试集　输出：错误率
    # num = len(dataSet[0])
    num = 0
    sum = 0
    for line in dataSet:
        num += 1
        if not_ok(line, root):
            sum += 1
    faultPro = sum/num
    print("错误率为：", faultPro)
    return faultPro

def not_ok(line, root):
    i = 0
    row = int(nameToRow[nodeVal[root]])
    while i < len(line):
        u = root
        if len(dict[u]) == 0:
            label = nodeVal[u]
            if line[-1] == label:
                return False
            else:
                return True
        for v in dict[u]:
            tmp = str(u)+str(v)
            other = line[row]
            val = edgeVal[tmp]

            if val == line[row]:
                root = v
                i += 1

                attr = nodeVal[v]
                if isLabel(attr):
                    return attr != line[-1]
                row = int(nameToRow[nodeVal[root]])
                break
    return True
def isLabel(attr):
    if attr == '1' or attr == '2' or attr == '3':
        return True
    return False

if __name__ == '__main__':
    solve()


