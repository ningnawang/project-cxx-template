import numpy as np

# counter-clockwise rotation of 2D points by a given angle (in degrees)
def rotate_mesh(v, angle = 5.0):
    if angle == 0.0:
        return v
    theta = np.radians(angle)
    c, s = np.cos(theta), np.sin(theta)
    R = np.array([[c, -s], [s, c]])

    v = np.atleast_2d(v) # at least 2 dimension
    rotated_v = v @ R.T
    return rotated_v