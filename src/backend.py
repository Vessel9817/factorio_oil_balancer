from math import dist, inf
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

def sample_hardcoded_alg(data: AbstractOilData) -> set[str]:
    out: set[str] = set()

    if data.solid_fuel < data.target.solid_fuel:
        if data.petroleum_gas >= data.target.petroleum_gas:
            out.add('SOLID_FUEL_FROM_PETROLEUM_GAS')
        elif data.light_oil >= data.target.light_oil:
            out.add('SOLID_FUEL_FROM_LIGHT_OIL')
        elif data.heavy_oil >= data.target.heavy_oil:
            out.add('SOLID_FUEL_FROM_HEAVY_OIL')

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

    # Set access is nondeterministic
    return out

def sample_dynamic_alg(data: AbstractOilData) -> list[str]:
    error = dist(
        (
            data.target.heavy_oil,
            data.target.light_oil,
            data.target.petroleum_gas,
            data.target.solid_fuel,
            data.target.lubricant
        ),
        (
            data.heavy_oil,
            data.light_oil,
            data.petroleum_gas,
            data.solid_fuel,
            data.lubricant
        )
    )
    h = data.heavy_oil
    l = data.light_oil
    p = data.petroleum_gas
    s = data.solid_fuel
    g = data.lubricant
    dh = h - data.target.heavy_oil
    dl = l - data.target.light_oil
    dp = p - data.target.petroleum_gas
    ds = s - data.target.solid_fuel
    dg = g - data.target.lubricant
    min_name, min_cost = 'NOTHING', error + 1

    costs = {
        'BASIC_OIL_PROCESSING': error + 18*dp + 81,
        'LUBRICANT': error - 20*dh + 20*dg + 200 if h >= 10 else inf,
        'LIGHT_OIL_CRACKING_TO_PETROLEUM_GAS': error - 30*dl + 20*dp + 325 if l >= 15 else inf,
        'HEAVY_OIL_CRACKING_TO_LIGHT_OIL': error - 40*dh + 30*dl + 625 if h >= 20 else inf,
        'SOLID_FUEL_FROM_PETROLEUM_GAS': error - 40*dp + 2*ds + 401 if p >= 20 else inf,
        'SOLID_FUEL_FROM_HEAVY_OIL': error - 40*dh + 2*ds + 401 if h >= 20 else inf,
        'SOLID_FUEL_FROM_LIGHT_OIL': error - 20*dl + 2*ds + 101 if l >= 10 else inf,
        'ADVANCED_OIL_PROCESSING': error + 10*dh + 18*dl + 22*dp + 227,
        'COAL_LIQUEFACTION': error + 26*dh + 8*dl + 4*dp + 189 if h >= 5 else inf,
    }

    for name, cost in costs.items():
        if cost <= min_cost:
            min_name, min_cost = name, cost

    return [] if min_name == 'NOTHING' else [min_name]

def sample_combined_alg(data: AbstractOilData) -> set[str] | list[str]:
    runners = sample_hardcoded_alg(data)
    
    return runners if len(runners) > 0 else sample_dynamic_alg(data)
