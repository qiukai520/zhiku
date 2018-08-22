import datetime
import time
from datetime import timedelta
import calendar



# 天
# now = datetime.datetime.today()
# today_zero = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,microseconds=now.microsecond)
# deadline = today_zero + timedelta(hours=18)
# print(now)
# print(deadline)


# 周
# today = datetime.date.today().weekday()
# target_day = calendar.FRIDAY
# print(target_day)
# del_day = target_day-today
#
# now = datetime.datetime.today()
# today_zero = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,microseconds=now.microsecond)
# deadline = today_zero + timedelta(del_day)
# deadline += timedelta(hours=18)
# deadline = deadline.strftime("%Y-%m-%d %H:%M:%S")
# print(deadline)


# 月
# current_year = datetime.date.today().year
# current_month = datetime.date.today().month
# print(current_month,current_year)
# # 获取当前月第一天的星期和当月的总天数
# firstDayWeekDay, monthRange = calendar.monthrange(current_year, current_month)
# print(calendar.monthrange(current_year, current_month))
# #  获取当前月的第一天
# firstDay = datetime.date(year=current_year, month=current_month, day=1)
# # 获取当前月的第一天
# lastDay = datetime.date(year=current_year, month=current_month, day=monthRange)
#
# print(firstDay,lastDay)

