"""
Color Accessibility & Color-Blindness Simulator blueprint
"""

from flask import Blueprint, render_template, request, jsonify
from utils.colorblind_simulator import simulate_colorblindness

bp = Blueprint('accessibility', __name__)


@bp.route('/')
def accessibility_tool():
    """Color accessibility and color-blindness simulator page"""
    return render_template('accessibility.html')


@bp.route('/simulate', methods=['POST'])
def simulate():
    """Simulate color blindness for a palette"""
    try:
        data = request.get_json()
        palette = data.get('palette', [])
        deficiency_type = data.get('deficiency_type', 'protanopia')
        
        if deficiency_type not in ['protanopia', 'deuteranopia', 'tritanopia']:
            return jsonify({
                'success': False,
                'error': 'Invalid deficiency type'
            }), 400
        
        simulated_palette = []
        for color in palette:
            simulated_color = simulate_colorblindness(color, deficiency_type)
            simulated_palette.append(simulated_color)
        
        return jsonify({
            'success': True,
            'palette': simulated_palette
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

