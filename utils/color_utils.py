"""
Color utility functions for palette generation and manipulation
Coolors-like random palette generation (deterministic, non-ML)
"""

import colorsys
import random
import math
from typing import List, Tuple, Dict


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB tuple to hex color"""
    return f"#{r:02x}{g:02x}{b:02x}"


def rgb_to_hsv(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """Convert RGB to HSV"""
    r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0
    return colorsys.rgb_to_hsv(r_norm, g_norm, b_norm)


def hsv_to_rgb(h: float, s: float, v: float) -> Tuple[int, int, int]:
    """Convert HSV to RGB"""
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))


def _color_distance_rgb(color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> float:
    """Calculate Euclidean distance between two RGB colors"""
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)


def _color_distance_hsl(color1: Tuple[float, float, float], color2: Tuple[float, float, float]) -> float:
    """Calculate distance between two HSL colors (weighted)"""
    h1, s1, l1 = color1
    h2, s2, l2 = color2
    
    # Hue distance (circular)
    h_diff = min(abs(h1 - h2), 1.0 - abs(h1 - h2))
    s_diff = abs(s1 - s2)
    l_diff = abs(l1 - l2)
    
    # Weighted distance (hue is more important)
    return math.sqrt((h_diff * 2) ** 2 + s_diff ** 2 + l_diff ** 2)


def _is_color_too_similar(new_color: Tuple[int, int, int], existing_colors: List[Tuple[int, int, int]], min_distance: float = 30.0) -> bool:
    """Check if a color is too similar to existing colors"""
    for existing in existing_colors:
        distance = _color_distance_rgb(new_color, existing)
        if distance < min_distance:
            return True
    return False


def generate_palette(
    num_colors: int,
    formal_playful: float = 0.5,  # Ignored but kept for API compatibility
    modern_classic: float = 0.5,  # Ignored but kept for API compatibility
    adjectives: List[str] = None,  # Ignored but kept for API compatibility
    seed: int = None
) -> List[str]:
    """
    Generate a Coolors-like random palette
    Creates aesthetically pleasing palettes using HSL constraints
    
    Args:
        num_colors: Number of colors to generate (>= 2)
        formal_playful: Ignored (kept for compatibility)
        modern_classic: Ignored (kept for compatibility)
        adjectives: Ignored (kept for compatibility)
        seed: Optional seed for deterministic generation
    
    Returns:
        List of hex color codes
    """
    if adjectives is None:
        adjectives = []
    
    if seed is not None:
        random.seed(seed)
    
    if num_colors < 2:
        num_colors = 2
    
    palette_rgb = []
    max_attempts = 1000
    
    # Strategy: Choose a base hue, then generate complementary/analogous/triadic colors
    base_hue = random.random()  # Random starting hue
    
    # Choose a color scheme type
    scheme_type = random.choice(['complementary', 'analogous', 'triadic', 'tetradic', 'split_complementary'])
    
    for i in range(num_colors):
        attempts = 0
        while attempts < max_attempts:
            if i == 0:
                # First color: base hue with good saturation and lightness
                hue = base_hue
                saturation = random.uniform(0.4, 0.9)  # Avoid muddy colors
                lightness = random.uniform(0.3, 0.7)  # Avoid too dark or too light
            else:
                # Subsequent colors: based on scheme
                if scheme_type == 'complementary':
                    hue = (base_hue + 0.5 + (i - 1) * 0.1) % 1.0
                elif scheme_type == 'analogous':
                    hue = (base_hue + (i - 1) * 0.08 + random.uniform(-0.05, 0.05)) % 1.0
                elif scheme_type == 'triadic':
                    hue = (base_hue + (i - 1) * 0.333 + random.uniform(-0.05, 0.05)) % 1.0
                elif scheme_type == 'tetradic':
                    hue = (base_hue + (i - 1) * 0.25 + random.uniform(-0.05, 0.05)) % 1.0
                elif scheme_type == 'split_complementary':
                    if i == 1:
                        hue = (base_hue + 0.5 + random.uniform(-0.1, 0.1)) % 1.0
                    else:
                        hue = (base_hue + random.uniform(0.4, 0.6) + (i - 2) * 0.1) % 1.0
                else:
                    hue = (base_hue + i * 0.2 + random.uniform(-0.1, 0.1)) % 1.0
                
                # Vary saturation and lightness for visual interest
                saturation = random.uniform(0.3, 0.95)
                lightness = random.uniform(0.25, 0.75)
            
            # Convert to RGB
            r, g, b = hsv_to_rgb(hue, saturation, lightness)
            new_color = (r, g, b)
            
            # Check if color is too similar to existing colors
            if not _is_color_too_similar(new_color, palette_rgb, min_distance=25.0):
                palette_rgb.append(new_color)
                break
            
            attempts += 1
        
        # If we couldn't find a sufficiently different color, use this one anyway
        if attempts >= max_attempts and len(palette_rgb) == i:
            r, g, b = hsv_to_rgb(
                (base_hue + i * 0.2) % 1.0,
                random.uniform(0.4, 0.8),
                random.uniform(0.3, 0.7)
            )
            palette_rgb.append((r, g, b))
    
    # Convert to hex
    return [rgb_to_hex(r, g, b) for r, g, b in palette_rgb]


def regenerate_unlocked_colors(
    palette: List[str],
    locked_indices: List[int],
    formal_playful: float = 0.5,  # Ignored
    modern_classic: float = 0.5,  # Ignored
    adjectives: List[str] = None,  # Ignored
    seed: int = None
) -> List[str]:
    """Regenerate only unlocked colors in a palette"""
    if adjectives is None:
        adjectives = []
    
    if seed is not None:
        random.seed(seed)
    
    new_palette = palette.copy()
    locked_colors_rgb = [hex_to_rgb(palette[i]) for i in locked_indices]
    
    for i in range(len(palette)):
        if i not in locked_indices:
            attempts = 0
            max_attempts = 500
            
            while attempts < max_attempts:
                # Generate a random color
                hue = random.random()
                saturation = random.uniform(0.4, 0.9)
                lightness = random.uniform(0.3, 0.7)
                
                r, g, b = hsv_to_rgb(hue, saturation, lightness)
                new_color = (r, g, b)
                
                # Check distance from all locked colors and existing palette colors
                all_existing = locked_colors_rgb + [hex_to_rgb(new_palette[j]) for j in range(len(new_palette)) if j != i and new_palette[j]]
                
                if not _is_color_too_similar(new_color, all_existing, min_distance=25.0):
                    new_palette[i] = rgb_to_hex(r, g, b)
                    break
                
                attempts += 1
            
            # Fallback if no good color found
            if attempts >= max_attempts:
                hue = random.random()
                saturation = random.uniform(0.4, 0.8)
                lightness = random.uniform(0.3, 0.7)
                r, g, b = hsv_to_rgb(hue, saturation, lightness)
                new_palette[i] = rgb_to_hex(r, g, b)
    
    return new_palette


def expand_palette(
    current_palette: List[str],
    new_size: int,
    formal_playful: float = 0.5,  # Ignored
    modern_classic: float = 0.5,  # Ignored
    adjectives: List[str] = None,  # Ignored
    seed: int = None
) -> List[str]:
    """Expand a palette to a larger size"""
    if adjectives is None:
        adjectives = []
    
    if new_size <= len(current_palette):
        return current_palette
    
    if seed is not None:
        random.seed(seed + len(current_palette))
    
    existing_colors_rgb = [hex_to_rgb(c) for c in current_palette]
    additional_count = new_size - len(current_palette)
    additional_colors = []
    
    for _ in range(additional_count):
        attempts = 0
        max_attempts = 500
        
        while attempts < max_attempts:
            hue = random.random()
            saturation = random.uniform(0.4, 0.9)
            lightness = random.uniform(0.3, 0.7)
            
            r, g, b = hsv_to_rgb(hue, saturation, lightness)
            new_color = (r, g, b)
            
            all_existing = existing_colors_rgb + [hex_to_rgb(c) for c in additional_colors]
            
            if not _is_color_too_similar(new_color, all_existing, min_distance=25.0):
                additional_colors.append(rgb_to_hex(r, g, b))
                break
            
            attempts += 1
        
        # Fallback
        if attempts >= max_attempts:
            hue = random.random()
            saturation = random.uniform(0.4, 0.8)
            lightness = random.uniform(0.3, 0.7)
            r, g, b = hsv_to_rgb(hue, saturation, lightness)
            additional_colors.append(rgb_to_hex(r, g, b))
    
    return current_palette + additional_colors
