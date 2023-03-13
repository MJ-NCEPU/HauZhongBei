import pandas as pd
import jieba
import warnings
import re
warnings.filterwarnings('ignore')
import json

# 第一大部分，查全率，查准率的计算
def judge(strs):
    strs = strs.split(",")
    l = []
    for s in strs:
        s = s.replace('[',"").replace(']',"").replace("'","")
        l.append(int(s))
    return l

def tongji(l1,l2):
    listes = []
    for i in range(988):
        l = []
        l.append(l1[i])
        ls = judge(l2[i])
        for s in ls:
            l.append(s)
        listes.append(l)
    return listes


def readdata1(data1s1,data1s2):
    ls1 = []
    ls2 = []
    ls2.append(data1s1[0])
    ls2.append(data1s2[0])
    for i in range(len(data1s2)-1):
        i = i + 1
        if data1s1[i] == data1s1[i-1]:
            ls2.append(data1s2[i])
        else:
            ls1.append(ls2)
            ls2 = []
            ls2.append(data1s1[i])
            ls2.append(data1s2[i])
    return ls1

def judgeidda(num,iddata2):
    flag = 0
    k = -1
    for j in range(len(iddata2)):
        if num == iddata2[j][0]:
            flag = 1
            k = j
            break
    if flag == 1:
        return True,k
    else:
        return False,0

def compareequal(s1,s2):
    if len(s1) != len(s2):
        return  False
    else:
        for i in range(len((s1))):
            if s1[i] not in s2:
                return False
    return True

def compareequal2(s1,s2):
    flag = 0
    for i in range(len((s1))):
        if s1[i] in s2:
             flag = 1
    if flag == 1:
        return True
    else:
        return False

def chaquanzhun(iddata1, iddata2):
    len1 = len(iddata1)
    len2 = len(iddata2)
    k = 0
    for i in range(len(iddata1)):
        if iddata1[i] in iddata2:
            k = k + 1
    recallrate = k/len2
    precisionrate = k/len1
    # 查全率，查准率
    return recallrate, precisionrate



def compare(iddata2,iddata1):
    l_i_q_z = []
    for i in range(len(iddata1)):
        lt = []
        t1,j = judgeidda(iddata1[i][0], iddata2)
        if t1 == True:
            t = compareequal2(iddata1[i], iddata2[j])
            if t == True:
                recallrate, precisionrate = chaquanzhun(iddata1[i], iddata2[j])
                lt.append(iddata1[i][0])
                lt.append(recallrate)
                lt.append(precisionrate)
                l_i_q_z.append(lt)
    return l_i_q_z


def main2():
    data1 = pd.read_csv(r'F:\taidibei\huazhongbei\shuju\0.2--1至7294.csv', sep=',', encoding='utf-8',
                        error_bad_lines=False)
    data2 = pd.read_csv(r'F:\taidibei\huazhongbei\附件2.csv', sep=',', encoding='utf-8', error_bad_lines=False)

    # id_data2是附件2中lable = 1 的questionID和duplicates
    # [99850, 95677],
    # [104165, 104161],
    # [101403, 100311],
    id_data2 = tongji(data2['questionID'], data2['duplicates'])

    # id_data1为问题相似度大于0.3的questionID和duplicates
    # [63022, 62860],
    # [46866, 46762],
    # [97939, 80376]
    id_data1 = readdata1(data1['id'], data1['du'])

    # l_i_q_z返回一个questionID和查全率,查准率
    # [99850, 0.5, 0.5],
    # [104165, 1.0, 1.0],
    # [101403, 1.0, 1.0]
    l_i_q_z = compare(id_data2, id_data1)

    f = open(r'F:\taidibei\huazhongbei\l_i_q_z0.2.csv', "w+")
    f.write('问题id'+","+'查全率'+","+"查准率"+"\n")
    for i in range(len(l_i_q_z)):
        f.write(str(l_i_q_z[i][0]) + ",")
        f.write(str(l_i_q_z[i][1]) + ",")
        f.write(str(l_i_q_z[i][2]) + "\n")


# 第二大部分，相似度的计算
# 2-garm分词
def n_garm(splits):
    l_str = []
    for i in range(len(splits)):
        lstr1 = []
        if i + 1 < len(splits):
            lstr1.append(splits[i])
            lstr1.append(splits[i + 1])
            l_str.append(lstr1)
    return l_str


# 获取问题和id
def contextCandel(data, num):
    listes = []
    for i in range(len(data)):
        datanum = []
        str = data[i].strip()
        str = re.sub('[\s+]', '', str)
        split_words = [x for x in jieba.cut(str) if x not in
                       stopone(r'F:\taidibei\huazhongbei\stop_words.utf8')]
        print(split_words)
        split_words = n_garm(split_words)
        datanum.append(num[i])
        datanum.append(split_words)
        listes.append(datanum)
    return listes


# 调用停词表
def stopone(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [l.strip() for l in f]


# n-garm比较
def judge(l, a, b):
    count1 = 0
    count2 = 0
    for i in range(len(l[a][1])):
        for j in range(len(l[b][1])):
            if l[a][1][i] == l[b][1][j]:
                count1 = count1 + 1
                break
    for i in range(len(l[b][1])):
        for j in range(len(l[a][1])):
            if l[b][1][i] == l[a][1][j]:
                count2 = count2 + 1
                break
    return (count1 + count2) / (len(l[a][1]) + len(l[b][1]))


# 计算相似度并存入csv
def compare_judge(l):
    f = open(r'F:\taidibei\huazhongbei\number.csv', "w+")
    for i in range(len(l)-1):
        k = i + 1
        for j in range(len(l)-k):
            if j + k < len(l):
                number = judge(l, i, j + k)
                # 选择相似度大于0.2的存储
                if number > 0.2:
                    f.write(str(l[i][0])+",")
                    f.write(str(l[j + k][0]) + ",")
                    f.write(str(number) + "\n")
    f.close()


def main1():
    data = pd.read_csv(r'F:\taidibei\huazhongbei\附件1.csv', sep=',', encoding='utf-8', error_bad_lines=False)
    l = contextCandel(data['translated'], data['id'])
    compare_judge(l)


def main3():
    data = pd.read_csv(r'F:\taidibei\huazhongbei\相似度大于0.2--1至7294.csv', sep=',', encoding='utf-8',
                       error_bad_lines=False)
    # 计算相似度大于0.2的csv里面除去重复的有多少数据
    ls1 = []
    ls2 = []
    ls2.append(data[0])
    count = 1
    for i in range(len(data) - 1):
        i = i + 1
        if data[i] == data[i - 1]:
            count = count + 1
        else:
            ls2.append(count)
            ls1.append(ls2)
            ls2 = []
            ls2.append(data[i])
            count = 1
    for i in ls1:
        print(i)


#按重复数量从大到小返回一个[[id,数量],[id,数量],[id,数量]]的列表
def main4(data, topK=806):
    tf_dic = {}
    for w in data:
        tf_dic[w] = tf_dic.get(w, 0)+1
    return sorted(tf_dic.items(), key=lambda x : x[1], reverse=True)[:topK]


def main():
    k = eval(input("请输入一个数字："))
    print("1.第二大部分，相似度的计算,写进csv.")
    print("2.第一大部分，查全率，查准率的计算，写近csv.")
    print("3.计算相似度大于0.2的csv里面除去重复的有多少数据.")
    print("4.重复数量从大到小返回一个[[id,数量],[id,数量],[id,数量]]的列表.")
    if k == 1:
        main1()
    if k == 2:
        main2()
    if k == 3:
        main3()
    if k == 4:
        main4()

if __name__ == '__main__':
    main()
