# Licensed under MIT license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""Functions to deal with DECaLS sweep catalog.

The sweeps are light-weight FITS binary tables (containing a subset of the most
commonly used Tractor measurements) of all the Tractor catalogs for which
`BRICK_PRIMARY==T` in rectangles of RA, Dec.

Please see:
    http://legacysurvey.org/dr8/files/#sweep-catalogs-region-sweep

"""

from astropy.io import fits

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
    
