import time

open_time=int(time.time())

while True:
    now_time=int(time.time())
    if now_time == open_time+30:
        print("30s到")
        break
    print(now_time)