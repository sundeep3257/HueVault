"""
Database models for User Archives
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Archive(db.Model):
    """User archive model"""
    __tablename__ = 'archives'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    display_name = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    projects = db.relationship('Project', backref='archive', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'display_name': self.display_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'project_count': len(self.projects)
        }


class Project(db.Model):
    """Project model within an archive"""
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    archive_id = db.Column(db.Integer, db.ForeignKey('archives.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    palette = db.Column(db.Text)  # JSON string of hex colors
    img_width = db.Column(db.Integer, default=260)
    img_height = db.Column(db.Integer, default=200)
    img_fit = db.Column(db.String(20), default='cover')  # cover | contain
    img_radius = db.Column(db.Integer, default=8)
    img_gap = db.Column(db.Integer, default=16)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    images = db.relationship('ProjectImage', backref='project', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        import json
        palette_list = json.loads(self.palette) if self.palette else []
        return {
            'id': self.id,
            'title': self.title,
            'palette': palette_list,
            'img_width': self.img_width,
            'img_height': self.img_height,
            'img_fit': self.img_fit,
            'img_radius': self.img_radius,
            'img_gap': self.img_gap,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'images': [img.to_dict() for img in self.images]
        }


class ProjectImage(db.Model):
    """Image associated with a project"""
    __tablename__ = 'project_images'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'filepath': self.filepath
        }

