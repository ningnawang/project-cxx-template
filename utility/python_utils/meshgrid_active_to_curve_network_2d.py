import numpy as np

def _append_cell_box(V, E, x0, y0, x1, y1):
    base = len(V)
    V.extend([
        [x0, y0],
        [x1, y0],
        [x1, y1],
        [x0, y1],
    ])
    E.extend([
        [base + 0, base + 1],
        [base + 1, base + 2],
        [base + 2, base + 3],
        [base + 3, base + 0],
    ])

def meshgrid_active_to_curve_network_2d(active_cells_mask, gx, gy):
    """Convert active-cell mask and meshgrid corners to (V,E).

    active_cells_mask uses matrix indexing: active_cells_mask[row=j, col=i].
    gx/gy must be corner grids with shape (ny+1, nx+1).
    """
    if gx.shape != gy.shape:
        raise ValueError("gx and gy must have identical shape")

    ny, nx = active_cells_mask.shape
    if gx.shape != (ny + 1, nx + 1):
        raise ValueError("gx/gy shape must be (ny+1, nx+1) matching active_cells_mask")

    # bit 0 stores "cell active" when mask is a packed bitfield.
    jj, ii = np.where((active_cells_mask & 1) > 0)
    V = []
    E = []
    for j, i in zip(jj, ii):
        x0 = gx[j, i]
        y0 = gy[j, i]
        x1 = gx[j, i + 1]
        y1 = gy[j + 1, i]
        _append_cell_box(V, E, x0, y0, x1, y1)

    if len(V) == 0:
        return np.zeros((0, 2)), np.zeros((0, 2), dtype=int)
    return np.array(V, dtype=float), np.array(E, dtype=int)