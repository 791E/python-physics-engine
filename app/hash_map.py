"""Module for the creation of spacial hash maps"""

from body import _Body


def get_spacial_cell(
    pos_x: float, pos_y: float, bounding_box: float, grid_size: int
) -> tuple[tuple[int, int], ...]:
    """
    Calculates which cells a body should belong to based on the smallest
    possible square bounding box. Calculates all possible cells where the center,
    the right, the top or the top-right part of the body is.

    Args:
        pos_x (float): x position of the body
        pos_y (float): y position of the body
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
    bodies: list[_Body], grid_size: int
) -> dict[tuple[int, int], list[_Body]]:
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
            i.x.pos,
            i.y.pos,
            i.attributes.bounding_box_radius,
            grid_size,
        )
        for cell in cells:
            if cell not in spacial_map:
                spacial_map[cell] = []
            spacial_map[cell].append(i)

    return spacial_map
