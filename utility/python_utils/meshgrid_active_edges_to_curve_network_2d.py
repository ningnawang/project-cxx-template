import numpy as np


def _append_edge(V, E, x0, y0, x1, y1):
    base = len(V)
    V.extend([[x0, y0], [x1, y1]])
    E.append([base + 0, base + 1])

# uint8
# m = active_cells_mask[j, i]  
# cell_active = (m & (1 << 0)) != 0
# bottom = (m & (1 << 1)) != 0
# right  = (m & (1 << 2)) != 0
# top    = (m & (1 << 3)) != 0
# left   = (m & (1 << 4)) != 0
def meshgrid_active_edges_to_curve_network_2d(active_cells_mask, gx, gy):
    """Convert per-cell edge bits in active_cells_mask to a unique edge curve network.

    Bit layout per cell:
      bit 1: bottom, bit 2: right, bit 3: top, bit 4: left.
    """
    if gx.shape != gy.shape:
        raise ValueError("gx and gy must have identical shape")

    ny, nx = active_cells_mask.shape
    if gx.shape != (ny + 1, nx + 1):
        raise ValueError("gx/gy shape must be (ny+1, nx+1) matching active_cells_mask")

    V = []
    E = []

    # edge_set = set()
    for j in range(ny):
        for i in range(nx):
            m = int(active_cells_mask[j, i])
            if m & (1 << 1):  # bottom
                _append_edge(V, E, gx[j, i], gy[j, i], gx[j, i + 1], gy[j, i])  # add edge to V,E
            if m & (1 << 2):  # right
                _append_edge(V, E, gx[j, i + 1], gy[j, i], gx[j + 1, i + 1], gy[j + 1, i + 1])  # add edge to V,E
            if m & (1 << 3):  # top
                _append_edge(V, E, gx[j, i], gy[j, i + 1], gx[j, i + 1], gy[j, i + 1])  # add edge to V,E
            if m & (1 << 4):  # left
                _append_edge(V, E, gx[j, i], gy[j, i], gx[j + 1, i], gy[j + 1, i])  # add edge to V,E

    if len(V) == 0:
        return np.zeros((0, 2)), np.zeros((0, 2), dtype=int)
    return np.array(V, dtype=float), np.array(E, dtype=int)
