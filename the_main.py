import numpy as np
from sklearn.neural_network import MLPRegressor  # 多层线性回归
from sklearn.preprocessing import StandardScaler
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import jieba
import jieba.posseg as psg
import re

#导入词性表，编程map的映射方便寻找
r_one=re.compile(r'(.{0,1000}.)\t')
r_two=re.compile(r'\t(.{0,1000}.)')
cixing_int={}
with open("F:\\python\\chatbotcorpus\\cixing_biaozhu",'r',encoding = 'utf-8') as fp:
    for i in fp.readlines():
        r1=r_one.findall(i)
        r2=r_two.findall(i)
        cixing_int[r1[0]]=int(r2[0])
print(cixing_int)

#构成神经训练用的数据
r_one=re.compile(r'(.{0,1000}.)\t')
r_two=re.compile(r'\t(.{0,1000}.)')
xunhuan_cishu=10
N=xunhuan_cishu
data=[]
with open("F:\\python\\chatbotcorpus\\xiaohuangji.tsv",'r',encoding = 'utf-8') as fp:
    for i in fp.readlines():
        r1=r_one.findall(i)
        r2=r_two.findall(i)
        if r1==[] or r2==[]:
           continue
        if xunhuan_cishu==0:
            break

        Q=[]#问题的词性序列
        R=[]#回答的词性序列
        for j in psg.cut(r1[0]):
            Q.append(j.flag)
        for k in psg.cut(r2[0]):
            R.append(k.flag)
        print(Q,R)


        linshi_data=[] #暂时储存单值的
        for j in range(5):
            if j<len(Q):
                cixing=Q[j]
                linshi_data.append(float(cixing_int[cixing]))
            else:
                linshi_data.append(0.0)


        for k in range(5):
            if k<len(R):
                cixing=R[k]
                linshi_data.append(float(cixing_int[cixing]))
            else:
                linshi_data.append(0.0)
        linshi_data.append(1.0)
        data.append(linshi_data)
        xunhuan_cishu=xunhuan_cishu-1
print(data)

#进行神经网络构造
dataMat = np.array(data)
X=dataMat[:,0:10]
y=[]
for i in range(N):
    y.append(1.0)
y=np.array(y)    
print(X)
print(y)
#进行归一化
scaler = StandardScaler() # 标准化转换
scaler.fit(X)  # 训练标准化对象
X = scaler.transform(X)   # 转换数据集
print(X)
print("YYYYYYY")
print(y)
solver='lbfgs'
# MLP的求解方法：L-BFGS 在小数据上表现较好，Adam 较为鲁棒，SGD在参数调整较优时会有最佳表现（分类效果与迭代次数）；SGD标识随机梯度下降。
# alpha:L2的参数：MLP是可以支持正则化的，默认为L2，具体参数需要调整
# hidden_layer_sizes=(5, 2) hidden层2层,第一层5个神经元，第二层2个神经元)，2层隐藏层，也就有3层神经网络
clf = MLPRegressor(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=1)
clf.fit(X, y)
# print('预测结果：', clf.predict([[1, 2, 0, 0, 0,2, 3, 4, 1, 0]]))  # 预测某个输入对象

# cengindex = 0
# for wi in clf.coefs_:
#     cengindex += 1  # 表示底第几层神经网络。
#     print('第%d层网络层:' % cengindex)
#     print('权重矩阵维度:',wi.shape)
#     print('系数矩阵：\n',wi)
bot = ChatBot(
    'Terminal',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch'
    ],
    database_uri='mongodb://localhost:27017/xiaohuangji_db'
)
houxuan_result=[]#候选结果进行储存
user_input = input()
for i in range(10):
    bot_response = bot.get_response(user_input)
    print(bot_response)
    houxuan_result.append(str(bot_response))


Q=[]
for j in psg.cut(user_input):
    Q.append(j.flag)
linshi_data=[]
for j in range(5):
    if j<len(Q):
        cixing=Q[j]
        linshi_data.append(float(cixing_int[cixing]))
    else:
        linshi_data.append(0.0)
maxflag=0
flag=0
maxshu=0.0
for i in houxuan_result:
    R=[]
    for j in psg.cut(i):
        R.append(j.flag)
    ceishi_data=[]
    for k in linshi_data:
        ceishi_data.append(k)
    for j in range(5):
        if j<len(R):
            cixing=R[j]
            ceishi_data.append(float(cixing_int[cixing]))
        else:
            ceishi_data.append(0.0)
    zhenshidata=[]
    zhenshidata.append(ceishi_data)
    zhenshidata=np.array(zhenshidata)
    print(zhenshidata)
    shuzhi=clf.predict(zhenshidata)[0]
    if shuzhi>maxshu:
        maxshu=shuzhi
        maxflag=flag
    flag=flag+1

print(houxuan_result[maxflag])



        


