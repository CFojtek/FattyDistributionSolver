from weight_distribution_solver.loads import PointLoad, UniformLoad
from weight_distribution_solver.platform import Platform
from weight_distribution_solver.supports import PointSupport

# Platform
length: float = 0.6
width: float = 0.6
platform: Platform = Platform(length, width)

# Uniform load
uniform_loads: list[UniformLoad] = [
    UniformLoad(165 + 15),
]

# Point loads
point_loads: list[PointLoad] = [
    PointLoad(300, 0.07, 0.15),
    PointLoad(300, 0.53, 0.15),
    PointLoad(300, 0.3, 0.53),
]

# Supports
safety_factor: float = 1
supports: list[PointSupport] = [
    PointSupport(0, 0),
    PointSupport(length, 0),
    PointSupport(0, width),
    PointSupport(length, width),
    PointSupport(length / 2, width / 2),
]
