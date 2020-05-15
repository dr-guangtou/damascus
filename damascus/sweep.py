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
import copy

import numpy as np

from astropy.io import fits

__all__ = ['sweep_to_box', 'SweepCatalog']


def sweep_to_box(sweep_name):
    '''Decode the Sweep catalog name into (RA, Dec) range.

    Parameters
    ----------
    sweep_name: `string`
        Path or the file name of the Sweep catalog.

    Returns
    -------
    box: `np.array`
        An array of the coordinates of the four corners of the box.

    '''
    # Extract the RA, Dec ranges of the Sweep file
    radec_str = os.path.splitext(
        os.path.split(sweep_name)[-1])[0].replace('sweep-', '').split('-')

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

    Attributes
    ----------
    attrib1
        description

    Examples
    --------

    Notes
    -----

    '''
    def __init__(self, catalog, read_in=False):
        '''Initialize a SweepCatalog object.

        Parameters
        ----------
        catalog: `str`
            Path to the FITS format sweep catalog.
        read_in: `bool`
            Read in the catalog immediately.

        Notes
        -----
            Will try to read the catalog using `astropy.fits` in `memap=True` mode.

        '''
        self._catalog_path = catalog
        self._catalog_name = os.path.split(catalog)[-1]
        assert os.path.isfile(catalog), FileNotFoundError("Cannot find the sweep catalog!")

        # Get the RA, Dec coordinates of the vertices
        self._vertices = sweep_to_box(self._catalog_name)

        # Open the FITS file
        self._hdu_list = self.open()
        self.header = self._hdu_list[1].header
        self._columns = self._get_columns()

        # Read the catalog data.
        self.data = None
        if read_in:
            self.load()

    def __repr__(self):
        return "Sweep Catalog: {0._catalog_name:s}".format(self)

    def open(self):
        ''' Open the FITS file as a HUDList.
        '''
        return fits.open(self._catalog_path, memmap=True)

    def load(self):
        ''' Read in the FITS catalog as FITS record.
        '''
        self.data = self._hdu_list[1].data

    def close(self):
        ''' Close the HDUList of the FITS file.
        '''
        self._hdu_list.close()

    def _get_columns(self):
        ''' Get the columns names of the Sweep catalog.
        '''
        cards = np.asarray(self.header.cards)[:, 0]
        return [self.header[key] for key in cards[
            np.asarray(['TTYPE' in card for card in cards])]]

    def has_column(self, col):
        ''' Check whether the catalog has certain column.

        Parameters
        ----------
        col: `string`
            Name of the column to check.

        Returns
        -------
        has_column: `bool`
            Whether the column is in the catalog or not.

        '''
        return col.upper().strip() in self.columns

    def demography(self):
        ''' Show the demography of different types of objects in the catalog.
        '''
        if self.data is None:
            self.load()
        print("# There are {:d} objects in the catalog".format(len(self.data)))


    def select(self):
        ''' Select a sub-sample of objects according to certain rule.

        Parameters
        ----------
        param1: `int`
             description

        Returns
        -------
        result: `bool`
            description

        '''
        return

    def cover(self, ra, dec):
        ''' Find out is the object covered or how many objects are covered in this sweep.

        Parameters
        ----------
        ra: `float` or `np.array`
             RA of the object or array of RA of the sample.
        dec: `float` or `np.array`
             Dec of the object or array of Dec of the sample.

        Returns
        -------
        result: `bool`
             Whether the object is covered, or a boolen mask for overlapped objects.

        '''
        if not np.isscalar(ra):
            assert len(ra) == len(dec), "RA & Dec array should have the same size."

        return ((ra >= self.ra_min) & (ra < self.ra_max) &
                (dec >= self.dec_min) & (dec < self.dec_max))

    @property
    def path(self):
        '''Path to the Sweep catalog.
        '''
        return self._catalog_path

    @property
    def name(self):
        '''Get the file name of the Sweep catalog.
        '''
        return self._catalog_name

    @property
    def vertices(self):
        '''Get the RA, Dec coordinates of the vertices.
        '''
        return self._vertices

    @property
    def ra_min(self):
        '''Get the minimum RA.
        '''
        return self._vertices.min(axis=0)[0]

    @property
    def ra_max(self):
        '''Get the minimum RA.
        '''
        return self._vertices.max(axis=0)[0]

    @property
    def dec_min(self):
        '''Get the minimum Dec.
        '''
        return self._vertices.min(axis=0)[1]

    @property
    def dec_max(self):
        '''Get the minimum Dec.
        '''
        return self._vertices.max(axis=0)[1]

    @property
    def ra_range(self):
        '''Get the range of RA of the sweep catalog.
        '''
        return [self.ra_min, self.ra_max]

    @property
    def dec_range(self):
        '''Get the range of Dec of the sweep catalog.
        '''
        return [self.dec_min, self.dec_max]

    @property
    def columns(self):
        '''Get the list of column names of the catalog.
        '''
        return self._columns
