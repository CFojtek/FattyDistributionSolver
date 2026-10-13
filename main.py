import logging

from config_example import platform, point_loads, safety_factor, supports, uniform_loads
from weight_distribution_solver.solver import Solver
from weight_distribution_solver.utils import mirror_around_axis

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


def main():
    # Solver
    logging.info("Starting solver...")
    solver = Solver(platform, safety_factor)

    for load in uniform_loads:
        solver.add_uniform_load(load)
    logging.info("Added uniform loads.")

    for load in point_loads:
        solver.add_point_load(load)
    logging.info("Added point loads.")

    for support in supports:
        solver.add_support(support)
    logging.info("Added supports.")

    logging.info("Starting solver...")
    solved_supports = solver.solve()
    logging.info("Solver finished!\n")

    applied_force = solver.calculate_total_applied_force()
    logging.info(
        f"Total applied force: {applied_force:.2f}N (={applied_force / 9.81:.2f}kg)\n"
    )

    for i, support in enumerate(solved_supports, 1):
        logging.info(f"{'--' * 5} {i} {'--' * 5}{support.pretty_sring()}")

    for i, support in enumerate(solved_supports, 1):
        mirrored_x, mirrored_y = mirror_around_axis(
            support.x, support.y, offset=platform.length / 2, axis="y"
        )
        logging.info(f"Mirrored support coordinates {i}: ({mirrored_x}, {mirrored_y})")


if __name__ == "__main__":
    main()
