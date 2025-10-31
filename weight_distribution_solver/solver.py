import logging

import numpy as np

from weight_distribution_solver.loads import PointLoad, UniformLoad
from weight_distribution_solver.platform import Platform
from weight_distribution_solver.supports import PointSupport
from weight_distribution_solver.utils import (
    calculate_distance,
    calculate_tributary_areas,
)

epsilon = 1e-10


class Solver:
    def __init__(self, platform: Platform, safety_factor: float) -> None:
        self.platform = platform
        self.safety_factor = safety_factor
        self.uniform_loads: list[UniformLoad] = []
        self.point_loads: list[PointLoad] = []
        self.supports: list[PointSupport] = []

    def add_uniform_load(self, load: UniformLoad) -> None:
        self.uniform_loads.append(load)

    def add_point_load(self, load: PointLoad) -> None:
        self.point_loads.append(load)

    def add_support(self, support: PointSupport) -> None:
        self.supports.append(support)

    def calculate_total_applied_force(self) -> float:
        applied_force = sum([load.force for load in self.point_loads])
        applied_force += (
            sum([load.pressure for load in self.uniform_loads]) * self.platform.area
        )
        return applied_force

    def check_force_balance(self) -> None:
        supporting_force = sum([support.force for support in self.supports])
        applied_force = self.calculate_total_applied_force()

        if abs(supporting_force - applied_force) > 1e-6:
            raise ValueError(
                "Force balance not satisfied! Applied forces are not equal to supporting forces."
            )

        logging.info("Force balance between applied and supporting forces satisfied")

    def solve(self) -> list[PointSupport]:
        if self.uniform_loads:
            logging.info("Calculating uniform loads...")

            aggregated_uniform_load = sum(load.pressure for load in self.uniform_loads)
            total_uniform_load = aggregated_uniform_load * self.platform.area

            support_coordinates = np.array(
                [[support.x, support.y] for support in self.supports]
            )
            tributary_areas = calculate_tributary_areas(
                self.platform, support_coordinates
            )

            for support, tributary_area in zip(self.supports, tributary_areas):
                fraction_area = tributary_area / self.platform.area
                support.force += total_uniform_load * fraction_area
                support.tributary_area = tributary_area

        if self.point_loads:
            logging.info("Calculating point loads...")

            for load in self.point_loads:
                distances_to_supports = [
                    calculate_distance(load.x, load.y, support.x, support.y)
                    for support in self.supports
                ]

                inverse_distances = [
                    1 / d if d != 0 else 1 / epsilon for d in distances_to_supports
                ]
                total_inverse_distance = sum(inverse_distances)
                normalized_weights = [
                    inverse_distance / total_inverse_distance
                    for inverse_distance in inverse_distances
                ]

                for support, weight in zip(self.supports, normalized_weights):
                    support.force += load.force * weight

        for support in self.supports:
            support.safety_factor = self.safety_factor
            support.design_force = support.force * self.safety_factor

        self.check_force_balance()

        return self.supports
