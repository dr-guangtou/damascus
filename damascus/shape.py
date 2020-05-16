# Licensed under MIT license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""Shape related functions."""

import numpy as np

from scipy.spatial import Delaunay
from scipy.spatial import ConvexHull

__all__ = ['alpha_shape', 'convex_hull', 'concave_hull']


def convex_hull(points):
    ''' Get the convex hull edges for a set of points.

    Parameters
    ----------
    points: `np.array` of shape (n,2) points
         Coordinates of the points.

    Returns
    -------
    edges: `np.array` of shape (n,2) points
        List of indices for boundary points.

    '''
    hull = ConvexHull(points)
    return np.vstack([points[hull.vertices, 0], points[hull.vertices, 1]]).T


def concave_hull(points, **kwargs):
    ''' Get the concave hull edges for a set of points.

    Parameters
    ----------
    points: `np.array` of shape (n,2) points
         Coordinates of the points.

    Returns
    -------
    edges: `np.array` of shape (n,2) points
        List of indices for boundary points.

    '''
    edges = np.asarray(alpha_shape(points, **kwargs)[0])
    return np.vstack([points[edges[:, 0], 0], points[edges[:, 1], 1]]).T


def alpha_shape(points, alpha, only_outer=True):
    '''Compute the alpha shape (concave hull) of a set of points.

    Parameters
    ----------
    points: np.array of shape (n,2) points
         Coordinates of the points.
    alpha: float
         Alpha parameter to control the behaviour of the concave hull.
    only_outer: bool, optional
         If we keep only the outer border or also the inner edges.
         Default: True

    Returns
    -------
    boundary_lst: list
        List of indices for boundary points.

    Notes
    -----
        From a StackOverflow answer by Iddo Hanniel:
        https://stackoverflow.com/questions/23073170/calculate-bounding-polygon-of-alpha-shape-from-the-delaunay-triangulation

    '''
    assert points.shape[0] > 3, "Need at least four points"

    def add_edge(edges, i, j):
        """
        Add a line between the i-th and j-th points,
        if not in the list already
        """
        if (i, j) in edges or (j, i) in edges:
            # Already added
            assert (j, i) in edges, "Can't go twice over same directed edge right?"
            if only_outer:
                # If both neighboring triangles are in shape, it's not a boundary edge
                edges.remove((j, i))
            return
        edges.add((i, j))

    tri = Delaunay(points)
    edges = set()
    # Loop over triangles:
    # ia, ib, ic = indices of corner points of the triangle
    for ia, ib, ic in tri.vertices:
        pa = points[ia]
        pb = points[ib]
        pc = points[ic]
        # Computing radius of triangle circumcircle
        a = np.sqrt((pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2)
        b = np.sqrt((pb[0] - pc[0]) ** 2 + (pb[1] - pc[1]) ** 2)
        c = np.sqrt((pc[0] - pa[0]) ** 2 + (pc[1] - pa[1]) ** 2)
        s = (a + b + c) / 2.0
        area = np.sqrt(s * (s - a) * (s - b) * (s - c))
        circum_r = a * b * c / (4.0 * area)
        if circum_r < alpha:
            add_edge(edges, ia, ib)
            add_edge(edges, ib, ic)
            add_edge(edges, ic, ia)

    return _stitch_boundaries(edges)

def _find_edges_with(i, edge_set):
    i_first = [j for (x, j) in edge_set if x==i]
    i_second = [j for (j, x) in edge_set if x==i]
    return i_first, i_second

def _stitch_boundaries(edges):
    """Stitches the output edge set into sequences of consecutive edges.

    Parameters
    ----------
    edges: set
         Set of (i,j) pairs representing edges of the alpha-shape. (i,j) are
         the indices in the points array.

    Returns
    -------
    boundary_lst: list
        List of indices for boundary points.

    Notes
    -----
        From a StackOverflow answer by Iddo Hanniel:
        https://stackoverflow.com/questions/50549128/boundary-enclosing-a-given-set-of-points

    """
    edge_set = edges.copy()
    boundary_lst = []
    while edge_set:
        boundary = []
        edge0 = edge_set.pop()
        boundary.append(edge0)
        last_edge = edge0
        while edge_set:
            _, j = last_edge
            j_first, j_second = _find_edges_with(j, edge_set)
            if j_first:
                edge_set.remove((j, j_first[0]))
                edge_with_j = (j, j_first[0])
                boundary.append(edge_with_j)
                last_edge = edge_with_j
            elif j_second:
                edge_set.remove((j_second[0], j))
                edge_with_j = (j, j_second[0])  # flip edge rep
                boundary.append(edge_with_j)
                last_edge = edge_with_j
            if edge0[0] == last_edge[1]:
                break
        boundary_lst.append(boundary)

    return boundary_lst
