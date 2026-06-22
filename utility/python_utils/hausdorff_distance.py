import gpytoolbox as gpy
import numpy as np

def hausdorff_distance(v1: np.ndarray,
                        f1: np.ndarray,
                        v2: np.ndarray,
                        f2: np.ndarray,
                        n: int = 200_000,
                        rng: np.random.Generator = np.random.default_rng()) -> float:
    """
    Symmetric approximate Hausdorff distance based on dense surface sampling.
    This replaces igl::hausdorff in a pure Python workflow.
    """
    if len(v1) == 0 or len(f1) == 0 or len(v2) == 0 or len(f2) == 0:
        return 1e12

    P1 = gpy.random_points_on_mesh(v1, f1, n, rng=rng)
    P2 = gpy.random_points_on_mesh(v2, f2, n, rng=rng)
    d1 = gpy.squared_distance(P1, P2, use_aabb=True, use_cpp=True)[0]
    d2 = gpy.squared_distance(P2, P1, use_aabb=True, use_cpp=True)[0]
    return float(max(np.sqrt(np.max(d1)), np.sqrt(np.max(d2))))
