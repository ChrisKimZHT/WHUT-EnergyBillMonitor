from request_website import get_session_id, get_data
from history import get_history, save_history
from send_msg import send_msg


def main():
    get_session_id()
    data = get_data()
    history = get_history()
    text = f"【用电情况】\n" \
           f"剩余电量: {data['roomlist']['remainPower']} kW·h\n" \
           f"累计电量: {data['roomlist']['ZVlaue']} kW·h\n" \
           f"使用电量: {round(float(data['roomlist']['ZVlaue']) - float(history), 2)} kW·h（距上次运行）\n" \
           f"查表时间: {data['roomlist']['readTime']}"
    save_history(data['roomlist']['ZVlaue'])
    if float(data['roomlist']['remainPower']) < 15.00:
        text += "\n[!] 电量不足，注意及时充值 [!]"
    print(text)
    send_msg(text)


if __name__ == "__main__":
    main()
