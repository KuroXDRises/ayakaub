from datetime import datetime, time


def is_overnight(start:time=time(22, 0), end:time=time(7, 0)) -> bool:
    now: time = datetime.now().time()
    return bool((now>=start) or (now<end))