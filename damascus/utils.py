"""Utility functions."""

import numpy as np

__all__ = ['mag_to_flux', 'flux_to_mag', 'e1_e2_to_shape']


def mag_to_flux(mag, zeropoint=27.0):
    """Convert magnitude into flux unit.
    """
    return 10.0 ** ((zeropoint - mag) / 2.5)

def flux_to_mag(flux, zeropoint=27.0):
    """Convert flux into magnitude unit.
    """
    # TODO: deal with negative values more gracefully
    return -2.5 * np.log10(flux) + zeropoint

def e1_e2_to_shape(e1, e2, shape_type='b_a'):
    """Convert the complex ellipticities to normal shape.
    """
    # Positiona angle
    pa = np.arctan(e2 / e1) * 0.5

    # Axis ratio or ellipticity or eccentricity
    abs_e = np.sqrt(e1 ** 2 + e2 ** 2)
    b_a = (1 - abs_e) / (1 + abs_e) 
    if shape_type == 'b_a':
        # Axis ratio
        return b_a, pa
    elif shape_type == 'ellip':
        # Ellipticity
        return 1.0 - b_a, pa
    elif shape_type == 'eccen':
        # Eccentricity
        return np.sqrt(1 - b_a ** 2), pa
    else:
        raise ValueError("# Wrong shape type: [b_a|ellip|eccen]")

def shape_to_e1_e2(b_a, pa):
    """Convert axis ratio and position angle into complex ellipticities.
    """
    abs_e = (1 - b_a) / (1 + b_a)
    return abs_e * np.cos(2 * pa), abs_e * np.sin(2 * pa)
