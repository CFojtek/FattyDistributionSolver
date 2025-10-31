import math

import numpy as np
from scipy.spatial import Voronoi
from shapely.geometry import Polygon, box

from weight_distribution_solver.platform import Platform


def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate Euclidean distance between two points"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calculate_tributary_areas(
    platform: Platform, support_coordinates: np.ndarray
) -> list[float]:
    """Calculate tributary areas for supports using Voronoi.
    Suports at the edges can have infinite areas. To solve this, we artificially add some support at some far away corners and clip the areas later.
    """

    x_edge = 5 * platform.length
    y_edge = 5 * platform.width
    artificial_coordinates = np.array(
        [
            [-x_edge, -y_edge],
            [-x_edge, y_edge],
            [x_edge, -y_edge],
            [x_edge, y_edge],
        ]
    )

    coordinates = np.vstack((support_coordinates, artificial_coordinates))
    voronoi = Voronoi(coordinates)

    platform_boundary = box(0, 0, platform.length, platform.width)
    tributary_areas = []
    for region_index in voronoi.point_region[: len(support_coordinates)]:
        region = voronoi.regions[region_index]
        if -1 in region or len(region) == 0:
            raise ValueError("Support has infinite tributary area")

        region_vertices = voronoi.vertices[region]
        voroni_polygon = Polygon(region_vertices)
        clipped_polygon = voroni_polygon.intersection(platform_boundary)

        area = clipped_polygon.area
        tributary_areas.append(area)

    if abs(platform.area - sum(tributary_areas)) > 1e-6:
        raise ValueError("Calculated tributary areas does not equal platform area")

    return tributary_areas


def mirror_around_axis(
    x: float, y: float, offset: float = 0, axis: str = "x"
) -> tuple[float, float]:
    """Mirror a point around an axis with an optional offset"""
    if axis == "x":
        mirrored_x = x
        mirrored_y = -y + 2 * offset
    elif axis == "y":
        mirrored_x = -x + 2 * offset
        mirrored_y = y
    else:
        raise ValueError("Axis must be 'x' or 'y'")

    return mirrored_x, mirrored_y
