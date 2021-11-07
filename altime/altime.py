import sys
import time

import ntptime
from machine import RTC
from micropython import const
from timers import Tmr

_rtc = RTC()

synced_time_sec = time.time()
time_diff_ms = time.ticks_ms()
DEBUG = True
TIMEZONE = 2  # from 0 UTC
_TIME_2000 = const(946684800)
_ONE_MINUTE = const(60 * 1000)


def _init_time():
    global synced_time_sec, time_diff_ms
    time_diff_ms = time.ticks_ms()
    synced_time_sec = time.time() + _TIME_2000 * 3600


_init_time()


def _time_tick(*args):
    global synced_time_sec, time_diff_ms
    current_t = time.ticks_ms()
    diff_int = time.ticks_diff(current_t, time_diff_ms)
    diff = str(diff_int)
    if diff_int >= 1000:
        seconds = int(diff[:-3])
        millis = int(diff[-3:])
    else:
        seconds = 0
        millis = diff_int
    synced_time_sec += seconds
    time_diff_ms = time.ticks_add(current_t, -millis)


def sync_time(*r):
    try:
        ntptime.settime()
        _init_time()
        (year, month, mday, hour, minute, second, weekday, yearday) = time.localtime(
            time.time() + TIMEZONE * 60 * 60
        )
        _rtc.datetime((year, month, mday, 0, hour, minute, second, 0))
        if DEBUG:
            print("Time-sync is done. Current time", _rtc.datetime())
        return
    except Exception as e:
        if DEBUG:
            print("Can not sync time")
            sys.print_exception(e)


def get_secs():
    current_t = time.ticks_ms()
    diff = time.ticks_diff(current_t, time_diff_ms)
    seconds = 0
    if diff >= 1000:
        seconds = int(str(diff)[:-3])
    return synced_time_sec + seconds


def get_ms():
    current_t = time.ticks_ms()
    diff = str(time.ticks_diff(current_t, time_diff_ms))
    seconds = 0
    if diff >= 1000:
        seconds = int(diff[:-3])
    return (synced_time_sec + seconds) * 1000 + int(diff[-3:])


def get_datetime():  # -> (year, month, mday, hour, minute, second, weekday, yeardays)
    return time.localtime(get_secs())


def get_rtc():
    (year, month, mday, hour, minute, second, weekday, yearday) = get_datetime()
    _rtc.datetime((year, month, mday, 0, hour, minute, second, 0))
    return _rtc


def to_minutes(h, m):
    if h >= 24 or m < 0 or m >= 60:
        raise Exception("Incorrect values Hours should be [0,23], minutes [0, 59]")
    return int(h * 60 + m)


def is_current_time_in_range(minutes_from, minutes_to):
    dt = get_datetime()
    current_minutes = to_minutes(dt[3], dt[4])
    if minutes_from > minutes_to:
        return current_minutes >= minutes_from or current_minutes <= minutes_to
    else:
        return minutes_from <= current_minutes <= minutes_to


def get_time_diff_ms(cmp_to_ms):
    crnt = get_secs()
    if cmp_to_ms > 1000:
        return crnt - (int(str(cmp_to_ms)[:-3]) - _TIME_2000)
    else:
        return crnt


_clock_timer = Tmr(period_ms=_ONE_MINUTE, func=_time_tick)  # 1m
_time_sync_timer = Tmr(period_ms=24 * 60 * _ONE_MINUTE, func=sync_time)  # 1D
