from dataclasses import dataclass
from typing import Union


@dataclass
class PointLoad:
    """Point load in N at position (x, y)"""

    force: float
    x: float
    y: float


@dataclass
class UniformLoad:
    """Uniform load in N/m²"""

    pressure: float


Load = Union[PointLoad, UniformLoad]
