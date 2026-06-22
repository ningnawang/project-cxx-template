def hex_to_rgba(hex_code):
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