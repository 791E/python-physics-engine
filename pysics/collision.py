"""
Using the separating axes theorem (SAT), calculate whether two bodies are colliding
(intersecting) and push them apart using the minimum translation vector (MTV) as well
as each bodies velocity, acceleration and mass. Also considers rotation for polygons.
Here is a great article about SAT: https://dyn4j.org/2010/01/sat/ 
"""

import numpy as np
from .body import _Body, Ball, Polygon
from .math_core import Vec2D


def project_body_to_line(body: _Body, projection_vec: Vec2D) -> tuple[float, float, float]:
    """
    Project a 2D body onto a 1D line (technically a Vec2D).

    Args:
        body (_Body): The body that should be projected onto a vector
        projection_vec (Vec2D): the line the body should be projected onto

    Returns:
        tuple[float, float, float]: Projection on the line as:
            line_angle, min_point_proj, max_point_proj
    """
    min_point_proj: float
    max_point_proj: float
    if isinstance(body, Polygon):
        min_point_proj = np.dot(projection_vec.components, body.vertices[0].components)
        max_point_proj = min_point_proj
        for i in range(len(body.vertices) - 1):
            point_proj: float = np.dot(projection_vec.components, body.vertices[i + 1].components)
            if point_proj > max_point_proj:
                max_point_proj = point_proj
            elif point_proj < max_point_proj:
                min_point_proj = point_proj

    elif isinstance(body, Ball):
        center_point_proj: float = np.dot(projection_vec.components, body.pos.components)
        min_point_proj = center_point_proj - body.r
        max_point_proj = center_point_proj + body.r

    line_angle: float = Vec2D(1, 0).angle(projection_vec)
    return (line_angle, min_point_proj, max_point_proj)



def calc_min_translation_vec(body1: _Body, body2: _Body) -> Vec2D:
    """
    Calculate the minimum translation vector for two bodies, based on each body's 1D projection.

    Args:
        body1 (_Body): First body to check for overlap (e.g. body.Ball or body.Polygon)
        body2 (_Body): Second body to check for overlap (e.g. body.Ball or body.Polygon)

    Returns:
        Vec2D: The minimum translation vector (null vector if the bodies don't overlap)
    """
    projections: list[tuple[float, float, float]] = []
    if isinstance(body1, Ball):
        projections.append(
            project_body_to_line(
                body1, (Vec2D(*(body2.pos.components - body1.pos.components)))
            )
        )
    elif isinstance(body1, Polygon):
        for vertex in body1.vertices:
            projection_vec: Vec2D
            projections.append(
                project_body_to_line(
                    body1, projection_vec
                )
        )

    return Vec2D(0, 0)


def collide(spacial_map: dict[tuple[int, int], list[_Body]]) -> None:
    """
    Calculates collisions between two bodies based on the spacial hash map.

    Args:
        spacial_map (dict[tuple[int, int], list[Body]]): The spacial hash map
            of every body in their respective cell
    """
    for cell in spacial_map.values():
        for i, body1 in enumerate(cell):
            for body2 in cell[i + 1 :]:
                translation_vec: Vec2D = calc_min_translation_vec(body1, body2)
                # TODO actual collision, based on velocities of the two bodies and the MTV
