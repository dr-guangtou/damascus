# Licensed under MIT license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""Functions to deal with DECaLS sweep catalog.

The sweeps are light-weight FITS binary tables (containing a subset of the most
commonly used Tractor measurements) of all the Tractor catalogs for which
`BRICK_PRIMARY==T` in rectangles of RA, Dec.

Please see:
    http://legacysurvey.org/dr8/files/#sweep-catalogs-region-sweep

"""

import os

import numpy as np

from astropy.io import fits

__all__ = ['sweep_to_box', 'SweepCatalog']


def sweep_to_box(sweep_name):
    '''Decode the Sweep catalog name into (RA, Dec) range. 
    
    Parameters
    ---------- 
    sweep_name: string
        Path or the file name of the Sweep catalog.
    
    Returns
    -------
    box: np.array
        An array of the coordinates of the four corners of the box.
    
    ''' 
    """Decode the name of the Sweep file into box of coordinates."""
    # Extract the RA, Dec ranges of the Sweep file
    radec_str = os.path.splitext(
        os.path.split(sweep_name)[1])[0].replace('sweep-', '').split('-')

    # Get the minimum and maximum RA & Dec
    ra_min = float(radec_str[0][0:3])
    dec_min = float(radec_str[0][-3:]) * (-1 if radec_str[0][3] == 'm' else 1)

    ra_max = float(radec_str[1][0:3])
    dec_max = float(radec_str[1][-3:]) * (-1 if radec_str[1][3] == 'm' else 1)

    return np.vstack(
        [[ra_min, ra_max, ra_max, ra_min],
         [dec_min, dec_min, dec_max, dec_max]]).T


class SweepCatalog(object):
    '''A class to deal with DECaLS sweep catalog

    Parameters
    ----------
    input: `int`
         description

    Attributes
    ----------
    attrib1
        description

    Examples
    --------


    Notes
    -----

    '''
    def __init__(self, catalog):
        '''Initialize a SweepCatalog object.

        Parameters
        ----------
        catalog: str
             Path to the FITS format sweep catalog.

        Notes
        -----
            Will try to read the catalog using `astropy.fits` in `memap=True` mode.

        '''

