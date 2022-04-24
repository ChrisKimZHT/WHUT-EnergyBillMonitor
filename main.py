from request_website import get_session_id, get_data
from send_msg import send_msg


def main():
    get_session_id()
    data = get_data()
    text = f"【用电情况】\n" \
           f"剩余电量: {data['roomlist']['remainPower']} kW·h\n" \
           f"累计电量: {data['roomlist']['ZVlaue']} kW·h\n" \
           f"查表时间: {data['roomlist']['readTime']}"
    print(text)
    send_msg(text)


if __name__ == "__main__":
    main()
