import numpy as np


def meshgrid_active_edges_to_curve_network_3d(active_cells_mask, gx, gy, gz):
    """Convert per-cell edge bits in active_cells_mask to a unique 3D edge network.

    Conventions:
    - active_cells_mask shape: (resX, resY, resZ), indexed as (i, j, k).
    - gx/gy/gz shape: (resX+1, resY+1, resZ+1), same indexing='ij' convention.
    - Bit layout per cell:
      bit 0: cell active
      bit 1: edge (0-1)
      bit 2: edge (1-2)
      bit 3: edge (2-3)
      bit 4: edge (3-0)
      bit 5: edge (4-5)
      bit 6: edge (5-6)
      bit 7: edge (6-7)
      bit 8: edge (7-4)
      bit 9: edge (0-4)
      bit 10: edge (1-5)
      bit 11: edge (2-6)
      bit 12: edge (3-7)
    """
    if gx.shape != gy.shape or gx.shape != gz.shape:
        raise ValueError("gx, gy, gz must have identical shape")
    if active_cells_mask.ndim != 3:
        raise ValueError("active_cells_mask must be a 3D array")

    res_x, res_y, res_z = active_cells_mask.shape
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
                m = int(active_cells_mask[i, j, k])
                if m == 0:
                    continue

                c0 = vid(i, j, k)
                c1 = vid(i + 1, j, k)
                c2 = vid(i + 1, j + 1, k)
                c3 = vid(i, j + 1, k)
                c4 = vid(i, j, k + 1)
                c5 = vid(i + 1, j, k + 1)
                c6 = vid(i + 1, j + 1, k + 1)
                c7 = vid(i, j + 1, k + 1)

                if m & (1 << 1):
                    edge_set.add((min(c0, c1), max(c0, c1)))
                if m & (1 << 2):
                    edge_set.add((min(c1, c2), max(c1, c2)))
                if m & (1 << 3):
                    edge_set.add((min(c2, c3), max(c2, c3)))
                if m & (1 << 4):
                    edge_set.add((min(c3, c0), max(c3, c0)))
                if m & (1 << 5):
                    edge_set.add((min(c4, c5), max(c4, c5)))
                if m & (1 << 6):
                    edge_set.add((min(c5, c6), max(c5, c6)))
                if m & (1 << 7):
                    edge_set.add((min(c6, c7), max(c6, c7)))
                if m & (1 << 8):
                    edge_set.add((min(c7, c4), max(c7, c4)))
                if m & (1 << 9):
                    edge_set.add((min(c0, c4), max(c0, c4)))
                if m & (1 << 10):
                    edge_set.add((min(c1, c5), max(c1, c5)))
                if m & (1 << 11):
                    edge_set.add((min(c2, c6), max(c2, c6)))
                if m & (1 << 12):
                    edge_set.add((min(c3, c7), max(c3, c7)))

    if len(edge_set) == 0:
        return np.zeros((0, 3)), np.zeros((0, 2), dtype=int)

    # Compact vertex indexing: keep only endpoints used by active edges.
    edges_old = sorted(edge_set)
    used_old_vids = sorted({vid for e in edges_old for vid in e})
    old_to_new = {old_vid: new_vid for new_vid, old_vid in enumerate(used_old_vids)}

    V = V_all[np.array(used_old_vids, dtype=int)]
    E = np.array(
        [[old_to_new[a], old_to_new[b]] for (a, b) in edges_old], dtype=int
    )
    return V.astype(float), E
   
