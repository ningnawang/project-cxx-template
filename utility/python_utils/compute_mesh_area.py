import numpy as np

def compute_mesh_area(V, F):
    """
    Compute total surface area of a triangle mesh.

    Parameters
    ----------
    V : (n, 3) numpy.ndarray
        Vertex positions.
    F : (m, 3) numpy.ndarray
        Triangle indices.

    Returns
    -------
    float
        Total surface area.
    """
    v0 = V[F[:, 0], :]
    v1 = V[F[:, 1], :]
    v2 = V[F[:, 2], :]
    cross_prod = np.cross(v1 - v0, v2 - v0)
    area = 0.5 * np.linalg.norm(cross_prod, axis=1)
    return area.sum()
