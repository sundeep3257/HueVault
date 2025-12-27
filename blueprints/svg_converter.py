"""
SVG Conversion Tool blueprint
"""

from flask import Blueprint, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
from config import Config
from utils.image_utils import convert_svg_to_raster
import os
import io

bp = Blueprint('svg_converter', __name__)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'svg'}


@bp.route('/')
def svg_converter():
    """SVG converter page"""
    return render_template('svg_converter.html')


@bp.route('/convert', methods=['POST'])
def convert():
    """Convert SVG to raster format"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type'}), 400
        
        output_format = request.form.get('format', 'png').lower()
        if output_format not in ['png', 'jpeg', 'jpg', 'tiff']:
            output_format = 'png'
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        upload_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(upload_path)
        
        try:
            # Convert SVG
            output_data = convert_svg_to_raster(
                upload_path,
                output_format=output_format,
                dpi=Config.SVG_DPI
            )
            
            # Determine output filename
            base_name = os.path.splitext(filename)[0]
            if output_format == 'jpg':
                output_format = 'jpeg'
            output_filename = f"{base_name}.{output_format}"
            
            # Return file
            return send_file(
                io.BytesIO(output_data),
                mimetype=f'image/{output_format}',
                as_attachment=True,
                download_name=output_filename
            )
        finally:
            # Clean up uploaded file
            if os.path.exists(upload_path):
                os.remove(upload_path)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

