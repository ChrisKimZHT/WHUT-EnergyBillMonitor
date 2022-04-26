import requests
import yaml
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

# http 请求头
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "cwsf.whut.edu.cn",
    "Origin": "http://cwsf.whut.edu.cn",
    "Referer": "http://cwsf.whut.edu.cn/MNetWorkUI/slogin.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "X-KL-Ajax-Request": "Ajax_Request",
    "X-Requested-With": "XMLHttpRequest"
}

# 请求到的 SessionID
session = requests.session()

# 配置变量
config_all = {
    "account": "",  # 账号
    "password": "",  # 密码
    "room": {},  # 房间信息
    "msg": {}  # 发信配置
}


# 账号配置文件初始化
def init_account():
    global config_all
    print("输入账号（通常为学号）：")
    account = input()
    print("输入密码（默认为身份证后六位）：")
    password = input()
    if try_login(account, password):
        print("登陆成功")
        config_all["account"] = account
        config_all["password"] = password
        return True
    else:
        print("登录失败，请重试")
        return False


# 尝试登录
def try_login(account, password):
    global session
    url = "http://cwsf.whut.edu.cn/MNetWorkUI/userLoginAction!mobileUserLogin.action"
    data = f"nickName={account}&password={password}"
    respounce = session.post(url=url, headers=headers, data=data).json()
    if respounce["returncode"] == "SUCCESS":
        return True
    else:
        return False


# 房间配置初始化
def init_room():
    print("[1] 余家头电费\n"
          "[X] 马房山学生电费\n"
          "[X] 马房山电费\n"
          "选择区域：")
    try:
        choice = int(input())
    except ValueError:
        print("输入错误")
        return False
    print("注意：此部分无输入检查，请仔细输入序号，否则无法查到正确的电费")
    if choice == 1 and yjt_room():
        return True
    elif choice == 2 and mfs_room_stu():
        return True
    elif choice == 3 and mfs_room():
        return True
    else:
        print("输入错误")
    return False


# 余家头房间查询
def yjt_room():
    global config_all
    config_room = {
        "factorycode": "",
        "area": "",
        "AreaID": "",
        "ArchitectureID": "",  # 宿舍楼编号
        "floor": "",  # 楼层
        "roomno": ""  # 宿舍电表号
    }
    print("[1] 学生区域: 余家头校区\n"
          "[X] 教工区域: 家属区\n"
          "选择区域：")
    try:
        choice_area = int(input())
    except ValueError:
        print("输入错误")
        return False
    if choice_area == 1:
        config_room["factorycode"] = "E023"
        config_room["area"] = "9004"
    elif choice_area == 2:
        return False  # 还没写家属区
    # 查Area_ID
    respounce_areaid = session.post(
        url="http://cwsf.whut.edu.cn/MNetWorkUI/elecManage!queryCampusList10497", headers=headers,
        data=f"factorycode={config_room['factorycode']}&area={config_room['area']}"
    ).json()
    for row in respounce_areaid["buildinglist"]:
        print(f"[{row['AreaID']}] {row['AreaName']}")
    print("选择校区：")
    config_room["AreaID"] = input()
    # 查ArchitectureID
    respounce_architectureid = session.post(
        url="http://cwsf.whut.edu.cn/MNetWorkUI/elecManage!queryFloorsList10497", headers=headers,
        data=f"Area_ID={config_room['AreaID']}&factorycode={config_room['factorycode']}&area={config_room['area']}"
    ).json()
    for row in respounce_architectureid["buildinglist"]:
        print(f"[{row['ArchitectureID']}] {row['ArchitectureName']}")
    print("选择楼栋：")
    config_room["ArchitectureID"] = input()
    # 获取楼层起始结尾值
    floor_begin = int()
    floor_end = int()
    for row in respounce_architectureid["buildinglist"]:
        if row["ArchitectureID"] == config_room["ArchitectureID"]:
            floor_begin = row["ArchitectureBegin"]
            floor_end = row["ArchitectureStorys"]
    print(f"当前楼栋可选楼层为{floor_begin}~{floor_end}\n"
          f"选择楼层：")
    config_room["floor"] = input()
    # 获取AmMeter_ID
    respounce_ammeterid = session.post(
        url="http://cwsf.whut.edu.cn/MNetWorkUI/elecManage!queryRoomList10497", headers=headers,
        data=f"floor={config_room['floor']}&ArchitectureID={config_room['ArchitectureID']}&factorycode={config_room['factorycode']}&area={config_room['area']}"
    ).json()
    for row in respounce_ammeterid["roomlist"]:
        print(f"[{row['AmMeter_ID']} {row['RoomName']}]")
    print("选择房间：")
    config_room["roomno"] = input()
    # 尝试查询电费
    respounce = session.post(url="http://cwsf.whut.edu.cn/MNetWorkUI/elecManage!querySydl10497", headers=headers,
                             data=f"roomno={config_room['roomno']}&factorycode={config_room['factorycode']}&area={config_room['area']}").json()
    if respounce["returncode"] == "SUCCESS":
        config_all["room"] = config_room
        print("查询成功，结果预览：\n"
              f"剩余电量：{respounce['roomlist']['remainPower']} kW·h\n"
              f"累计电量：{respounce['roomlist']['ZVlaue']} kW·h\n"
              f"查表时间：{respounce['roomlist']['readTime']}")
        return True
    else:
        print("查询失败")
        return False


