import requests
import yaml

# 读入配置文件
with open("./config.yaml") as config_file:
    config_all = yaml.safe_load(config_file)
# 账号密码
account = config_all["account"]
password = config_all["password"]
# 房间编号
roomno = config_all["room"]["roomno"]
factorycode = config_all["room"]["factorycode"]
area = config_all["room"]["area"]

# 登录取得的 SessionID
session: requests.Session

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
    global session
    url = "http://cwsf.whut.edu.cn/MNetWorkUI/userLoginAction!mobileUserLogin.action"
    data = f"nickName={account}&password={password}"
    session = requests.Session()
    session.post(url=url, headers=headers, data=data)
    return session


# 获取数据
def get_data():
    url = "http://cwsf.whut.edu.cn/MNetWorkUI/elecManage!querySydl10497"
    data = f"roomno={roomno}&factorycode={factorycode}&area={area}"
    respounce = session.post(url=url, headers=headers, data=data).json()
    return respounce
