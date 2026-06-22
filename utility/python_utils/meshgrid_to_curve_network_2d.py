import numpy as np

def meshgrid_to_curve_network_2d(gx, gy):
    """Convert a structured meshgrid to (V, E) for polyscope curve network."""
    if gx.shape != gy.shape:
        raise ValueError("gx and gy must have identical shape")
    n_rows, n_cols = gx.shape
    V = np.column_stack((gx.ravel(), gy.ravel()))
    edges = []

    # Horizontal grid lines.
    for r in range(n_rows):
        row_start = r * n_cols
        for c in range(n_cols - 1):
            edges.append([row_start + c, row_start + c + 1])

    # Vertical grid lines.
    for r in range(n_rows - 1):
        row_start = r * n_cols
        next_row_start = (r + 1) * n_cols
        for c in range(n_cols):
            edges.append([row_start + c, next_row_start + c])

    E = np.asarray(edges, dtype=int)
    return V, E