import numpy as np

def extract_vertex_face_given_mesh_and_fid(V_pd, F_pd, given_fid):
    """
    Extract a single-triangle mesh from global V/F by face id.

    Args:
        V_pd: (N, 3) numpy array of vertices
        F_pd: (M, 3) numpy array of triangle indices
        given_fid: int, target face id

    Returns:
        V_out: (3, 3) numpy array, local vertices of the triangle
        F_out: (1, 3) numpy array, local face indices [[0,1,2]]
        global_vids: (3,) numpy array, original vertex ids in V_pd
    """
    if given_fid < 0 or given_fid >= F_pd.shape[0]:
        raise IndexError(f"given_fid={given_fid} is out of range [0, {F_pd.shape[0] - 1}]")

    face = F_pd[given_fid]
    global_vids = np.asarray(face, dtype=int)

    if global_vids.ndim != 1:
        raise ValueError("F_pd[given_fid] must be a 1D list/array of vertex ids")

    V_out = V_pd[global_vids].copy()
    F_out = [list(range(len(global_vids)))]

    return V_out, F_out