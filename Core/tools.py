import math


def heap_search(heap: list, v, lessThan=lambda __a, __b: __a < __b):
    __heapLen = len(heap)
    if __heapLen == 0:
        return None, None
    __index, __candidateCount = __heapLen // 2, __heapLen / 2
    while __candidateCount > 1:
        if lessThan(v, heap[__index]):
            __candidateCount = math.floor(__candidateCount)
            __index -= int(math.ceil(__candidateCount / 2))
            __candidateCount /= 2
        else:
            __candidateCount = math.ceil(__candidateCount)
            __index += int(math.floor(__candidateCount / 2))
            __candidateCount /= 2

    if __index == 1 and lessThan(v, heap[__index]):
        __index -= 1

    if lessThan(v, heap[__index]):
        if __index == 0:
            return None, 0
        return __index - 1, __index
    elif lessThan(heap[__index], v):
        if __index == __heapLen - 1:
            return __heapLen, None
        return __index, __index + 1
    else:
        return __index


def heap_insert(heap: list, v, lessThan=lambda __a, __b: __a < __b):
    __index = heap_search(heap, v, lessThan=lessThan)
    if isinstance(__index, int):
        heap[__index] = v
    else:
        if __index[1] is None:
            heap.append(v)
        else:
            heap.insert(__index[1], v)


def count_if(iterable, func):
    __c = 0
    for __i in iterable:
        if func(__i):
            __c += 1
    return __c
