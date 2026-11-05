from dataclasses import dataclass


@dataclass
class Event:
    id: int
    start: int
    end: int

    def collides_with(self, other: "Event") -> bool:
        return self.end >= other.start and other.end >= self.start


@dataclass
class PositionedEvent:
    id: int
    start: int
    end: int
    column: int = 0
    num_columns: int = 1
    col_span: int = 1
    left: float = 0.0
    width: float = 1.0
