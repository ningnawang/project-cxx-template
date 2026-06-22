import numpy as np

# pts are query points in a numpy array of shape (N,2) or (N,3)
def grad_finite_diffs(func, pts, dx=1e-6, dy=1e-6, dz=1e-6):
    pts = np.asarray(pts, dtype=float)
    if pts.ndim == 1:
        pts = pts.reshape(1, -1)
    if pts.ndim != 2 or pts.shape[1] not in (2, 3):
        raise ValueError("pts must have shape (N,2) or (N,3)")

    dim = pts.shape[1]

    # Compute central finite differences
    gradx = (func(pts + np.array([dx] + [0.0] * (dim - 1))) -
             func(pts - np.array([dx] + [0.0] * (dim - 1)))) / (2 * dx)
    grady = (func(pts + np.array([0.0, dy] + [0.0] * (dim - 2))) -
             func(pts - np.array([0.0, dy] + [0.0] * (dim - 2)))) / (2 * dy)

    if dim == 3:
        gradz = (func(pts + np.array([0.0, 0.0, dz])) -
                 func(pts - np.array([0.0, 0.0, dz]))) / (2 * dz)
        grad_vals = np.stack([gradx, grady, gradz], axis=-1).reshape(-1, 3)
    else:
        grad_vals = np.stack([gradx, grady], axis=-1).reshape(-1, 2)

    # Normalize
    norms = np.linalg.norm(grad_vals, axis=1, keepdims=True)
    pos_norms = norms.squeeze() > 0
    grad_vals[pos_norms] /= norms[pos_norms]
    if not np.all(pos_norms):
        grad_vals[~pos_norms] = 0.0

    return grad_vals if grad_vals.shape[0] > 1 else grad_vals[0]
