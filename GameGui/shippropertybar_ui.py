import pygame

import core
import GameCore.kernel as game

FPS = 30
_surface: pygame.Surface = ...
_paintingArea: pygame.Rect = ...
_activated = False
_propertyBarBackgrounds: list = ...
_barsView: list = ...
_barColors: list = ...
_barColors_OnFill: list = ...
_barColors_CloseToFill: list = ...
_barColors_OnExhausted: list = ...
_barColors_CloseToExhausted: list = ...
_barChangeAnimationDuration = 0


def _drawBar(target: pygame.Surface, targetRect: pygame.Rect, source: pygame.Surface, percent: float, color):
    __sourceRect = source.get_rect()
    for __x in range(0, targetRect.w):
        for __y in range(0, int(targetRect.h * (100 - percent) / 100)):
            __sourcePos = core.mapFromRectToRect(target=__sourceRect, source=targetRect, sourcePos=(__x, __y))
            if source.get_at(__sourcePos)[3] > 0:
                target.set_at((__x, __y), (0, 0, 0, 255))
            else:
                target.set_at((__x, __y), (0, 0, 0, 0))
        for __y in range(int(targetRect.h * (100 - percent) / 100), targetRect.h):
            __sourcePos = core.mapFromRectToRect(target=__sourceRect, source=targetRect, sourcePos=(__x, __y))
            if source.get_at(__sourcePos)[3] > 0:
                target.set_at((__x, __y), color)
            else:
                target.set_at((__x, __y), (0, 0, 0, 0))
    __absOffset = target.get_abs_offset()
    pygame.display.update(pygame.Rect(targetRect.x + __absOffset[0], targetRect.y + __absOffset[1],
                                      targetRect.w, targetRect.h))


def _getBarsRealColor():
    __c = {}
    for __i in range(0, 4):
        if game.shipProperty(__i) < 10:
            __c.update({__i: _barColors_CloseToExhausted[__i]})
        elif game.shipProperty(__i) > 90:
            __c.update({__i: _barColors_OnFill[__i]})
        else:
            __c.update({__i: _barColors[__i]})
    return __c


def _dictFromList(l: list):
    __d = {}
    for __i in range(0, len(l)):
        __d.update({__i: l[__i]})
    return __d


def drawPropertyBars(barsRect: pygame.Rect, values: dict = ..., colors: dict = ...):
    __barSize = (barsRect.h, barsRect.h)
    __barSpacing = (barsRect.w - barsRect[0] * 4) / 3
    if colors is ...:
        colors = _getBarsRealColor()
    if values is ...:
        values = _dictFromList(game._shipProperties)
    for __which in values:
        __barRect = pygame.Rect(barsRect[0], barsRect[1] + __barSpacing * __which, __barSize[0], __barSize[1])
        _surface.blit(_propertyBarBackgrounds[__which], __barRect)
        core.adjustRect(__barRect, 3, 3, -3, -3)
        _drawBar(_surface, __barRect, _barsView[__which], values[__which], colors[__which])
    pygame.display.update(barsRect)


def animatePropertyBarChange(barsRect: pygame.Rect, oldValues: dict, newValues: dict):
    barValueChangeAnimationStarted()
    __frames, __changes, __barColor = FPS * _barChangeAnimationDuration, {}, {}

    for __i in oldValues.keys():
        __newValue, __oldValue = newValues[__i], oldValues[__i]
        __changes.update({__i: (__newValue - __oldValue) / __frames})
        __barColor.update({__i: _barColors_OnFill[__i] if __newValue > __oldValue else _barColors_OnExhausted \
            if __newValue < __oldValue else _barColors[__i]})
    for __i in range(0, int(__frames)):
        drawPropertyBars(barsRect, oldValues[__i] + __changes[__i] * __i, )
    barValueChangeAnimationEnded()

def setPaintingInfo(propertyBarBackgrounds: list = ..., barsView: list = ..., barColors: list = ...,
                    barColors_OnFill: list = ..., barColors_CloseToFill: list = ..., barColors_OnExhausted: list = ...,
                    barColors_CloseToExhausted: list = ...):
    global _propertyBarBackgrounds, _barsView, _barColors, _barColors_OnFill, _barColors_CloseToFill, \
        _barColors_OnExhausted, _barColors_CloseToExhausted
    if propertyBarBackgrounds:
        _propertyBarBackgrounds = propertyBarBackgrounds
    if barsView:
        _barsView = barsView
    if barColors:
        _barColors = barColors
    if barColors_OnFill:
        _barColors_OnFill = barColors_OnFill
    if barColors_CloseToFill:
        _barColors_CloseToFill = barColors_CloseToFill
    if _barColors_OnExhausted:
        _barColors_OnExhausted = barColors_OnExhausted
    if barColors_CloseToExhausted:
        _barColors_CloseToExhausted = barColors_CloseToExhausted


def testPaintingInfo():
    return _propertyBarBackgrounds and _barsView and _barColors and _barColors_OnFill and _barColors_CloseToFill \
           and _barColors_OnExhausted and _barColors_CloseToExhausted


def initialize(surface: pygame.Surface, paintingArea: pygame.Rect):
    if not testPaintingInfo():
        print(F"Some painting info is invalid plz use setPaintingInfo to update the info.")
        return
    global _surface, _paintingArea
    _surface, _paintingArea = surface, paintingArea
    drawPropertyBars(paintingArea)
    _activated = True


def cleanUp(delPaitingInfo=True):
    global _propertyBarBackgrounds, _barsView, _barColors, _barColors_OnFill, _barColors_CloseToFill, \
        _barColors_OnExhausted, _barColors_CloseToExhausted, _surface, _paintingArea
    if delPaitingInfo:
        _propertyBarBackgrounds = ...
        _barsView = ...
        _barColors = ...
        _barColors_OnFill = ...
        _barColors_CloseToFill = ...
        _barColors_OnExhausted = ...
        _barColors_CloseToExhausted = ...
    _surface = ...
    _paintingArea = ...


def receiveEvent(e):
    return e

@core.signal
def barValueChangeAnimationStarted():
    pass

@core.signal
def barValueChangeAnimationEnded():
    pass


# slots:
def _onBarValueChange(which: game.SpaceShipProperties, newValue, oldValue):
    if _activated:
        animatePropertyBarChange(_paintingArea, newValues={which: newValue}, oldValues={which: oldValue})


core.connect(game.shipPropertyChanged, _onBarValueChange)
