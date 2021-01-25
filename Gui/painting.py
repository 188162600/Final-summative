import math
import pygame
import Core.geo
import Core.kernel


# def setMaskAt(target: pygame.Surface, mask, pos):
#     """
#     NOTE: the clor must have alpha
#     """
#     target.set_at(pos, maskColor(target.get_at(pos), mask))


def maskColor(color: tuple, mask: tuple):
    """
    NOTE: the colors must have alpha
    """
    if mask[3] == 255:
        return mask
    if color[3] == 0 and mask[3] == 0:
        return 0, 0, 0, 0
    __alpha, __colorAlpha = (color[3] + mask[3]) - (color[3] * mask[3]) // 255, color[3] * (255 - color[3]) // 255
    return ((color[0] * __colorAlpha + mask[0] * mask[3]) // __alpha,
            (color[1] * __colorAlpha + mask[1] * mask[3]) // __alpha,
            (color[2] * __colorAlpha + mask[2] * mask[3]) // __alpha
            , __alpha)


def fastMaskColor(color: tuple, mask: tuple):
    """
    NOTE: the colors must have alpha
    """
    if mask[3] == 255:
        return mask
    if color[3] == 0 and mask[3] == 0:
        return 0, 0, 0, 0
    __colorOpa = ((color[3] + mask[3]) - (color[3] * mask[3]) / 255) / 255
    return ((color[0] * __colorOpa + mask[0] * mask[3]),
            (color[1] * __colorOpa + mask[1] * mask[3]),
            (color[2] * __colorOpa + mask[2] * mask[3])
            , 255)


def fillSurface(target: pygame.Surface, colorAt_or_color, testValid=None, *, targetRect: pygame.Rect = None):
    """
    :param targetRect:

    :param target:
    :param colorAt_or_color: pygame.Color or callable
    :param testValid: (pos:typing.Tuple[int,int])->bool test if fillSurface need to set the color at a point
    :return:
    """
    if targetRect is None:
        targetRect = target.get_rect()
    else:
        targetRect.clamp(target.get_rect())
    if testValid is None:
        testValid = lambda __pos: True
    if isinstance(colorAt_or_color, tuple):
        __color = colorAt_or_color
        colorAt_or_color = lambda __pos: __color

    for __x in range(targetRect.left, targetRect.right):
        for __y in range(targetRect.top, targetRect.bottom):
            __pos = (__x, __y)
            if testValid(__pos):
                target.set_at(__pos, colorAt_or_color(__pos))


# def blit(target: pygame.Surface, source: pygame.Surface, fromTargetToSource,
#          testValidOnTarget=None, testValidOnSource=None, *, targetRect: pygame.Rect = None):
#     if testValidOnSource is None:
#         fillSurface(target, colorAt_or_color=lambda __pos: source.get_at(fromTargetToSource(__pos)),
#                     testValid=testValidOnTarget, targetRect=targetRect)
#     else:
#         fillSurface(target, colorAt_or_color=
#         lambda __pos: source.get_at(fromTargetToSource(__pos)) if testValidOnSource(__pos) else target.get_at(__pos),
#                     testValid=testValidOnTarget, targetRect=targetRect)
#

def vAlignLines(items, lineSpacing: float, rect: pygame.Rect,
                alignment: Core.kernel.Alignment = Core.kernel.AlignTop | Core.kernel.AlignLeft, *,
                key_size, key_setRect):
    """
    :param items:
    :param lineSpacing:
    :param rect:
    :param alignment:
    :param key_size: (item)->size
    :param key_setRect: (item,pygame.Rect)->None
    :return:

    alignHorizontalLines aligns items in a vertical line.
    """
    __top, __left = rect.top, rect.left
    __hAlignment, __VAlignment = alignment & Core.kernel.AlignHorizontal_Mask, alignment & Core.kernel.AlignVertical_Mask
    if __hAlignment == 0:
        __hAlignment = Core.kernel.AlignLeft
    if __VAlignment == 0:
        __hAlignment = Core.kernel.AlignTop

    if __VAlignment != Core.kernel.AlignTop:
        __h = 0
        for __i in items:
            __size = key_size(__i)
            __h += __size[1]
            __h += lineSpacing
        if __VAlignment == Core.kernel.AlignHCenter:
            __top = rect.x + (rect.h - __h) / 2
        if __VAlignment == Core.kernel.AlignBottom:
            __top = rect.x + (rect.h - __h)
    __headFactor = {Core.kernel.AlignLeft: 0, Core.kernel.AlignHCenter: 0.5, Core.kernel.AlignRight: 1}[__VAlignment]
    for __i in items:
        __size = key_size(__i)
        key_setRect(__i, pygame.Rect(__left + (rect.w - __size[0]) * __headFactor, __top, __size[0], __size[1]))


def wrapText(text: str, font: pygame.font.Font, rect: pygame.Rect, lineSpacing):
    """
    wrap text and yield the wrap line in form of (text,text size)
    """
    __y, __textIndex, __textLen = 0, 0, len(text)
    while __textIndex < __textLen:
        __x, __lineHeight, __lineWidth, __lineLen = 0, 0, 0, 0
        while __textIndex + __lineLen < __textLen:
            __textSize = font.size(text[__textIndex + __lineLen])
            if (__lineWidth + __textSize[0] > rect.w) and rect.w > 0:
                break
            __lineHeight = max(__lineHeight, __textSize[1])
            __lineWidth += __textSize[0]
            __lineLen += 1
        yield text[__textIndex:__textIndex + __lineLen], (__lineWidth, __lineHeight)
        if (__y + __lineHeight > rect.h) and rect.h > 0:
            break
        __textIndex += __lineLen
        __y += (__lineHeight + lineSpacing)


