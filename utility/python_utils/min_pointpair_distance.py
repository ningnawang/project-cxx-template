import numpy as np
from scipy.spatial import cKDTree

def min_pointpair_distance(V: np.ndarray) -> float:
    """
    Compute the minimum Euclidean distance between any two points in V.

    Parameters
    ----------
    V : (n, d) float ndarray
        Input point coordinates.

    Returns
    -------
    float
        Minimum distance between any pair of points.
    """
    if V.shape[0] < 2:
        return 0.0

    # Build KD-tree
    tree = cKDTree(V)

    # Query nearest neighbor for each point (k=2: itself + nearest)
    dists, idxs = tree.query(V, k=2)

    # dists[:, 0] is zero (self), so use dists[:, 1]
    return float(np.min(dists[:, 1]))
