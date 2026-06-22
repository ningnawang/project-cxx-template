import numpy as np


def meshgrid_to_curve_network_3d(gx, gy, gz):
    """Convert grid edges to a unique 3D edge network.
    gx/gy/gz shape: (resX+1, resY+1, resZ+1), same indexing='ij' convention.
    """
    if gx.shape != gy.shape or gx.shape != gz.shape:
        raise ValueError("gx, gy, gz must have identical shape")

    res_x, res_y, res_z = gx.shape[0] - 1, gy.shape[1] - 1, gz.shape[2] - 1
    if gx.shape != (res_x + 1, res_y + 1, res_z + 1):
        raise ValueError(
            "gx/gy/gz shape must be (resX+1, resY+1, resZ+1) matching active_cells_mask"
        )

    # Global grid vertices in row-first (i, j, k).
    V_all = np.column_stack((gx.ravel(), gy.ravel(), gz.ravel()))
    n_y = gx.shape[1]
    n_z = gx.shape[2]

    def vid(i, j, k):
        return (i * n_y + j) * n_z + k

    edge_set = set()
    for i in range(res_x):
        for j in range(res_y):
            for k in range(res_z):
                c0 = vid(i, j, k)
                c1 = vid(i + 1, j, k)
                c2 = vid(i + 1, j + 1, k)
                c3 = vid(i, j + 1, k)
                c4 = vid(i, j, k + 1)
                c5 = vid(i + 1, j, k + 1)
                c6 = vid(i + 1, j + 1, k + 1)
                c7 = vid(i, j + 1, k + 1)
                edge_set.update([(c0, c1), (c1, c2), (c2, c3), (c3, c0), (c4, c5), (c5, c6), (c6, c7), (c7, c4), (c0, c4), (c1, c5), (c2, c6), (c3, c7)])

    if len(edge_set) == 0:
        return np.zeros((0, 3)), np.zeros((0, 2), dtype=int)
    E = np.array(list(edge_set), dtype=int)
    V = V_all
    return V.astype(float), E
   
