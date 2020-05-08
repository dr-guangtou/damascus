"""Functions to deal with specific HSC data."""

import numpy as np

def filter_healpix_mask(mask, catalog, ra='ra', dec='dec', verbose=True):
    """Filter a catalog through a Healpix mask.

    Parameters
    ----------
    mask : healpy mask data
        healpy mask data
    catalog : numpy array or astropy.table
        Catalog that includes the coordinate information
    ra : string
        Name of the column for R.A.
    dec : string
        Name of the column for Dec.
    verbose : boolen, optional
        Default: True

    Return
    ------
        Selected objects that are covered by the mask.
    """
    import healpy

    nside, hp_indices = healpy.get_nside(mask), np.where(mask)[0]

    phi, theta = np.radians(catalog[ra]), np.radians(90. - catalog[dec])

    hp_masked = healpy.ang2pix(nside, theta, phi, nest=True)

    select = np.in1d(hp_masked, hp_indices)

    if verbose:
        print("# %d/%d objects are selected by the mask" % (select.sum(), len(catalog)))

    return catalog[select]