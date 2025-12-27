"""
HueVault - A comprehensive design tool for graphic designers
Main Flask application entry point
"""

from flask import Flask
from config import Config
from models import db
import os

def create_app(config_class=Config):
    """Application factory pattern for Flask"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize database
    db.init_app(app)
    
    # Ensure necessary directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PROJECTS_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'archives'), exist_ok=True)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from blueprints.palette import bp as palette_bp
    app.register_blueprint(palette_bp, url_prefix='/palette')
    
    from blueprints.accessibility import bp as accessibility_bp
    app.register_blueprint(accessibility_bp, url_prefix='/accessibility')
    
    from blueprints.svg_converter import bp as svg_bp
    app.register_blueprint(svg_bp, url_prefix='/svg')
    
    from blueprints.background_removal import bp as bg_bp
    app.register_blueprint(bg_bp, url_prefix='/background')
    
    from blueprints.projects import bp as projects_bp
    app.register_blueprint(projects_bp, url_prefix='/projects')
    
    from blueprints.archives import bp as archives_bp
    app.register_blueprint(archives_bp, url_prefix='/archives')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
