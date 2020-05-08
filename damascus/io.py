# Licensed under MIT license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""Functions to deal with file i/o."""

import os
import glob

import numpy as np

import healpy

__all__ = ['read_healpix_fits', 'find_files']

def read_healpix_fits(fits_file, nest=True):
    """Read the FITS format healpix file."""
    return healpy.read_map(fits_file, nest=nest, dtype=np.bool)

def find_files(loc, pattern, verbose=True):
    """Gather a list of pathes to all SWEEP catalogs."""
    if loc[-1] is not '/':
        loc += '/'

    file_list = glob.glob(loc + pattern)
    if verbose:
        print("# Find {:d} {:s} files".format(len(file_list), pattern))
    return file_list
