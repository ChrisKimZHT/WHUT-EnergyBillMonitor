import requests
import yaml
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

# 读入配置文件
config_file = open("./config.yaml")
config_dict = yaml.safe_load(config_file)
config_file.close()
# cqhttp 配置
cqhttp = False
mail = False
if "cqhttp" in config_dict["msg"].keys():
    cqhttp = True
    url = "http://" + config_dict["msg"]["cqhttp"]["url"] + "/send_msg"
    uid = config_dict["msg"]["cqhttp"]["uid"]
    gid = config_dict["msg"]["cqhttp"]["gid"]
if "mail" in config_dict["msg"].keys():
    mail = True
    ssl = config_dict["msg"]["mail"]["ssl"]
    host = config_dict["msg"]["mail"]["host"]
    port = config_dict["msg"]["mail"]["port"]
    account = config_dict["msg"]["mail"]["account"]
    password = config_dict["msg"]["mail"]["password"]
    sender = config_dict["msg"]["mail"]["sender"]
    receiver = config_dict["msg"]["mail"]["receiver"]


# 发送信息
def send_msg(text):
    if cqhttp:
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
    if mail:
        if ssl:
            server = smtplib.SMTP_SSL(host, port)
        else:
            server = smtplib.SMTP_SSL(host, port)
        server.login(account, password)
        msg = MIMEText(text, "plain", "utf-8")
        msg["From"] = formataddr(["WHUT-EnergyBillMonitor", sender])
        msg["Subject"] = "【WHUT-EnergyBillMonitor】"
        server.sendmail(sender, receiver, msg.as_string())
        server.close()
