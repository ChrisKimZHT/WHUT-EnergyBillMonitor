import requests
import yaml
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

# 读入配置文件
with open("./config.yaml") as config_file:
    config_all = yaml.safe_load(config_file)
cqhttp = False
mail = False
# 如果有cqhttp配置，则读取
if "cqhttp" in config_all["msg"].keys():
    cqhttp = True
    url = config_all["msg"]["cqhttp"]["url"]
    uid = config_all["msg"]["cqhttp"]["uid"]
    gid = config_all["msg"]["cqhttp"]["gid"]
# 如果有邮箱配置，则读取
if "mail" in config_all["msg"].keys():
    mail = True
    ssl = config_all["msg"]["mail"]["ssl"]
    host = config_all["msg"]["mail"]["host"]
    port = config_all["msg"]["mail"]["port"]
    account = config_all["msg"]["mail"]["account"]
    password = config_all["msg"]["mail"]["password"]
    sender = config_all["msg"]["mail"]["sender"]
    receiver = config_all["msg"]["mail"]["receiver"]


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
            server = smtplib.SMTP(host, port)
        server.login(account, password)
        msg = MIMEText(text, "plain", "utf-8")
        msg["From"] = formataddr(["WHUT-EnergyBillMonitor", sender])
        msg["Subject"] = "【WHUT-EnergyBillMonitor】"
        server.sendmail(sender, receiver, msg.as_string())
        server.close()
