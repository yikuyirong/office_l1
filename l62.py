import pygame
from sys import exit


def main():
    img_background_filename = r"assets\background.jpg"
    img_fish_filename = r"assets\fish.png"

    pygame.init()

    screen = pygame.display.set_mode((1366, 768), 0, 32)

    pygame.display.set_caption("Sea world")

    backgroud = pygame.image.load(img_background_filename)
    fish = pygame.image.load(img_fish_filename)

    x = 0
    y = 0

    pos = (0, 0)

    def move(key, pos):
        if event.key == pygame.K_DOWN:
            return pos[0], pos[1] + 10
        elif event.key == pygame.K_UP:
            return pos[0], pos[1] - 10
        elif event.key == pygame.K_LEFT:
            return pos[0] - 10, pos[1]
        elif event.key == pygame.K_RIGHT:
            return pos[0] + 10, pos[1]

    while True:

        screen.blit(backgroud, (0, 0))

        screen.blit(fish, (x, y))

        event = pygame.event.wait()

        while event:

            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                event = pygame.event.poll()

        # for event in pygame.event.wait():
        #     if event.type == pygame.QUIT:
        #         exit()
        #     elif event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_DOWN:
        #             y = y + 10
        #         elif event.key == pygame.K_UP:
        #             y = y - 10
        #         elif event.key == pygame.K_LEFT:
        #             x = x - 10
        #         elif event.key == pygame.K_RIGHT:
        #             x = x + 10
        #
        # print(x, y)

        # (x, y) = pygame.mouse.get_pos()
        #
        # x = x - fish.get_width() / 2
        # y = y - fish.get_height() / 2
        #
        # screen.blit(fish, (x, y))

        pygame.display.update()


if __name__ == '__main__':
    main()
