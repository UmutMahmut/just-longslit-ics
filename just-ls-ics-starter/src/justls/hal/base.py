from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class InstrumentState:
    slit_width_um: float = 100.0
    grating: str = "G1"
    lamp_on: bool = False
    temperature_c: float = 20.0

class HAL(ABC):
    @abstractmethod
    def get_state(self) -> InstrumentState: ...

    @abstractmethod
    def set_slit_width(self, width_um: float) -> InstrumentState: ...

    @abstractmethod
    def select_grating(self, name: str) -> InstrumentState: ...

    @abstractmethod
    def set_lamp(self, on: bool) -> InstrumentState: ...
