import os
import numpy as np

def write_xyz(path, seeds, grads=None):
    """
    Save seeds (and optionally gradients) to an XYZ file.

    Args:
        path (str): output file path.
        seeds (array-like): (N, D) array, where D = 2 or 3.
        grads (array-like, optional): (N, D) array of gradients.
    """
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    seeds = np.asarray(seeds, dtype=float)

    if seeds.ndim != 2 or seeds.shape[1] not in (2, 3):
        raise ValueError(f"seeds must be Nx2 or Nx3, got shape {seeds.shape}")

    use_grads = grads is not None
    if use_grads:
        grads = np.asarray(grads, dtype=float)
        if grads.shape != seeds.shape:
            print(f"[Warning] Gradient shape {grads.shape} "
                  f"does not match seeds shape {seeds.shape}. Saving positions only.")
            use_grads = False

    # Construct header and data
    if use_grads:
        data = np.hstack([seeds, grads])
        if seeds.shape[1] == 3:
            header = "x y z gx gy gz"
        else:
            header = "x y gx gy"
    else:
        data = seeds
        header = "x y z" if seeds.shape[1] == 3 else "x y"

    np.savetxt(path, data, fmt="%.9f", header=header, comments="")
    print(f"Saved {data.shape[0]} entries to {path}")