def mfs_room_stu():
    pass


def mfs_room():
    pass


# 发信配置初始化
def init_msg():
    global config_all
    config_msg = dict()
    while True:
        print("是否配置cqhttp？(Y/N)")
        is_send_cqhttp = input()
        if is_send_cqhttp == "Y" or is_send_cqhttp == "y":
            config_msg["cqhttp"] = set_cqhttp()
            break
        elif is_send_cqhttp == "N" or is_send_cqhttp == "n":
            break
        else:
            print("输入错误")
    while True:
        print("是否配置邮件？(Y/N)")
        is_send_mail = input()
        if is_send_mail == "Y" or is_send_mail == "y":
            config_msg["mail"] = set_mail()
            break
        elif is_send_mail == "N" or is_send_mail == "n":
            break
        else:
            print("输入错误")
    config_all["msg"] = config_msg


def set_cqhttp():
    while True:
        cqhttp_dict = {
            "url": "http://127.0.0.1:5700/send_msg",
            "uid": "",
            "gid": ""
        }
        print("输入cqhttp的http监听地址和端口（留空默认为127.0.0.1:5700）：")
        input_url = input()
        if input_url != "":
            cqhttp_dict["url"] = "http://" + input_url + "/send_msg"
        print("输入收信QQ号（留空则不发送私聊）：")
        input_uid = input()
        if input_uid != "":
            cqhttp_dict["uid"] = input_uid
        print("输入收信QQ群号（留空则不发送群聊）：")
        input_gid = input()
        if input_gid != "":
            cqhttp_dict["gid"] = input_gid
        try:
            try_send_qq_msg(cqhttp_dict)
        except requests.RequestException:
            print("发送出现问题，开始重新设置")
            continue
        print("已发送测试消息，是否收到消息？(Y/N)")
        is_receive = input()
        if is_receive == "Y" or is_receive == "y":
            break
        elif is_receive == "N" or is_receive == "n":
            print("开始重新设置")
        else:
            print("输入错误，默认开始重新设置")
    return cqhttp_dict


def set_mail():
    while True:
        mail_dict = {
            "ssl": bool(),
            "host": "",
            "port": int(),
            "account": "",
            "password": "",
            "sender": "",
            "receiver": ""
        }
        while True:
            print("是否使用SSL邮件？(Y/N)")
            is_ssl = input()
            if is_ssl == "Y" or is_ssl == "y":
                mail_dict["ssl"] = True
                break
            elif is_ssl == "N" or is_ssl == "n":
                mail_dict["ssl"] = False
                break
            else:
                print("输入错误")
        print("输入SMTP服务器地址（如smtp.qq.com）：")
        mail_dict["host"] = input()
        while True:
            print("输入SMTP服务器端口（如465）：")
            try:
                mail_dict["port"] = int(input())
                break
            except ValueError:
                print("输入错误")
        print("输入账号：")
        mail_dict["account"] = input()
        print("输入密码：")
        mail_dict["password"] = input()
        print("输入发件人邮箱：")
        mail_dict["sender"] = input()
        print("输入收件人邮箱：")
        mail_dict["receiver"] = input()
        try:
            try_send_mail(mail_dict)
        except Exception:
            print("发送出现问题，开始重新设置")
            continue
        print("已发送测试消息，是否收到消息？(Y/N)")
        is_receive = input()
        if is_receive == "Y" or is_receive == "y":
            break
        elif is_receive == "N" or is_receive == "n":
            print("开始重新设置")
        else:
            print("输入错误，默认开始重新设置")
    return mail_dict


# 尝试发送qq消息
def try_send_qq_msg(config):
    url = config["url"]
    data_user = {
        "user_id": config["uid"],
        "message": "【WHUT-EnergyBillMonitor】\n发送cqhttp私聊测试"
    }
    data_group = {
        "group_id": config["gid"],
        "message": "【WHUT-EnergyBillMonitor】\n发送cqhttp群聊测试"
    }
    if data_user["user_id"] != "":
        requests.get(url, params=data_user)
    if data_group["group_id"] != "":
        requests.get(url, params=data_group)


# 尝试发送邮件
def try_send_mail(config):
    if config["ssl"]:
        mail = smtplib.SMTP_SSL(config["host"], config["port"])
    else:
        mail = smtplib.SMTP_SSL(config["host"], config["port"])
    mail.login(config["account"], config["password"])
    msg = MIMEText("若收到该邮件，则SMTP配置无误", "plain", "utf-8")
    msg["From"] = formataddr(["WHUT-EnergyBillMonitor", config["sender"]])
    msg["Subject"] = "【WHUT-EnergyBillMonitor】邮件发送测试"
    mail.sendmail(config["sender"], config["receiver"], msg.as_string())
    mail.close()


# 保存配置文件
def save_config():
    print(f"配置文件内容预览：{config_all}")
    config_file = open("./config.yaml", "w")
    yaml.safe_dump(config_all, config_file)
    print(f"配置文件保存成功：config.yaml")
    config_file.close()


if __name__ == "__main__":
    print("开始设置配置文件 config.yaml")
    while True:
        print("=====账号=====")
        if init_account():
            break
    while True:
        print("=====房间=====")
        if init_room():
            break
    print("=====消息=====")
    init_msg()
    print("=====保存=====")
    save_config()
    print("配置文件设置完毕！")
    print("注意：配置文件中含有账号密码敏感信息，注意防范泄露。")
