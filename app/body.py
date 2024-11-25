"""Bodies that follow the laws of physics"""

from dataclasses import dataclass, fields
import pygame


@dataclass
class CoordinateAttributes:
    """
    Attributes such as coordinates and velocity for bodies

    Args:
        pos (float): Position of the body
        vel (float): Velocity of the body
        accel (float): Acceleration of the body
    """

    pos: float = 0
    vel: float = 0
    accel: float = 0


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

    dt: float = 1
    m: float = 1
    col: tuple[int, ...] = (255, 255, 255, 255)
    bounding_box_radius: float = 1


class Body:
    """
    A general class for different bodies. Should not be used on it's own,
    but rather be extended to different kinds of bodies.

    Methods:
        print_attrs: Print all attributes defined by BodyAttributes
        update_pos: Update the body's position using the Euler-Chromer method
    """

    def __init__(
        self,
        x_attr: CoordinateAttributes,
        y_attr: CoordinateAttributes,
        attr: BodyAttributes,
    ):
        """
        Should not be initialized on itself, but rather with 'super().__init__(attr)'
        from a subclass's __init__ constructor

        Args:
            x_attr (CoordinateAttributes): Attributes related to x coordinates
                (e.g. position, speed)
            y_attr (CoordinateAttributes): Attributes related to y coordinates
                (e.g. position, speed)
            attr (BodyAttributes): Non-coordinate attributes that can be used
                by any subclass of 'Body'
        """
        self.x = x_attr
        self.y = y_attr
        self.attributes = attr

    def print_attrs(self) -> None:
        """Print all attributes for debugging purposes"""
        print("\nGeneral attributes:")
        for field in fields(self.attributes):
            value = getattr(self.attributes, field.name)
            print(f"{field.name}: {value}")

        print("\nx coordinate attributes:")
        for field in fields(self.x):
            value = getattr(self.x, field.name)
            print(f"{field.name}: {value}")

        print("\ny coordinate attributes:")
        for field in fields(self.y):
            value = getattr(self.y, field.name)
            print(f"{field.name}: {value}")

    def update_pos(self) -> None:
        """Calculate the body's new position based on position, velocity and acceleration"""
        self.x.pos = self.x.vel * self.attributes.dt
        self.y.pos = self.y.vel * self.attributes.dt

        self.x.vel = self.x.vel + self.x.accel * self.attributes.dt
        self.y.vel = self.y.vel + self.y.accel * self.attributes.dt


@dataclass
class BallAttributes:
    """
    Ball-specific attributes

    Args:
        r (float): Radius of the ball
    """

    r: float = 0


class Ball(Body):
    """The simplest shape for collisions: a ball"""

    def __init__(
        self,
        x_attr: CoordinateAttributes,
        y_attr: CoordinateAttributes,
        attr: BodyAttributes,
        ball_attr: BallAttributes,
    ):
        """
        Args:
            attr (BodyAttributes): Attributes that could be used for any Body
            ball_attr (BallAttributes): Ball specific attributes
        """
        super().__init__(x_attr, y_attr, attr)
        self.ball_attributes = ball_attr

    def print_attrs(self):
        super().print_attrs()
        print("\nBall specific attributes:")
        for field in fields(self.ball_attributes):
            value = getattr(self.ball_attributes, field.name)
            print(f"{field.name}: {value}")

    def draw(self, screen: pygame.Surface) -> None:
        """Draw itself at it's position on the pygame screen"""
