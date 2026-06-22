import numpy as np

# same order as 
def meshgrid_single_cell_to_curve_network_3d(cell_i, cell_j, cell_k, gx, gy, gz):
    """Return one cell as a curve network with canonical corner ordering.

    Corner order matches grid_activation_pipeline_3d.cpp:
      c0=(xmin, ymin, zmin)
      c1=(xmax, ymin, zmin)
      c2=(xmax, ymax, zmin)
      c3=(xmin, ymax, zmin)
      c4=(xmin, ymin, zmax)
      c5=(xmax, ymin, zmax)
      c6=(xmax, ymax, zmax)
      c7=(xmin, ymax, zmax)
    """
    if gx.shape != gy.shape or gx.shape != gz.shape:
        raise ValueError("gx, gy, gz must have identical shape")
    if gx.ndim != 3:
        raise ValueError("gx, gy, gz must be 3D arrays")

    res_x, res_y, res_z = gx.shape[0] - 1, gx.shape[1] - 1, gx.shape[2] - 1
    if not (0 <= cell_i < res_x and 0 <= cell_j < res_y and 0 <= cell_k < res_z):
        raise ValueError("cell index out of range")

    V = np.array(
        [
            [gx[cell_i, cell_j, cell_k], gy[cell_i, cell_j, cell_k], gz[cell_i, cell_j, cell_k]],
            [gx[cell_i + 1, cell_j, cell_k], gy[cell_i + 1, cell_j, cell_k], gz[cell_i + 1, cell_j, cell_k]],
            [gx[cell_i + 1, cell_j + 1, cell_k], gy[cell_i + 1, cell_j + 1, cell_k], gz[cell_i + 1, cell_j + 1, cell_k]],
            [gx[cell_i, cell_j + 1, cell_k], gy[cell_i, cell_j + 1, cell_k], gz[cell_i, cell_j + 1, cell_k]],
            [gx[cell_i, cell_j, cell_k + 1], gy[cell_i, cell_j, cell_k + 1], gz[cell_i, cell_j, cell_k + 1]],
            [gx[cell_i + 1, cell_j, cell_k + 1], gy[cell_i + 1, cell_j, cell_k + 1], gz[cell_i + 1, cell_j, cell_k + 1]],
            [gx[cell_i + 1, cell_j + 1, cell_k + 1], gy[cell_i + 1, cell_j + 1, cell_k + 1], gz[cell_i + 1, cell_j + 1, cell_k + 1]],
            [gx[cell_i, cell_j + 1, cell_k + 1], gy[cell_i, cell_j + 1, cell_k + 1], gz[cell_i, cell_j + 1, cell_k + 1]],
        ],
        dtype=float,
    )

    E = np.array(
        [
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 0],
            [4, 5],
            [5, 6],
            [6, 7],
            [7, 4],
            [0, 4],
            [1, 5],
            [2, 6],
            [3, 7],
        ],
        dtype=int,
    )

    return V, E
