import Core.signal, Core.UUID

__planets = {}
__reports = {}
__responds = {}
__effects = {}
__characters = {}
PlanetInfo = int
ReportInfo = int
RespondInfo = int
RespondEffectInfo = int
CharacterInfo = int
SpaceShipProperties = int
UserProperties = int

PlanetName = 0
"""(str)"""
PlanetLoc = 1
"""(typing.Tuple[int,int])"""
PlanetChapterIntroduction = 2
"""(str)"""
PlanetChapterBar = 4
"""(Chapter)"""
PlanetChapterLeavePlanet = 5
"""(Chapter)"""
PlanetChapterShop = 6
"""(Chapter)"""

ReportDetail = 0
"""(str)"""
ReportReporter = 1
"""(Character)"""
ReportRespondOpt1 = 2
"""(Respond)"""
ReportRespondOpt2 = 3
"""(Respond)"""
ReportIsSimple = 4

RespondDetail = 0
"""(str)"""
RespondEffect = 1
"""(Effect)"""

EffectOnSpaceShipProperties = 0
"""EffectOnSpaceShipProperties is a dict that the key is SpaceShipProperties 
and the value is change of the properties(dict)"""
Effect_EndingGame = 1
"""(bool)"""
EffectOnUserProperties_gain = 2
EffectOnUserProperties_lose = 3
"""(dict)"""
Effect_UnlockingChapter = 4
Effect_RemovingReport = 5
"""(chapter)"""
Effect_Consequent = 6

ChapterName = 0
ChapterIncludingEvent = 1
ChapterIsSpacial = 2
Chapter_FirstReport = 3
Chapter_StartIsSelectable = 4

CharacterName = 0
CharacterViewPath = 1
CharacterView = 2
CharacterStdReports = 3

Ship_PowerSupply = 0
Ship_OxyWaterSupply = 1
Ship_Officer = 2
Ship_Protection = 3

User_Prop = 0
User_Money = 1


#

def createPlanet(name: str, loc: tuple, chapterIntroduction, chapterBar, chapterLeavingPlanet, chapter):
    __uuid = Core.UUID.createUUID()
    __planets.update({__uuid: [name, loc, chapterIntroduction, None, chapterBar, chapterLeavingPlanet, chapter]})
    return __uuid


def createReport(detail: str, reporter, respondOpt1, respondOpt2, isSimple=False):
    __uuid = Core.UUID.createUUID()
    __reports.update({__uuid: [detail, reporter, respondOpt1, respondOpt2, isSimple]})
    return __uuid


def createRespond(detail, effect):
    __uuid = Core.UUID.createUUID()
    __responds.update({__uuid: [detail, effect]})
    return __uuid


def createRespondEffect():
    pass


def respondEffectInfo():
    pass


def createCharacter():
    pass


def getInfo(o, info):
    return o[info]


def setShipProperty():
    pass


def shipProperty(which):
    pass


def setUserProperty():
    pass


def userProperty():
    pass


def userPropertyEffectIsAffordable():
    pass


#
_destPlanet = ...
_currentPlanet = ...
_currentReport = ...
_currentChapter = ...
_shipProperties = [0, 0, 0, 0]


# signals

# @Core.signal.signal
def enteredPlanet(planet):
    pass


# @Core.signal.signal
def leftPlanet(planet):
    pass


# @Core.signal.signal
def destPlanetChanged(planet):
    pass


# @Core.signal.signal
def respondedReport(respond, report):
    pass


# @Core.signal.signal
def reported(report):
    pass


# @Core.signal.signal
def userPropertyChanged(which: UserProperties, newValue, oldValue):
    pass


# @Core.signal.signal
def shipPropertyChanged(which: SpaceShipProperties, newValue, oldValue):
    pass


def choseRespond():
    pass


enteredPlanet = Core.signal.signal(enteredPlanet)
leftPlanet = Core.signal.signal(leftPlanet)
destPlanetChanged = Core.signal.signal(destPlanetChanged)
respondedReport = Core.signal.signal(respondedReport)
reported = Core.signal.signal(reported)
userPropertyChanged = Core.signal.signal(userPropertyChanged)
shipPropertyChanged = Core.signal.signal(shipPropertyChanged)

Chapter_TheBegining = createCharacter()


# _destPlanet = ...
# _currentPlanet = ...
# _currentReport = ...
# _currentChapter = ...
# _principleChapter = ...
def destPlanet():
    pass


def currentPlanet():
    pass


def currentReport():
    pass


def currentChapter():
    pass


def principleChapter():
    pass


def selectingChapterStart():
    pass


def chooseRespond(which):
    pass


def setCurrentReport(e):
    pass
