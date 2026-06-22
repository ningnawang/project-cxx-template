import trimesh
from typing import Union

MeshLike = Union[str, "trimesh.Trimesh", "trimesh.Scene"]


def ensure_trimesh(path_or_mesh: MeshLike, process: bool = True) -> "trimesh.Trimesh":
    """
    Load a mesh from path or accept an existing mesh/scene.
    Triangulation/repairs are handled by trimesh for proximity queries.
    """
    m = path_or_mesh
    if not hasattr(m, "vertices"):   # assume it's a path
        m = trimesh.load(path_or_mesh, force="mesh", process=process)
    if isinstance(m, trimesh.Scene):
        m = m.to_mesh()
    if not isinstance(m, trimesh.Trimesh):
        raise TypeError("Input must resolve to a trimesh.Trimesh or a path loadable as one.")
    if process:
        # Keep the mesh geometry as-is (open/non-manifold ok), just ensure coherence
        m.remove_unreferenced_vertices()
        m.fix_normals()
    return m
