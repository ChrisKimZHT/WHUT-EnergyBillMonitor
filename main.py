import requests

# 账号密码
account = ""
password = ""
# 房间编号
roomno = ""
factorycode = ""
area = ""
# 消息发送
uid = ""
gid = ""

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


# 登录取得 SessionID
def get_session_id():
    url = "http://cwsf.whut.edu.cn/MNetWorkUI/userLoginAction!mobileUserLogin.action"
    data = f"nickName={account}&password={password}"
    session = requests.Session()
    session.post(url=url, headers=headers, data=data)
    return session


# 获取数据
def get_data(session):
    url = "http://cwsf.whut.edu.cn/MNetWorkUI/elecManage!querySydl10497"
    data = f"roomno={roomno}&factorycode={factorycode}&area={area}"
    respounce = session.post(url=url, headers=headers, data=data).json()
    return respounce


# 发送信息
def send_msg(text):
    url = "http://127.0.0.1:5700/send_msg"
    data_user = {
        "user_id": uid,
        "message": text
    }
    data_group = {
        "group_id": gid,
        "message": text
    }
    if data_user["user_id"] != "":
        requests.get(url, params=data_user)
    if data_group["group_id"] != "":
        requests.get(url, params=data_group)


def main():
    session = get_session_id()
    data = get_data(session)
    print(data)
    text = f"【用电情况】\n" \
           f"剩余电量: {data['roomlist']['remainPower']} kW·h\n" \
           f"累计电量: {data['roomlist']['ZVlaue']} kW·h\n" \
           f"查表时间: {data['roomlist']['readTime']}\n"
    print(text)
    send_msg(text)


if __name__ == "__main__":
    main()
