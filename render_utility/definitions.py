import sys
import os
import numpy as np

def hex_to_rgba_01(hex_code):
    """
    Convert a hex color code (6 or 8 digits, with or without #) to an RGBA tuple (0.0 to 1.0).
    """
    # Remove '#' if present and ensure the correct length
    hex_code = hex_code.lstrip('#')
    if len(hex_code) not in (6, 8):
        raise ValueError("Hex code must be 6 or 8 digits long")

    # Split into components
    r_hex = hex_code[0:2]
    g_hex = hex_code[2:4]
    b_hex = hex_code[4:6]
    a_hex = hex_code[6:8] if len(hex_code) == 8 else "ff" # Default to fully opaque if no alpha

    # Convert hex to integer (0-255)
    r = int(r_hex, 16)
    g = int(g_hex, 16)
    b = int(b_hex, 16)
    a = int(a_hex, 16)

    # Convert to float (0.0-1.0)
    r_float = r / 255.0
    g_float = g / 255.0
    b_float = b / 255.0
    a_float = a / 255.0

    return (r_float, g_float, b_float, a_float)

blue_c1 = "#B9D9EB" # columbia
blue_c2 = "#1D4F91" # columbia
pink_c1 = "#AE2573" # columbia

blue_1 = "#6690ffff"
blue_2 = "#6baed6ff"
blue_3 = "#1F78B4"
blue_4 = "#053c5d"

green_1 = "#B2DF8A"
green_2 = "#33A02C"
red_1 = "#FB9A99"
red_2 = "#E31A1C"
red_3 = "#8B0000"
orange_1 = "#FDBF6F"
orange_2 = "#FF7F00"
orange_3 = "#d95f0e"
bg_1 = "#FFF7E2"
bg_2 = "#FDBF95"
bg_3 = "#F0BA90"

brown = "#B15928"
purple_1 = "#998ec3" #"#CAB2D6"
purple_2 = "#b974e1"
purple_3 = "#b040f6"
purple_4 = "#7236b2"
yellow_1 = "#FFFF99"
yellow_2 = "#E1D623"
grey_1 = "#808080"
grey_2 = "#2D2D2D"
grey_3 = "#D2D2D2"
pink_1 = "#dd3497"
white = "#FFFFFF"



input_mesh_color = hex_to_rgba_01(grey_1) # to make utility happy
gt_color = hex_to_rgba_01(grey_1)
input_color = hex_to_rgba_01(grey_1)
input_color = hex_to_rgba_01(grey_3)
non_manifold_edge_color = hex_to_rgba_01(red_3)
non_manifold_vertex_color = hex_to_rgba_01(red_3)

mm3_color = hex_to_rgba_01(yellow_2)
meshudf_color = hex_to_rgba_01(purple_3)
capudf_color = hex_to_rgba_01(purple_2)
geoudf_color = hex_to_rgba_01(purple_1)
nsdudf_color = hex_to_rgba_01(purple_4)

dcudf_color = hex_to_rgba_01(orange_3)
dcudf2_color = hex_to_rgba_01(orange_1)

dmudf_color = hex_to_rgba_01(green_2) # DualMeshUDF

superpower_color = hex_to_rgba_01(blue_3)
ours_color = hex_to_rgba_01(blue_3)

non_manifold_edge_color = hex_to_rgba_01(red_3)
non_manifold_vertex_color = hex_to_rgba_01(red_3)
nsdudf_color = hex_to_rgba_01(brown)
ndc_color = hex_to_rgba_01(pink_1)

color_power_diagram = "#7b3106"
color_power_contour = "#8e20e2"
color_super_power_contour = "#ef709d" 

type_to_color = {
	'gt': input_mesh_color,
    'input': input_mesh_color,
	'ours': superpower_color,
    'mm3': mm3_color,
    'superpower': superpower_color,
	'meshudf': meshudf_color,
	'capudf': capudf_color,
	'geoudf': geoudf_color,
	'nsdudf': nsdudf_color,
	'dcudf': dcudf_color,
	'dcudf2': dcudf2_color,
    'dmudf': dmudf_color,
    'ndc': ndc_color,
    'nsdudf': nsdudf_color,
    "powerdiagram": hex_to_rgba_01(color_power_diagram),
    "powercontour": hex_to_rgba_01(color_power_contour),
    "superpowercontour": hex_to_rgba_01(color_super_power_contour),
}