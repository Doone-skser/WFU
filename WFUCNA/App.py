import os
import threading
import time
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QWidget
from PyQt5.Qt import QPushButton
from PyQt5.Qt import QLabel
from PyQt5.Qt import QApplication
from PyQt5.Qt import QCheckBox
from PyQt5.Qt import QToolButton
from PyQt5.Qt import QDialog
from PyQt5.Qt import QLineEdit
from PyQt5.Qt import QMessageBox
import sys
from Cnet import CNET
from Autorun import AutoRun
import RegRead
import webbrowser
import ConfiRead
from requests import get
import Ico

# 解决根目录无法在打包后正确获取的问题
gen_path = os.path.dirname(os.path.realpath(sys.argv[0]))


class Window(QWidget):
    # 初始化
    def __init__(self):
        super().__init__()
        self.new_login = CNET()
        self.version = "1.3"   # 版本号信息

        # 检查是否有配置文件如果没有则生成
        self.dl_confi = QDialog(self)
        self.dl_confi.setFixedSize(390, 400)
        self.dl_confi.setWindowTitle("校园网助手")
        self.dl_confi.setWindowIcon(QIcon(':/0.ico'))
        self.dl_confi.geometry().center()
        self.dl_confi.setWindowOpacity(0.9)
        self.dl_confi.setStyleSheet('background-color: #2A2A2A; color: white')

        if not ConfiRead.isExist():
            if not RegRead.readconfi():
                # 第一次弹窗
                lb_welcome = QLabel(self.dl_confi)
                lb_welcome.setText("欢迎使用")
                lb_welcome.setStyleSheet("font-size: 38px; font: bold;")
                lb_welcome.adjustSize()
                lb_welcome.move(120, 30)

                lb = QLabel("温馨提示:\n1、第一次使用请输入您的账号以及密码!\n2、账号等信息保存在D盘的WFU_CNA.conf文件里。\n"
                            "3、请不要删除它，否则下次启动将会弹出本窗。\n4、可以在生成的conf文件里修改账号或密码.", self.dl_confi)
                lb.setStyleSheet("font-size: 18x; color: #FF00FF; font: bold")
                lb.move(10, 290)
                lb.adjustSize()

                lb1 = QLabel("账 户", self.dl_confi)
                lb1.setStyleSheet("font-size: 26px; font: bold")
                lb1.adjustSize()
                lb1.move(40, 106)
                lb2 = QLabel("密 码", self.dl_confi)
                lb2.setStyleSheet("font-size: 26px; font: bold")
                lb2.adjustSize()
                lb2.move(40, 156)

                # lb3 = QLabel("激活码", self.dl_confi)
                # lb3.setStyleSheet("font-size: 26px; font: bold")
                # lb3.adjustSize()
                # lb3.move(40, 206)

                # 输入框
                self.tl_acc = QLineEdit(self.dl_confi)   # 账户
                self.tl_acc.resize(200, 40)
                self.tl_acc.move(130, 100)
                self.tl_acc.setPlaceholderText("在此键入您的账号")
                self.tl_acc.setStyleSheet("font-size: 20px; font: bold")
                self.tl_pwd = QLineEdit(self.dl_confi)   # 密码
                self.tl_pwd.resize(200, 40)
                self.tl_pwd.setEchoMode(2)
                self.tl_pwd.setPlaceholderText("在此键入账号的密码")
                self.tl_pwd.move(130, 150)
                self.tl_pwd.setStyleSheet("font-size: 20px; font: bold")
                # self.tl_act = QLineEdit(self.dl_confi)  # 激活码
                # self.tl_act.resize(180, 40)
                # self.tl_act.move(140, 200)

                # 验证提示
                q_verify = QLabel(self.dl_confi)
                q_verify.move(30, 260)
                q_verify.setStyleSheet("font-size: 22px; font: bold")

                # 提交槽
                def cao_save():
                    if self.tl_acc.text() and self.tl_pwd.text():
                        result = self.new_login.main(self.tl_acc.text(), self.tl_pwd.text())
                        if result == "重复认证" or result == "认证成功":
                            self._acc = self.tl_acc.text()
                            self._pwd = self.tl_pwd.text()
                            ConfiRead.createConfi(accout=self._acc, password=self._pwd, key=None)
                            RegRead.write(self._acc, self._pwd)
                            time.sleep(1)
                            self.dl_confi.done(1)
                        else:
                            q_verify.setText(result)
                            q_verify.adjustSize()
                    else:
                        q_verify.setText("请输入完全后再提交")
                        q_verify.adjustSize()

                # 弹窗按钮
                self.pb_save = QPushButton(self.dl_confi)
                self.pb_save.resize(100, 40)
                self.pb_save.setText("提 交")
                self.pb_save.move(60, 210)
                self.pb_save.pressed.connect(cao_save)
                self.pb_quit = QPushButton(self.dl_confi)
                self.pb_quit.resize(100, 40)
                self.pb_quit.setText("退 出")
                self.pb_quit.move(220, 210)
                self.pb_quit.pressed.connect(lambda: quit())
                res = self.dl_confi.exec()
                if res == 0:
                    quit()
            else:
                confi_data = RegRead.readconfi()
                self._acc = confi_data["accout"]
                self._pwd = confi_data["password"]
                print("读取成功！")
        else:
            confi_data = ConfiRead.readData()
            self._acc = confi_data["accout"]
            self._pwd = confi_data["password"]
        self.setWindowTitle("校园网助手")
        self.setFixedSize(500, 300)
        self.setStyleSheet('background-color: #2A2A2A; color: white')
        self.geometry().center()
        self.setWindowIcon(QIcon(':/0.ico'))
        self.ui()

        # 线程初始化
        self.thread_time = None
        self.thread_listen = None
        self.thread_time_status = True
        self.thread_listen_status = True
        self.thread_forced_update = threading.Thread(target=self.force_update, args=())
        self.forced_update = True
        self.thread_forced_update.start()

        # 状态提示
        self.ts_status = QLabel(self)
        self.ts_status.setText("当前状态：等待操作")
        self.ts_status.adjustSize()
        self.ts_status.move(30, 140)

        # 在线时长
        self.ts_time = QLabel(self)
        self.ts_time.setText("在线时长：监听后显示")
        self.ts_time.adjustSize()
        self.ts_time.move(30, 165)

        # 成功认证次数
        self.ts_success = QLabel(self)
        self.ts_success.setText("认证成功次数：监听后显示")
        self.ts_success.adjustSize()
        self.ts_success.move(30, 190)

        # 断网次数
        self.ts_disconnect_times = QLabel(self)
        self.ts_disconnect_times.setText("断网次数：监听后显示")
        self.ts_disconnect_times.adjustSize()
        self.ts_disconnect_times.move(30, 215)

        # 异常提示
        self.ts_error = QLabel(self)
        self.ts_error.setText("异常提示：监听后显示")
        self.ts_error.adjustSize()
        self.ts_error.move(30, 240)

        # 版本号
        self.ts_version = QLabel(self)
        self.ts_version.setText(f"当前版本 {self.version}")
        self.ts_version.setStyleSheet("color: #3B78DD; font: bold")
        self.ts_version.adjustSize()
        self.ts_version.move(30, 265)

        # 计数与规则
        self.disconnect_times = 0    # 断网次数
        self.success_times = 0       # 成功次数
        self.wired_mode = False      # 有线模式
        self.close_tk = False   # 自动更新

        # 检查更新
        self.tb_auth = QToolButton(self)
        self.tb_auth.setText("网页认证")
        self.tb_auth.setStyleSheet("font-size: 16px;")
        self.tb_auth.adjustSize()
        self.tb_auth.move(12, 0)
        self.tb_auth.setAutoRaise(True)
        self.tb_auth.pressed.connect(self.cao_auth)

        # 充 值
        self.tb_recharge = QToolButton(self)
        self.tb_recharge.setText("充 值")
        self.tb_recharge.setStyleSheet("font-size: 16px;")
        self.tb_recharge.adjustSize()
        self.tb_recharge.move(99, 0)
        self.tb_recharge.setAutoRaise(True)
        self.tb_recharge.pressed.connect(self.cao_recharge)

        # 关于软件
        self.tb_about = QToolButton(self)
        self.tb_about.setText("关于校园网助手")
        self.tb_about.setStyleSheet("font-size: 16px;")
        self.tb_about.adjustSize()
        self.tb_about.move(161, 0)
        self.tb_about.setAutoRaise(True)
        self.tb_about.pressed.connect(self.cao_about)

    # 关闭提示
    def closeEvent(self, event):
        quitMsgBox = QMessageBox()
        quitMsgBox.setWindowIcon(QIcon(':/0.ico'))
        quitMsgBox.setWindowTitle('校园网助手')
        quitMsgBox.setStyleSheet('background-color: #2A2A2A; color: white')
        # 设置提示框的内容
        quitMsgBox.setText('\n是否退出校园网助手？\n')
        quitMsgBox.resize(300, 200)
        # 设置按钮标准，一个yes一个no
        quitMsgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        # 获取两个按钮并且修改显示文本
        buttonY = quitMsgBox.button(QMessageBox.Yes)
        buttonY.setText('确定')
        buttonN = quitMsgBox.button(QMessageBox.No)
        buttonN.setText('取消')
        quitMsgBox.exec_()
        # 判断返回值，如果点击的是Yes按钮，我们就关闭组件和应用，否则就忽略关闭事件
        if quitMsgBox.clickedButton() == buttonY:
            if not self.close_tk:
                self.close_tk = True
            if self.thread_time_status:
                self.thread_time_status = False
            if self.thread_listen_status:
                self.thread_listen_status = False
            event.accept()
        else:
            event.ignore()

    def force_update(self):
        print("自动更新程序启动")
        while True:
            if self.close_tk:
                break
            elif self.new_login.check_net():
                version_new = self.new_login.get_version(self.version)
                if version_new:
                    if version_new["value"] == "True":
                        if self.thread_time_status:
                            self.thread_time_status = False
                        if self.thread_listen_status:
                            self.thread_listen_status = False
                        self.ts_status.setText("当前状态：检测到新版本正在关闭已有服务并更新")
                        self.ts_status.adjustSize()
                        time.sleep(1)
                        th = threading.Thread(target=self.auto_update, args=())
                        th.start()
                        break
                    else:
                        self.ts_status.setText(f"当前状态：您使用的是最新版本{self.version}")
                        self.ts_status.adjustSize()
                        break
            else:
                time.sleep(3)
        print("自动更新程序结束")

    # 自动更新
    def auto_update(self):
        version_new = self.new_login.get_version(self.version)
        print(version_new)
        if version_new:
            if version_new["value"] == "True":
                self.start_download(version_new['version'])
                print('正在执行自动化操作')

    # 关于槽
    @classmethod
    def cao_about(cls):
        webbrowser.open("https://www.nvidia.fun/index.php/archives/98/")

    # 充值槽
    @classmethod
    def cao_recharge(cls):
        webbrowser.open("http://210.44.64.60/shop/User/login")

    # 打开网页认证
    @classmethod
    def cao_auth(cls):
        webbrowser.open("http://210.44.64.60/gportal/web/login")

    def ui(self):
        self.label()
        self.bt()

    def label(self):
        label1 = QLabel(self)
        label1.setText("校园网助手")
        label1.setStyleSheet("font-size: 35px; font: bold; color: #6495ED")
        label1.adjustSize()
        label1.move(157, 35)

    def bt(self):
        bt_login = QPushButton(self)
        bt_login.setText("登 录")
        bt_login.setStyleSheet('size: 20px')
        bt_login.resize(100, 40)
        bt_login.move(69, 90)
        bt_login.pressed.connect(self.login)

        bt_listen = QPushButton(self)
        bt_listen.setText("监 听")
        bt_listen.resize(100, 40)
        bt_listen.move(199, 90)
        bt_listen.clicked.connect(self.cao_listen)

        bt_logout = QPushButton(self)
        bt_logout.setText("下 线")
        bt_logout.resize(100, 40)
        bt_logout.move(329, 90)
        bt_logout.pressed.connect(self.cao_logout)

        bt_lines = QCheckBox(self)
        bt_lines.setText("有线模式")
        bt_lines.move(350, 230)
        bt_lines.setChecked(False)
        bt_lines.stateChanged.connect(self.wired_mode_switch)

        bt_autorun = QCheckBox(self)
        bt_autorun.setText("开机自启动")
        bt_autorun.move(350, 260)
        if RegRead.read_reg():
            bt_autorun.setChecked(True)
        else:
            bt_autorun.setChecked(False)
        bt_autorun.stateChanged.connect(lambda: self.check(bt_autorun.isChecked()))

    # 有限模式
    def wired_mode_switch(self):
        if self.wired_mode:
            print("有线模式关闭")
            self.wired_mode = False
        else:
            print("有线模式开启")
            self.wired_mode = True

    # 登陆方法
    def login(self):
        if self.new_login.check_wifi() or self.wired_mode:
            res = self.new_login.main(self._acc, self._pwd)
            self.ts_status.setText(f'当前状态：{res}')
            self.ts_status.adjustSize()
            return res
        else:
            self.ts_status.setText(f'当前状态：未连接有线或者WiFi')
            self.ts_status.adjustSize()
            return False

    # 获取时间的槽
    def cao_get_time(self):
        if not self.thread_time:
            self.thread_time = threading.Thread(target=self.get_time, args=())
            self.thread_time.start()
        else:
            if not self.thread_time_status:
                self.thread_time_status = True
                self.thread_time = threading.Thread(target=self.get_time, args=())
                self.thread_time.start()

    # 获取在线时间的方法
    def get_time(self):
        while True:
            if self.thread_time_status:
                try:
                    time.sleep(1)
                    self.ts_time.setText(f'在线时长：{self.new_login.get_online_time()}')
                    self.ts_time.adjustSize()
                except:
                    self.ts_time.setText(f'在线时长：获取失败')
                    self.ts_time.adjustSize()
            else:
                print('时间检查终止')
                self.ts_time.setText(f'在线时长：已被暂停')
                self.ts_time.adjustSize()
                break
        print('时间检查方法结束')

    # 下线的槽
    def cao_logout(self):
        if self.thread_time_status:
            self.thread_time_status = False
        if self.thread_listen_status:
            self.thread_listen_status = False
        res = self.new_login.logout()
        self.ts_status.setText(f'当前状态：{res}')
        self.ts_status.adjustSize()

    # 监听的槽
    def cao_listen(self):
        self.ts_time.setText(f'在线时长：正在获取...')
        self.ts_time.adjustSize()
        self.cao_get_time()
        if self.new_login.check_wifi() or self.wired_mode:
            if not self.thread_listen:
                self.thread_listen = threading.Thread(target=self.listen, args=())
                th_disconnext_times = threading.Thread(target=self.disconnext_times, args=())
                self.thread_listen.start()
                th_disconnext_times.start()
                self.ts_status.setText('当前状态：正在监听')
                self.ts_status.adjustSize()
                self.ts_error.setText('异常提示：正常')
                self.ts_success.setText(f'认证成功次数：{self.success_times}')
            else:
                if not self.thread_listen_status:
                    self.thread_listen_status = True
                    self.thread_listen = threading.Thread(target=self.listen, args=())
                    th_disconnext_times = threading.Thread(target=self.disconnext_times, args=())
                    self.thread_listen.start()
                    th_disconnext_times.start()
                    self.ts_status.setText('当前状态：正在监听')
                    self.ts_status.adjustSize()
                    self.ts_error.setText('异常提示：正常')
                    self.ts_success.setText(f'认证成功次数：{self.success_times}')

        else:
            self.ts_status.setText(f'当前状态：未连接WiFi，请连接WiFi后再试！')
            self.ts_status.adjustSize()

    # 监听方法
    def listen(self):
        while True:
            if self.thread_listen_status:
                try:
                    if self.new_login.check_net():
                        time.sleep(0.1)
                        if self.ts_status != "'当前状态：正在监听":
                            self.ts_status.setText(f'当前状态：正在监听')
                            self.ts_status.adjustSize()

                    # 判断连接是否正常
                    elif not self.new_login.check_wifi():
                        if self.wired_mode:     # 有线模式下
                            if self.new_login.check_net(url="http://210.44.64.60/"):
                                self.disconnect_times += 1
                                if self.login() == "认证成功":
                                    self.success_times += 1
                                self.ts_success.setText(f'认证成功次数：{str(self.success_times)}')
                            else:
                                self.ts_status.setText(f'当前状态：有线连接不正确！')
                                self.ts_status.adjustSize()
                            time.sleep(5)
                        # 无线模式下
                        else:
                            self.disconnect_times += 1
                            self.ts_status.setText(f'当前状态：未连接WiFi，请连接后再试！')
                            self.ts_status.adjustSize()
                            time.sleep(5)
                    else:
                        self.disconnect_times += 1
                        if self.login() == "认证成功":
                            self.success_times += 1
                        self.ts_success.setText(f'认证成功次数：{str(self.success_times)}')
                        self.ts_success.adjustSize()
                        time.sleep(5)
                except Exception as e:
                    self.ts_status.setText(f'当前状态：{e}')
                    self.ts_status.adjustSize()
            else:
                self.ts_status.setText(f'当前状态：监听已被暂停')
                self.ts_status.adjustSize()
                self.ts_success.setText(f'认证成功次数：监听后显示')
                self.ts_success.adjustSize()
                print('监听终止')
                break
        print('监听方法结束')

    # 断网次数刷新方法
    def disconnext_times(self):
        while True:
            if self.thread_listen_status:
                self.ts_disconnect_times.setText(f"断网次数：{str(self.disconnect_times)}")
                time.sleep(2)
            else:
                self.ts_disconnect_times.setText(f"断网次数：监听后显示")
                break
        print("断网次数方法已结束")

    @classmethod
    def check(cls, switch: bool):
        """开机自启动函数"""
        if switch:
            print("开启自启动")
            AutoRun(switch='open', key_name='yjrz')  # 键的名称

        else:
            print("关闭自启动")
            AutoRun(switch='close', key_name='yjrz')

    def start_download(self, version):
        url = 'https://oss.nvidia.fun/%E6%A0%A1%E5%9B%AD%E7%BD%91%E5%8A%A9%E6%89%8B.exe'
        response = get(url, stream=True)  # stream=True必须写上
        size = 0  # 初始化已下载大小
        count_tmp = 0
        chunk_size = 1024  # 每次下载的数据大小
        content_size = int(response.headers['Content-Length'])  # 下载文件总大小
        try:
            if response.status_code == 200:  # 判断是否响应成功
                print('[File size]:{size:.2f} MB'.format(size=content_size / chunk_size / 1024))  # 开始下载，显示下载文件大小
                filepath = gen_path + '\\校园网助手' + version + '.exe'
                time1 = time.time()
                with open(filepath, 'wb') as file:  # 显示进度条
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size += len(data)
                        now_data = float(size / content_size * 100)
                        if time.time() - time1 > 0.2:
                            speed = (size - count_tmp) / 1024 / 1024 / 0.2
                            count_tmp = size
                            time1 = time.time()
                            self.ts_status.setText(f'当前状态：正在下载更新包{int(now_data)}%, 速度{self.formatFloat(speed)}M/S')
                            self.ts_status.adjustSize()
                self.ts_status.setText('当前状态：下载完成，请使用新版本！')
                self.ts_status.adjustSize()
                os.system(filepath)
        except Exception as e:
            print(e)

    @classmethod
    def formatFloat(cls, num):
        return '{:.2f}'.format(num)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())
