from logger import log
from config import conf_dormitory
from query import query_data
from notification import msg
from history import get_history, save_history

if __name__ == "__main__":
    log.info("开始请求数据")
    data = query_data()
    log.debug(f"取得数据: {data}")
    if data["status"]:
        text = f"【用电情况】v1.0.1\n" \
               f"剩余电量: {data['remain']} kW·h\n" \
               f"累计电量: {data['total']} kW·h\n" \
               f"使用电量: {round(data['total'] - get_history(), 2)} kW·h（距上次运行）"
        if not conf_dormitory["is_mafangshan"]:
            text += f"\n查表时间: {data['time']}"
        text += "\n@WHUT-EnergyBillMonitor"
        if data['remain'] < 15.00:
            text += "\n[!] 电量不足，注意及时充值 [!]"
        log.debug(f"生成消息完成: \n{text}")
        save_history(data['total'])
        msg(text)
    else:
        msg("发生错误，请查看程序日志排查")
