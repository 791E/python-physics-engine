"""Calculate collisions for all collision-enabled objects using a spacial hash map"""

import math
from body import Body


def ball_ball_collisions(
    spacial_map: dict[tuple[int, int], list[Body]], radius: int
) -> None:
    """
    Calculates collisions between two bodies based on the spacial hash map.
    IMPORTANT: For now this only works, if all the bodies are Ball objects.
    TODO: Change to / replace with something that can calculate elastic collisions
    for polygons (all Body objects).

    Args:
        spacial_map (dict[tuple[int, int], list[Body]]): The spacial hash map
            of every body in their respective cell
        radius (int): Radius of the colliding balls. Use (Ball.ball_attributes.r)

    Returns:
        None
    """
    for cell_balls in spacial_map.values():
        for i, ball1 in enumerate(cell_balls):
            for _, ball2 in enumerate(cell_balls[i + 1 :]):
                # Check distance between the two balls
                dx = ball1.attributes.x - ball2.attributes.x
                dy = ball1.attributes.y - ball2.attributes.y
                # TODO: don't use math (use numpy)
                distance = math.sqrt(dx**2 + dy**2)
                if distance < 2 * radius:
                    # Simple collision response: swap velocities
                    ball1.attributes.vx, ball2.attributes.vx = (
                        ball2.attributes.vx,
                        ball1.attributes.vx,
                    )
                    ball1.attributes.vy, ball2.attributes.vy = (
                        ball2.attributes.vy,
                        ball1.attributes.vy,
                    )
