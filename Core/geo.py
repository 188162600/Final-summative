import math
import Core.tools
import pygame
import random

IntersectionType = int
NoIntersection = 0
UnboundedIntersection = 1
BoundedIntersection = 2

__360Div2Pi = 180 / math.pi


def fuzzCompare(a, b):
    return (a - 0.000001) < b < (a + 0.000001)


def radianToAngle(r):
    return r * __360Div2Pi


def angleToRadian(angle):
    return angle / __360Div2Pi


def makeLine(a: float, k):
    return a, k


def lineFromPointSlope(point, slope):
    __k = point[1] - slope * point[0]
    return makeLine(slope, __k)


def lineFromPointAngle(point, angle, *, fromRadius=False):
    if not fromRadius:
        angle /= __360Div2Pi
    __a = math.tan(angle)
    __k = point[1] - __a * point[0]
    return makeLine(__a, __k)


def line_a(line):
    return line[0]


def line_k(line):
    return line[1]


def line_produce(line, x):
    return line_k(line) + line_a(line) * x


def line_pointAtY(line, y):
    if line_a(line) == 0:
        if line_k(line) == y:
            return y
        return None
    return (y - line_k(line) / line_a(line)), y


def line_intersection(line, other):
    if line_a(line) == math.inf or line_a(line) == -math.inf:
        if line_a(other) == math.inf or line_a(other) == -math.inf:
            return 0, 0
        return 0, line_produce(other, 0)
    if line_a(other) == math.inf or line_a(other) == -math.inf:
        return 0, line_produce(line, 0)
    if line_a(line) == line_a(other):
        if line_k(line) == line_k(other):
            return 0, line_k(line)
        return None
    __x = (line_k(line) - line_k(other)) / (line_a(other) - line_a(line))
    return __x, line_produce(line, __x)


def seg_fromAngle(angle, start, length, *, fromRadian=False):
    if not fromRadian:
        angle = angleToRadian(angle)
    if angle == math.pi / 2:
        return start, (start[0], start[1] - length)
    elif angle == -math.pi / 2:
        return start, (start[0], start[1] + length)
    __xDistance, __yDistance = math.cos(angle) * length, math.sin(angle) * length
    return makeSegment(start, (start[0] + __xDistance, start[1] + __yDistance))


def makeSegment(p1: tuple = (0, 0), p2: tuple = (0, 0)):
    return p1, p2


def seg_pointAtX(seg, x, considerContains=True):
    if considerContains and not inRange(seg_x1(seg), seg_x2(seg), x):
        return None
    __xDis = seg_xDistance(seg)
    if __xDis == 0:
        return x, seg_y1(seg)
    __a = seg_yDistance(seg) / __xDis
    return x, __a * (x - seg_x1(seg)) + seg_y1(seg)


def seg_p1(seg):
    return seg[0]


def seg_p2(seg):
    return seg[1]


def seg_x1(seg):
    return seg_p1(seg)[0]


def seg_x2(seg):
    return seg_p2(seg)[0]


def seg_y1(seg):
    return seg_p1(seg)[1]


def seg_y2(seg):
    return seg_p2(seg)[1]


def seg_length(seg):
    return math.sqrt(seg_xDistance(seg) ** 2 + seg_yDistance(seg) ** 2)


def seg_xDistance(seg):
    return seg_x2(seg) - seg_x1(seg)


def seg_yDistance(seg):
    return seg_y2(seg) - seg_y1(seg)


def seg_pointAt(seg, time: float):
    return seg_x1(seg) + seg_xDistance(seg) * time, seg_y1(seg) + seg_yDistance(seg) * time


def seg_angle(seg, *, returnRadian=False):
    if (seg_xDistance(seg)) == 0:
        __r = math.pi / 2
    else:
        __r = math.atan(seg_yDistance(seg) / seg_xDistance(seg))
    if seg_xDistance(seg) < 0:
        __r = math.pi + __r
    return __r if returnRadian else radianToAngle(__r)


def seg_normalVector(seg, length):
    return seg_fromAngle(seg_normalVectorAngle(seg, returnRadian=True), seg_center(seg), length, fromRadian=True)


# def seg_slope(seg, precise=False):
#     __xDistance = seg_xDistance(seg)
#     if __xDistance == 0:
#         return math.inf
#     if precise and __xDistance < 0:
#         return seg_yDistance(seg) / seg_xDistance(seg)
#     return -seg_yDistance(seg) / seg_xDistance(seg)


def seg_angleTo(seg, otherSeg, *, returnRadian=False):
    return seg_angle(seg, returnRadian=returnRadian) - seg_angle(otherSeg, returnRadian=returnRadian)


