import requests
import yaml

# import smtplib

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
config_dict = {
    "account": "",
    "password": "",
    "room": {},
    "msg": {}
}


def init_account():
    global config_dict
    print("输入账号（通常为学号）：")
    account = input()
    print("输入密码（默认为身份证后六位）：")
    password = input()
    if try_login(account, password):
        print("登陆成功")
        config_dict["account"] = account
        config_dict["password"] = password
        return True
    else:
        print("登录失败")
        return False


def try_login(account, password):
    global session
    url = "http://cwsf.whut.edu.cn/MNetWorkUI/userLoginAction!mobileUserLogin.action"
    data = f"nickName={account}&password={password}"
    respounce = session.post(url=url, headers=headers, data=data).json()
    if respounce["returncode"] == "SUCCESS":
        return True
    else:
        return False


def init_room():
    print("[1] 余家头电费\n"
          "[暂不支持] 马房山学生电费\n"
          "[暂不支持] 马房山电费\n"
          "选择区域：")
    choice = int(input())
    if choice == 1:
        if yujiatou_room():
            return True
    # elif choice == 2:
    #     mafangshan_stu_room()
    # elif choice == 3:
    #     mafangshan_room()
    return False


def yujiatou_room():
    global config_dict
    room_dict = {
        "factorycode": "",
        "area": "",
        "AreaID": "",
        "ArchitectureID": "",
        "floor": "",
        "roomno": "",
    }
    print("[1] 学生区域: 余家头校区\n"
          "[暂不支持] 教工区域: 家属区\n"
          "选择区域：")
    choice_area = int(input())
    if choice_area == 1:
        room_dict["factorycode"] = "E023"
        room_dict["area"] = "9004"
    # elif choice_area == 2:
    #     pass
    respounce_areaid = session.post(
        url="http://cwsf.whut.edu.cn/MNetWorkUI/elecManage!queryCampusList10497", headers=headers,
        data=f"factorycode={room_dict['factorycode']}&area={room_dict['area']}"
    ).json()
    for row in respounce_areaid["buildinglist"]:
        print(f"[{row['AreaID']}] {row['AreaName']}")
    print("选择校区：")
    room_dict["AreaID"] = input()
    respounce_architectureid = session.post(
        url="http://cwsf.whut.edu.cn/MNetWorkUI/elecManage!queryFloorsList10497", headers=headers,
        data=f"Area_ID={room_dict['AreaID']}&factorycode={room_dict['factorycode']}&area={room_dict['area']}"
    ).json()
    for row in respounce_architectureid["buildinglist"]:
        print(f"[{row['ArchitectureID']}] {row['ArchitectureName']}")
    print("选择楼栋：")
    room_dict["ArchitectureID"] = input()
    floor_begin = 0
    floor_end = 0
    for row in respounce_architectureid["buildinglist"]:
        if row["ArchitectureID"] == room_dict["ArchitectureID"]:
            floor_begin = row["ArchitectureBegin"]
            floor_end = row["ArchitectureStorys"]
    print(f"当前楼栋可选楼层为{floor_begin}~{floor_end}\n"
          f"选择楼层：")
    room_dict["floor"] = input()
    respounce_ammeterid = session.post(
        url="http://cwsf.whut.edu.cn/MNetWorkUI/elecManage!queryRoomList10497", headers=headers,
        data=f"floor={room_dict['floor']}&ArchitectureID={room_dict['ArchitectureID']}&factorycode={room_dict['factorycode']}&area={room_dict['area']}"
    ).json()
    for row in respounce_ammeterid["roomlist"]:
        print(f"[{row['AmMeter_ID']} {row['RoomName']}]")
    print("选择房间：")
    room_dict["roomno"] = input()
    respounce = try_get_data(room_dict["roomno"], room_dict["factorycode"], room_dict["area"])
    if respounce["returncode"] == "SUCCESS":
        config_dict["room"] = room_dict
        print("查询成功\n"
              f"剩余电量：{respounce['roomlist']['remainPower']} kW·h\n"
              f"累计电量：{respounce['roomlist']['ZVlaue']} kW·h\n"
              f"查表时间：{respounce['roomlist']['readTime']}")
        return True
    else:
        print("查询失败")
        return False


# def mafangshan_stu_room():
#     pass
#
#
# def mafangshan_room():
#     pass


def try_get_data(roomno, factorycode, area):
    url = "http://cwsf.whut.edu.cn/MNetWorkUI/elecManage!querySydl10497"
    data = f"roomno={roomno}&factorycode={factorycode}&area={area}"
    respounce = session.post(url=url, headers=headers, data=data).json()
    return respounce


def init_msg():
    global config_dict
    msg_dict = {
        "typ": 0
    }
    print("[1] cqhttp\n"
          "[暂不支持] 邮件\n"
          "选择发信方式：")
    choice_msg = int(input())
    if choice_msg == 1:
        cqhttp_dict = {
            "url": "127.0.0.1:5700",
            "uid": "",
            "gid": ""
        }
        msg_dict["typ"] = 1
        print("输入cqhttp的http监听地址和端口（留空默认为127.0.0.1:5700）：")
        input_url = input()
        if input_url != "":
            cqhttp_dict["url"] = input_url
        print("输入收信QQ号（留空则不发送私聊）：")
        input_uid = input()
        if input_uid != "":
            cqhttp_dict["uid"] = input_uid
        print("输入收信QQ群号（留空则不发送群聊）：")
        input_gid = input()
        if input_gid != "":
            cqhttp_dict["gid"] = input_gid
        msg_dict["cqhttp"] = cqhttp_dict
        config_dict["msg"] = msg_dict
        try_send_qq_msg()
        print("已发送测试消息，注意查收")
    # elif choice_msg == 2:
    #     pass


def try_send_qq_msg():
    url = "http://" + config_dict["msg"]["cqhttp"]["url"] + "/send_msg"
    data_user = {
        "user_id": config_dict["msg"]["cqhttp"]["uid"],
        "message": "这是一条来自WHUT-EnergyBillMonitor的测试消息"
    }
    data_group = {
        "group_id": config_dict["msg"]["cqhttp"]["gid"],
        "message": "这是一条来自WHUT-EnergyBillMonitor的测试消息"
    }
    if data_user["user_id"] != "":
        requests.get(url, params=data_user)
    if data_group["group_id"] != "":
        requests.get(url, params=data_group)


def save_config():
    print(f"配置文件内容预览：{config_dict}")
    config_file = open("./config.yaml", "w")
    yaml.safe_dump(config_dict, config_file)
    print(f"配置文件保存成功：config.yaml")
    config_file.close()


def init():
    print("开始设置配置文件 config.yaml")
    print("=====账号=====")
    if not init_account():
        return
    print("=====房间=====")
    if not init_room():
        return
    print("=====消息=====")
    init_msg()
    print("=====保存=====")
    save_config()
    print("配置文件设置完毕")


init()
