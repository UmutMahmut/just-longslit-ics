from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from .capabilities import Capabilities


@dataclass(frozen=True)
class State:
    slit_width_um: float
    lamp_on: bool
    temperature_c: float


    slit_angle_deg: float = 0.0
class HAL(ABC):
    """Hardware Abstraction Layer (HAL) for JUST Long-Slit ICS.

    New interface ONLY (旧接口不保留):
      - set_slit_width_um
      - set_slit_angle_deg
      - set_calib_lamp_on
      - get_state / get_capabilities
    """

    @abstractmethod
    def get_state(self) -> State:
        raise NotImplementedError

    @abstractmethod
    def get_capabilities(self) -> Capabilities:
        raise NotImplementedError

    @abstractmethod
    def set_slit_width_um(self, width_um: float) -> State:
        raise NotImplementedError




    @abstractmethod
    def set_slit_angle_deg(self, angle_deg: float) -> State:
        raise NotImplementedError
    @abstractmethod
    def set_calib_lamp_on(self, on: bool) -> State:
        raise NotImplementedError
