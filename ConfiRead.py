import json
import os


# 配置存储位置
directory = os.getenv('APPDATA') + r"\WFU_CNA"
file = os.getenv('APPDATA') + r"\WFU_CNA\config"


# 判断文件是否存在
def isExist():
    try:
        with open(file, "r", encoding='utf-8') as f:
            return True
    except FileNotFoundError:
        return False


# 创建配置文件
def createConfi(accout, password, key):
    if not isExist():
        try:
            os.mkdir(directory)
        except:
            pass
    data_dict = {
        'accout': accout,
        'password': password,
        'key': key
    }
    try:
        with open(file, "w", encoding='utf-8') as file_data:
            json.dump(data_dict, file_data)
        return True
    except:
        return False


# 读取配置文件
def readData():
    try:
        with open(file, "r", encoding='utf-8') as file_data:
            return json.load(file_data)
    except:
        return False


if __name__ == '__main__':
    print(file)