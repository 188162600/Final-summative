import random


def _createUUIDDateField(digit: int):
    __date = str(random.randint(0, 10 ** digit - 1))
    return '0' * (digit - len(__date)) + __date


# create a universal unique id and return a string like this "00000000-0000-0000-0000-000000000000".
def createUUID():
    return f"{_createUUIDDateField(8)}-" \
           f"{_createUUIDDateField(4)}-" \
           f"{_createUUIDDateField(4)}-" \
           f"{_createUUIDDateField(2)}{_createUUIDDateField(2)}-" \
           f"{_createUUIDDateField(2)}{_createUUIDDateField(2)}{_createUUIDDateField(2)}{_createUUIDDateField(2)}{_createUUIDDateField(2)}"
