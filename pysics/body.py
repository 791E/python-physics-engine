"""Bodies that follow the laws of physics"""

from dataclasses import dataclass, fields
import pygame
from .coordinate_system import CoordSys
from .math_core import Vec2D


@dataclass
class BodyAttributes:
    """
    Body attributes that aren't directly related to coordinates.

    Args:
        dt (float): For now arbitrary value, later pygame's tickrate should be used
        m (float): Mass of the body
        col (tuple[int,...]): RGB or RGBA color
        bounding_box_radius (float): Half the sidelength of the smallest possible square
            that can be drawn around the body
    """

    coord_sys: CoordSys
    dt: float = 1
    m: float = 1
    col: tuple[int, ...] = (255, 255, 255, 255)
    bounding_box_radius: float = 1


class _Body:
    """
    A general class for different bodies. Should not be used on it's own,
    but rather be extended to different kinds of bodies.

    Methods:
        print_attrs: Print all attributes defined by BodyAttributes
        update_pos: Update the body's position using the Euler-Chromer method
    """

    def __init__(
        self,
        pos_vec: tuple[float, float],
        vel_vec: tuple[float, float],
        accel_vec: tuple[float, float],
        attr: BodyAttributes,
    ):
        """
        Should not be initialized on itself, but rather with
        'super().__init__(x_attr, y_attr, attr)'
        from a subclass's __init__ constructor

        Args:
            x_attr (CoordinateAttributes): Attributes related to x coordinates
                (e.g. position, speed)
            y_attr (CoordinateAttributes): Attributes related to y coordinates
                (e.g. position, speed)
            attr (BodyAttributes): Non-coordinate attributes that can be used
                by any subclass of 'Body'
        """
        self.pos = Vec2D(*pos_vec)
        self.vel = Vec2D(*vel_vec)
        self.accel = Vec2D(*accel_vec)
        self.attributes = attr

    def print_attrs(self) -> None:
        """Print all attributes for debugging purposes"""
        print("\nGeneral attributes:")
        for field in fields(self.attributes):
            value = getattr(self.attributes, field.name)
            print(f"{field.name}: {value}")

        print("\nCoordinate related attributes")


    def update_pos(self) -> None:
        """Calculate the body's new position based on position, velocity and acceleration"""
        self.pos = self.pos + self.vel * self.attributes.dt

        self.vel = self.vel.components + self.accel.components * self.attributes.dt


@dataclass
class BallAttributes:
    """
    Ball-specific attributes

    Args:
        r (float): Radius of the ball
    """

    r: float = 0


class Ball(_Body):
    """The simplest shape for collisions: a ball"""

    def __init__(
        self,
        pos_vec: tuple[float, float],
        vel_vec: tuple[float, float],
        accel_vec: tuple[float, float],
        attr: BodyAttributes,
        ball_attr: BallAttributes,
    ):
        """
        Args:
            attr (BodyAttributes): Attributes that could be used for any Body
            ball_attr (BallAttributes): Ball specific attributes
        """
        super().__init__(pos_vec, vel_vec, accel_vec, attr)
        self.ball_attributes = ball_attr

    def print_attrs(self):
        super().print_attrs()
        print("\nBall specific attributes:")
        for field in fields(self.ball_attributes):
            value = getattr(self.ball_attributes, field.name)
            print(f"{field.name}: {value}")

    def draw(self, screen: pygame.Surface) -> None:
        """Draw itself at it's position on the pygame screen"""
        pygame.draw.circle(
            screen,
            self.attributes.col,
            self.attributes.coord_sys.coord(*self.pos),
            self.attributes.coord_sys.distance(self.ball_attributes.r),
        )

    def update_pos(self, wall_collision: bool = True) -> None:
        """
        Update position and check for collisions with the walls.

        Args:
            wall_collision (bool): Whether collision with the walls should
            be performed or not.
        """
        super().update_pos()

        if wall_collision:
            if not self.pos.components[0] in range(self.attributes.coord_sys.x_tot):
                self.pos.components[0] *= -1
            if not self.pos.components[1] in range(self.attributes.coord_sys.y_tot):
                self.pos.components[1] *= -1


class Polygon(_Body):
    """A more complex shape with collision and rotation"""

    def __init__(
        self,
        pos_vec: tuple[float, float],
        vel_vec: tuple[float, float],
        accel_vec: tuple[float, float],
        attr: BodyAttributes,
        vertices: tuple[tuple[int, int], ...],
    ):
        super().__init__(pos_vec, vel_vec, accel_vec, attr)
        self.vertices: list[Vec2D]
        for vertex in vertices:
            self.vertices.append(Vec2D(*vertex))

    def print_attrs(self):
        super().print_attrs()
        print("\nPolygon specific attributes")
        print("Vertices:")
        for i in len(self.vertices):
            print(f"Vertex at index {i}: {self.vertices[i]}")

    def draw(self, screen: pygame.Surface) -> None:
        """Draw itself at it's position on the pygame screen"""
        screen_vertices = []
        for vertex in self.vertices:
            screen_vertices.append(
                self.attributes.coord_sys.coord(*vertex)
            )
        pygame.draw.polygon(screen, self.attributes.col, screen_vertices)
