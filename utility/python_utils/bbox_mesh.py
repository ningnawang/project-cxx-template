import numpy as np

def bbox_mesh(nx, ny=None, bbox_min=None, bbox_max=None):
    """
    Triangle mesh of a square/rectangle.

    If bbox_min and bbox_max are given, generate a regular triangular mesh of
    the rectangle [xmin,xmax] x [ymin,ymax]. Otherwise, generate the same
    square mesh as regular_square_mesh() on [-1,1] x [-1,1].

    Parameters
    ----------
    nx : int
        Number of vertices along x.
    ny : int, optional (default None)
        Number of vertices along y. Defaults to nx.
    bbox_min : array-like of length 2, optional
        [xmin, ymin]. If None, defaults to [-1, -1].
    bbox_max : array-like of length 2, optional
        [xmax, ymax]. If None, defaults to [ 1,  1].

    Returns
    -------
    V : (nx*ny, 2) float64
        Vertex coordinates.
    F : (2*(nx-1)*(ny-1), 3) int32
        Triangle vertex indices into V.

    Notes
    -----
    - Vertex ordering increases by rows (y) then columns (x):
      (x0,y0), (x1,y0), ..., (x_{nx-1},y0), (x0,y1), ...
    - Each grid cell is split into two triangles with a consistent diagonal.
    """
    if ny is None:
        ny = nx
    if nx < 2 or ny < 2:
        raise ValueError("nx and ny must be at least 2.")

    # Decide bounds: provided bbox or the default [-1, 1]^2
    if bbox_min is None or bbox_max is None:
        xmin, ymin = -1.0, -1.0
        xmax, ymax =  1.0,  1.0
    else:
        bbmin = np.asarray(bbox_min, dtype=np.float64).ravel()
        bbmax = np.asarray(bbox_max, dtype=np.float64).ravel()
        if bbmin.shape != (2,) or bbmax.shape != (2,):
            raise ValueError("bbox_min and bbox_max must be length-2.")
        if np.any(bbmin > bbmax):
            raise ValueError("bbox_min must be <= bbox_max element-wise.")
        xmin, ymin = bbmin
        xmax, ymax = bbmax

    xs = np.linspace(xmin, xmax, nx)
    ys = np.linspace(ymin, ymax, ny)
    X, Y = np.meshgrid(xs, ys)  # shapes: (ny, nx)

    V = np.stack([X.ravel(), Y.ravel()], axis=-1).astype(np.float64)

    # Cell indexing (two triangles per quad)
    inds = np.arange(nx * ny, dtype=np.int32).reshape(ny, nx)
    i0 = inds[:-1, :-1].ravel()
    i1 = inds[:-1,  1:].ravel()
    i2 = inds[ 1:, :-1].ravel()
    i3 = inds[ 1:,  1:].ravel()

    F = np.stack(
        (
            np.concatenate([i0, i0]),
            np.concatenate([i3, i1]),
            np.concatenate([i2, i3]),
        ),
        axis=-1,
    ).astype(np.int32)

    return V, F
