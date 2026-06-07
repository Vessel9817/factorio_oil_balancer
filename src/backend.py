from typing import Callable, Optional

from .data import AbstractOilData, OilData, OilDataRecord

class Simulator:
    def __init__(
        self,
        alg: Callable[[AbstractOilData], set[str]],
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

        if len(runners) < 1:
            return False

        self.data.tick(runners)

        return True

def sample_alg(data: AbstractOilData) -> set[str]:
    out: set[str] = set()

    if data.solid_fuel < data.target.solid_fuel:
        if data.petroleum_gas >= data.target.petroleum_gas:
            out.add('PETROLEUM_GAS_TO_SOLID_FUEL')
        elif data.light_oil >= data.target.light_oil:
            out.add('LIGHT_OIL_TO_SOLID_FUEL')
        elif data.heavy_oil >= data.target.heavy_oil:
            out.add('HEAVY_OIL_TO_SOLID_FUEL')

    if data.heavy_oil < data.target.heavy_oil:
        out.add('ADVANCED_OIL_PROCESSING')
        out.add('COAL_LIQUEFACTION')

    if data.lubricant < data.target.lubricant:
        out.add('LUBRICANT')

    if data.light_oil < data.target.light_oil:
        out.add('HEAVY_OIL_CRACKING_TO_LIGHT_OIL')

    if data.petroleum_gas < data.target.petroleum_gas:
        if data.light_oil >= data.target.light_oil:
            out.add('LIGHT_OIL_CRACKING_TO_PETROLEUM_GAS')
        else:
            out.add('BASIC_OIL_PROCESSING')

    return out
