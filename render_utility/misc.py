import sys
import os
import numpy as np
import blendertoolbox as bt
import math
import bmesh
import bpy
from .definitions import *

def setup_scene(cam_location=(0.0, -2.1, 0.5),cam_rotations=(75, 0, 0),focal_length = 50, shadowcatcher_height = -0.35, shadow_alpha_thres = 0, fast = True, imgRes_x = 1080, imgRes_y = 1080,
                energy_lights = [100, 50, 20]):

    div_samples = 1
    div_res = 1
    if fast:
        div_samples = 10 # render it faster for iterating
        div_res = 4
    imgRes_x = imgRes_x // div_res
    imgRes_y = imgRes_y // div_res

    numSamples = 1000 // div_samples
    exposure = 1.25 


    bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

    # set invisible plane (shadow catcher)
    if shadowcatcher_height is not None:
        bt.invisibleGround(shadowBrightness=0.9,location=(0,0,shadowcatcher_height))

    # keep shadow catcher alpha clean
    bpy.context.view_layer.cycles.use_denoising = True

    cam = bt.setCamera_from_UI(cam_location, cam_rotations, focalLength = focal_length)

    # ## set light
    # ## Option1: Three Point Light System 
    sun = None
    # this setup is good if we use the default cam_location and cam_rotations
    bpy.ops.object.light_add(type='AREA', radius=1, location=(-1.25, -1.25, 1))
    keylight = bpy.context.object
    keylight.rotation_euler = (math.radians(40), math.radians(-50), math.radians(0))
    bpy.context.object.data.shape = 'DISK'
    bpy.context.object.data.energy = energy_lights[0]
    bpy.ops.object.light_add(type='AREA', radius=1, location=(1.25, -1.25, 1))
    keylight = bpy.context.object
    keylight.rotation_euler = (math.radians(40), math.radians(50), math.radians(0))
    bpy.context.object.data.shape = 'DISK'
    bpy.context.object.data.energy = energy_lights[1]
    bpy.ops.object.light_add(type='AREA', radius=1, location=(-1.25, 1.25, 1))
    keylight = bpy.context.object
    keylight.rotation_euler = (math.radians(-40), math.radians(-50), math.radians(0))
    bpy.context.object.data.shape = 'DISK'
    bpy.context.object.data.energy = energy_lights[2]

    ## set ambient light
    bt.setLight_ambient(color=(0.5,0.5,0.5,1)) 

    ## if shadow_alpha_thres > 0,
    ## set gray shadow to completely white with a threshold (optional but recommended)
    bt.shadowThreshold(alphaThreshold = shadow_alpha_thres, interpolationMode = 'CARDINAL')
    return cam, sun

def plot_mesh(path_to_mesh, color=superpower_color, wireframe=None,
    location=(0,0,0), rotation=(0,0,0), scale=(1,1,1), smooth_shading = False, sbd = 0):
    mesh = bt.readMesh(path_to_mesh, location, rotation, scale=scale)
    AOStrength = 1.0
    if wireframe is None:
        meshcolor = bt.colorObj(color, 0.5, 0.9, 0.8, 0.0, 0.0)
        bt.setMat_plastic(mesh, meshcolor)
    else:
        edgeColor = bt.colorObj((0,0,0,0),0.5, 1.0, 1.0, 0.0, 0.0)
        bt.setMat_edge(mesh, wireframe, edgeColor, color, AOStrength)

    if smooth_shading:
        for f in mesh.data.polygons:
            f.use_smooth = True
    if sbd>0:
        bt.subdivision(mesh, level = sbd)


    return mesh

def plot_gt_mesh(path_to_mesh, wireframe=None,
    location=(0,0,0), rotation=(0,0,0), scale=(1,1,1)):
    return plot_mesh(path_to_mesh, color=input_mesh_color, wireframe=wireframe,
        location=location, rotation=rotation, scale=scale)

def save_file(filename):
    bpy.ops.wm.save_mainfile(filepath=filename)

def render_image(filename, cam):
    bt.renderImage(filename, cam)

def plot_point_cloud(path,radius=0.003,color=superpower_color,rotation=(0,0,0)):
    mesh = bt.readMesh(path, (0,0,0), rotation, scale=(1,1,1))
    # # set material 
    ptColor = bt.colorObj(color, 0.5, 1.3, 1.0, 0.0, 0.0)
    ptSize = radius
    bt.setMat_pointCloud(mesh, ptColor, ptSize)
    return mesh

