"""
Configuration settings for HueVault Flask application
"""

import os
from pathlib import Path

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{os.path.join(Path(__file__).parent, "huevault.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File upload settings
    UPLOAD_FOLDER = os.path.join(Path(__file__).parent, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'svg', 'tiff', 'tif', 'gif', 'webp'}
    
    # Project storage
    PROJECTS_FOLDER = os.path.join(Path(__file__).parent, 'projects')
    OUTPUT_FOLDER = os.path.join(Path(__file__).parent, 'static', 'outputs')
    
    # SVG conversion settings
    SVG_DPI = 1200
    
    # IBM Color Palette (accent colors)
    IBM_COLORS = {
        'blue': '#0f62fe',
        'cyan': '#0072c3',
        'purple': '#8a3ffc',
        'magenta': '#d12771',
        'red': '#da1e28',
        'orange': '#ff832b',
        'yellow': '#f1c21b',
        'green': '#24a148',
        'teal': '#007d79',
        'gray': '#8d8d8d'
    }

