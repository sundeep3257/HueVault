"""
Background Removal Tool blueprint
"""

from flask import Blueprint, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
from config import Config
from utils.image_utils import remove_background_color
import os
import io

bp = Blueprint('background_removal', __name__)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'tiff', 'tif'}


@bp.route('/')
def background_removal():
    """Background removal tool page"""
    return render_template('background_removal.html')


@bp.route('/remove', methods=['POST'])
def remove():
    """Remove background color from image"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type'}), 400
        
        background_color = request.form.get('background_color', '#FFFFFF')
        tolerance = int(request.form.get('tolerance', 10))
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        upload_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(upload_path)
        
        try:
            # Remove background
            img = remove_background_color(upload_path, background_color, tolerance)
            
            # Determine output format (same as input, but JPEG doesn't support transparency)
            file_ext = filename.rsplit('.', 1)[1].lower()
            if file_ext in ['jpg', 'jpeg']:
                # JPEG doesn't support transparency - convert to PNG
                file_ext = 'png'
                output_filename = f"{os.path.splitext(filename)[0]}_no_bg.png"
            elif file_ext == 'tif':
                file_ext = 'tiff'
                output_filename = f"{os.path.splitext(filename)[0]}_no_bg.tiff"
            else:
                output_filename = f"{os.path.splitext(filename)[0]}_no_bg.{file_ext}"
            
            # Get DPI from image info or use 1200
            dpi = img.info.get('dpi', (1200, 1200))
            if isinstance(dpi, tuple) and len(dpi) == 2:
                dpi_x, dpi_y = dpi
            else:
                dpi_x, dpi_y = 1200, 1200
            
            # Save to bytes with DPI metadata
            output_buffer = io.BytesIO()
            
            if file_ext == 'png':
                img.save(output_buffer, format='PNG', dpi=(dpi_x, dpi_y))
            elif file_ext == 'tiff':
                img.save(output_buffer, format='TIFF', dpi=(dpi_x, dpi_y))
            else:
                img.save(output_buffer, format='PNG', dpi=(dpi_x, dpi_y))
            
            output_buffer.seek(0)
            
            # Return file
            return send_file(
                output_buffer,
                mimetype=f'image/{file_ext}',
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

