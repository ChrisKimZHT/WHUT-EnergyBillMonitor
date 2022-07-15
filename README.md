# WHUT-EnergyBillMonitor

通过访问学校电费查询网页，获取寝室电费，并且通过 cqhttp 发送到 QQ 号或 QQ 群，或通过邮件发送到指定邮箱。

配置方法非常简单，只需按程序提示输入信息和选择选项即可完成配置。

配置完成后，可通过 crontab 等手段定时运行，即可定时获取寝室电费情况，及时充值，防止意外停电。

### 效果预览

![Preview](https://assets.zouht.com/img/md/WHUT-EnergyBillMonitor-README-01.png)

### 功能介绍

- **支持区域**（我也不知道为啥一个系统学校要分这么多）
    - 余家头电费
        - 学生区域
        - ~~教工区域~~
    - 马房山学生电费
    - ~~马房山电费~~
- **发信方式**
    - cqhttp
        - 私聊
        - 群聊
    - 邮件

### 所需模块

- requests
    - `pip install requests`
- pyyaml
    - `pip install PyYAML`

### 使用方式

**1. 获取寝室编号**

1.1 访问学校缴费平台 `http://cwsf.whut.edu.cn/` ，如下图所示。

![2](https://assets.zouht.com/img/md/WHUT-EnergyBillMonitor-README-02.png)

1.2 登录账号，进入服务选择页面。选择校区（只支持红框内两个）

![3](https://assets.zouht.com/img/md/WHUT-EnergyBillMonitor-README-03.png)

1.3 进入以下页面后，按键盘 `F12` 打开开发者工具。

![4](https://assets.zouht.com/img/md/WHUT-EnergyBillMonitor-README-04.png)

如下图，首先选择 `Network(网络)` 选项卡，然后点击左上侧圆圈按钮，使其为红色圆圈即开始记录日志。然后**不要**关闭它，进行下一步操作。

![5](https://assets.zouht.com/img/md/WHUT-EnergyBillMonitor-README-05.png)

1.4 在网页选好你的寝室，使其能显示查询的结果。

![6](https://assets.zouht.com/img/md/WHUT-EnergyBillMonitor-README-06.png)

然后查看开发者工具，找到**最后一个**请求，点击它后会出现详细信息。在右侧选项卡点击 `Payload(预览)` ，然后**记录**下方的数值。 

![7](https://assets.zouht.com/img/md/WHUT-EnergyBillMonitor-README-07.png)

**2. 初始化程序**

第一次运行，程序无法找到配置文件将会进行配置文件初始化操作。该操作是交互式的，请按照程序的提示准确填写相关信息，包括上一步获得的若干数值。

**3. 运行程序**

配置文件初始化后，今后再运行时，程序将会自动查询，无需人工介入。因此 Linux 用户可添加到 `crontab` 来实现定时的电量查询。

### 温馨提示

- 学校网页深夜有时候会进行维护，此时无法访问进行查询，建议早晨或夜晚定时运行。
- 由于程序使用相对路径，crontab 运行时需要先 cd 到程序根目录再运行 `main.py`，否则程序将找不到 `config.yaml` 而报错。
- 发送的邮件邮箱可能被自动标为垃圾邮件，可以添加白名单。
