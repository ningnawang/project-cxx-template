import numpy as np

def scale_vertices_to_cube(
    V: np.ndarray,
    cube_min: float = -1.0,
    cube_max: float = 1.0,
    scale_buffer: float = 0.9,
) -> np.ndarray:
    """
    Load a mesh vertex set, then scale + recenter it to fit inside [cube_min, cube_max]^3.
    If scale_buffer != 1.0, then the shape fit [cube_min*scale_buffer, cube_min*scale_buffer]^3.
    Uniform scaling uses the largest extent to preserve aspect ratio.
    """
    V = np.asarray(V, dtype=np.float64)
    cube_min *= scale_buffer
    cube_max *= scale_buffer
    bounds = np.array([V.min(axis=0), V.max(axis=0)])  # shape (2, 3)
    extents = bounds[1] - bounds[0]
    max_extent = float(extents.max())
    if max_extent <= 0:
        raise ValueError("Mesh has zero extent; cannot scale into a cube.")

    target_extent = cube_max - cube_min
    if target_extent <= 0:
        raise ValueError("cube_max must be greater than cube_min.")

    center = (bounds[1] + bounds[0]) * 0.5
    scale = target_extent / max_extent
    cube_center = (cube_min + cube_max) * 0.5
    V = (V - center) * scale + cube_center

    return V