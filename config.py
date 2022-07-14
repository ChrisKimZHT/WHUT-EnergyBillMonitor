import os
import yaml

conf_notification = {
    "mail": {
        "enable": False,
        "ssl": False,
        "host": "",
        "port": 0,
        "account": "",
        "password": "",
        "sender": "",
        "receiver": "",
    },
    "cqhttp": {
        "enable": False,
        "api": "",
        "uid": "",
        "gid": "",
    }
}
conf_dormitory = {
    "account": "",
    "password": "",
    "is_mafangshan": True,
    "mafangshan": {
        "meterId": "",
        "factorycode": "",
    },
    "yujiatou": {
        "roomno": "",
        "factorycode": "",
        "area": "",
    }
}


def save_config():
    all_config = {
        "notification": conf_notification,
        "dormitory": conf_dormitory,
    }
    try:
        with open("config.yaml", "w") as config_file:
            yaml.safe_dump(all_config, config_file, sort_keys=False)
    except:
        print("配置文件保存失败")


def load_config():
    global conf_notification, conf_dormitory
    try:
        with open("config.yaml", "r") as config_file:
            all_config = yaml.safe_load(config_file)
        conf_notification = all_config["notification"]
        conf_dormitory = all_config["dormitory"]
    except:
        print("配置文件读取失败，请检查配置文件是否有格式错误")


def init_config():
    global conf_dormitory
    print("======寝室设置======")
    conf_dormitory["account"] = input("输入账号: ")
    conf_dormitory["password"] = input("输入密码: ")
    is_mafangshan = input("选择校区(Y.马房山/N.余家头): ")
    if is_mafangshan == "Y" or is_mafangshan == "y":
        is_mafangshan = True
    else:
        is_mafangshan = False
    print("下面的数据请按文档指导获取后准确填写")
    if is_mafangshan:
        conf_dormitory["mafangshan"]["meterId"] = input("meterId: ")
        conf_dormitory["mafangshan"]["factorycode"] = input("factorycode: ")
    else:
        conf_dormitory["yujiatou"]["roomno"] = input("roomno: ")
        conf_dormitory["yujiatou"]["factorycode"] = input("factorycode: ")
        conf_dormitory["yujiatou"]["area"] = input("area: ")
    print("======推送设置======")
    print("---邮件推送---\n"
          "正确配置并启用后，每次运行后程序会发送电子邮件到对应账户。\n"
          "邮件发送使用SMTP协议，可在各大电子邮箱平台找到配置方法。")
    enable_email = input("是否启用邮件推送(Y/N): ")
    if enable_email == "Y" or enable_email == "y":
        conf_notification["mail"]["enable"] = True
        ssl = input("是否启用SSL(Y/N): ")
        if ssl == "Y" or ssl == "y":
            conf_notification["mail"]["ssl"] = True
        else:
            conf_notification["mail"]["ssl"] = False
        conf_notification["mail"]["host"] = input("输入SMTP服务器地址，如smtp.qq.com: ")
        conf_notification["mail"]["port"] = int(input("输入SMTP服务器端口，如465: "))
        conf_notification["mail"]["account"] = input("输入发信账号: ")
        conf_notification["mail"]["password"] = input("输入发信密码: ")
        conf_notification["mail"]["sender"] = input("输入发信邮箱: ")
        conf_notification["mail"]["receiver"] = input("输入收信邮箱: ")
    print("---QQ推送---\n"
          "正确配置并启用后，每次运行后程序会发送QQ消息到对应收信QQ号或QQ群。\n"
          "需要正确配置go-cqhttp(https://github.com/Mrs4s/go-cqhttp)并启用HTTP API接口。\n"
          "！若你不知道cqhttp是什么，请不要启用！")
    enable_cqhttp = input("是否启用QQ推送(Y/N): ")
    if enable_cqhttp == "Y" or enable_cqhttp == "y":
        conf_notification["cqhttp"]["enable"] = True
        conf_notification["cqhttp"]["api"] = input(
            "cqhttp http API 地址(留空默认\"http://127.0.0.1:5700/send_msg\"): ") or "http://127.0.0.1:5700/send_msg"
        conf_notification["cqhttp"]["uid"] = input("收信QQ号，不填则不发送: ")
        conf_notification["cqhttp"]["gid"] = input("收信群号，不填则不发送: ")
    print("======设置完成======")
    save_config()
    print("======保存完成======")


if os.path.exists("config.yaml"):
    load_config()
else:
    print("未发现配置文件，进行配置文件初始化")
    init_config()
