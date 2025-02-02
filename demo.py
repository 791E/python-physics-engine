"""
This file shows off the possibilities of the pysics module. It does not
define any bodies, but rather shows how to set up a basic simulation with
the pysics module.
"""

import pygame
from pysics import _Body, Ball, CoordSys, HashMap, BallCollider

# Import necessary modules

# Initialize pygame
pygame.init()

# Set up the display
screen: pygame.Surface = pygame.display.set_mode((1280, 720), flags=pygame.RESIZABLE)
clock: pygame.time.Clock = pygame.time.Clock()
RUNNING: bool = True

FRAME_RATE: int = 60

# Initialize pysics

# Coordinate system needs to be initialized before bodies are defined
coord_system: CoordSys = CoordSys(screen)

# Define bodies
# Either, define them in the list directly, or append them later
balls: list[_Body] = []

# The hasher (and therefore the collider) need to be initialized after
# the list of bodies is defined
hasher: HashMap = HashMap(50, balls)
# Since we are using a BallCollider object here, we must ensure that
# all bodies in the list passed into the hasher are Ball objects
ball_collider: BallCollider = BallCollider(hasher)

# Main loop
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    # Set a background
    screen.fill("white")
    # Paint the borders of the coordinate system
    coord_system.paint_borders()

    # Check for collisions
    ball_collider.collide()

    for ball in balls:
        # All bodies are Ball objects for sure, this check is simply performed in order for
        # pylint and Mypy not to scream at me
        if isinstance(ball, Ball):
            # Update the position of the ball
            ball.update_pos()
            # Draw the ball on the screen
            ball.draw(screen)

            # Any per-ball calculations and drawing can be done here

    # Perform any additional calculations or drawing here

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FRAME_RATE)

# Quit pygame
pygame.quit()
