## 校园网助手(1.5版本)

### 新功能
 
 * 启动后就可以自动监听自动联网，不需要手动操作了。

### 下载地址

#### Windows（XP用户遇到问题欢迎在[关于页面][1]提交您的问题）：
 轻巧版： [**自建云**][2] （无需安装直接运行，约51M）

### BUG修复 2022年2月22日18:12

 * **修复了不能在WIN XP/7（32位）系统上运行的问题。**
 * **修复了不能在无WiFi的设备上运行的问题。**
 * 修复了修改账户信息卡死的BUG。


### UI变化
 
 * 现在可以通过界面内的“修改账户信息”来修改您的账户信息。
 * 移除了断网次数统计，增加了联网质量提醒。


----------


## 校园网助手(1.4版本)

###  新皮肤 *

**黑色主题** 已上线1.4版本

### 新功能 *

校园网助手1.4版本不再使用exe单独文件形式，而是推出安装包形式。安装更省心，启动速度更快，更新更方便，运行更稳定啦。

###  BUG 修复 2021年12月25日17:45

* 修复了导致在等待网络连接时，监听方法不起作用的问题。
* 修复了时间显示0时0分0秒的BUG。
* 修复了在有线模式下少概率的认证失败问题。
* 修复了一个问题，大大降低软件无响应的概率。
* 修复了更新逻辑，现在可以自动检查是否有新版，并根据需要升级了。
* 修复了下线的逻辑，现在第一次点击下线将不会断网而是会终止监听，第二次则会下线网络。


----------


## 校园网助手(1.3版本）


### BUG修复 2021年10月8日 22:27

* 删除了时间查询的按钮，并与监听融为一体。
* 删除了检查更新的按钮，在联网后将会自动下载新版本。
* 优化了部分文字以及文本提示


----------


## 校园网助手(1.2版本）

### BUG修复 2021年10月4日 17:54

* 修复了在点击关闭时不能正常退出监听或者时间查询的服务的问题。


----------


## 校园网助手(1.1版本）

### BUG修复 2021年10月4日 11:59

在推出校园网助手安卓端后，发现1.0版本存在许多的BUG，例如：

* **问题**：在每次点击监听时，都会创建一个子线程这样会导致误点多次使得子线程数量增加，从而出现网络堵塞的情况。时间查询亦是如此。

  > 现在点击监听或者时间查询后，如果有正在执行监听或者时间查询的子线程后，将不会采取任何操作

* **问题**：在点击监听或者是时间查询后，创建的子线程无法在关闭主程序后自动退出，从而导致子线程残留的问题

  > 现在关闭软件或者是点击下线都将会时已有的子线程全部结束，不会存在子线程残留的问题啦~

### 新功能

* 新增**下线**，除了最基本的下线操作外，还会将已有的监听和时间查询全部取消，您可以再次点击相应的功能继续操作哦


----------


##  校园网助手(1.0版本）

###  功能修复 2021年9月27日 17:44

* 修复了电脑没有D盘而导致的用户配置文件无法生成的问题。此版本（21.9.27.2）之后将在创建**WFU_CNA.conf**的基础上，还会在注册表**HKEY_CURRENT_USER\\Software\\WFU_CNA**里生成用户的账号信息，以便无D盘用户的使用。

* 优化了部分文字显示

### 功能修复 2021年9月20日
* 修复了**版本更新**的功能，现在可以直接检查最新版本啦。

> 如果是最新版本将会打开本页面，请在下载地址获取最新版本哟~

###  新功能 2021年9月19日

* 新增**在线时长查询**，您可以点击时间查询来显示实时的在线时长（据上一次认证成功到现在）并且是实时的

>  客户端将每隔1S发送一个时间查询请求获取最新的时长信息。

* 新增**监听功能**，自动检测网络变化并自动认证您的网络。

>  客户端将每0.1S发送一个GET请求baidu.com来确认您的网络是否连接正常，其域名将可以在之后的版本里自定义

* 新增**开机自启动**，勾选此选项，软件将在注册表启动项里新建或者删除名称为**yjrz**数据为当前软件的绝对路径。

> 默认不自启动，如果开启它可能会影响开机的时长，取决于您的电脑。

* 新增**在线模式**，此选项是为了有线连接的用户。勾选后，软件将忽略WIFI是否连接，请有线用户务必勾选此选项以正常使用。

> 在之后的版本将会把此选项放入设置中。

* 新增**欢迎页面**，第一次使用将会进入欢迎页，请根据提示填写您的账户和密码，提交后软件将会自动认证其真实性并在您电脑的D盘里创建名为**WFU_CNA.conf**的配置文件，如果您想更改配置的密码，可以使用TXT打开并修改其password的值以防止自动认证时出现密码错误。

> 日后将在设置里添加配置文件路径的功能，敬请期待。

* 新增**快捷充值**、**检查更新**页面您可以快捷的充值您的账号或者查看软件是否有更新

> 强烈建议检查更新，因为在软件初期许多功能尚存BUG，如果您在使用过程中遇到任何问题请在关于页面与我取得联系。


  [1]: https://www.nvidia.fun/index.php/start-page.html
  [2]: https://oss.nvidia.fun/%E6%A0%A1%E5%9B%AD%E7%BD%91%E5%8A%A9%E6%89%8B.exe
  [3]: https://github.com/Doone-skser/WFU
