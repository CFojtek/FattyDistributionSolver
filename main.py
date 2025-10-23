import logging

from config import platform, point_loads, safety_factor, supports, uniform_loads
from weight_distribution_solver.solver import Solver

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

    for i, support in enumerate(solved_supports, 1):
        logging.info(f"{'--' * 5} {i} {'--' * 5}{support.pretty_sring()}")


if __name__ == "__main__":
    main()
