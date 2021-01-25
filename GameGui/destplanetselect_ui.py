import pygame
import random
import core
import gui


def factorDrawStar(surface):
    # f = pygame.font.Font(pygame.font.get_default_font(), 10)
    __starRoto = random.randint(0, 90)

    def __drawEllipse(rect, color):
        pygame.draw.ellipse(s, color, rect)

    def __drawStar(rect: pygame.Rect, color):
        pygame.draw.polygon(surface, color,
                            core.makeStar(rect.center, 4, rect.w * 0.33 * 2 ** 0.5, rect.w, __starRoto))
        # star=core.makeStar(rect.center, 4, rect.w*2**0.5 , rect.w ,rotation=20)
        # for __i in range(0,len(star)):
        #     __text=f.render(str(__i),True,(100,100,100))
        #     surface.blit(__text,(star[__i],__text.get_size()))

    __options = (__drawEllipse, __drawStar)
    __weights = (15, 1)

    def __draw(rect: pygame.Rect, color):
        random.choices(__options, __weights)[0](rect, color)

    return __draw


def drawStars(rect: pygame.Rect, n: int, colorsSeq=((57, 50, 94), (49, 64, 87), (77, 87, 110)),
              sizesSeq=((4, 4), (6, 6), (8, 8)), *, drawStar):
    """
    :param n:
    :param rect:
    :param colorsSeq:
    :param sizesSeq:
    :param drawStar: (rect,color)->None
    :return:
    """
    for __i in range(0, n):
        drawStar(pygame.Rect(
            (random.randint(rect.left, rect.right), random.randint(rect.left, rect.right)), random.choice(sizesSeq)),
            random.choice(colorsSeq))


pygame.init()
s = pygame.display.set_mode((1000, 1000), pygame.SCALED)
drawStars(s.get_rect(), 300, drawStar=factorDrawStar(s))
pygame.display.update()
pygame.time.wait(100000)
