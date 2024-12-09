"""
A dynamic coordinate system for defining positions more easily.
Credits to @DanceMonkey276 on GitHub, <https://github.com/DanceMonkey276/>
"""

import pygame


class CoordSys:
    """Apply a 1000x1500 coordinate system to a pygame screen"""

    def __init__(self, display: pygame.Surface) -> None:
        self.display: pygame.Surface = display
        self.x_tot: int = 1500
        self.y_tot: int = 1000

    def __repr__(self) -> str:
        return f"< Coordinate System ([0, {self.x_tot}], [0, {self.y_tot}]) >"

    def _update_dimensions(self) -> tuple[float, float, float, float, float]:
        scale: float
        if (
            self.display.get_width() / self.x_tot
            > self.display.get_height() / self.y_tot
        ):
            scale = self.display.get_height() / self.y_tot
        else:
            scale = self.display.get_width() / self.x_tot

        return (
            scale,  # scale_factor
            self.display.get_width(),  # display width
            self.display.get_height(),  # display height
            (self.display.get_width() - self.x_tot * scale) / 2,  # x offset
            (self.display.get_height() - self.y_tot * scale) / 2,  # y offset
        )

    def distance(self, d: float) -> float:
        """Return the distance in the coordinate system as pixels on the pygame screen

        Args:
            d (float): The distance which will be converted

        Returns:
            float: The distance in pixels on the pygame screen
        """
        return self._update_dimensions()[0] * d

    def coord(self, x: float, y: float) -> tuple[float, float]:
        """Return the coordinate in the coordinate system as coordinate on the pygame screen

        Args:
            x (float): The x-coordinate which will be converted
            y (float): The y-coordinate which will be converted

        Returns:
            Tuple[float, float]: The coordinate on the screen
        """
        scale, _, h, x_off, y_off = self._update_dimensions()
        return (
            scale * x + x_off,
            h - ((scale * y) + y_off),
        )

    def paint_borders(self) -> None:
        """Draw borders on the pygame screen to mark the coordinate system"""
        _, w, h, x_off, y_off = self._update_dimensions()
        # Draw the borders to the left and right
        pygame.draw.rect(
            self.display,
            (0, 0, 0),
            (0, 0, x_off, h),
        )
        pygame.draw.rect(
            self.display,
            (0, 0, 0),
            (
                w - x_off,
                0,
                x_off,
                h,
            ),
        )

        # Draw the borders to the top and bottom
        pygame.draw.rect(
            self.display,
            (0, 0, 0),
            (0, 0, w, y_off),
        )
        pygame.draw.rect(
            self.display,
            (0, 0, 0),
            (
                0,
                h - y_off,
                w,
                y_off,
            ),
        )
