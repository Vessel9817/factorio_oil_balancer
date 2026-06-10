from abc import abstractmethod
from typing import Iterable, NamedTuple, Optional

class OilDataRecord(NamedTuple):
    heavy_oil: int
    light_oil: int
    petroleum_gas: int
    lubricant: int
    solid_fuel: int

class AbstractOilData:
    @property
    @abstractmethod
    def heavy_oil(self) -> int:
        pass

    @property
    @abstractmethod
    def light_oil(self) -> int:
        pass

    @property
    @abstractmethod
    def petroleum_gas(self) -> int:
        pass

    @property
    @abstractmethod
    def lubricant(self) -> int:
        pass

    @property
    @abstractmethod
    def solid_fuel(self) -> int:
        pass

    @property
    @abstractmethod
    def target(self) -> OilDataRecord:
        pass

class OilData(AbstractOilData):
    def __init__(
        self,
        target: OilDataRecord,
        current: Optional[OilDataRecord] = None
    ) -> None:
        self._basic_oil_processing_tick = 0
        self._advanced_oil_processing_tick = 0
        self._coal_liquefaction_tick = 0
        self._heavy_oil_cracking_tick = 0
        self._light_oil_cracking_tick = 0
        self._target = target
        self._heavy_oil = 0 if current is None else current.heavy_oil
        self._light_oil = 0 if current is None else current.light_oil
        self._petroleum_gas = 0 if current is None else current.petroleum_gas
        self._solid_fuel = 0 if current is None else current.solid_fuel
        self._lubricant = 0 if current is None else current.lubricant

    @property
    def heavy_oil(self) -> int:
        return self._heavy_oil

    @property
    def light_oil(self) -> int:
        return self._light_oil

    @property
    def petroleum_gas(self) -> int:
        return self._petroleum_gas

    @property
    def lubricant(self) -> int:
        return self._lubricant

    @property
    def solid_fuel(self) -> int:
        return self._solid_fuel

    @property
    def target(self) -> OilDataRecord:
        return self._target

    def tick_basic_oil_processing(self) -> None:
        self._basic_oil_processing_tick += 1

        if self._basic_oil_processing_tick >= 5:
            self._basic_oil_processing_tick = 0
            self._petroleum_gas += 45

    def tick_advanced_oil_processing(self) -> None:
        self._advanced_oil_processing_tick += 1

        if self._advanced_oil_processing_tick >= 5:
            self._advanced_oil_processing_tick = 0
            self._heavy_oil += 25
            self._light_oil += 45
            self._petroleum_gas += 55

    def tick_coal_liquefaction(self) -> None:
        if self._heavy_oil < 25:
            return
        if self._coal_liquefaction_tick == 0:
            self._heavy_oil -= 25

        self._coal_liquefaction_tick += 1

        if self._coal_liquefaction_tick >= 5:
            self._coal_liquefaction_tick = 0
            self._heavy_oil += 90
            self._light_oil += 20
            self._petroleum_gas += 10

    def tick_heavy_oil_cracking(self) -> None:
        if self._heavy_oil < 40:
            return
        if self._coal_liquefaction_tick == 0:
            self._heavy_oil -= 40

        self._heavy_oil_cracking_tick += 1

        if self._heavy_oil_cracking_tick >= 2:
            self._heavy_oil_cracking_tick = 0
            self._light_oil += 30

    def tick_light_oil_cracking(self) -> None:
        if self._light_oil < 30:
            return
        if self._coal_liquefaction_tick == 0:
            self._light_oil -= 30

        self._light_oil_cracking_tick += 1

        if self._light_oil_cracking_tick >= 2:
            self._light_oil_cracking_tick = 0
            self._petroleum_gas += 20

    def tick_heavy_solid_fuel(self) -> None:
        if self._heavy_oil < 20:
            return

        self._heavy_oil -= 20
        self._solid_fuel += 1

    def tick_light_solid_fuel(self) -> None:
        if self._light_oil < 10:
            return

        self._light_oil -= 10
        self._solid_fuel += 1

    def tick_petroleum_solid_fuel(self) -> None:
        if self._petroleum_gas < 20:
            return

        self._petroleum_gas -= 20
        self._solid_fuel += 1

    def tick_lubricant(self) -> None:
        if self._heavy_oil < 10:
            return

        self._heavy_oil -= 10
        self._lubricant += 10

    RUNNERS = {
        'BASIC_OIL_PROCESSING': tick_basic_oil_processing,
        'ADVANCED_OIL_PROCESSING': tick_advanced_oil_processing,
        'COAL_LIQUEFACTION': tick_coal_liquefaction,
        'HEAVY_OIL_CRACKING_TO_LIGHT_OIL': tick_heavy_oil_cracking,
        'LIGHT_OIL_CRACKING_TO_PETROLEUM_GAS': tick_light_oil_cracking,
        'SOLID_FUEL_FROM_HEAVY_OIL': tick_heavy_solid_fuel,
        'SOLID_FUEL_FROM_LIGHT_OIL': tick_light_solid_fuel,
        'SOLID_FUEL_FROM_PETROLEUM_GAS': tick_petroleum_solid_fuel,
        'LUBRICANT': tick_lubricant
    }

    def tick(self, runners: Iterable[str]) -> None:
        ran: set[str] = set()

        for runner in runners:
            if runner not in ran:
                assert runner in OilData.RUNNERS, f'Invalid runner name: {runner}'

                ran.add(runner)

                OilData.RUNNERS[runner](self)
