import numpy as np

# the order of vertices/edges are re-sorted, 
# so NOT really comply to the convension in grid_activation_pipeline_3d.h
def meshgrid_active_to_curve_network_3d(active_cells_mask, gx, gy, gz):
    """Convert per-cell edge bits in active_cells_mask to a unique 3D edge network.

    Conventions:
    - active_cells_mask shape: (resX, resY, resZ), indexed as (i, j, k).
    - gx/gy/gz shape: (resX+1, resY+1, resZ+1), same indexing='ij' convention.
    - Bit layout per cell:
      bit 0: cell active
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
                edge_set.update([(c0, c1), (c1, c2), (c2, c3), (c3, c0), (c4, c5), (c5, c6), (c6, c7), (c7, c4), (c0, c4), (c1, c5), (c2, c6), (c3, c7)])
                
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
   
