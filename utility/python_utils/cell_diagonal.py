import numpy as np

# This is a direct adaptation of the C++ cell_diagonal function
def cell_diagonal(GV, resX, resY, resZ):
    min_x = np.min(GV[:, 0])
    min_y = np.min(GV[:, 1])
    min_z = np.min(GV[:, 2])

    dx = (np.max(GV[:, 0]) - min_x) / (resX - 1)
    dy = (np.max(GV[:, 1]) - min_y) / (resY - 1)
    dz = (np.max(GV[:, 2]) - min_z) / (resZ - 1)

    h = min(dx, dy, dz)
    dim_sqrt = np.sqrt(3.0)
    cell_diag = h * dim_sqrt

    return cell_diag