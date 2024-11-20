"""Calculate collisions for all collision-enabled objects using a spacial hash map"""

import math
from body import Body


def get_spacial_cell(
    pos_x: int, pos_y: int, bounding_box: float, grid_size: int
) -> tuple[tuple[int, int], ...]:
    """
    Calculates which cells a body should belong to based on the smallest
    possible square bounding box. Calculates all possible cells where the center,
    the right, the top or the top-right part of the body is.

    Args:
        pos_x (int): x position of the body
        pos_y (int): y position of the body
        bounding_box (float): Half of a bodies smallest possible
            encapsulating square's sidelength (Body.bounding_box_radius should be used)
        grid_size (int): sidelength of one cell of the grid

    Returns:
        tuple[tuple[int, int],...]: A tuple of tuples of x and y coordinates of the cell
    """

    cell = int(pos_x // grid_size), int(pos_y // grid_size)
    cell_top = int(pos_x // grid_size), int((pos_y + bounding_box) // grid_size)
    cell_top_right = int((pos_x + bounding_box) // grid_size), int(pos_y // grid_size)
    cell_right = (
        int((pos_x + bounding_box) // grid_size),
        int((pos_y + bounding_box) // grid_size),
    )

    # Use set() in order not to return duplicate values
    unique_cells: set[tuple[int, int]] = {cell, cell_top, cell_top_right, cell_right}
    return tuple(unique_cells)


def generate_map(
    bodies: list[Body], grid_size: int
) -> dict[tuple[int, int], list[Body]]:
    """
    Generate a dictionary of cells populated with balls

    Args:
        bodies (list[Body]): The list of every body
        grid_size (int): The sidelength of one cell in the grid

    Returns:
        dict[tuple[int, int], list[Body]]: The spacial hash map
            of every body in their respective cell
    """
    spacial_map: dict = {}
    for i in bodies:
        cells = get_spacial_cell(
            i.attributes.x,
            i.attributes.y,
            i.attributes.bounding_box_radius,
            grid_size,
        )
        for cell in cells:
            if cell not in spacial_map:
                spacial_map[cell] = []
            spacial_map[cell].append(i)

    return spacial_map


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
