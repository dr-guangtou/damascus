# Licensed under MIT license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""Functions to deal with specific HSC data."""

import numpy as np

import healpy as hp

from astropy.io import fits

from sklearn.cluster import DBSCAN
from sklearn.neighbors import KDTree

from . import io
from . import shape

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
    nside, hp_indices = hp.get_nside(fdfc_mask), np.where(fdfc_mask)[0]
    phi, theta = np.radians(cat[ra]), np.radians(90. - cat[dec])
    hp_masked = hp.ang2pix(nside, theta, phi, nest=True)
    select = np.in1d(hp_masked, hp_indices)

    if verbose:
        print("# Find {:d} objects inside the FDFC region".format(select.sum()))

    if select.sum() < 1:
        return None
    return cat[select]

def get_fdfc_borders(healpix_mask, nest=False, n_samples=10000,
                     distance=1.0, use_boundary=True, alpha=0.1,
                     verbose=True):
    """Get the outer borders of each field in the FDFC region."""
    # Read in the healpix mask and get the NSIDE and pixel indices.
    mask = hp.read_map(healpix_mask, nest=nest)
    nside, hp_indices = hp.get_nside(mask), np.where(mask)[0]

    # Get the pixel coordinate information.
    if not use_boundary:
        ra, dec = hp.pixelfunc.pix2ang(nside, hp_indices, lonlat=True)
    else:
        # Use pixel boundary
        bounds = hp.boundaries(nside, hp_indices, step=1, nest=nest)
        ra, dec = hp.pixelfunc.vec2ang(np.hstack(bounds).T, lonlat=True)

    # Select a small sample for training clustering model
    mask = np.random.random(size=len(ra)) < n_samples / len(ra)

    # Find continous regions in (ra, dec) space
    field = DBSCAN(eps=distance).fit_predict(
        np.vstack((ra[mask], dec[mask])).T)

    # ID of unique fields
    field_unique = np.unique(field)
    if verbose:
        print("# Find {:d} unique continous fields".format(len(field_unique)))

    # Transfer the field label to all coordinates
    tree = KDTree(np.vstack((ra[mask], dec[mask])).T, leaf_size=2)
    field_all = field[
        tree.query(np.vstack((ra, dec)).T, k=1,
                   return_distance=False).flatten()]

    # Go through each field and get the borders.
    borders = {}
    for field_id in field_unique:
        region = (field_all == field_id)

        # Get the sorted edge coordinates of a concave hull of the points.
        # This is based on the vertices of Delaunay triangulation.
        edges = shape.alpha_shape(np.vstack([ra[region], dec[region]]).T, alpha=alpha)

        borders[field_id + 1] = np.vstack(
            [ra[region][np.asarray(edges[0])[:, 0]],
             dec[region][np.asarray(edges[0])[:, 1]]]).T

    return borders
