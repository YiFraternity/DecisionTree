### 决策树，ID3，C.45算法的分别实现
# 决策树学习算法
    1, IF D中的样本全部属于同一类 THEN:
           将node标记为C类叶子结点;RETURN
       END IF
    2, IF A=∅ ,OR D中的样本在A上取值相同 THEN:
           将node标记为叶子结点，其类别标记为D中样本最多的类;RETURN
       END IF
    3, 从A中选择最优划分属性ai;
    4, FOR ai的每一个值value DO:
           为node生成一个分支;令Dv表示D中在ai上取值为value的样本子集;
           IF Dv为空 THEN:
               将分支结点标记为叶子节点，其类标标记为Ｄ中样本最多的类;RETURN
           ELSE:
               以create_tree_id3(Dv, A|{ai})为分支结点
           END IF
       END FOR
# id3.py
    ID3进行选择最优划分属性
    利用信息增益进行最优划分属性
    # 信息增益公式:Gain(D,attr)=BaseEntropy - H(BaseEntropy|attr)
# c45.py
    C4.5进行选自己最优属性划分
    利用增益率进行最优属性划分
    # 增益率公式: Gain_ratio(D, attr)=Gain(D, attr)/IV(a),
                其中:IV(a)=-∑(v=1)[(DV)/D]log[(DV)/D],即属性a的熵值
# op_file.py
    对文件进行操作
# w_data.csv
    西瓜数据集2.0的表格
# w_data_code.csv
    西瓜数据集2.0表格编码之后的表格(ps:此程序就没有用到)
# w_dataset.txt
    w_data->w_data_code如何进行编码的说明
