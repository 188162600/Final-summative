import pygame
import pygame.locals
import GameCore.kernel as game
import gui
import core

ReportPaintingInfo = int
ReportFont = 0
ReportForeground = 1
ReportBackground = 2
ReportRespondFont = 3
ReportRespondForeground = 4
ReportRespondBackground = 5

_surface: pygame.Surface = ...
_paintingArea: pygame.Rect = ...
_paintingInfo: tuple = ...
_inclination: float = 0
_activated = False
_reportSelectRect = {}
_onSelect = False


def setActivated(a=True):
    global _activated
    _activated = a


def drawReportSelect(rect: pygame.Rect, reports: list):
    pass


def drawReportTextLine(text: str, rect: pygame.Rect):
    pass


def drawReportRespondTextLine(text: str, rect: pygame.Rect):
    pass


def drawReportRespond(mainContent: pygame.Surface, mainContentTopLeft, mainContentTopRight,
                      mainContentBottomRight, mainContentBottomLeft):
    if _inclination > 0:
        __textTopRight = mainContentTopRight
        __textTop = core.lineFromPointAngle(__textTopRight, angle=0, fromRadius=False)
        __textTopLeft = core.seg_intersection(core.makeSegment(mainContentTopLeft, mainContentBottomLeft),
                                              __textTop)
        __textHeight = mainContentTopLeft[1] - __textTopLeft[1]
        __text = (game.getInfo(game.currentReport(), game.ReportRespondOpt1), game.RespondDetail)
        __textAlignment = core.AlignLeft
    elif _inclination < 0:
        __textTopLeft = mainContentTopLeft
        __textTop = core.lineFromPointAngle(mainContentTopLeft, angle=0, fromRadius=False)
        __textTopRight = core.seg_intersection(core.makeSegment(mainContentTopRight, mainContentBottomRight),
                                               __textTop)
        __textHeight = mainContentTopLeft[1] - __textTopLeft[1]
        __text = game.getInfo(game.getInfo(game.currentReport(),
                                           game.ReportRespondOpt2), game.RespondDetail)
        __textAlignment = core.AlignRight
    else:
        return

    gui.fillSurface(mainContent, getPaintingInfo(ReportBackground),
                    targetRect=mainContent.get_rect(h=__textHeight * 2),
                    testValid=lambda __pos: mainContent.get_at(__pos)[3] > 0)
    gui.drawText(__text, getPaintingInfo(ReportFont),
                 pygame.Rect(__textTopLeft, (__textTopRight[0] - __textTopLeft[0], __textHeight)), 2,
                 __textAlignment, drawline=drawReportRespondTextLine)


def drawReportMainContent(rect: pygame.Rect, drawRespond):
    __newRect = core.rotateRectAt(rect, (rect.x + rect.w / 2, rect.bottom + rect.h), _inclination)
    __content = game.getInfo(game.getInfo(
        game.currentReport(), game.ReportReporter), game.CharacterView)
    __content = pygame.transform.scale(__content, rect.size)
    __content = pygame.transform.rotate(__content, _inclination)

    if game.getInfo(game.currentReport(), game.ReportIsSimple):
        __rect = core.rectAdjusted(rect, 12, 12, -12, -12)
        gui.drawText(game.ReportDetail, getPaintingInfo(ReportFont), __rect, 2,
                     core.AlignVCenter,drawline= drawReportTextLine)
    elif drawRespond:
        drawReportRespond(__content, __newRect[0], __newRect[1], __newRect[2], __newRect[3])
    _surface.blit(__content, pygame.Rect(core.polygonBoundingRect(__newRect).topleft, rect.size))


def drawReport(drawRespond=True):
    __mainContentPaintingArea = pygame.Rect(_paintingArea.x, _paintingArea.y + _paintingArea.h * 2 // 8
                                            , _paintingArea.w, _paintingArea.h * 7 // 8)
    __reporterNamePaintingArea = pygame.Rect(_paintingArea.x, _paintingArea.y + _paintingArea.h * 7 // 8
                                             , _paintingArea.w, _paintingArea.h * 1 // 8)
    __detailPaintingArea = pygame.Rect(_paintingArea.x, _paintingArea.y, _paintingArea.w, _paintingArea.h * 2 // 8)
    __detail = game.getInfo(game.currentReport(), game.ReportDetail)
    if game.selectingChapterStart():
        __reports = game.getInfo(game.currentChapter(), game.ChapterIncludingEvent)
        drawReportSelect(__mainContentPaintingArea, __reports)
    else:
        drawReportMainContent(__mainContentPaintingArea, drawRespond)

    if not game.getInfo(game.currentReport(), game.ReportIsSimple):
        gui.drawText(__detail, getPaintingInfo(ReportFont), __detailPaintingArea,
                     2, core.AlignCenter, drawline=drawReportTextLine)
        __characterName = game.getInfo(game.getInfo(game.currentReport(), game.ReportReporter), game.ChapterName)
        __name = getPaintingInfo(ReportFont).render(__characterName, True, getPaintingInfo(ReportForeground))
        _surface.blit(__name, __name.get_rect(center=__reporterNamePaintingArea.center))


def setPaintingInfo(font, foreground, background, respondFont, respondForeground, respondBackground):
    global _paintingInfo
    _paintingInfo = (font, foreground, background, respondFont, respondForeground, respondBackground)
    drawReport()


def getPaintingInfo(which: ReportPaintingInfo):
    return _paintingInfo[which]


def initialize(surface: pygame.Surface, paintingArea: pygame.Rect, report):
    if not _paintingInfo:
        print("paintingArea is", _paintingInfo, "update it.")
    global _surface, _paintingArea
    _surface = surface
    _paintingArea = paintingArea
    game.reported(report)
    drawReport()


def _reportSelect_receiveEvent(e):
    if e.type == pygame.MOUSEBUTTONUP:
        if e.button == pygame.locals.BUTTON_RIGHT:
            for __rect in _reportSelectRect:
                __rect: pygame.Rect = __rect
                if __rect.collidepoint(e.pos):
                    game.setCurrentReport(_reportSelectRect[__rect])


def _report_recieveEvent(e):
    global _inclination
    if e.type == pygame.MOUSEMOTION:
        __x, __y = e.pos[0] - _surface.get_abs_offset()[0] - _paintingArea.x, e.pos[1] - _surface.get_abs_offset()[
            1] - _paintingArea.y
        _inclination = core.seg_angle(core.makeSegment(_paintingArea.midbottom, e.p), returnRadian=False)
        drawReport(drawRespond=abs(_inclination) > 5)
    elif e.type == pygame.MOUSEBUTTONUP:
        if e.button == pygame.locals.BUTTON_RIGHT:
            __timer = pygame.time.Clock()
            if _inclination >= 15:
                for __i in range(0, 40):
                    _inclination += 1
                    __timer.tick(1)
                game.chooseRespond(
                    game.ReportInfo(game.currentReport(), game.ReportRespondOpt1))

            elif _inclination <= 15:
                for __i in range(0, 40):
                    _inclination += 1
                    __timer.tick(1)
                    game.chooseRespond(
                        game.ReportInfo(game.currentReport(), game.ReportRespondOpt2))


def receiveEvent(e):
    if game.selectingChapterStart():
        _reportSelect_receiveEvent(e)
    else:
        _report_recieveEvent(e)


def _gameCurrentReportChanged(report):
    if _activated:
        drawReport()


def _gameCurrentChapterChanged(chapter):
    if _activated and game.getInfo(chapter, game.Chapter_StartIsSelectable):
        drawReport()
