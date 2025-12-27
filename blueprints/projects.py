"""
Public Project Pages blueprint
"""

from flask import Blueprint, render_template, request, jsonify, send_from_directory
from config import Config
import os
import json

bp = Blueprint('projects', __name__)


@bp.route('/')
def projects_list():
    """List all public projects"""
    projects = []
    if os.path.exists(Config.PROJECTS_FOLDER):
        for filename in os.listdir(Config.PROJECTS_FOLDER):
            if filename.endswith('.json'):
                project_path = os.path.join(Config.PROJECTS_FOLDER, filename)
                try:
                    with open(project_path, 'r', encoding='utf-8') as f:
                        project_data = json.load(f)
                        project_data['id'] = os.path.splitext(filename)[0]
                        projects.append(project_data)
                except:
                    continue
    
    return render_template('projects.html', projects=projects)


@bp.route('/create', methods=['GET', 'POST'])
def create_project():
    """Create a new project page"""
    if request.method == 'GET':
        return render_template('create_project.html')
    
    # POST - Save project
    try:
        data = request.get_json()
        
        title = data.get('title', 'Untitled Project')
        description = data.get('description', '')
        palettes = data.get('palettes', [])
        logos = data.get('logos', [])
        favicons = data.get('favicons', [])
        graphics = data.get('graphics', [])
        
        # Generate project ID from title
        project_id = title.lower().replace(' ', '-').replace('_', '-')
        # Remove special characters
        project_id = ''.join(c for c in project_id if c.isalnum() or c == '-')
        
        project_data = {
            'title': title,
            'description': description,
            'palettes': palettes,
            'logos': logos,
            'favicons': favicons,
            'graphics': graphics
        }
        
        # Save project JSON
        project_path = os.path.join(Config.PROJECTS_FOLDER, f"{project_id}.json")
        with open(project_path, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, indent=2)
        
        return jsonify({
            'success': True,
            'project_id': project_id,
            'url': f'/projects/{project_id}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/<project_id>')
def view_project(project_id):
    """View a specific project page"""
    project_path = os.path.join(Config.PROJECTS_FOLDER, f"{project_id}.json")
    
    if not os.path.exists(project_path):
        return render_template('error.html', 
                             error='Project not found',
                             message='The requested project does not exist.'), 404
    
    try:
        with open(project_path, 'r', encoding='utf-8') as f:
            project_data = json.load(f)
        
        return render_template('project_view.html', project=project_data, project_id=project_id)
    except Exception as e:
        return render_template('error.html',
                             error='Error loading project',
                             message=str(e)), 500

