from request_website import get_session_id, get_data
from history import get_history, save_history
from send_msg import send_msg


def main():
    try:
        get_session_id()
        data = get_data()
    except Exception:
        print("[ERROR] 获取电量信息失败")
        send_msg("【用电情况】获取电量数据失败")
        return
    try:
        history = get_history()
    except Exception:
        print("[WARNING] 获取上次电量失败")
        send_msg("【用电情况】获取上次电量失败")
        history = 0
    text = f"【用电情况】\n" \
           f"剩余电量: {data['roomlist']['remainPower']} kW·h\n" \
           f"累计电量: {data['roomlist']['ZVlaue']} kW·h\n" \
           f"使用电量: {round(float(data['roomlist']['ZVlaue']) - float(history), 2)} kW·h（距上次运行）\n" \
           f"查表时间: {data['roomlist']['readTime']}"
    try:
        save_history(data['roomlist']['ZVlaue'])
    except Exception:
        print("[WARNING] 保存本次电量失败")
        send_msg("【用电情况】保存本次电量失败")
    if float(data['roomlist']['remainPower']) < 15.00:
        text += "\n[!] 电量不足，注意及时充值 [!]"
    try:
        print(text)
        send_msg(text)
    except:
        print("[ERROR] 消息发送失败")


if __name__ == "__main__":
    main()
