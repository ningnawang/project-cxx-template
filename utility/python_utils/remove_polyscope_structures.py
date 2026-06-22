import polyscope as ps

def remove_curve_network(name):
    if ps.has_curve_network(name):
        try:
            ps.remove_curve_network(name)
        except Exception:
            # print(f"unable to remove point cloud {name}")
            pass
def remove_point_cloud(name):
    if ps.has_point_cloud(name):
        try:
            ps.remove_point_cloud(name)
        except Exception:
            # print(f"unable to remove point cloud {name}")
            pass
def remove_surface_mesh(name):
    if ps.has_surface_mesh(name):
        try:
            ps.remove_surface_mesh(name)
        except Exception:
            # print(f"unable to remove surface mesh {name}")
            pass