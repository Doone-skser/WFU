import json


# 判断文件是否存在
def isExist():
    try:
        with open(r"D:\WFU_CNA.conf", "r", encoding='utf-8') as f:
            return True
    except FileNotFoundError:
        return False


# 创建配置文件
def createConfi(accout, password, key):
    data_dict = {
        'accout': accout,
        'password': password,
        'key': key
    }
    try:
        with open(r"D:\WFU_CNA.conf", "w", encoding='utf-8') as file_data:
            json.dump(data_dict, file_data)
        return True
    except:
        return False


# 读取配置文件
def readData():
    try:
        with open(r"D:\WFU_CNA.conf", "r", encoding='utf-8') as file_data:
            return json.load(file_data)
    except:
        return False
