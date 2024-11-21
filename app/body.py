"""Bodies that follow the laws of physics"""

from dataclasses import dataclass, fields
import pygame


@dataclass
class BodyAttributes:
    """
    Attributes such as coordinates and velocity for bodies

    Args:
        dt (float): For now arbitrary value, later pygame's tickrate should be used
        x (float): X coordinate of the body
        y (float): Y coordinate of the body
        vx (float): Velocity in the x direction
        vy (float): Velocity in the y direction
        ax (float): Acceleration in the x direction
        ay (float): Acceleration in the y direction
        m (float): Mass of the body
        col (tuple[int,...]): RGB or RGBA color
        bounding_box_radius (float): Half the sidelength of the smallest possible square
            that can be drawn around the body
    """

    dt: float = 1
    x: float = 0
    y: float = 0
    vx: float = 0
    vy: float = 0
    ax: float = 0
    ay: float = 0
    m: float = 1
    col: tuple[int,...] = (255, 255, 255)
    bounding_box_radius: float = 1


class Body:
    """
    A general class for different bodies. Should not be used on it's own,
    but rather be extended to different kinds of bodies.

    Methods:
        print_attrs: Print all attributes defined by BodyAttributes
        update_pos: Update the body's position using the Euler-Chromer method
    """

    def __init__(self, attr: BodyAttributes):
        """
        Should not be initialized on itself, but rather with 'super().__init__(attr)'
        from a subclass's __init__ constructor

        Args:
            attr (BodyAttributes): Attributes that can be used by any subclass of 'Body'
        """
        self.attributes = attr

    def print_attrs(self) -> None:
        """Print all attributes for debugging purposes"""
        for field in fields(self.attributes):
            value = getattr(self.attributes, field.name)
            print(f"{field.name}: {value}")

    def update_pos(self) -> None:
        """Calculate the body's new position based on position, velocity and acceleration"""
        self.attributes.x = self.attributes.vx * self.attributes.dt
        self.attributes.y = self.attributes.vy * self.attributes.dt

        self.attributes.vx = (
            self.attributes.vx + self.attributes.ax * self.attributes.dt
        )
        self.attributes.vy = (
            self.attributes.vy + self.attributes.ay * self.attributes.dt
        )


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

    def __init__(self, attr: BodyAttributes, ball_attr: BallAttributes):
        """
        Args:
            attr (BodyAttributes): Attributes that could be used for any Body
            ball_attr (BallAttributes): Ball specific attributes
        """
        super().__init__(attr)
        self.ball_attributes = ball_attr

    def print_attrs(self):
        super().print_attrs()
        for field in fields(self.ball_attributes):
            value = getattr(self.ball_attributes, field.name)
            print(f"{field.name}: {value}")

    def draw(self, screen: pygame.Surface) -> None:
        """Draw itself at it's position on the pygame screen"""
