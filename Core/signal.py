__signals = {}


def signal(func):
    def _(*args, **kwargs):
        for __i in __signals.get(_):
            __i(*args, **kwargs)
        func(*args, **kwargs)

    __signals.update({_: []})
    return _


# NOTE: The process that the signal call the slot is not thread-safe
def connect(__signal, __slot):
    try:
        __slots: list = __signals.get(__signals)
        __slots.append(__slot)
    except KeyError:
        pass

def disconnect(__signal, __slot):
    try:
        __slots: list = __signals.get(__signals)
        __slots.remove(__slot)
    except KeyError:
        pass


