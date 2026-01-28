"""Surveying module for civil engineering applications
"""

import math

from typing import Tuple


def distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Calculate the Euclidean distance between two points.

    Args:
        p1 (tuple[float, float]): Coordinates of the first point (x1, y1).
        p2 (tuple[float, float]): Coordinates of the second point (x2, y2).

    Returns:
        float: The Euclidean distance between the two points.
    """
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def horizontal_distance(slope_distance: float, angle_deg: float) -> float:
    """Calculate the horizontal distance given the slope distance and angle.

    Args:
        slope_distance (float): The slope distance.
        angle_deg (float): The angle in degrees.

    Returns:
        float: The horizontal distance.
    """
    angle_rad = math.radians(angle_deg)
    return slope_distance * math.cos(angle_rad)

def elevation_difference(slope_distance: float, angle_deg: float) -> float:
    """Calculate the elevation difference given the slope distance and angle.

    Args:
        slope_distance (float): The slope distance.
        angle_deg (float): The angle in degrees.

    Returns:
        float: The elevation difference.
    """
    angle_rad = math.radians(angle_deg)
    return slope_distance * math.sin(angle_rad)
