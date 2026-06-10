from math import dist
from typing import Callable, Iterable

from . import backend, cli, data, samples

if __name__ == '__main__':
    algs: list[Callable[[data.AbstractOilData], Iterable[str]]] = [
        samples.hardcoded_alg,
        samples.dynamic_alg,
        samples.dynamic_hardcoded_alg,
        samples.computed_alg,
        samples.dynamic_computed_alg
    ]
    alg_msg = \
        'Please select an algorithm:\n' \
        '(0) Hardcoded\n' \
        '(1) Dynamic\n' \
        '(2) Hardcoded+Dynamic\n' \
        '(3) Computed\n' \
        '(4) Computed+Dynamic\n'

    alg_index = cli.get_int(alg_msg)

    while alg_index < 0 or alg_index >= len(algs):
        alg_index = cli.get_int(f"Algorithm {alg_index} doesn't exist\n{alg_msg}")

    # Running simulation
    alg = algs[alg_index]
    sim = backend.Simulator(alg)
    i = 0

    while sim.tick():
        i += 1

    # Aggregating simulation results
    hours = i // (60 * 60)
    mins = round(i / 60) - 60 * hours
    error = dist(
        (
            sim.data.target.heavy_oil,
            sim.data.target.light_oil,
            sim.data.target.petroleum_gas,
            sim.data.target.solid_fuel,
            sim.data.target.lubricant
        ),
        (
            sim.data.heavy_oil,
            sim.data.light_oil,
            sim.data.petroleum_gas,
            sim.data.solid_fuel,
            sim.data.lubricant
        )
    )

    print('Results:')
    print(f'- Heavy oil: {sim.data.heavy_oil}')
    print(f'- Light oil: {sim.data.light_oil}')
    print(f'- Petroleum gas: {sim.data.petroleum_gas}')
    print(f'- Lubricant: {sim.data.lubricant}')
    print(f'- Solid fuel: {sim.data.solid_fuel}')
    print(f'\nOverall error: {error}')
    print(f'Completed in {i} seconds (about {hours}h {mins}mins)')
