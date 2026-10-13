# Weight Distribution Solver

A Python tool for calculating the forces on point supports of a rectangular platform under uniform and point loads. Given a platform with known dimensions, applied loads (uniform pressure and concentrated point loads), and support positions, it computes how each support reacts — including both actual and design forces accounting for a safety factor.

## Concepts

- **Platform**: A rectangle defined by `length` × `width` (meters).
- **Uniform load** (`UniformLoad`): Distributed pressure in N/m² over the entire platform area, distributed to supports proportionally to their tributary areas (Voronoi-based).
- **Point load** (`PointLoad`): Concentrated force in N at a specific `(x, y)` position on the platform. It is distributed to supports inversely proportional to distance from each support.
- **Support** (`PointSupport`): A point at `(x, y)` that carries the reaction force from the applied loads. The solver reports actual force, design force (× safety factor), and equivalent mass in kg.

## Installation

Requires **Python ≥ 3.12** and **Poetry**.

```bash
poetry install
```

## Usage

### 1. Create or edit a config file

Define your `Platform`, `UniformLoad`s, `PointLoad`s, `PointSupport`s, and `safety_factor` in a Python file. See the existing examples:

| Config file        | Description                                      |
| ------------------ | ------------------------------------------------ |
| `config_example.py`  | Simple example: 0.6 m × 0.6 m platform with distributed point support forces (only one in the public repo)     |

**Minimal config** (`my_config.py`):
```python
from weight_distribution_solver.platform import Platform
from weight_distribution_solver.loads import PointLoad, UniformLoad
from weight_distribution_solver.supports import PointSupport

length = 1.0
width = 0.8
platform = Platform(length, width)

uniform_loads: list[UniformLoad] = [
    UniformLoad(200),  # N/m² over entire platform
]

point_loads: list[PointLoad] = [
    PointLoad(500, 0.3, 0.4),  # 500 N at (x=0.3, y=0.4)
]

safety_factor: float = 1.2

supports: list[PointSupport] = [
    PointSupport(0, 0),
    PointSupport(length, 0),
    PointSupport(0, width),
    PointSupport(length, width),
]
```

### 2. Run the solver

Edit `main.py` to point at your config instead of the default:

```python
# In main.py, replace:
from config_drum import platform, point_loads, safety_factor, supports, uniform_loads

# With:
from my_config import platform, point_loads, safety_factor, supports, uniform_loads
```

Then run:
```bash
poetry run python main.py
```

### 3. Read the output

The solver prints to stdout (log level INFO):

- Total applied force (N and kg)
- Force per support: position, actual force (N), design force (N), equivalent mass (kg)
- Mirrored coordinates for reference

**Example output:**
```
INFO root: Starting solver...
INFO root: Added uniform loads.
INFO root: Added point loads.
INFO root: Added supports.
INFO root: Force balance between applied and supporting forces satisfied
INFO root: Total applied force: 3500,23N =(1647,21kg)
INFO root: -- -- -- -- -- 1 -- -- -- -- --
        Support at Position (0, 0)
        Actual force: 872,56N
        Design force: 1047,07N
        Mass: 106,83kg
...
```

## Improvements
- Add CLI parser instead of using config.py files
- Validate that point loads and supports are within geometry boundaries
- Add different platform geometry types
- Add tests

## License

MIT (see LICENSE file).

Author: Christian Fojtek