# def plot_spheres(path_to_mesh, color=positive_sphere_color,
#     location=(0,0,0), rotation=(90,0,0), scale=(1,1,1)):
#     mesh = bt.readMesh(path_to_mesh,
#         location=location, rotation=rotation, scale=scale)
#     transparency = 0.5
#     transmission = 0.5
#     bt.setMat_transparent(mesh, color, transparency, transmission)
#     for f in mesh.data.polygons:
#         f.use_smooth = True
#     return mesh


def shade_auto_smooth(
    obj,
    *,
    angle_deg: float = 30.0,
    exclude_negative: bool = True,
    sharp_nonmanifold: bool = True,
    sharp_boundary: bool = True,
    make_faces_smooth: bool = True,
):
    """
    Custom "shade auto smooth":
      - Marks an edge as SMOOTH only if its signed dihedral angle is in [0, angle_deg]
        (or [-angle_deg, angle_deg] if exclude_negative=False).
      - Marks all other edges SHARP.
      - Optionally marks non-manifold/boundary edges sharp.
      - Enables mesh auto-smooth so sharp edges actually split normals.

    Parameters
    ----------
    obj : bpy.types.Object
        Mesh object to modify (e.g. returned by plot_mesh()).
    angle_deg : float
        Smoothing threshold in degrees.
    exclude_negative : bool
        If True, concave edges (negative signed dihedral) will be sharp even if small magnitude.
    sharp_nonmanifold : bool
        If True, edges with >2 linked faces are marked sharp.
    sharp_boundary : bool
        If True, boundary/loose edges (<2 linked faces) are marked sharp.
    make_faces_smooth : bool
        If True, sets all faces to smooth shading (edge sharpness controls splits).

    Returns
    -------
    dict with counts for debugging.
    """
    if obj is None or obj.type != 'MESH':
        raise TypeError("shade_auto_smooth expects a mesh Object (bpy.types.Object with type == 'MESH').")

    me = obj.data
    angle_rad = math.radians(angle_deg)

    # Work in object mode data (this is what you want for scripted/offscreen renders)
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.faces.ensure_lookup_table()
    bm.edges.ensure_lookup_table()

    if make_faces_smooth:
        for f in bm.faces:
            f.smooth = True

    n_smooth = 0
    n_sharp = 0
    n_boundary = 0
    n_nonmanifold = 0

    for e in bm.edges:
        lf = e.link_faces
        if len(lf) == 2:
            # Signed dihedral: negative typically concave, positive typically convex
            a = e.calc_face_angle_signed()  # radians, [-pi, pi]

            if exclude_negative:
                # Smooth only if convex-ish and below threshold
                is_smooth = (a >= 0.0) and (a <= angle_rad)
            else:
                # Smooth if magnitude is below threshold (classic behavior)
                is_smooth = abs(a) <= angle_rad

            e.smooth = bool(is_smooth)   # True => smooth across edge, False => sharp edge
            if is_smooth:
                n_smooth += 1
            else:
                n_sharp += 1

        elif len(lf) < 2:
            n_boundary += 1
            e.smooth = not sharp_boundary  # boundary edges often look better sharp
            if e.smooth:
                n_smooth += 1
            else:
                n_sharp += 1

        else:  # >2 faces
            n_nonmanifold += 1
            e.smooth = not sharp_nonmanifold
            if e.smooth:
                n_smooth += 1
            else:
                n_sharp += 1

    # Write back
    bm.to_mesh(me)
    bm.free()
    me.update()

    # Enable auto-smooth so sharp edges split normals in render
    # (In newer Blender versions this still exists on mesh data; if your version differs,
    #  you can remove these lines and rely on edge splits/sharp flags + smooth shading.)
    if hasattr(me, "use_auto_smooth"):
        me.use_auto_smooth = True
    if hasattr(me, "auto_smooth_angle"):
        # Set to threshold (or even pi); sharp edges marked above will still force splitting.
        me.auto_smooth_angle = angle_rad

    return {
        "smooth_edges": n_smooth,
        "sharp_edges": n_sharp,
        "boundary_edges": n_boundary,
        "nonmanifold_edges": n_nonmanifold,
        "angle_deg": angle_deg,
        "exclude_negative": exclude_negative,
    }