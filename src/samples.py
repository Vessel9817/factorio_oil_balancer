from math import inf

from .data import AbstractOilData

def hardcoded_alg(data: AbstractOilData) -> set[str]:
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

    if data.lubricant < 10 * round(data.target.lubricant / 10):
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

def dynamic_alg(data: AbstractOilData) -> list[str]:
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
    min_name, min_cost = 'NOTHING', 1

    costs = {
        'BASIC_OIL_PROCESSING': 18*dp + 81,
        'LUBRICANT': -20*dh + 20*dg + 200 if h >= 10 else inf,
        'LIGHT_OIL_CRACKING_TO_PETROLEUM_GAS': -30*dl + 20*dp + 325 if l >= 15 else inf,
        'HEAVY_OIL_CRACKING_TO_LIGHT_OIL': -40*dh + 30*dl + 625 if h >= 20 else inf,
        'SOLID_FUEL_FROM_PETROLEUM_GAS': -40*dp + 2*ds + 401 if p >= 20 else inf,
        'SOLID_FUEL_FROM_HEAVY_OIL': -40*dh + 2*ds + 401 if h >= 20 else inf,
        'SOLID_FUEL_FROM_LIGHT_OIL': -20*dl + 2*ds + 101 if l >= 10 else inf,
        'ADVANCED_OIL_PROCESSING': 10*dh + 18*dl + 22*dp + 227,
        'COAL_LIQUEFACTION': 26*dh + 8*dl + 4*dp + 189 if h >= 5 else inf,
    }

    for name, cost in costs.items():
        if cost <= min_cost:
            min_name, min_cost = name, cost

    return [] if min_name == 'NOTHING' else [min_name]

def combined_alg(data: AbstractOilData) -> set[str] | list[str]:
    runners = hardcoded_alg(data)

    return runners if len(runners) > 0 else dynamic_alg(data)
