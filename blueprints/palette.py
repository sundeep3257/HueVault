"""
Color Palette Generator blueprint
"""

from flask import Blueprint, render_template, request, jsonify
from utils.color_utils import (
    generate_palette,
    regenerate_unlocked_colors,
    expand_palette,
    hex_to_rgb,
    rgb_to_hex
)
import json

bp = Blueprint('palette', __name__)


@bp.route('/')
def palette_generator():
    """Palette generator page"""
    return render_template('palette.html')


@bp.route('/generate', methods=['POST'])
def generate():
    """Generate a new palette based on user inputs"""
    try:
        data = request.get_json()
        
        num_colors = int(data.get('num_colors', 5))
        formal_playful = float(data.get('formal_playful', 0.5))
        modern_classic = float(data.get('modern_classic', 0.5))
        adjectives = data.get('adjectives', [])
        manual_colors = data.get('manual_colors', [])  # List of hex codes
        seed = data.get('seed', None)
        
        # If manual colors provided, use them and generate remaining
        if manual_colors:
            palette = manual_colors[:num_colors]
            remaining = num_colors - len(manual_colors)
            if remaining > 0:
                additional = generate_palette(
                    remaining, formal_playful, modern_classic, adjectives, seed
                )
                palette.extend(additional)
        else:
            palette = generate_palette(
                num_colors, formal_playful, modern_classic, adjectives, seed
            )
        
        return jsonify({
            'success': True,
            'palette': palette
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@bp.route('/regenerate', methods=['POST'])
def regenerate():
    """Regenerate unlocked colors in an existing palette"""
    try:
        data = request.get_json()
        
        current_palette = data.get('palette', [])
        locked_indices = data.get('locked_indices', [])
        formal_playful = float(data.get('formal_playful', 0.5))
        modern_classic = float(data.get('modern_classic', 0.5))
        adjectives = data.get('adjectives', [])
        seed = data.get('seed', None)
        
        new_palette = regenerate_unlocked_colors(
            current_palette,
            locked_indices,
            formal_playful,
            modern_classic,
            adjectives,
            seed
        )
        
        return jsonify({
            'success': True,
            'palette': new_palette
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@bp.route('/expand', methods=['POST'])
def expand():
    """Expand a palette to a larger size"""
    try:
        data = request.get_json()
        
        current_palette = data.get('palette', [])
        new_size = int(data.get('new_size', len(current_palette) + 1))
        formal_playful = float(data.get('formal_playful', 0.5))
        modern_classic = float(data.get('modern_classic', 0.5))
        adjectives = data.get('adjectives', [])
        seed = data.get('seed', None)
        
        expanded_palette = expand_palette(
            current_palette,
            new_size,
            formal_playful,
            modern_classic,
            adjectives,
            seed
        )
        
        return jsonify({
            'success': True,
            'palette': expanded_palette
        })
    except Exception as e:
        return jsonify({
        'success': False,
        'error': str(e)
    }), 400

