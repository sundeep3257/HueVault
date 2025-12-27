"""
Image processing utilities for SVG conversion and background removal
"""

import os
from PIL import Image
import cairosvg
import io
from typing import Tuple, Optional


def convert_svg_to_raster(
    svg_path: str,
    output_format: str = 'png',
    dpi: int = 1200
) -> bytes:
    """
    Convert SVG to PNG, JPEG, or TIFF at specified DPI
    
    Args:
        svg_path: Path to SVG file
        output_format: 'png', 'jpeg', or 'tiff'
        dpi: Output resolution in DPI
    
    Returns:
        Bytes of the converted image
    """
    # Read SVG file
    with open(svg_path, 'rb') as f:
        svg_data = f.read()
    
    # Convert SVG to PNG first (CairoSVG outputs PNG)
    png_data = cairosvg.svg2png(
        bytestring=svg_data,
        dpi=dpi
    )
    
    # If PNG is requested, return as-is
    if output_format.lower() == 'png':
        return png_data
    
    # Convert PNG to requested format
    img = Image.open(io.BytesIO(png_data))
    
    output_buffer = io.BytesIO()
    
    if output_format.lower() in ['jpeg', 'jpg']:
        # Convert RGBA to RGB for JPEG (no transparency)
        if img.mode == 'RGBA':
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[3])  # Use alpha channel as mask
            img = rgb_img
        img.save(output_buffer, format='JPEG', quality=95, dpi=(dpi, dpi))
    elif output_format.lower() == 'tiff':
        img.save(output_buffer, format='TIFF', dpi=(dpi, dpi))
    else:
        # Default to PNG
        img.save(output_buffer, format='PNG', dpi=(dpi, dpi))
    
    return output_buffer.getvalue()


def remove_background_color(
    image_path: str,
    background_color: str,
    tolerance: int = 10
) -> Image.Image:
    """
    Remove a solid background color from an image
    
    Args:
        image_path: Path to input image
        background_color: Hex color of background to remove (e.g., "#FFFFFF")
        tolerance: Color matching tolerance (0-255)
    
    Returns:
        PIL Image with transparent background (RGBA mode)
    """
    # Open image
    img = Image.open(image_path)
    
    # Preserve original DPI if available
    dpi = img.info.get('dpi', (1200, 1200))
    if isinstance(dpi, tuple) and len(dpi) == 2:
        dpi_x, dpi_y = dpi
    else:
        dpi_x, dpi_y = 1200, 1200
    
    # Convert to RGBA if not already
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Parse background color
    bg_color = background_color.lstrip('#')
    bg_r = int(bg_color[0:2], 16)
    bg_g = int(bg_color[2:4], 16)
    bg_b = int(bg_color[4:6], 16)
    
    # Create mask for pixels to remove
    data = img.getdata()
    new_data = []
    
    for item in data:
        r, g, b, a = item
        
        # Check if pixel is within tolerance of background color
        if (abs(r - bg_r) <= tolerance and
            abs(g - bg_g) <= tolerance and
            abs(b - bg_b) <= tolerance):
            # Make transparent
            new_data.append((r, g, b, 0))
        else:
            # Keep original
            new_data.append(item)
    
    # Update image with new data
    img.putdata(new_data)
    
    # Store DPI in image info for later saving
    img.info['dpi'] = (dpi_x, dpi_y)
    
    return img


def get_image_dimensions(image_path: str) -> Tuple[int, int]:
    """Get width and height of an image"""
    with Image.open(image_path) as img:
        return img.size

