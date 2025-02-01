"""Module for the creation of spacial hash maps"""

from typing import Optional
import numpy as np
from .body import _Body
from .math_core import Vec2D


class HashMap:
    """
    Easily create hash maps for efficient collision detection.
    """
    def __init__(self, grid_size: int, bodies: list[_Body]):
        """
        Args:
            grid_size (int): The sidelength of one cell of the grid
            bodies (list[Body]): The list of every body
        """
        self.grid_size = grid_size
        self.bodies = bodies

    def get_spacial_cell(
        self, pos_vec: Vec2D, bounding_box: float
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
        pos_x, pos_y = pos_vec.components

        if np.isnan(pos_x):
            pos_x = 0
        if np.isnan(pos_y):
            pos_y = 0

        cell = (int(pos_x // self.grid_size), int(pos_y // self.grid_size))
        cell_top = (int(pos_x // self.grid_size), int((pos_y + bounding_box) // self.grid_size))
        cell_top_right = (int((pos_x + bounding_box) // self.grid_size), int(
            pos_y // self.grid_size
        ))
        cell_right = (
            int((pos_x + bounding_box) // self.grid_size),
            int((pos_y + bounding_box) // self.grid_size),
        )

        # Use set() in order not to return duplicate values
        unique_cells: set[tuple[int, int]] = {
            cell,
            cell_top,
            cell_top_right,
            cell_right,
        }
        return tuple(unique_cells)

    def generate_map(
        self, bodies: Optional[list[_Body]] = None
    ) -> dict[tuple[int, int], list[_Body]]:
        """
        Generate a dictionary of cells populated with balls

        Args:
            bodies (list[Body]): (optional) The list of every body.
                If the argument is omitted, the original list of bodies will be used.

        Returns:
            dict[tuple[int, int], list[Body]]: The spacial hash map
                of every body in their respective cell
        """
        if not bodies:
            bodies = self.bodies
        spacial_map: dict = {}
        for body in bodies:
            cells = self.get_spacial_cell(
                body.pos,
                body.bounding_box_radius,
            )
            for cell in cells:
                if cell not in spacial_map:
                    spacial_map[cell] = []
                spacial_map[cell].append(body)

        return spacial_map