def drawText(text: str, font: pygame.font.Font, rect: pygame.Rect, lineSpacing: float,
             alignment: Core.kernel.Alignment, drawline):
    """
    :param alignment:
    :param lineSpacing:
    :param text:
    :param font:
    :param rect:
    :param drawline: (str,pygame.Rect)->None
    :return:
    """
    __wrapped = wrapText(text, font, rect, lineSpacing)
    vAlignLines(__wrapped, lineSpacing, rect, alignment, key_size=lambda __x: __x[1],
                key_setRect=lambda __text_size, __rect: drawline(__text_size[0], rect))


#
# def drawText(surface: pygame.Surface, text: str, color: tuple, rect: pygame.Rect, font: pygame.font.Font,
#              aa=False, bkg=None, lineSpacing=2):
#     __y, __textIndex, __textLen = 0, 0, len(text)
#     while __textIndex < __textLen:
#
#         __x, __lineHeight, __lineWidth, __lineLen = 0, 0, 0, 0
#         while __textIndex + __lineLen < __textLen:
#             __textSize = font.size(text[__textIndex + __lineLen])
#             if (__lineWidth + __textSize[0] > rect.w) and rect.w > 0:
#                 break
#             __lineHeight = max(__lineHeight, __textSize[1])
#             __lineWidth += __textSize[0]
#             __lineLen += 1
#
#         if (__y + __lineHeight > rect.h) and rect.h > 0:
#             break
#         if bkg is None:
#             __text = font.render(text[__textIndex:__textIndex + __lineLen], aa, color)
#         else:
#             __text = font.render(text[__textIndex:__textIndex + __lineLen], aa, color, bkg)
#
#         surface.blit(__text, __text.get_rect(x=rect.x, y=__y + rect.y))
#         __textIndex += __lineLen
#         __y += __lineHeight
#         __y += lineSpacing


def drawLine(surface: pygame.Surface, line, color: tuple):
    __rect = surface.get_rect()
    if __rect.width == 0:
        return
    __rectSlope, __slope = __rect.h / __rect.w, Core.geo.line_a(line)
    if __slope > __rectSlope:
        pygame.draw.line(surface, color, Core.geo.line_pointAtY(line, __rect.top),
                         Core.geo.line_pointAtY(line, __rect.bottom))
    else:
        pygame.draw.line(surface, color, (__rect.left, Core.geo.line_produce(line, __rect.left)),
                         (__rect.right, Core.geo.line_produce(line, __rect.right)))


def drawSeg(surface: pygame.Surface, seg, color: tuple):
    pygame.draw.line(surface, color, Core.geo.seg_p1(seg), Core.geo.seg_p2(seg))


def rotoblit(surface: pygame.Surface, source: pygame.Surface, destBeforeRoto: pygame.Rect,
             angle: float, where, *, scaleToDest=True):
    if scaleToDest:
        source = pygame.transform.scale(source, destBeforeRoto.size)
    __topLeft = Core.geo.polygonBoundingRect(
        Core.geo.rotateRectAt(source.get_rect(x=destBeforeRoto.x, y=destBeforeRoto.y),
                              where, -angle, useRadian=False)).topleft
    source = pygame.transform.rotate(source, angle)
    __dest = pygame.Rect(__topLeft, source.get_size())
    surface.blit(source, __dest)


#
# def rotateAt(surface: pygame.Surface, rotation, at: tuple, *, offset: list = None,
#              newBoundingRegion: list = None) -> pygame.Surface:
#     """
#     Rotate the copy of the surface at the point and return the copy.
#     newBoundingRect is the bounding rect of the copy at the old coordination.
#     """
#     __newRect = pygame.Rect
#     rotation *= (math.pi / 180)
#
#     def getDetail():
#         newBoundingRegion.clear()
#         newBoundingRegion.extend(Core.geo.rotateRectAt(surface.get_rect(), at, rotation, useRadian=True))
#         __boundingRect = Core.geo.polygonBoundingRect(newBoundingRegion)
#         __newRect.x, __newRect.y, __newRect.h, __newRect.w = \
#             __boundingRect.x, __boundingRect.y, __boundingRect.h, __boundingRect.w
#         offset.clear()
#         offset.extend((__newRect.x, __newRect.y))
#         Core.geo.translatePolygon(newBoundingRegion, -offset[0], -offset[1])
#
#     if offset is None:
#         offset = []
#     if newBoundingRegion is None:
#         newBoundingRegion = []
#         getDetail()
#     else:
#         getDetail()
#         Core.geo.translatePolygon(newBoundingRegion, -offset[0], -offset[1])
#
#     __newSurface = pygame.Surface((__newRect.w, __newRect.h), flags=pygame.SRCALPHA)
#     __surfaceRect = surface.get_rect()
#     for __x in range(0, __newSurface.get_width()):
#         for __y in range(0, __newSurface.get_height()):
#             __rotated = Core.geo.rotatePoint((__x + offset[0], __y + offset[1]), rotation=-rotation,
#                                              at=(at[0] + offset[0], at[1] + offset[1]))
#
#             if __surfaceRect.collidepoint(__rotated):
#                 __newSurface.set_at((__x, __y),
#                                     surface.get_at((int(__rotated[0]), int(__rotated[1]))))
#             else:
#                 __newSurface.set_at((__x, __y), (0, 0, 0, 0))
#     return __newSurface
