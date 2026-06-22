import numpy as np

def bbox_rec_mesh(nx,
                  ny=None,
                  nz=None,
                  type='rotationally-symmetric',
                  bbox_min=None,
                  bbox_max=None):
    """
    Tetrahedral/hex volume mesh of a cube or rectangular box.

    If bbox_min and bbox_max are provided, generate a regular mesh over the
    rectangular box [xmin,xmax] x [ymin,ymax] x [zmin,zmax]. Otherwise,
    generate the same cube mesh as regular_cube_mesh() on [0,1]^3.

    Parameters
    ----------
    nx : int
        number of vertices on the x-axis
    ny : int, optional (default None)
        number of vertices on the y-axis, default nx
    nz : int, optional (default None)
        number of vertices on the z-axis, default ny
    type : str, optional (default 'rotationally-symmetric')
        cube division scheme:
          - 'five' : 5 tets per cell
          - 'reflectionally-symmetric' : 6 tets per cell
          - 'rotationally-symmetric' (default) : 6 tets per cell
          - 'hex' : hex cells (8 verts) instead of tets
    bbox_min : (3,) array-like, optional
        [xmin, ymin, zmin]
    bbox_max : (3,) array-like, optional
        [xmax, ymax, zmax]

    Returns
    -------
    V : (N, 3) float64
        vertex list
    T : (M, 4) or (M, 8) int32
        connectivity (tets or hexes depending on `type`)
    """
    if ny is None: ny = nx
    if nz is None: nz = ny
    if nx < 2 or ny < 2 or nz < 2:
        raise ValueError("nx, ny, nz must be at least 2.")

    # Bounds: default [0,1]^3 (matches regular_cube_mesh)
    if (bbox_min is None) and (bbox_max is None):
        xmin, ymin, zmin = 0.0, 0.0, 0.0
        xmax, ymax, zmax = 1.0, 1.0, 1.0
    else:
        if (bbox_min is None) ^ (bbox_max is None):
            raise ValueError("Provide both bbox_min and bbox_max, or neither.")
        bbmin = np.asarray(bbox_min, dtype=np.float64).ravel()
        bbmax = np.asarray(bbox_max, dtype=np.float64).ravel()
        if bbmin.shape != (3,) or bbmax.shape != (3,):
            raise ValueError("bbox_min and bbox_max must be length-3.")
        if np.any(bbmin > bbmax):
            raise ValueError("bbox_min must be <= bbox_max element-wise.")
        xmin, ymin, zmin = bbmin
        xmax, ymax, zmax = bbmax

    # Map type string
    dictionary = {
        'five': 0,
        'reflectionally-symmetric': 1,
        'rotationally-symmetric': 2,
        'hex': 3
    }
    mesh_type = dictionary.get(type, -1)
    if mesh_type == -1:
        raise ValueError(f"Unknown type '{type}'. "
                         "Use 'five', 'reflectionally-symmetric', "
                         "'rotationally-symmetric', or 'hex'.")

    # Coordinate grid (keep exact indexing/order semantics)
    xs = np.linspace(xmin, xmax, nx)
    ys = np.linspace(ymin, ymax, ny)
    zs = np.linspace(zmin, zmax, nz)

    # Original uses z, x, y with indexing='ij'
    z, x, y = np.meshgrid(zs, xs, ys, indexing='ij')  # shapes: (nz, nx, ny)

    # Flatten with Fortran order to match idx layout below
    V = np.concatenate(
        (
            np.reshape(x, (-1, 1), order='F'),
            np.reshape(y, (-1, 1), order='F'),
            np.reshape(z, (-1, 1), order='F'),
        ),
        axis=1,
    ).astype(np.float64)

    # Integer index grid with same (nz, nx, ny) shape and Fortran ordering
    idx = np.arange(nx * ny * nz, dtype=np.int32).reshape((nz, nx, ny), order='F')

    # Corner indices of each cell (consistent with original function)
    v1 = np.reshape(idx[:-1, :-1, :-1], (-1, 1), order='F')
    v2 = np.reshape(idx[:-1,  1:, :-1], (-1, 1), order='F')
    v5 = np.reshape(idx[ 1:, :-1, :-1], (-1, 1), order='F')
    v6 = np.reshape(idx[ 1:,  1:, :-1], (-1, 1), order='F')
    v3 = np.reshape(idx[:-1, :-1,  1:], (-1, 1), order='F')
    v4 = np.reshape(idx[:-1,  1:,  1:], (-1, 1), order='F')
    v7 = np.reshape(idx[ 1:, :-1,  1:], (-1, 1), order='F')
    v8 = np.reshape(idx[ 1:,  1:,  1:], (-1, 1), order='F')

    # Connectivity per scheme
    if mesh_type == 0:  # five
        t1 = np.hstack((v5, v3, v2, v1))
        t2 = np.hstack((v3, v2, v8, v5))
        t3 = np.hstack((v3, v4, v8, v2))
        t4 = np.hstack((v3, v8, v7, v5))
        t5 = np.hstack((v2, v6, v8, v5))
        T = np.vstack((t1, t2, t3, t4, t5))
    elif mesh_type == 1:  # reflectionally-symmetric
        t1 = np.hstack((v3, v4, v7, v1))
        t2 = np.hstack((v4, v5, v7, v1))
        t3 = np.hstack((v4, v8, v7, v5))
        t4 = np.hstack((v2, v6, v8, v5))
        t5 = np.hstack((v4, v2, v8, v5))
        t6 = np.hstack((v4, v2, v5, v1))
        T = np.vstack((t1, t2, t3, t4, t5, t6))
    elif mesh_type == 2:  # rotationally-symmetric (default)
        t1 = np.hstack((v1, v3, v7, v8))
        t2 = np.hstack((v1, v8, v7, v5))
        t3 = np.hstack((v1, v3, v8, v4))
        t4 = np.hstack((v1, v4, v8, v2))
        t5 = np.hstack((v1, v6, v8, v5))
        t6 = np.hstack((v1, v2, v8, v6))
        T = np.vstack((t1, t2, t3, t4, t5, t6))
    elif mesh_type == 3:  # hex (Polyscope's ordering convention)
        T = np.hstack((v1, v2, v4, v3, v5, v6, v8, v7))

    return V, T.astype(np.int32, copy=False)
