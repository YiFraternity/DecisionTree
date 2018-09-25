"""
创建决策树
"""
import operator
import numpy as np

import c45
import id3
import op_file

BASE_ENT_NUM = -1

def split_data_set(data_set, axis, attr):
    """
    划分数据集,提取数据集中包括属性是该属性值的所有数据
    :@param data_set: 数据集
    :@param axis:属性值
    :@param attr:属性
    """
    i = 1
    i_set = []
    data_set_splited = []
    for data in data_set:
        if data[0] == attr:
            for attr_val in data[1:]:
                if attr_val == axis:
                    i_set.append(i)
                    i += 1
                else:
                    i += 1
    data_set = np.array(data_set)
    for i in i_set:
        data_row = data_set[:, i]   # type:numpy.array
        data_set_splited.append(list(data_row))
    data_set_splited = np.transpose(data_set_splited)
    attrs = [data[0] for data in data_set]
    data_set_splited = np.insert(data_set_splited, 0, values=attrs, axis=1)
    i = 0
    for data in data_set_splited:
        if data[0] != attr:
            i += 1
        else:
            break
    data_set_splited = np.delete(data_set_splited, i, axis=0)
    data_set_splited = np.ndarray.tolist(data_set_splited)
    # print(type(data_set_splited))
    # print(data_set_splited)
    return data_set_splited

def majority_cnt(class_lst):
    '''
    数据集已经处理了所有属性，但是类标签依然不是唯一的，
    此时我们需要决定如何定义该叶子节点，在这种情况下，
    我们通常会采用多数表决的方法决定该叶子节点的分类
    '''
    class_count = {}
    for vote in class_lst:
        if vote not in class_count.keys():
            class_count[vote] = 0
        class_count[vote] += 1
    class_count_sort = sorted(
        class_count.items(), key=operator.itemgetter(1), reverse=True)
    return class_count_sort[0][0]


def create_tree_id3(data_set, labels):
    """
    使用ID3算法创建树
    :@Input:  数据集和标签
    :@Output: 决策树
    :@flow: 01, IF D中的样本全部属于同一类 THEN:
                    将node标记为C类叶子结点;RETURN
                END IF
            02, IF A=∅ ,OR D中的样本在A上取值相同 THEN:
                    将node标记为叶子结点，其类别标记为D中样本最多的类;RETURN
                END IF
            03, 从A中选择最优划分属性ai;
            04, FOR ai的每一个值value DO:
                    为node生成一个分支;令Dv表示D中在ai上取值为value的样本子集;
                    IF Dv为空 THEN:
                        将分支结点标记为叶子节点，其类标标记为Ｄ中样本最多的类;RETURN
                    ELSE:
                        以create_tree_id3(Dv, A|{ai})为分支结点
                    END IF
                END FOR
    """
    class_lst = data_set[BASE_ENT_NUM][1:]  # 该类别第一个是类别名称
    if class_lst.count(class_lst[0]) == len(class_lst):
        # 如果类别完全相同，停止划分
        return class_lst[0]
    if len(data_set[1]) == 2:
        # 遍历完所有特征值时，返回数量最多的
        return majority_cnt(class_lst)
    # 获取最佳划分属性
    best_attr = id3.get_info_gain(data_set)
    best_attr_label = best_attr[0]
    print("此时最优索引为", end=":")
    print(best_attr_label)
    id3_tree = {best_attr_label:{}}
    labels.remove(best_attr_label) # 删除此时属性
    # 得到列表包括节点所有的属性值
    attr_values = []
    for example in data_set:
        if example[0] == best_attr[0]:
            attr_values = example[1:]
    attr_val_set = set(attr_values)
    for value in attr_val_set:
        sub_labels = labels[:]
        # 递归调用创建决策树
        id3_tree[best_attr_label][value] = create_tree_id3(
            split_data_set(data_set, value, best_attr[0]), sub_labels)
    return id3_tree

def create_tree_c45(data_set, labels):
    """
    利用C4.5算法创建树
    :@Input:  数据集和标签
    :@Output: 决策树
    :@flow: 01, IF D中的样本全部属于同一类 THEN:
                    将node标记为C类叶子结点;RETURN
                END IF
            02, IF A=∅ ,OR D中的样本在A上取值相同 THEN:
                    将node标记为叶子结点，其类别标记为D中样本最多的类;RETURN
                END IF
            03, 从A中选择最优划分属性ai;
            04, FOR ai的每一个值value DO:
                    为node生成一个分支;令Dv表示D中在ai上取值为value的样本子集;
                    IF Dv为空 THEN:
                        将分支结点标记为叶子节点，其类标标记为Ｄ中样本最多的类;RETURN
                    ELSE:
                        以create_tree_c45(Dv, A|{ai})为分支结点
                    END IF
                END FOR
    """
    class_lst = data_set[BASE_ENT_NUM][1:]  # 该类别第一个是类别名称
    if class_lst.count(class_lst[0]) == len(class_lst):
        # 如果类别完全相同，停止划分
        return class_lst[0]
    if len(data_set[1]) == 2:
        # 遍历完所有特征值时，返回数量最多的
        return majority_cnt(class_lst)
    # 获取最佳划分属性
    best_attr = c45.get_gain_ratio(data_set)
    best_attr_label = best_attr[0]
    print("此时最优索引为", end=":")
    print(best_attr_label)
    c45_tree = {best_attr_label:{}}
    labels.remove(best_attr_label) # 删除此时属性
    # 得到列表包括节点所有的属性值
    attr_values = []
    for example in data_set:
        if example[0] == best_attr[0]:
            attr_values = example[1:]
    attr_val_set = set(attr_values)
    for value in attr_val_set:
        sub_labels = labels[:]
        # 递归调用创建决策树
        c45_tree[best_attr_label][value] = create_tree_id3(
            split_data_set(data_set, value, best_attr[0]), sub_labels)
    return c45_tree

if __name__ == "__main__":
    FLNAME = "/home/lyh/mycode/decision_tree/w_data.csv"
    CONT_COL = op_file.read_csv_by_col(FLNAME)
    LABELS = [ATTR[0] for ATTR in CONT_COL][1:]
    ID3_TREE = create_tree_id3(CONT_COL, LABELS)
    print(ID3_TREE)
    LABELS = [ATTR[0] for ATTR in CONT_COL][1:]
    C45_TREE = create_tree_c45(CONT_COL, LABELS)
    print(C45_TREE)
