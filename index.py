import timeit

while True :
    time_count = timeit.default_timer()  # 시작 시간 체크
    start_time = 0
    print(time_count)
    for i in range(100000000):
        start_time += 1
terminate_time = timeit.default_timer()  # 종료 시간 체크

print("%f초 걸렸습니다." % (terminate_time - start_time))