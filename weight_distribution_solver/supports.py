from dataclasses import dataclass, field


@dataclass
class PointSupport:
    """Support at position (x, y)"""

    x: float
    y: float

    safety_factor: float = field(init=False, default=1.0)
    tributary_area: float = field(init=False, default=0.0)
    force: float = field(init=False, default=0.0)
    design_force: float = field(init=False, default=0.0)

    def pretty_sring(self) -> str:
        mass: float = self.design_force / 9.81

        return f"""
        Support at Position ({self.x}, {self.y})
        Actual force: {self.force:.2f}N
        Design force: {self.design_force:.2f}N
        Mass: {mass:.2f}kg
        """
