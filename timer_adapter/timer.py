try:
    from altimer import Altimer

    def Timer(period_ms, func, delay_ms=0):
        return Altimer(period_ms, func, delay_ms)


except Exception:
    from machine import Timer as mTimer

    def Timer(period_ms, func, delay_ms=0):
        t = mTimer(-1)

        def init():
            t.init(period=period_ms, mode=Timer.PERIODIC, callback=func)

        if delay_ms:
            r = mTimer(-1)
            r.init(period=delay_ms, mode=Timer.ONE_SHOT, callback=init)
        else:
            init()
        return t
