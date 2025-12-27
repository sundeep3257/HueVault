"""
Color-blindness simulation using deterministic color space transformations
Based on cone-response-based color space conversions
Deterministic, no ML required
"""

from typing import Tuple


def _matrix_multiply(matrix, vector):
    """Multiply a 3x3 matrix by a 3-element vector"""
    result = [0.0, 0.0, 0.0]
    for i in range(3):
        for j in range(3):
            result[i] += matrix[i][j] * vector[j]
    return result


def rgb_to_lms(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """
    Convert RGB to LMS (Long, Medium, Short wavelength) cone response space
    Uses the Bradford transformation matrix
    """
    # Normalize RGB to 0-1
    r_norm = r / 255.0
    g_norm = g / 255.0
    b_norm = b / 255.0
    
    # Convert to linear RGB (gamma correction)
    def linearize(c):
        if c <= 0.04045:
            return c / 12.92
        return ((c + 0.055) / 1.055) ** 2.4
    
    r_lin = linearize(r_norm)
    g_lin = linearize(g_norm)
    b_lin = linearize(b_norm)
    
    # Transformation matrix to LMS (Bradford transform)
    # This approximates cone responses
    transform_matrix = [
        [0.31399022, 0.63951294, 0.04649755],
        [0.15537241, 0.75789446, 0.08670142],
        [0.01775239, 0.10944209, 0.87256922]
    ]
    
    rgb_vector = [r_lin, g_lin, b_lin]
    lms = _matrix_multiply(transform_matrix, rgb_vector)
    
    return tuple(lms)


def lms_to_rgb(l: float, m: float, s: float) -> Tuple[int, int, int]:
    """Convert LMS back to RGB"""
    # Inverse transformation matrix
    inv_transform = [
        [5.47221206, -4.6419601, 0.16963708],
        [-1.1252419, 2.29317094, -0.1678952],
        [0.02980165, -0.19318073, 1.16364789]
    ]
    
    lms_vector = [l, m, s]
    rgb_lin = _matrix_multiply(inv_transform, lms_vector)
    
    # Gamma correction (convert back from linear)
    def delinearize(c):
        if c <= 0.0031308:
            return 12.92 * c
        return 1.055 * (c ** (1.0 / 2.4)) - 0.055
    
    r_lin, g_lin, b_lin = rgb_lin
    r = delinearize(max(0, min(1, r_lin)))
    g = delinearize(max(0, min(1, g_lin)))
    b = delinearize(max(0, min(1, b_lin)))
    
    return (int(r * 255), int(g * 255), int(b * 255))


def simulate_protanopia(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """
    Simulate Protanopia (red-blindness)
    L cones are missing or non-functional
    """
    l, m, s = rgb_to_lms(r, g, b)
    
    # In protanopia, L cones don't work, so we shift L response to M
    # This is a simplified model
    l_sim = 0.0  # L cones don't respond
    m_sim = m + (l * 1.05)  # M cones pick up some L response
    s_sim = s
    
    return lms_to_rgb(l_sim, m_sim, s_sim)


def simulate_deuteranopia(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """
    Simulate Deuteranopia (green-blindness)
    M cones are missing or non-functional
    """
    l, m, s = rgb_to_lms(r, g, b)
    
    # In deuteranopia, M cones don't work, so we shift M response to L
    l_sim = l + (m * 1.05)  # L cones pick up some M response
    m_sim = 0.0  # M cones don't respond
    s_sim = s
    
    return lms_to_rgb(l_sim, m_sim, s_sim)


def simulate_tritanopia(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """
    Simulate Tritanopia (blue-blindness)
    S cones are missing or non-functional
    """
    l, m, s = rgb_to_lms(r, g, b)
    
    # In tritanopia, S cones don't work, so we shift S response to L and M
    l_sim = l + (s * 0.3)  # L cones pick up some S response
    m_sim = m + (s * 0.7)  # M cones pick up most S response
    s_sim = 0.0  # S cones don't respond
    
    return lms_to_rgb(l_sim, m_sim, s_sim)


def simulate_colorblindness(hex_color: str, deficiency_type: str) -> str:
    """
    Simulate color blindness for a hex color
    
    Args:
        hex_color: Hex color string (e.g., "#FF0000")
        deficiency_type: "protanopia", "deuteranopia", or "tritanopia"
    
    Returns:
        Hex color string representing how it appears with the deficiency
    """
    # Convert hex to RGB
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    # Apply appropriate simulation
    if deficiency_type.lower() == 'protanopia':
        r_sim, g_sim, b_sim = simulate_protanopia(r, g, b)
    elif deficiency_type.lower() == 'deuteranopia':
        r_sim, g_sim, b_sim = simulate_deuteranopia(r, g, b)
    elif deficiency_type.lower() == 'tritanopia':
        r_sim, g_sim, b_sim = simulate_tritanopia(r, g, b)
    else:
        # Unknown type, return original
        return f"#{hex_color}"
    
    # Convert back to hex
    return f"#{r_sim:02x}{g_sim:02x}{b_sim:02x}"

