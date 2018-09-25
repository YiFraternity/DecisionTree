"""
:@func: 读取文件
"""
import csv
from itertools import islice

def read_csv_by_row(flname):
    """
    逐行读取CSV文件内容
    :@param: flname(文件名)
    """
    file_name = open(flname)
    conts = csv.reader(file_name, delimiter=',')
    content = []
    for cont in islice(conts, 1, None):
        content.append(cont)
    # print(content)
    return content

def read_csv_by_col(flname):
    """
    按列读取CSV文件内容
    :@param: flname(文件名)
    """
    file_name = open(flname)
    conts = csv.reader(file_name, delimiter=',')
    content = []
    numbers = []       # 编号
    colors = []        # 色泽
    gentis = []        # 根蒂
    knocks = []        # 敲声
    veins = []         # 纹理
    umbils = []        # 脐部
    touchs = []        # 触感
    gorbs = []         # 好坏瓜
    for row in islice(conts, 0, None):
        number = row[0]
        color = row[1]
        genti = row[2]
        knock = row[3]
        vein = row[4]
        umbil = row[5]
        touch = row[6]
        gorb = row[7]
        numbers.append(number)
        colors.append(color)
        gentis.append(genti)
        knocks.append(knock)
        veins.append(vein)
        umbils.append(umbil)
        touchs.append(touch)
        gorbs.append(gorb)
    content.append(numbers)
    content.append(colors)
    content.append(gentis)
    content.append(knocks)
    content.append(veins)
    content.append(umbils)
    content.append(touchs)
    content.append(gorbs)
    # print(content)
    return content

if __name__ == "__main__":
    FLNAME = "/home/lyh/mycode/decision_tree/w_data.csv"
    read_csv_by_col(FLNAME)
    read_csv_by_row(FLNAME)
