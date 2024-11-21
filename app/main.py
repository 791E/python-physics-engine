"""A simple physics engine written in python with pygame"""

import pygame
import body

pygame.init()
screen: pygame.Surface = pygame.display.set_mode((1280, 720), flags=pygame.RESIZABLE)
clock: pygame.time.Clock = pygame.time.Clock()
RUNNING: bool = True

ball1 = body.Ball(
    body.BodyAttributes(1, 0, 0, 10, 0, 0, 0, 1, (255, 0, 0), 1), body.BallAttributes(1)
)
ball1.print_attrs()

ball2 = body.Ball(
    body.BodyAttributes(1, 0, 0, 0, 0, 0, 0, 1, (0, 255, 0), 1),
    body.BallAttributes(r=1),
)

while RUNNING:
    # Check whether the program was quit, then terminate pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    screen.fill("red")

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
