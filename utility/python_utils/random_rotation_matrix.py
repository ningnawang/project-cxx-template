
import numpy as np

def axis_angle_rotation_matrix(axis, angle):
    """
    Rodrigues' rotation formula
    axis: (3,)
    angle: scalar (radians)
    """
    axis = axis / np.linalg.norm(axis)
    x, y, z = axis
    c = np.cos(angle)
    s = np.sin(angle)
    C = 1.0 - c

    R = np.array([
        [c + x*x*C,     x*y*C - z*s, x*z*C + y*s],
        [y*x*C + z*s,   c + y*y*C,   y*z*C - x*s],
        [z*x*C - y*s,   z*y*C + x*s, c + z*z*C]
    ])
    return R


def random_rotation_matrix(rot_seed=None, rot_angle=None):
    if rot_seed is not None:
        np.random.seed(rot_seed)

    axis = np.random.rand(3)
    axis = axis / np.linalg.norm(axis)

    if rot_angle is None:
        angle = np.random.uniform(0.0, 2.0 * np.pi)
    else:
        angle = np.radians(rot_angle)

    print(f"pick rotation axis {axis} and angle {angle}")
    return axis_angle_rotation_matrix(axis, angle)