def seg_normalVectorAngle(seg, *, returnRadian=False):
    if returnRadian:
        return seg_angle(seg, returnRadian=returnRadian) - math.pi / 2

    return seg_angle(seg, returnRadian=returnRadian) + 90


def seg_toLine(seg):
    __xDis = seg_xDistance(seg)
    return lineFromPointSlope(seg_p1(seg), math.inf if __xDis == 0 else seg_yDistance(seg) / seg_xDistance(seg))


def _seg_intersects(seg, otherSeg):
    return min(seg_x1(seg), seg_x2(seg)) <= max(seg_x1(otherSeg), seg_x2(otherSeg)) and \
           min(seg_y1(seg), seg_y2(seg)) <= max(seg_y1(otherSeg), seg_y2(otherSeg))


def inRange(limit1, limit2, v, elasticity=None):
    if elasticity is None:
        return limit1 <= v <= limit2 or limit2 <= v <= limit1
    return limit1 - elasticity <= v <= limit2 - elasticity or limit2 - elasticity <= v <= limit1 + elasticity


def seg_intersection(seg, otherLine_or_segment, point: list = None, *, otherIsSeg=True):
    if otherIsSeg:
        if seg_x1(otherLine_or_segment) == seg_x2(otherLine_or_segment):
            __inter = seg_pointAtX(seg, seg_x1(otherLine_or_segment), considerContains=False)
        else:
            if seg_x1(seg) == seg_x2(seg):
                print(seg_pointAtX(otherLine_or_segment, seg_x1(seg)))
                __inter = seg_pointAtX(otherLine_or_segment, seg_x1(seg), considerContains=False)
            else:
                __inter = line_intersection(seg_toLine(seg), seg_toLine(otherLine_or_segment))
    else:
        if line_a(otherLine_or_segment) == math.inf or line_a(otherLine_or_segment) == -math.inf:
            __inter = seg_pointAtX(seg, seg_x1(otherLine_or_segment), considerContains=False)
        else:
            __inter = line_intersection(seg_toLine(seg), otherLine_or_segment)
    if __inter is None:
        return NoIntersection
    if point is not None:
        point.clear()
        point.extend(__inter)
    if not (inRange(seg_x1(seg), seg_x2(seg), __inter[1], elasticity=0.000001) or
            inRange(seg_x1(otherLine_or_segment), seg_x2(otherLine_or_segment), __inter[1],
                    elasticity=0.000001)):
        return UnboundedIntersection
    return BoundedIntersection

    # if otherIsSeg else otherLine_or_segment)
    #
    # if __inter is None:
    #     return NoIntersection
    # if point is not None:
    #     point.clear()
    #     point.extend((__inter[0], __inter[1]))
    # if inRange(seg_x1(seg), seg_x2(seg), __inter[0]):
    #     if otherIsSeg and not inRange(seg_x1(otherLine_or_segment), seg_x2(otherLine_or_segment), __inter[0]):
    #         return UnboundedIntersection
    #     return BoundedIntersection
    # return UnboundedIntersection


def seg_center(seg):
    return (seg_x1(seg) + seg_x2(seg)) / 2, (seg_y1(seg) + seg_y2(seg)) / 2


# using radian
def rotatePoint(point: tuple, rotation, at: tuple) -> tuple:
    if (point[0] - at[0]) == 0:
        __oldRotation = math.pi / 2
    else:
        __oldRotation = math.atan((at[1] - point[1]) / (at[0] - point[0]))
    if point[0] < at[0]:
        __oldRotation = math.pi + __oldRotation
    __length = math.sqrt((point[1] - at[1]) ** 2 + (point[0] - at[0]) ** 2)
    __oldRotation += rotation
    # print(radianToAngle(__oldRotation), at[0] + math.cos(__oldRotation) * __length, at[1] + math.sin(__oldRotation) * __length)
    return at[0] + math.cos(__oldRotation) * __length, at[1] + math.sin(__oldRotation) * __length


# [topLeft,topRight,bottomRight,bottomLeft]
def rotateRectAt(rect: pygame.Rect, pos, rotation, *, useRadian=False) -> list:
    if not useRadian:
        rotation /= __360Div2Pi

    return [rotatePoint(rect.topleft, rotation, pos), rotatePoint(rect.topright, rotation, pos),
            rotatePoint(rect.bottomright, rotation, pos), rotatePoint(rect.bottomleft, rotation, pos)]


def translatePolygon(poly: list, x, y):
    __len_poly = len(poly)
    for __i in range(0, __len_poly):
        __point = poly[__i]
        poly[__i] = (__point[0] + x, __point[1] + y)


