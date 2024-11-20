"""Bodies that follow the laws of physics"""

from dataclasses import dataclass, fields
import pygame


@dataclass
class BodyAttributes:
    """Attributes such as coordinates and velocity for bodies"""

    x: int = 0
    y: int = 0
    vx: int = 0
    vy: int = 0
    m: int = 1
    col: tuple[int, int, int] = (255, 255, 255)
    # Half the sidelength of the smallest possible square that can be drawn around the body
    bounding_box_radius: float = 1


class Body:
    """
    A general class for different bodies. Should not be used on it's own,
    but rather be extended to different kinds of bodies.
    """

    def __init__(self, attr: BodyAttributes):
        self.attributes = attr


    def print_attrs(self) -> None:
        """Print all attributes for debugging purposes"""
        for field in fields(self.attributes):
            value = getattr(self.attributes, field.name)
            print(f"{field.name}: {value}")


@dataclass
class BallAttributes(BodyAttributes):
    """Ball-specific attributes"""

    r: int = 0


class Ball(Body):
    """The simplest shape for collisions: a ball"""

    def __init__(self, attr: BodyAttributes, ball_attr: BallAttributes):
        super().__init__(attr)
        self.ball_attributes = ball_attr


    def draw(self, screen: pygame.Surface) -> None:
        """Draw itself at it's position on the pygame screen"""
