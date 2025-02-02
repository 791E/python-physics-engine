"""
This is only a temporary solution for ball - ball collisions. This is not
the final product and will be deleted as soon as I get general collision to work.

IMPORTANT: The list of bodies may only include balls. If it contains any other bodies,
the program will crash. This is intentional, as other collisions are not yet implemented.
"""

import numpy as np
from .hash_map import HashMap
from .math_core import Vec2D
from .body import _Body, Ball


class BallCollider:
    """
    Simple, fully elastic ball-to-ball collision

    Args:
        balls_hasher (HashMap): The HashMap instance which calculates the hash cells for
            all the balls. That HashMap instance may only include Balls in it's bodies attribute.
    """

    def __init__(self, balls_hasher: HashMap):
        self.hasher = balls_hasher

    def calculate_resulting_velocity(
        self, colliding_ball: Ball, secondary_ball: Ball
    ) -> tuple[Vec2D, Vec2D]:
        """
        Return the resulting velocity of colliding_ball after
        colliding with secondary_ball as a Vec2D

        Args:
            colliding_ball (Ball): The ball of which we want to get the new velocity
            secondary_ball (Ball): The secondary ball, with which the first ball is colliding

        Returns:
            Vec2D: The new velocity vector for colliding_ball
        """
        dx: float = secondary_ball.pos.components[0] - colliding_ball.pos.components[0]
        dy: float = secondary_ball.pos.components[1] - colliding_ball.pos.components[1]
        distance: float = np.sqrt(dx**2 + dy**2)

        if distance <= colliding_ball.r + secondary_ball.r:  # Collision detected

            normal: Vec2D = Vec2D(dx / distance, dy / distance)

            # Velocity components along normal
            velocity1_normal: float = np.dot(
                colliding_ball.vel.components, normal.components
            )
            velocity2_normal: float = np.dot(
                secondary_ball.vel.components, normal.components
            )

            # Fully elastic collision
            velocity1_normal_after: float = (
                velocity1_normal * (colliding_ball.m - secondary_ball.m)
                + 2 * secondary_ball.m * velocity2_normal
            ) / (colliding_ball.m + secondary_ball.m)
            velocity2_normal_after: float = (
                velocity2_normal * (secondary_ball.m - colliding_ball.m)
                + 2 * colliding_ball.m * velocity1_normal
            ) / (colliding_ball.m + secondary_ball.m)

            velocity1_normal_vector: np.ndarray = normal.components * (
                velocity1_normal_after - velocity1_normal
            )
            velocity2_normal_vector: np.ndarray = normal.components * (
                velocity2_normal_after - velocity2_normal
            )

            new_colliding_ball_velocity: np.ndarray = (
                colliding_ball.vel.components + velocity1_normal_vector
            )
            new_secondary_ball_velocity: np.ndarray = (
                secondary_ball.vel.components + velocity2_normal_vector
            )

            # Separate balls to prevent overlap
            overlap: float = (colliding_ball.r + secondary_ball.r - distance) / 2
            colliding_ball.pos.components[0] -= overlap * normal.components[0]
            colliding_ball.pos.components[1] -= overlap * normal.components[1]
            secondary_ball.pos.components[0] += overlap * normal.components[0]
            secondary_ball.pos.components[1] += overlap * normal.components[1]

            return Vec2D(*new_colliding_ball_velocity), Vec2D(
                *new_secondary_ball_velocity
            )

        return colliding_ball.vel, secondary_ball.vel

    def collide(self):
        """
        Use the above functions to calculate the resulting velocity vector of the balls
        after the collision.
        """
        hash_map: dict[tuple[int, int], list[_Body]] = self.hasher.generate_map()

        # Collision response. Key of the dict is the ball and the value is
        # it's new velocity vector
        # This is necessary because if I try to change the velocity of the balls
        # before calculating all the new velocities, some of the velocities will be incorrect
        collision_response: dict[Ball, Vec2D] = {}

        if not all(
            isinstance(body, Ball) for cells in hash_map.values() for body in cells
        ):
            raise TypeError("All bodies must be pysics.body.Ball objects")

        # Calculate the new velocity vectors and add them to the collision_response dict
        for cell in hash_map.values():
            balls: list[Ball] = [body for body in cell if isinstance(body, Ball)]
            for i, ball1 in enumerate(balls):
                for ball2 in balls[i + 1 :]:
                    new_vel1, new_vel2 = self.calculate_resulting_velocity(ball1, ball2)
                    collision_response[ball1] = new_vel1
                    collision_response[ball2] = new_vel2

        # Perform the collision responses, by iterating over the collision_response dict
        for ball, res_vel in collision_response.items():
            ball.vel = res_vel
