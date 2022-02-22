import os
import threading
import time
import sys
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
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
from Cnet import CNET
from Autorun import AutoRun
import RegRead
import webbrowser
import ConfiRead
import ping3
import Ico

# 解决根目录无法在打包后正确获取的问题
gen_path = os.path.dirname(os.path.realpath(sys.argv[0]))


class Window(QWidget):
    # 初始化
    def __init__(self):
        super().__init__()
        self.new_login = CNET()
        self.version = "1.5"   # 版本号信息
        self.check_version = True  # 是否检查版本
        self.auto_listen = False  # 启动软件时自动监听
        # 检查是否有配置文件如果没有则生成
        self.dl_confi = QDialog(self)
        self.dl_confi.setFixedSize(390, 400)
        self.dl_confi.setWindowTitle("校园网助手")
        self.dl_confi.setWindowIcon(QIcon(':/0.ico'))
        self.dl_confi.geometry().center()
        self.dl_confi.setWindowOpacity(0.91)
        self.dl_confi.setStyleSheet('background-color: #2A2A2A; color: white')

        if not ConfiRead.isExist():
            if not RegRead.readconfi():
                # 第一次弹窗
                lb_welcome = QLabel(self.dl_confi)
                lb_welcome.setText("欢迎使用")
                lb_welcome.setStyleSheet("font-size: 38px; font: bold;")
                lb_welcome.adjustSize()
                lb_welcome.move(120, 30)

                lb = QLabel("温馨提示:\n第一次使用请输入您的账号以及密码。", self.dl_confi)
                lb.setStyleSheet("font-size: 18x; color: #FFFFFF; font: bold")
                lb.move(10, 290)
                lb.adjustSize()

                lb = QLabel("免责声明：本软件不会以任何形式或手段收集您电脑上的任何\n数据（用户信息存储在本地），您在软件中的操作也不会被记\n录。但除软件之外的操作如"
                            "感染木马病毒或因为自身操作而产\n生的问题本软件不承担任何责任。点击登录则同意此条款！\n", self.dl_confi)
                lb.setStyleSheet("font-size: 18x; color: #F0000F; font: bold")
                lb.move(10, 330)
                lb.adjustSize()

                lb1 = QLabel("账 户", self.dl_confi)
                lb1.setStyleSheet("font-size: 26px; font: bold")
                lb1.adjustSize()
                lb1.move(40, 106)
                lb2 = QLabel("密 码", self.dl_confi)
                lb2.setStyleSheet("font-size: 26px; font: bold")
                lb2.adjustSize()
                lb2.move(40, 156)

                # 输入框
                self.tl_acc = QLineEdit(self.dl_confi)   # 账户
                self.tl_acc.resize(200, 40)
                self.tl_acc.move(130, 100)
                self.tl_acc.setPlaceholderText("在此键入您的账号")
                self.tl_acc.setStyleSheet("font-size: 20px; font: bold")
                self.tl_pwd = QLineEdit(self.dl_confi)   # 密码
                self.tl_pwd.resize(200, 40)
                self.tl_pwd.setEchoMode(2)
                self.tl_pwd.setPlaceholderText("在此键入您的密码")
                self.tl_pwd.move(130, 150)
                self.tl_pwd.setStyleSheet("font-size: 20px; font: bold")

                # 验证提示
                q_verify = QLabel(self.dl_confi)
                q_verify.move(30, 260)
                q_verify.setStyleSheet("font-size: 18px; font: bold")

                # 提交槽
                def cao_save():
                    if self.tl_acc.text() and self.tl_pwd.text():
                        result = self.new_login.main(self.tl_acc.text(), self.tl_pwd.text())
                        if result == "重复认证" or result == "认证成功" or result == "认证拒绝":
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

        else:
            confi_data = ConfiRead.readData()
            self._acc = confi_data["accout"]
            self._pwd = confi_data["password"]

        # 主界面
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
        self.thread_forced_update_status = True
        self.thread_forced_update = threading.Thread(target=self.force_update, args=())
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
        self.ts_success.setText("认证成功：监听后显示")
        self.ts_success.adjustSize()
        self.ts_success.move(30, 190)

        # 网络质量
        self.ts_network_quality = QLabel(self)
        self.ts_network_quality.setText("网络质量：监听后显示")
        self.ts_network_quality.adjustSize()
        self.ts_network_quality.move(30, 215)

        # 账号提示
        self.ts_accout = QLabel(self)
        self.ts_accout.setText("当前账号：{}".format(self._acc.replace(self._acc[3:7], '****')))
        self.ts_accout.adjustSize()
        self.ts_accout.move(30, 240)

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
        self.disconnect_times_status = True  # 计数重复判断

        # 网页认证
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
        self.tb_about.setText("关于与升级CNA")
        self.tb_about.setStyleSheet("font-size: 16px;")
        self.tb_about.adjustSize()
        self.tb_about.move(165, 0)
        self.tb_about.setAutoRaise(True)
        self.tb_about.pressed.connect(self.cao_about)

        # 网页认证
        self.tb_auth = QToolButton(self)
        self.tb_auth.setText("修改账户信息")
        self.tb_auth.setStyleSheet("font-size: 16px;")
        self.tb_auth.adjustSize()
        self.tb_auth.move(293, 0)
        self.tb_auth.setAutoRaise(True)
        self.tb_auth.pressed.connect(self.change_confi)

        # 参数配置
        self.changeAccoutResult = False

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
            self.thread_forced_update_status = False
            if self.thread_time_status:
                self.thread_time_status = False
            if self.thread_listen_status:
                self.thread_listen_status = False
            print('正在退出所有线程')
            event.accept()
        else:
            event.ignore()

    # 自动更新
    def force_update(self):
        while True:
            if not self.check_version or not self.thread_forced_update_status:
                print('更新线程已退出！')
                break
            elif self.new_login.check_net():
                self.cao_listen()
                version_new = self.new_login.get_version(self.version)
                if version_new:
                    time.sleep(3)
                    if version_new["value"] == "True":
                        self.ts_version.setText("当前版本：{0}(有新版本{1})".format(self.version, version_new['version']))
                        self.ts_version.adjustSize()
                        break
                    else:
                        self.ts_version.setText(f"当前版本 {self.version} （已是最新版本）")
                        self.ts_version.adjustSize()
                        break
            else:
                self.cao_listen()
                time.sleep(3)

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
        # 标签
        label1 = QLabel(self)
        label1.setText("校园网助手")
        label1.setStyleSheet("font-size: 35px; font: bold; color: #6495ED")
        label1.adjustSize()
        label1.move(157, 35)

        # 按钮
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

    # 连接模式切换
    def wired_mode_switch(self):
        if self.wired_mode:
            self.wired_mode = False
        else:
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
                self.ts_time.setText(f'在线时长：已被重置')
                self.ts_time.adjustSize()
                print('时间查询线程已退出！')
                break

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
        # if self.new_login.check_wifi() or self.wired_mode:
        if not self.thread_listen:
            self.thread_listen = threading.Thread(target=self.listen, args=())
            th_disconnext_times = threading.Thread(target=self.disconnext_times, args=())
            self.thread_listen.start()
            th_disconnext_times.start()
            self.ts_status.setText('当前状态：正在监听')
            self.ts_status.adjustSize()
            self.ts_success.setText(f'认证成功：{self.success_times}次')
        else:
            if not self.thread_listen_status:
                self.thread_listen_status = True
                self.thread_listen = threading.Thread(target=self.listen, args=())
                th_disconnext_times = threading.Thread(target=self.disconnext_times, args=())
                self.thread_listen.start()
                th_disconnext_times.start()
                self.ts_status.setText('当前状态：正在监听')
                self.ts_status.adjustSize()
                self.ts_success.setText(f'认证成功：{self.success_times}次')

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
                        # 有线模式下
                        if self.wired_mode:
                            if self.new_login.check_net(url="http://210.44.64.60/"):
                                if self.disconnect_times_status:
                                    self.disconnect_times += 1
                                    self.disconnect_times_status = False
                                if self.login() == "认证成功":
                                    self.success_times += 1
                                    self.disconnect_times_status = True
                                self.ts_success.setText(f'认证成功：{str(self.success_times)}次')
                            else:
                                self.ts_status.setText(f'当前状态：有线连接不正确！')
                                self.ts_status.adjustSize()
                            time.sleep(5)

                        # 无线模式下
                        else:
                            if self.disconnect_times_status:
                                self.disconnect_times += 1
                                self.disconnect_times_status = False
                            self.ts_status.setText(f'当前状态：WiFi连接不正确！')
                            self.ts_status.adjustSize()
                            time.sleep(1)
                    else:
                        if self.disconnect_times_status:
                            self.disconnect_times += 1
                            self.disconnect_times_status = False
                        if self.login() == "认证成功":
                            self.success_times += 1
                            self.disconnect_times_status = True
                        self.ts_success.setText(f'认证成功：{str(self.success_times)}次')
                        self.ts_success.adjustSize()
                        time.sleep(1)
                except Exception as e:
                    self.ts_status.setText(f'当前状态：{e}')
                    self.ts_status.adjustSize()
            else:
                self.ts_status.setText(f'当前状态：下线完成！')
                self.ts_status.adjustSize()

                print('监听线程已退出！')
                break

    # 网络质量刷新方法
    def disconnext_times(self):
        while True:
            if self.thread_listen_status:
                res = ping3.ping('baidu.com')
                if res:
                    res = int(float(res) * 1000)
                else:
                    res = 0
                if 0 < res <= 50:
                    self.ts_network_quality.setText(f"网络质量：极好")
                if 50 < res <= 200:
                    self.ts_network_quality.setText(f"网络质量：良好")
                if 200 < res <= 800:
                    self.ts_network_quality.setText(f"网络质量：一般")
                if res > 800:
                    self.ts_network_quality.setText(f"网络质量：很差")
                if res == 0:
                    self.ts_network_quality.setText(f"网络质量：无网络")
                time.sleep(1)
            else:
                self.ts_network_quality.setText(f"网络质量：已被重置")
                print('网络质量检测已退出！')
                break

    # 修改密码
    def change_confi(self):
        # 第一次弹窗
        tc = QDialog(self)
        tc.setFixedSize(390, 240)
        tc.setWindowTitle('修改账户信息')
        tc.setWindowIcon(QIcon(':/0.ico'))
        tc.geometry().center()
        tc.setWindowOpacity(0.91)
        tc.setStyleSheet('background-color: #2A2A2A; color: white')

        lb = QLabel("温馨提示：修改后不需要重启软件！", tc)
        lb.setStyleSheet("font-size: 18x; color: #F0000F; font: bold")
        lb.move(10, 210)
        lb.adjustSize()

        lb1 = QLabel("账 户", tc)
        lb1.setStyleSheet("font-size: 26px; font: bold")
        lb1.adjustSize()
        lb1.move(40, 26)
        lb2 = QLabel("密 码", tc)
        lb2.setStyleSheet("font-size: 26px; font: bold")
        lb2.adjustSize()
        lb2.move(40, 76)

        # 输入框
        tl_acc = QLineEdit(tc)  # 账户
        tl_acc.resize(200, 40)
        tl_acc.move(130, 20)
        # self.tl_acc.setPlaceholderText("账户")
        tl_acc.setStyleSheet("font-size: 22px; font: bold")

        tl_pwd = QLineEdit(tc)  # 密码
        tl_pwd.resize(200, 40)
        tl_pwd.setEchoMode(2)
        # self.tl_pwd.setPlaceholderText("密码")
        tl_pwd.move(130, 70)
        tl_pwd.setStyleSheet("font-size: 22px; font: bold")

        # 验证提示
        q_verify = QLabel(tc)
        q_verify.move(20, 180)
        q_verify.setStyleSheet("font-size: 18px; font: bold")

        # 提交槽
        def cao_save():
            if tl_acc.text() and tl_pwd.text():
                q_verify.setText("正在验证信息")
                q_verify.adjustSize()
                res = self.changeAccout(tl_acc.text(), tl_pwd.text())
                if not res:
                    self.ts_accout.setText("当前账号：{}".format(self._acc.replace(self._acc[3:7], '****')))
                    self.ts_accout.adjustSize()
                    tc.close()
                else:
                    q_verify.setText(res)
                    q_verify.adjustSize()
            else:
                q_verify.setText("请输入完全后再提交")
                q_verify.adjustSize()

        # 弹窗按钮
        pb_save = QPushButton(tc)
        pb_save.resize(100, 40)
        pb_save.setText("提 交")
        pb_save.move(60, 130)
        pb_save.pressed.connect(cao_save)

        pb_quit = QPushButton(tc)
        pb_quit.resize(100, 40)
        pb_quit.setText("退 出")
        pb_quit.move(220, 130)
        pb_quit.pressed.connect(lambda: tc.done(0))
        tc.exec()

    def changeAccout(self, acc, psw):
        self.changeAccoutResult = False
        res = self.new_login.main(acc, psw)
        if res == "重复认证" or res == "认证成功" or res == "认证拒绝":
            self._acc = acc
            self._pwd = psw
            ConfiRead.createConfi(accout=self._acc, password=self._pwd, key=None)
            RegRead.write(self._acc, self._pwd)
            self.changeAccoutResult = True
            return False
        return res

    @classmethod
    def check(cls, switch: bool):
        """开机自启动函数"""
        if switch:
            print("开启自启动")
            AutoRun(switch='open', key_name='yjrz')  # 键的名称

        else:
            print("关闭自启动")
            AutoRun(switch='close', key_name='yjrz')

    @classmethod
    def formatFloat(cls, num):
        return '{:.2f}'.format(num)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())
