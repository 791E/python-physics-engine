"""Useful math functions for linear algebra"""

from __future__ import annotations
import numpy as np


class Vec2D:
    """
    2D vectors, for positions, rotations, velocities and accelerations of bodies.
    """

    def __init__(self, x: float, y: float):
        """
        Args:
            x (float): x component of the vector
            y (float): y component of the vector
        """
        self.components = np.array([x, y])

    def __iter__(self):
        """
        Iterate over the magnitudes. Example usage (assuming vec is a Vec2D):
        sum(*vec) # does the same as
        sum(vec.components[0], vec.components[0])
        """
        return iter(self.components)

    @property
    def magnitude(self):
        """
        The self-updating magnitude of the vector
        """
        return np.sqrt(np.sum(np.square(self.components)))

    def rotate(self, theta: float, deg: bool = False) -> None:
        """
        Rotate itself the specified number of radians / degrees

        Args:
            theta (float): By how much the vector should be rotated
            deg (bool): Whether or not to use degrees as unit. Default is radians.
        """
        if deg:
            theta = theta * np.pi / 180

        rot_matrix = np.array(
            [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]]
        )

        self.components = np.round(rot_matrix @ self.components, decimals=15)

    def add(self, *other_vec: Vec2D) -> None:
        """
        Add another vector to self.vec

        Args:
            *other_vec (Vec2D): All the vectors that should be added to self.components
        """
        for vec in other_vec:
            self.components += vec.components

    def angle(self, other_vec: Vec2D, deg: bool = False) -> float:
        """
        Calculate the angle between self.components and other_vec.components
        Formats the output as degree if deg=True is specified, uses radian by default.

        Args:
            other_vec (Vec2D): The secondary vector which the angle should be taken from
            deg (bool): Whether or not to convert the result from radians to degrees
        """
        dot_product = np.dot(self.components, other_vec.components)
        magnitudes_sum = np.sqrt(
            self.components[0] ** 2 + self.components[1]
        ) * np.sqrt(other_vec.components[0] ** 2 + other_vec.components[1])

        if deg:
            return np.round(np.arccos(dot_product / magnitudes_sum) * 180 / np.pi, decimals=14)

        return np.arccos(dot_product / magnitudes_sum)
