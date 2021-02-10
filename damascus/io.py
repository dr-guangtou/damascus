# Licensed under MIT license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""Functions to deal with file i/o."""

import os
import glob
import pickle

import numpy as np

import healpy

__all__ = ['read_healpix_fits', 'find_files', 'save_to_pickle', 'read_from_pickle']

def read_healpix_fits(fits_file, nest=True):
    """Read the FITS format healpix file."""
    return healpy.read_map(fits_file, nest=nest, dtype=np.bool)

def find_files(loc, pattern, verbose=True):
    """Gather a list of pathes to all SWEEP catalogs."""
    if loc[-1] != '/':
        loc += '/'

    file_list = glob.glob(loc + pattern)
    if verbose:
        print("# Find {:d} {:s} files".format(len(file_list), pattern))
    return file_list

def save_to_pickle(obj, name):
    '''Save a data structure to pickle file.

    Parameters
    ----------
    obj: Python object
        Data to save. Can be numpy array or dictionary.
    name: string
        File name for pickle file.

    Returns
    -------

    '''
    output = open(name, 'wb')
    pickle.dump(obj, output, protocol=2)
    output.close()

def read_from_pickle(name, py2=False):
    ''' Read data from pickle file.

    Parameters
    ----------
    name: string
        File name for pickle file.

    Returns
    -------
    obj: Python object
        Data to save. Can be numpy array or dictionary.

    Notes
    -----
        About how to unpickling Python 2 object in Python 3, please see
        this StackOverflow post: 
            https://stackoverflow.com/questions/28218466/unpickling-a-python-2-object-with-python-3


    '''
    if py2:
        return pickle.load(open(name, "rb"), encoding='latin1')
    return pickle.load(open(name, "rb"))
