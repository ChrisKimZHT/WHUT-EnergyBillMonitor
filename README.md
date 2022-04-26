# WHUT-EnergyBillMonitor

通过访问学校电费查询网页，获取寝室电费，并且通过 cqhttp 发送到 QQ 号或 QQ 群，或通过邮件发送到指定邮箱。

可通过 crontab 定时运行，即可定时获取寝室电费情况，及时充值，防止意外停电。

### 功能介绍

- **支持区域**
    - 余家头电费
        - 学生区域
        - ~~教工区域~~（不打算支持）
    - ~~马房山学生电费~~（暂不支持）
    - ~~马房山电费~~（不打算支持）
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

请先运行 `init_config.py` 生成配置文件，按照程序操作后，将会自动生成包含账号密码、寝室号的配置文件 `config.yaml`.

配置文件生成后，即可运行 `main.py` 查询电费，可添加 crontab 定时运行指令 `python main.py`.

注意：由于程序使用相对路径，crontab 运行时需要先 cd 到程序根目录再运行 `main.py`，否则程序将找不到 `config.yaml` 而报错。