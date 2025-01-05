"""
Using the separating axes theorem (SAT), calculate whether two bodies are colliding
(intersecting) and push them apart using the minimum translation vector (MTV) as well
as each bodies velocity, acceleration and mass. Also considers rotation for polygons.
Here is a great article about SAT: https://dyn4j.org/2010/01/sat/ 
"""

from .body import _Body
from .math_core import Vec2D

def project_body_to_vec(body: _Body, projection_vec: Vec2D) -> tuple[Vec2D, Vec2D]:
    """
    Project a 2D body onto a 1D line (technically a Vec2D).

    Args:
        body (_Body): The body that should be projected onto a vector
        projection_vec (Vec2D): the 
    """
    pass

def calc_min_translation_vec(body1: _Body, body2: _Body) -> Vec2D:
    """
    Calculate the minimum translation vector for two bodies, based on each body's 1D projection.

    Args:
        body1 (_Body): First body to check for overlap (e.g. body.Ball or body.Polygon)
        body2 (_Body): Second body to check for overlap (e.g. body.Ball or body.Polygon)

    Returns:
        Vec2D: The minimum translation vector (null vector if the bodies don't overlap)
    """

def collide(spacial_map: dict[tuple[int, int], list[_Body]]) -> None:
    """
    Calculates collisions between two bodies based on the spacial hash map.

    Args:
        spacial_map (dict[tuple[int, int], list[Body]]): The spacial hash map
            of every body in their respective cell
    """
