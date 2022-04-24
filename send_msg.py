import requests
import yaml

# 读入配置文件
config_file = open("./config.yaml")
config_dict = yaml.safe_load(config_file)
config_file.close()
# cqhttp 配置
url = "http://" + config_dict["msg"]["cqhttp"]["url"] + "/send_msg"
uid = config_dict["msg"]["cqhttp"]["uid"]
gid = config_dict["msg"]["cqhttp"]["gid"]


# 发送信息
def send_msg(text):
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
