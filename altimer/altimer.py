import sys
import time

import uheapq
from machine import Timer

_seq = []  # List[Tuple[AlTimer, start_at_ms]]


def _exec(*arg):
    if _seq:
        current_ms = time.ticks_ms()
        while _seq:
            tm_ms, tmr = uheapq.heappop(_seq)
            if not tmr._is_stopped():
                break
        if time.ticks_diff(tm_ms, current_ms) <= 0:
            try:
                tmr.func(tmr)
            except Exception as e:
                sys.print_exception(e)
            if not tmr._is_stopped():
                uheapq.heappush(_seq, (time.ticks_add(tm_ms, tmr.period_ms), tmr))
        else:
            uheapq.heappush(_seq, (tm_ms, tmr))


_main_sys_timer = Timer(-1)
_main_sys_timer.init(period=500, mode=Timer.PERIODIC, callback=_exec)


class AlTimer:
    def __init__(self, period_ms, func, delay=0) -> None:
        self.period_ms = period_ms
        self.func = func
        self._stop = False
        uheapq.heappush(_seq, (time.ticks_ms() + delay, self))

    def stop(self):
        self._stop = True

    def _is_stopped(self):
        return self._stop

    def __gt__(self, other):
        return self.period_ms > other.period_ms

    def __eq__(self, o):  # ->bool
        return self.period_ms == o.period_ms
