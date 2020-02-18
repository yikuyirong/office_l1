import pygame
from sys import exit
from random import randint


def main():
    screen_size = (1366, 768)

    pygame.init()

    screen = pygame.display.set_mode(screen_size, 0, 32)

    font = pygame.font.SysFont("consolas", 16)

    font_height = font.get_linesize()

    events = list()

    while True:
        event = pygame.event.wait()

        events.append(event)

        events = events[-int(screen_size[1] / font_height):]

        if event.type == pygame.QUIT:
            exit()

        screen.fill((255,255,255))

        for (index, event) in enumerate(events):
            screen.blit(font.render(str(event), True, (randint(0, 255), randint(0, 255), randint(0, 255))),
                        (0, index * font_height))

        pygame.display.update()


if __name__ == '__main__':
    main()
