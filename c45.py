"""
:@func: C4.5算法的实现
"""
from math import log
from itertools import islice

import op_file

BASE_ENT_NUM = -1

def entropy(d_list):
    """
    计算信息熵
    :@formula: Ent(D)=-[(P1)log2(P1)+(P2)log2(P2)+(P3)log2(P3)+...+(Pn)log2(Pn)]
            其中Pi是当前集合D中第i类样本所占的比例
    :@param: d_list
    """
    row_number = len(d_list)    # 多少
    label_num = {}
    # 创建分类字典
    for data in d_list:
        if data not in label_num.keys():
            label_num[data] = 0
        label_num[data] += 1
    # print(label_num)
    # 计算信息熵
    ent = 0.0
    for key in label_num:
        prob = float(label_num[key]) / row_number
        ent -= prob * log(prob, 2)
    return ent

def ent_condition(data_set, attr):
    """
    确定属性是attr时基础的条件熵
    :@formual: H[Y|X]=∑P(x)H(Y|X=x)
    :@param: data_set
    :@param: attr
    """
    ent_cond = 0.0
    attr_num = {}    # 存放的是某个属性的所有取值
    for data in data_set:
        if attr == data[0]:
            data_len = len(data) - 1
            for i in range(1, len(data)):
                if data[i] not in attr_num.keys():
                    attr_num[data[i]] = [i]
                else:
                    attr_num[data[i]].append(i)
    # 求给定条件下的baseEntropy
    for key in attr_num:
        attr_num_cond = []
        for num in attr_num[key]:
            label_cond = data_set[BASE_ENT_NUM][num]   # baseEntropy
            attr_num_cond.append(label_cond)
        ent = entropy(attr_num_cond)
        ent_cond += len(attr_num[key])/data_len*ent
    return ent_cond

def get_gain_ratio(data_set):
    """
    获得最大的属性的信息增益率
    :@formula: Gain_ratio(D, attr)=Gain(D, attr)/IV(a),
            其中:IV(a)=-∑(v=1)[(DV)/D]log[(DV)/D]
    :@param: data_set
    :@return: 最大属性的信息增益率以及属性
    """
    gain_ratio_all = {}
    base_ent = entropy(data_set[-1][1:])
    for data in islice(data_set, 1, len(data_set)-1):
        attr = data[0]
        attr_ent_cond = ent_condition(data_set, attr)
        attr_info_gain = base_ent - attr_ent_cond
        attr_gain_radio = attr_info_gain/entropy(data[1:])
        gain_ratio_all[attr] = attr_gain_radio
    gain_ratio_best_lst = sorted(gain_ratio_all.items(), key=lambda item: item[-1], reverse=True)
    gain_ratio = gain_ratio_best_lst[0]
    return gain_ratio

if __name__ == "__main__":
    FLNAME = "/home/lyh/mycode/decision_tree/w_data.csv"
    CONT_COL = op_file.read_csv_by_col(FLNAME)
    print(get_gain_ratio(CONT_COL))
