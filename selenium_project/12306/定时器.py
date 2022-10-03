import time
import datetime
# while True:
#     time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) # 刷新
#     print(time_now)
#     if time_now == "2022-09-20 14:15:00": #此处设置每天定时的时间
#     # 此处3⾏替换为需要执⾏的动作
#         print("hello")
#     subject = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 定时发送测试"
#     print('\r%s' %subject,end='')
#     time.sleep(1) # 因为以秒定时，所以暂停2秒，使之不会在1秒内执⾏多次
# s = time.perf_counter()
# time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) # 刷新
# dateTime_now = datetime.datetime.strptime(time_now,"%Y-%m-%d %H:%M:%S")
# # datetime.datetime.now().strftime('%Y-%m-%d')

# time.sleep(3)

# time_now_3 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) # 刷新
# dateTime_now_3 = datetime.datetime.strptime(time_now_3,"%Y-%m-%d %H:%M:%S")
# print("一共用时{}秒".format(dateTime_now_3 - dateTime_now))
# print(time.perf_counter() - s)

tiss = datetime.datetime.now()
time.sleep(2)
tisss = datetime.datetime.now()
print(tiss)
print(tisss)
print((tisss-tiss).seconds)