def polygonBoundingRect(polygon, *, key_pos=lambda __pos: __pos) -> pygame.Rect:
    """
    :type polygon: typing.Iterable
    :param key_pos:
    :return:
    """
    __top, __left, __right, __bottom = math.inf, math.inf, -math.inf, -math.inf
    for __item in polygon:
        __pos = key_pos(__item)
        __left, __top, __right, __bottom = min(__pos[0], __left), min(__pos[1], __top), \
                                           max(__pos[0], __right), max(__pos[1], __bottom)

    return pygame.Rect(__left, __top, __right - __left, __bottom - __top)


def rectAdjusted(rect: pygame.Rect, x1, y1, x2, y2):
    return pygame.Rect(rect.x + x1, rect.y + y1, rect.w + x2, rect.h + y2)


def adjustRect(rect: pygame.Rect, x1, y1, x2, y2):
    rect.x += x1
    rect.y += y1
    rect.w += x2
    rect.h += y2


def mapFromRectToRect(target: pygame.Rect, source: pygame.Rect, sourcePos: tuple):
    return ((sourcePos[0] - source.x) / source.w) * target.w + target.x, (
            (sourcePos[1] - source.y) / source.h) * target.h + target.y


def makeRegPolygon(center, sides: int, lengthToCenter: float, rotation=0, *, fromRadian=False):
    __radian = math.pi * 2 / sides
    __polygon = []
    __ro = rotation if fromRadian else angleToRadian(rotation)
    for __i in range(0, sides):
        __polygon.append(seg_p2(seg_fromAngle(__ro + __radian * __i, center, lengthToCenter, fromRadian=True)))
    return __polygon


def pointFToPoint(point):
    return int(point[0]), int(point[1])


def makeStar(center, sides, centerToConcaveSide: float, cornerHeight: float, rotation=0, *,
             fromRadian=False):
    if not fromRadian:
        rotation = angleToRadian(rotation)

    __poly = makeRegPolygon(center, sides, centerToConcaveSide, rotation, fromRadian=True)
    __star = []

    for __i in range(-1, sides - 1):
        __star.append(__poly[__i])
        __star.append(seg_p2(seg_fromAngle(seg_normalVectorAngle(
            makeSegment(__poly[__i], __poly[__i + 1]), returnRadian=True),
            seg_center(makeSegment(__poly[__i], __poly[__i + 1])), cornerHeight, fromRadian=True)))

    return __star


def makeCircle(center: tuple, r: float):
    return center, r


def circleCenter(circle):
    return circle[0]


def circleR(circle):
    return circle[1]


def perpendicularBisector(seg):
    __yDis = seg_yDistance(seg)
    __a = math.inf if __yDis == 0 else - seg_xDistance(seg) / __yDis
    return lineFromPointSlope(seg_center(seg), __a)


def triangleCircumcircle(p1: tuple, p2: tuple, p3: tuple):
    __line1, __line2 = seg_normalVector(makeSegment(p1, p2), 65535), seg_normalVector(makeSegment(p2, p3), 65535)
    __center = []
    seg_intersection(__line1, __line2, __center)
    # pygame.draw.line(pygame.display.get_surface(), (50, 122, 255), __line1[0], __line1[1])
    # pygame.draw.line(pygame.display.get_surface(), (50, 122, 255), __line2[0], __line2[1]),
    if not __center:
        __line3 = seg_normalVector(makeSegment(p2, p3), 65535)

        if not seg_intersection(__line2, __line3, __center, otherIsSeg=True):
            return makeCircle((0, 0), math.inf)
        return makeCircle((__center[0], __center[1]), math.inf)

    return makeCircle((__center[0], __center[1]), seg_length(makeSegment((__center[0], __center[1]), p1)))


def circleContains(circle, p):
    return abs(circleR(circle)) + 0.000001 >= abs(seg_length(makeSegment(circleCenter(circle), p)))


def sharedSides(polygons, *, key_pos=lambda __pos: __pos):
    """
    :type polygons: typing.Iterable[typing.Sequence]
    :param key_pos:
    :return: typing.Dict[Side,Polygons]
    """
    __sides = {}
    __sharedSides = {}
    for __polygon in polygons:
        for __i in range(-1, len(__sides) - 1):
            __side = (key_pos(__polygon[__i]), key_pos(__polygon[__i + 1]))
            if __side in __sides:
                __sharedSides.update({__side: [__sides[__side], __polygon]})
            elif __sides in __sharedSides:
                __sharedSides[__side].append(__polygon)
    return __sharedSides


