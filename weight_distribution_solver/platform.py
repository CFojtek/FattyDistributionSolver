from dataclasses import dataclass


@dataclass
class Platform:
    length: float
    width: float

    @property
    def area(self) -> float:
        return self.length * self.width
