from logger import log


def get_history() -> float:
    try:
        log.debug("读取历史记录")
        with open("./history.txt", "r") as file:
            last_remain = file.read()
        log.debug(f"历史电量: {last_remain}")
        return float(last_remain)
    except:
        log.debug("读取出现异常，尝试初始化历史文件")
        save_history(0.0)
        return 0.0


def save_history(value: float) -> None:
    log.debug(f"写入历史记录: {value}")
    with open("./history.txt", "w") as file:
        file.write(str(value))
