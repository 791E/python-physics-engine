"""Bodies that follow the laws of physics"""

from dataclasses import dataclass
import pygame
from .coordinate_system import CoordSys
from .math_core import Vec2D


@dataclass(init=False, repr=False)
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
        coord_sys: CoordSys,
        bounding_box_radius: float,
        pos_vec: tuple[float, float] = (0, 0),
        vel_vec: tuple[float, float] = (0, 0),
        accel_vec: tuple[float, float] = (0, 0),
        dt: float = 1,
        m: float = 1,
        col: tuple[int, ...] = (255, 255, 255, 255),
    ):
        self.coord_sys = coord_sys
        self.bounding_box_radius = bounding_box_radius
        self.pos = Vec2D(*pos_vec)
        self.vel = Vec2D(*vel_vec)
        self.accel = Vec2D(*accel_vec)
        self.dt = dt
        self.m = m
        self.col = col

    def __hash__(self):
        return hash(
            (
                self.coord_sys,
                self.bounding_box_radius,
                self.pos,
                self.vel,
                self.accel,
                self.dt,
                self.m,
                self.col,
            )
        )

    def __eq__(self, other):
        if isinstance(other, _Body):
            return (
                self.coord_sys == other.coord_sys
                and self.bounding_box_radius == other.bounding_box_radius
                and self.pos == other.pos
                and self.vel == other.vel
                and self.accel == other.accel
                and self.dt == other.dt
                and self.m == other.m
                and self.col == other.col
            )
        return False

    def print_attrs(self) -> None:
        """Print all attributes for debugging purposes"""
        print(f"{'\n'*3}{self}\n")
        for attr, value in self.__dict__.items():
            if isinstance(value, list):
                print(f"{attr}:")
                for item in value:
                    print(str(item))
                print()
            else:
                print(f"{attr}: {value}")

    def update_pos(self) -> None:
        """Calculate the body's new position based on position, velocity and acceleration"""
        self.pos.components = self.pos.components + self.vel.components * self.dt

        self.vel.components = self.vel.components + self.accel.components * self.dt


class Ball(_Body):
    """The simplest shape for collisions: a ball"""

    def __init__(self, coord_sys: CoordSys, r: float = 1, **kwargs):
        """
        Args:
            attr (BodyAttributes): Attributes that could be used for any Body
            ball_attr (BallAttributes): Ball specific attributes
        """
        super().__init__(coord_sys, bounding_box_radius=r, **kwargs)
        self.r = r

    def __hash__(self):
        return hash((super().__hash__(), self.r))

    def __eq__(self, other):
        if isinstance(other, Ball):
            return super().__eq__(other) and self.r == other.r
        return False

    def draw(self, screen: pygame.Surface) -> None:
        """Draw itself at it's position on the pygame screen"""
        pygame.draw.circle(
            screen,
            self.col,
            self.coord_sys.coord(*self.pos),
            self.coord_sys.distance(self.r),
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
            if not self.pos.components[0] in range(self.coord_sys.x_tot):
                self.pos.components[0] *= -1
            if not self.pos.components[1] in range(self.coord_sys.y_tot):
                self.pos.components[1] *= -1


class Polygon(_Body):
    """A more complex shape with collision and rotation"""

    def __init__(
        self,
        coord_sys: CoordSys,
        vertices: tuple[tuple[int, int], ...],
        rotational_vel: float = 0,
        rotational_accel: float = 0,
        **kwargs,
    ):
        self.vertices: list[Vec2D] = []
        for vertex in vertices:
            self.vertices.append(Vec2D(*vertex))
        self.rotational_vel = rotational_vel
        self.rotational_accel = rotational_accel

        bounding_box_radius = max(vertex.magnitude for vertex in self.vertices)
        super().__init__(coord_sys, bounding_box_radius, **kwargs)

    def __hash__(self):
        return hash(
            (
                super().__hash__(),
                self.vertices,
                self.rotational_vel,
                self.rotational_accel,
            )
        )

    def __eq__(self, other):
        if isinstance(other, Polygon):
            return (
                super().__eq__(other)
                and self.vertices == other.vertices
                and self.rotational_vel == other.rotational_vel
                and self.rotational_accel == other.rotational_accel
            )
        return False

    def draw(self, screen: pygame.Surface) -> None:
        """Draw itself at it's position on the pygame screen"""
        screen_vertices = []
        for vertex in self.vertices:
            screen_vertices.append(self.coord_sys.coord(*vertex))
        pygame.draw.polygon(screen, self.col, screen_vertices)
