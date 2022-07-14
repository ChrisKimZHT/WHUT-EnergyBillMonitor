import requests
from config import conf_dormitory
from logger import log


def login() -> tuple:
    log.info("进行登录操作")
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
    url = "http://cwsf.whut.edu.cn/MNetWorkUI/userLoginAction!mobileUserLogin.action"
    data = f"nickName={conf_dormitory['account']}&password={conf_dormitory['password']}"
    log.debug(f"发送请求: {data}")
    session = requests.Session()
    respounce = session.post(url=url, headers=headers, data=data).json()
    log.debug(f"收到响应: {respounce}")
    if respounce["returncode"] == "SUCCESS":
        log.info("登陆成功")
        return True, session
    else:
        log.error("登陆失败")
        return False, session


def mafangshan(session: requests.Session) -> dict:
    log.info("进行马房山校区查询")
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        # "Content-Length": "",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        # "Cookie": "JSESSIONID=",
        "Host": "cwsf.whut.edu.cn",
        "Origin": "http://cwsf.whut.edu.cn",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://cwsf.whut.edu.cn/MNetWorkUI/nyyPayElecPages51274E035",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "X-KL-Ajax-Request": "Ajax_Request",
        "X-Requested-With": "XMLHttpRequest",
    }
    url = "http://cwsf.whut.edu.cn/MNetWorkUI/queryReserve"
    data = f"meterId={conf_dormitory['mafangshan']['meterId']}&factorycode={conf_dormitory['mafangshan']['factorycode']}"
    log.debug(f"发送请求: {data}")
    respounce = session.post(url=url, headers=headers, data=data).json()
    log.debug(f"收到响应: {respounce}")
    return respounce


def yujiatou(session: requests.Session) -> dict:
    log.info("进行余家头校区查询")
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        # "Content-Length": "",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        # "Cookie": "JSESSIONID=",
        "Host": "cwsf.whut.edu.cn",
        "Origin": "http://cwsf.whut.edu.cn",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://cwsf.whut.edu.cn/MNetWorkUI/elecdetails51244E023",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "X-KL-Ajax-Request": "Ajax_Request",
        "X-Requested-With": "XMLHttpRequest",
    }
    url = "http://cwsf.whut.edu.cn/MNetWorkUI/elecManage!querySydl10497"
    data = f"roomno={conf_dormitory['yujiatou']['roomno']}&factorycode={conf_dormitory['yujiatou']['factorycode']}&area={conf_dormitory['yujiatou']['area']}"
    log.debug(f"发送请求: {data}")
    respounce = session.post(url=url, headers=headers, data=data).json()
    log.debug(f"收到响应: {respounce}")
    return respounce


def query_data() -> dict:
    ret = login()
    if ret[0]:
        if conf_dormitory["is_mafangshan"]:
            return mafangshan(ret[1])
        else:
            return yujiatou(ret[1])
    else:
        pass


print(query_data())