def polygon_contains(polygon, point) -> bool:
    """
    This is based on ray casting algorithm.  https://en.wikipedia.org/wiki/Ray_casting
    :param polygon:
    :param point:
    :return:
    """
    __ray = lineFromPointAngle(point, 0, fromRadius=True)
    __leftIntersection, __rightIntersection = 0, 0
    for __i in range(-1, len(polygon) - 1):
        __inter, __p1, __p2 = [], polygon[__i], polygon[__i + 1]
        if seg_intersection(makeSegment(__p1, __p2), __ray, point=__inter, otherIsSeg=False) == BoundedIntersection:
            if __inter[0] > point[0]:
                if __inter[1] != __p1[1] and __inter[0] != __p2[0]:
                    __rightIntersection += 1

            elif __inter[0] < point[0]:

                if __inter[1] != __p1[1] and __inter[0] != __p2[0]:
                    __leftIntersection += 1

            else:
                __rightIntersection, __leftIntersection = __rightIntersection + 1, __leftIntersection + 1

    return bool(__rightIntersection % 2 and __rightIntersection != 0 and __leftIntersection % 2 and __leftIntersection)


def polygonCenter(polygon):
    __x, __y, __len = 0, 0, 0
    for __i in polygon:
        __x += __i[0]
        __y += __i[1]
        __len += 1
    if __len == 0:
        return 0, 0
    return __x / __len, __y / __len


def normalizedPolygon(polygon):
    __center = polygonCenter(polygon)
    __newPoly = []
    __slopeToVertex = []
    for __i in polygon:
        __slopeToVertex.append(seg_angle(makeSegment(__center, __i), returnRadian=True))
    __indexes = sorted(range(0, len(polygon)), key=lambda __i: __slopeToVertex[__i])
    for __i in __indexes:
        __newPoly.append(polygon[__i])
    return __newPoly


def randomPoint(restriction: pygame.Rect):
    return random.randint(restriction.left, restriction.right), random.randint(restriction.top, restriction.bottom)


def randomPoints(restriction: pygame.Rect, n):
    __points = []
    for __i in range(0, n):
        __points.append((random.randint(restriction.left, restriction.right),
                         random.randint(restriction.top, restriction.bottom)))
    return __points


def polygonSharedSides(polygons):
    """
    :type polygons: typing.Iterable[list]
    :return:
    """
    __edges = {}
    for __poly in polygons:
        for __i in range(-1, len(__poly) - 1):
            __side, __reveredSide = (__poly[__i], __poly[__i + 1]), (__poly[__i + 1], __poly[__i])
            if __side in __edges:
                __edges[__side] += 1
            elif __reveredSide in __edges:
                __edges[__reveredSide] += 1
            else:
                __edges.update({__side: 1})
    return filter(lambda __x: __edges[__x] > 1, __edges)


def polygonUnsharedSides(polygons):
    """
        :type polygons: typing.Iterable[list]
        :return:
        """
    __edges = {}
    for __poly in polygons:
        for __i in range(-1, len(__poly) - 1):
            __side, __reveredSide = (__poly[__i], __poly[__i + 1]), (__poly[__i + 1], __poly[__i])
            if __side in __edges:
                __edges[__side] += 1
            elif __reveredSide in __edges:
                __edges[__reveredSide] += 1
            else:
                __edges.update({__side: 1})
    return filter(lambda __x: __edges[__x] == 1, __edges)
#
# pygame.init()
#
# s = pygame.display.set_mode((500, 500))
# f = pygame.font.Font(pygame.font.get_default_font(), 10)
# t = ((200, 200), (300, 200), (250, 300))
# c = triangleCircumcircle(*t)
# pygame.draw.circle(s, (100, 100, 100), c[0], c[1])
# timer = pygame.time.Clock()
# p = (0, 0)
# pygame.draw.lines(s, (50, 50, 50), True, t)
# pygame.display.update()
#
# while True:
#     s.fill((0, 0, 0))
#     for e in pygame.event.get():
#         if e.type == pygame.MOUSEMOTION:
#             s.fill((0, 0, 0))
#             p = e.pos
#             print(p)
#         elif e.type == pygame.QUIT:
#             quit()
#         pygame.draw.circle(s, (100, 100, 100), c[0], c[1])
#         pygame.draw.lines(s, (50, 50, 50), True, t)
#
#         # pygame.draw.lines(s,(200,200,200),True,t)
#         pygame.draw.circle(s, (200, 200, 200), p, 10)
#
#         text = f.render(str(circleContains(c, p)), True, (200, 200, 200))
#         s.blit(text, (0, 0))
#         # pygame.display.update()
#         timer.tick(60)
