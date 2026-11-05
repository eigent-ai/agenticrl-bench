"""Material property lookups and interpolation for engineering analysis."""


# Built-in material databases
_THERMAL_EXPANSION_DATA = {
    'steel': [
        (20.0, 1.20e-5),
        (100.0, 1.22e-5),
        (200.0, 1.27e-5),
        (300.0, 1.33e-5),
        (400.0, 1.39e-5),
        (500.0, 1.45e-5),
    ],
    'aluminum': [
        (20.0, 2.31e-5),
        (100.0, 2.38e-5),
        (200.0, 2.47e-5),
        (300.0, 2.56e-5),
        (400.0, 2.67e-5),
    ],
    'titanium': [
        (20.0, 8.60e-6),
        (100.0, 8.80e-6),
        (200.0, 9.10e-6),
        (300.0, 9.40e-6),
        (400.0, 9.70e-6),
    ],
}


def interpolate_yield_strength(temperature, data_points):
    """Linearly interpolate yield strength at a given temperature.

    Args:
        temperature: temperature in degrees C
        data_points: list of (temperature, yield_strength) tuples, sorted by temperature

    Returns:
        Interpolated yield strength as float
    """
    if temperature <= data_points[0][0]:
        return float(data_points[0][1])
    if temperature >= data_points[-1][0]:
        return float(data_points[-1][1])

    for i in range(len(data_points) - 1):
        t0, y0 = data_points[i]
        t1, y1 = data_points[i + 1]
        if t0 <= temperature <= t1:
            frac = (temperature - t0) / (t1 - t0)
            return float(y0 + frac * (y1 - y0))

    return float(data_points[-1][1])


def thermal_expansion_coefficient(material, temp):
    """Look up thermal expansion coefficient by material and temperature.

    Args:
        material: material name (e.g. 'steel', 'aluminum', 'titanium')
        temp: temperature in degrees C

    Returns:
        Thermal expansion coefficient (1/K) as float
    """
    material = material.lower()
    if material not in _THERMAL_EXPANSION_DATA:
        raise ValueError(f"Unknown material: {material}")

    data_points = _THERMAL_EXPANSION_DATA[material]
    temps = [d[0] for d in data_points]
    coeffs = [d[1] for d in data_points]

    if temp <= temps[0]:
        return coeffs[0]
    if temp >= temps[-1]:
        return coeffs[-1]

    for i in range(len(temps) - 1):
        if temps[i] <= temp <= temps[i + 1]:
            frac = (temp - temps[i]) / (temps[i + 1] - temps[i])
            return coeffs[i] + frac * (coeffs[i + 1] - coeffs[i])

    return coeffs[-1]
