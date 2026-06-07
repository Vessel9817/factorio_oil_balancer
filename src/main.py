from math import dist

from . import backend

if __name__ == '__main__':
    sim = backend.Simulator(backend.sample_alg)
    i = 0

    while sim.tick():
        i += 1

    hours = i // (60 * 60)
    mins = round(i / 60) - 60 * hours
    error = dist(
        (
            sim.data.heavy_oil,
            sim.data.light_oil,
            sim.data.petroleum_gas,
            sim.data.solid_fuel,
            sim.data.lubricant
        ),
        (
            sim.data.target.heavy_oil,
            sim.data.target.light_oil,
            sim.data.target.petroleum_gas,
            sim.data.target.solid_fuel,
            sim.data.target.lubricant
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
