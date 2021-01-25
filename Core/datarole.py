import copy

DataRole = copy.copy(list)


def createDataRole(data, roleIsSequential=False) -> DataRole:
    """
    :param data:
    :type data:typing.Dict[int,object]
    :param roleIsSequential:
    :return:
    """

    if roleIsSequential:
        return list(data.values())
    __dataRole = []
    for __i in data:
        __dataRole.insert(__i, data[__i])


def setDataRole(dataRole: DataRole, which: int, data):
    dataRole[which] = data


def getDataRole(dataRole: DataRole, which):
    return dataRole[which]
