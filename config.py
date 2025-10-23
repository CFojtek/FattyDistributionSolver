from weight_distribution_solver.loads import PointLoad, UniformLoad
from weight_distribution_solver.platform import Platform
from weight_distribution_solver.supports import PointSupport

# Platform
length: float = 1.5
width: float = 1.2
platform: Platform = Platform(length, width)

# Uniform load
uniform_loads: list[UniformLoad] = [
    UniformLoad(200),
]

# Point loads
point_loads: list[PointLoad] = [
    PointLoad(850, 0.75, 0),
    PointLoad(200, 0.4, 1),
    PointLoad(200, 1.1, 1),
]

# Supports
safety_factor: float = 1
supports: list[PointSupport] = [
    PointSupport(0, 0),
    PointSupport(length, 0),
    PointSupport(0, width),
    PointSupport(length, width),
    PointSupport(length / 2, 0),
    PointSupport(length / 2, 0.75 * width),
]
