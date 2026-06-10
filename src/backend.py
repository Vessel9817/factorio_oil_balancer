from typing import Callable, Iterable, Optional

from .data import AbstractOilData, OilData, OilDataRecord

class Simulator:
    def __init__(
        self,
        alg: Callable[[AbstractOilData], Iterable[str]],
        data: Optional[OilData] = None
    ) -> None:
        self._alg = alg

        if data is None:
            target = OilDataRecord(
                heavy_oil = 12500,
                light_oil = 12500,
                petroleum_gas = 12500,
                lubricant = 12500,
                solid_fuel = 1200
            )
            self.data = OilData(target)
        else:
            self.data = data

    def tick(self) -> bool:
        # Simulates 1 second of runtime
        runners = self._alg(self.data)

        if not runners:
            return False

        self.data.tick(runners)

        return True
