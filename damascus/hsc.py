"""Functions to deal with specific HSC data."""

import numpy as np

import healpy

from astropy.io import fits

from . import io

__all__ = ['filter_hsc_fdfc_mask']

HSC_ZP = 27.0  # Zeropoint for HSC survey

def filter_hsc_fdfc_mask(cat, fdfc_mask, ra='RA', dec='DEC', verbose=True):
    """Filter a catalog through HSC FDFC mask."""
    # Read the fits catalog if input is path to the file
    if isinstance(cat, str):
        cat = fits.open(cat, memmap=True)[1].data

    # Read the healpix mask if input is path to the file
    if isinstance(fdfc_mask, str):
        fdfc_mask = io.read_healpix_fits(fdfc_mask)

    # Find the matched objects
    nside, hp_indices = healpy.get_nside(fdfc_mask), np.where(fdfc_mask)[0]
    phi, theta = np.radians(cat[ra]), np.radians(90. - cat[dec])
    hp_masked = healpy.ang2pix(nside, theta, phi, nest=True)
    select = np.in1d(hp_masked, hp_indices)

    if verbose:
        print("# Find {:d} objects inside the FDFC region".format(select.sum()))

    if select.sum() < 1:
        return None
    return cat[select]
