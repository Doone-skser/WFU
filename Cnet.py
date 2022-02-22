from requests import get, post
from lxml import html
from Crypto.Cipher import AES
import base64
from pywifi import PyWiFi
from pywifi import const
import json


class CNET(PyWiFi):
    def __init__(self, ):
        super().__init__()
        self.AES_MODE = AES.MODE_CBC  # AES加密模式
        self.url_login_get = 'http://210.44.64.60/gportal/web/login'
        self.url_login_post = 'http://210.44.64.60/gportal/web/authLogin'
        self.url_logout = 'http://210.44.64.60/gportal/web/authLogout'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
        }
        self._accout = None
        self._psw = None
        self._key = '1234567887654321'.encode("utf-8")  # AES16位自定义秘钥
        self.login_sign = None
        self.login_iv = None

    # 方法集合
    def main(self, _act: str, _pwd: str):
        self._accout = _act
        self._psw = _pwd
        return self._login()

    # 获取cookie以及加密
    def _cookie(self):
        response = get(url=self.url_login_get, headers=self.headers)
        self.headers.update(response.cookies.get_dict())
        selector = html.fromstring(response.text)
        ul = selector.xpath('//*[@id="frmLogin"]/ul/input')
        wifi_name = ul[0].xpath("@value")[0]
        ip = ul[2].xpath("@value")[0]
        login_sign = ul[8].xpath("@value")[0]
        self.login_iv = ul[9].xpath("@value")[0]
        url = "nasName=" + wifi_name + "&nasIp=&userIp=" + ip + "&userMac=&ssid=&apMac=&pid=20&vlan=&sign=" + \
              login_sign + "&iv=" + self.login_iv + "&name=" + self._accout + "&password=" + self._psw
        # print(url)
        data = self.add_to_16(url)
        cry = AES.new(self._key, self.AES_MODE, iv=self.login_iv.encode('utf-8'))
        self.login_sign = base64.encodebytes(cry.encrypt(data)).decode('ascii')

    # 登陆方法
    def _login(self):
        self._cookie()
        post_data = {
            "data": self.login_sign,
            "iv": self.login_iv
        }
        try:
            response = post(self.url_login_post, data=post_data, headers=self.headers, timeout=3).json()
            if "密码错误" in response['info']:
                return "密码错误"
            if "账号不存在" in response['info']:
                return "账号错误"
            if "认证成功，稍后跳转" in response['info']:
                return "认证成功"
            if "认证拒绝" in response['info']:
                return "认证拒绝"
            if "已认证" in response['info']:
                return "重复认证"
            if "频繁" in response['info']:
                return "操作频繁"
            return response['info']
        except:
            return '认证超时'

    # 检查wifi是否连接
    @classmethod
    def check_wifi(cls):
        try:
            wifi = PyWiFi()
            ifaces = wifi.interfaces()[0]
            if ifaces.status() == const.IFACE_CONNECTED:
                return True
            else:
                return False
        except:
            return False

    def logout(self):
        try:
            res = post(self.url_logout).json()
            return res['info']
        except:
            return '下线失败，请检查网络连接是否正常！'

    # 获取在线时长
    @classmethod
    def get_online_time(cls):
        url = 'http://210.44.64.60/gportal/web/queryAuthState'
        try:
            response = get(url, timeout=3).json()
            time = response['data']['data']['onlineTime']
            if time == 0:
                return '未认证或服务器错误'

            else:
                secs = int(time)
                m, s = divmod(secs, 60)
                h, m = divmod(m, 60)
                res = str(h) + "时" + str(m) + "分" + str(s) + "秒"
                return res
        except:
            return '时间服务器失去响应'

    # 处理加密缺位问题
    @classmethod
    def add_to_16(cls, text):
        if len(text.encode('utf-8')) % 16:
            add = 16 - (len(text.encode('utf-8')) % 16)
        else:
            add = 0
        text = text + ('\0' * add)
        return text.encode('utf-8')

    # 检查网络连接
    @classmethod
    def check_net(cls, url=None):
        try:
            if url:
                res = get(url, timeout=1)
                if res.status_code == 200:
                    return True
                else:
                    return False
            else:
                res = get("http://www.baidu.com", timeout=1)
                if res.status_code == 200:
                    return True
                else:
                    return False
        except:
            return False

    @classmethod
    def get_version(cls, version):
        try:
            url = "https://o.nvidia.fun:11111/update"
            data = {
                "version": version
            }
            headers = {
                "Content-Type": "application/json;charset=utf8"
            }
            res = post(url=url, data=json.dumps(data), headers=headers, timeout=1).json()
            return res
        except:
            return None

    @classmethod
    def post_cna(cls, action, numbers, version):
        try:
            url = "https://o.nvidia.fun:11111/m5h3K2LMgRq9IiUI"
            data = {
                'numbers': numbers,
                'action': action,
                'version': version
            }
            headers = {
                "Content-Type": "application/json;charset=utf8"
            }
            res = post(url=url, data=json.dumps(data), headers=headers, timeout=1).json()
            return res
        except:
            return None
