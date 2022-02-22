import winreg


def read_reg():
    location = r"Software\Microsoft\Windows\CurrentVersion\Run"
    # 获取注册表该位置的所有键值
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, location)
    try:
        winreg.QueryValueEx(key, "yjrz")
        return True
    except:
        winreg.CloseKey(key)
        return False


def write(accout, password):
    """
    :param accout: 账户
    :param password: 密码
    :return: 成功则返True，失败返回False
    """
    location = r"Software"
    # 获取注册表该位置的所有键值
    try:
        key_w = winreg.OpenKey(winreg.HKEY_CURRENT_USER, location)
        new_key = winreg.CreateKey(key_w, "WFU_CNA")
        winreg.SetValue(new_key, "accout", winreg.REG_SZ, accout)
        winreg.SetValue(new_key, "password", winreg.REG_SZ, password)
        winreg.CloseKey(key_w)
        winreg.CloseKey(new_key)
        return True
    except:
        return False


def readconfi():
    """
    :return: 成功则返数据，失败返回False
    """
    pwd_location = r"Software\WFU_CNA\password"
    act_location = r"Software\WFU_CNA\accout"

    # 获取注册表该位置的所有键值
    try:
        key_pwd = winreg.OpenKey(winreg.HKEY_CURRENT_USER, pwd_location)
        key_act = winreg.OpenKey(winreg.HKEY_CURRENT_USER, act_location)
        try:
            accout = winreg.EnumValue(key_act, 0)
            password = winreg.EnumValue(key_pwd, 0)
            data = {
                "accout": accout[1],
                "password": password[1]
            }
            return data
        except:
            winreg.CloseKey(key_act)
            winreg.CloseKey(key_pwd)
            return False
    except:
        return False
