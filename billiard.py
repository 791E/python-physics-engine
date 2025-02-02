import pygame
from pysics import _Body, Ball, CoordSys, HashMap, BallCollider
import math

# initialise pygame
pygame.init()
screen: pygame.Surface = pygame.display.set_mode((1280, 720), flags=pygame.RESIZABLE)
clock: pygame.time.Clock = pygame.time.Clock()
RUNNING: bool = True

FRAME_RATE: int = 120

# initialize pysics

# coordinate system needs to be initialised before bodies are defined
coord_system: CoordSys = CoordSys(screen)

# define balls
balls: list[_Body] = []

# Calculate positions for a triangular billiard setup
rows: int = 3
ball_radius: float = 10
spacing: float = 1.5
start_x: float = 800
start_y: float = screen.get_height() // 2

for row in range(rows):
    for col in range(row + 1):
        y: float = start_y + (col - row / 2) * 2 * ball_radius * spacing
        x: float = start_x + row * math.sqrt(3) * ball_radius * spacing
        balls.append(
            Ball(
                coord_system,
                r=ball_radius,
                dt=FRAME_RATE,
                pos_vec=(x, y),
                vel_vec=(0, 0),
                col=(0, 255, 0),
                m=1,
            )
        )

balls.append(
    Ball(
        coord_system,
        r=ball_radius,
        dt=FRAME_RATE,
        pos_vec=(100, 360),
        vel_vec=(10, 0),
        col=(255, 0, 0),
        m=1,
    )
)

# the hasher (and therefore the collider) need to be initialised after
# the list of bodies is defined
hasher: HashMap = HashMap(50, balls)
# since we are using a BallCollider object here, we must ensure, that
# all bodies in the list passed into the hasher are Ball objects
ball_collider: BallCollider = BallCollider(hasher)

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    screen.fill("white")
    coord_system.paint_borders()

    # Check for collisions
    ball_collider.collide()

    for ball in balls:
        if isinstance(ball, Ball):
            ball.update_pos()
            ball.draw(screen)

            # draw the velocity vector to visualize the movement of the balls
            pygame.draw.line(
                screen,
                (0, 0, 0),
                coord_system.coord(ball.pos.components[0], ball.pos.components[1]),
                coord_system.coord(
                    ball.pos.components[0] + ball.vel.components[0],
                    ball.pos.components[1] + ball.vel.components[1],
                ),
            )
            pygame.draw.circle(
                screen,
                (0, 0, 0),
                coord_system.coord(
                    ball.pos.components[0] + ball.vel.components[0],
                    ball.pos.components[1] + ball.vel.components[1],
                ),
                1,
            )

    pygame.display.flip()

    clock.tick(FRAME_RATE)

pygame.quit()