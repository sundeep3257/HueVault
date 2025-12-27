"""
User Archives blueprint
"""

from flask import Blueprint, render_template, request, jsonify, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
from config import Config
from models import db, Archive, Project, ProjectImage
import os
import json
import uuid

bp = Blueprint('archives', __name__)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'}


@bp.route('/')
def archives_list():
    """List all public archives"""
    archives = Archive.query.all()
    archive_list = []
    
    for archive in archives:
        # Get first project's first image for preview
        preview_image = None
        if archive.projects:
            first_project = archive.projects[0]
            if first_project.images:
                preview_image = first_project.images[0].filepath
        
        archive_data = archive.to_dict()
        archive_data['preview_image'] = preview_image
        archive_list.append(archive_data)
    
    deleted = request.args.get('deleted', '0') == '1'
    return render_template('archives_list.html', archives=archive_list, deleted=deleted)


@bp.route('/go', methods=['GET', 'POST'])
def go_to_archive():
    """Navigate to archive edit mode by username"""
    if request.method == 'GET':
        return redirect(url_for('archives.archives_list'))
    
    username = request.form.get('username', '').strip().lower()
    if not username:
        return redirect(url_for('archives.archives_list'))
    
    return redirect(url_for('archives.edit_archive', username=username))


@bp.route('/<username>/view')
def view_archive(username):
    """View archive (read-only)"""
    username = username.lower().strip()
    archive = Archive.query.filter_by(username=username).first()
    
    if not archive:
        return render_template('error.html', 
                             error='Archive not found',
                             message='The requested archive does not exist.'), 404
    
    projects = [p.to_dict() for p in archive.projects]
    
    return render_template('archive_view.html', archive=archive, projects=projects, edit_mode=False)


@bp.route('/<username>/edit')
def edit_archive(username):
    """Edit archive (requires username entry)"""
    username = username.lower().strip()
    archive = Archive.query.filter_by(username=username).first()
    
    if not archive:
        # Create new archive
        archive = Archive(username=username, display_name=username.title())
        db.session.add(archive)
        db.session.commit()
    
    projects = [p.to_dict() for p in archive.projects]
    
    return render_template('archive_edit.html', archive=archive, projects=projects, edit_mode=True)


@bp.route('/<username>/update', methods=['POST'])
def update_archive(username):
    """Update archive display name"""
    try:
        archive = Archive.query.filter_by(username=username.lower()).first()
        if not archive:
            return jsonify({'success': False, 'error': 'Archive not found'}), 404
        
        data = request.get_json()
        display_name = data.get('display_name', '').strip()
        
        if display_name:
            archive.display_name = display_name
            db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/<username>/project', methods=['POST'])
def add_project(username):
    """Add a project to an archive"""
    try:
        archive = Archive.query.filter_by(username=username.lower()).first()
        if not archive:
            return jsonify({'success': False, 'error': 'Archive not found'}), 404
        
        title = request.form.get('title', '').strip()
        palette_json = request.form.get('palette', '[]')
        
        if not title:
            return jsonify({'success': False, 'error': 'Title is required'}), 400
        
        # Parse palette
        try:
            palette = json.loads(palette_json)
            if not isinstance(palette, list):
                palette = []
        except:
            palette = []
        
        # Get layout settings
        img_width = int(request.form.get('img_width', 260))
        img_height = int(request.form.get('img_height', 200))
        img_fit = request.form.get('img_fit', 'cover')
        img_radius = int(request.form.get('img_radius', 8))
        img_gap = int(request.form.get('img_gap', 16))
        
        # Create project
        project = Project(
            archive_id=archive.id,
            title=title,
            palette=json.dumps(palette),
            img_width=img_width,
            img_height=img_height,
            img_fit=img_fit,
            img_radius=img_radius,
            img_gap=img_gap
        )
        db.session.add(project)
        db.session.flush()  # Get project ID
        
        # Handle image uploads
        uploaded_files = request.files.getlist('images')
        project_dir = os.path.join(Config.UPLOAD_FOLDER, 'archives', username, str(project.id))
        os.makedirs(project_dir, exist_ok=True)
        
        for file in uploaded_files:
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add UUID to avoid conflicts
                unique_filename = f"{uuid.uuid4().hex[:8]}_{filename}"
                filepath = os.path.join(project_dir, unique_filename)
                file.save(filepath)
                
                # Store relative path for serving
                relative_path = f"archives/{username}/{project.id}/{unique_filename}"
                
                project_image = ProjectImage(
                    project_id=project.id,
                    filename=filename,
                    filepath=relative_path
                )
                db.session.add(project_image)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'project': project.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/<username>/projects/<int:project_id>/update', methods=['POST'])
def update_project(username, project_id):
    """Update an existing project"""
    try:
        archive = Archive.query.filter_by(username=username.lower()).first()
        if not archive:
            return jsonify({'success': False, 'error': 'Archive not found'}), 404
        
        project = Project.query.filter_by(id=project_id, archive_id=archive.id).first()
        if not project:
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        title = request.form.get('title', '').strip()
        palette_json = request.form.get('palette', '[]')
        
        if title:
            project.title = title
        
        # Parse palette
        try:
            palette = json.loads(palette_json)
            if isinstance(palette, list):
                project.palette = json.dumps(palette)
        except:
            pass
        
        # Update layout settings
        if request.form.get('img_width'):
            project.img_width = int(request.form.get('img_width'))
        if request.form.get('img_height'):
            project.img_height = int(request.form.get('img_height'))
        if request.form.get('img_fit'):
            project.img_fit = request.form.get('img_fit')
        if request.form.get('img_radius'):
            project.img_radius = int(request.form.get('img_radius'))
        if request.form.get('img_gap'):
            project.img_gap = int(request.form.get('img_gap'))
        
        # Handle new image uploads
        uploaded_files = request.files.getlist('images')
        project_dir = os.path.join(Config.UPLOAD_FOLDER, 'archives', username, str(project.id))
        os.makedirs(project_dir, exist_ok=True)
        
        for file in uploaded_files:
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex[:8]}_{filename}"
                filepath = os.path.join(project_dir, unique_filename)
                file.save(filepath)
                
                relative_path = f"archives/{username}/{project.id}/{unique_filename}"
                
                project_image = ProjectImage(
                    project_id=project.id,
                    filename=filename,
                    filepath=relative_path
                )
                db.session.add(project_image)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'project': project.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/<username>/projects/<int:project_id>/delete', methods=['POST'])
def delete_project(username, project_id):
    """Delete a project"""
    try:
        archive = Archive.query.filter_by(username=username.lower()).first()
        if not archive:
            return jsonify({'success': False, 'error': 'Archive not found'}), 404
        
        project = Project.query.filter_by(id=project_id, archive_id=archive.id).first()
        if not project:
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        # Delete project directory
        project_dir = os.path.join(Config.UPLOAD_FOLDER, 'archives', username, str(project.id))
        if os.path.exists(project_dir):
            import shutil
            shutil.rmtree(project_dir)
        
        db.session.delete(project)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/<username>/projects/<int:project_id>/images/<int:image_id>/delete', methods=['POST'])
def delete_image(username, project_id, image_id):
    """Delete an image from a project"""
    try:
        archive = Archive.query.filter_by(username=username.lower()).first()
        if not archive:
            return jsonify({'success': False, 'error': 'Archive not found'}), 404
        
        project = Project.query.filter_by(id=project_id, archive_id=archive.id).first()
        if not project:
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        image = ProjectImage.query.filter_by(id=image_id, project_id=project.id).first()
        if not image:
            return jsonify({'success': False, 'error': 'Image not found'}), 404
        
        # Delete file
        filepath = os.path.join(Config.UPLOAD_FOLDER, image.filepath)
        if os.path.exists(filepath):
            os.remove(filepath)
        
        db.session.delete(image)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/<username>/delete', methods=['POST'])
def delete_archive(username):
    """Delete an archive and all associated data"""
    try:
        username = username.lower().strip()
        archive = Archive.query.filter_by(username=username).first()
        
        if not archive:
            return jsonify({'success': False, 'error': 'Archive not found'}), 404
        
        # Verify username confirmation
        data = request.get_json()
        confirmed_username = data.get('username', '').strip().lower()
        
        if confirmed_username != username:
            return jsonify({'success': False, 'error': 'Username confirmation does not match'}), 400
        
        # Delete all uploaded files for this archive
        archive_dir = os.path.join(Config.UPLOAD_FOLDER, 'archives', username)
        if os.path.exists(archive_dir):
            import shutil
            shutil.rmtree(archive_dir)
        
        # Delete all projects and images (cascade should handle this, but we'll be explicit)
        for project in archive.projects:
            # Delete project images
            for image in project.images:
                db.session.delete(image)
            db.session.delete(project)
        
        # Delete the archive
        db.session.delete(archive)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(Config.UPLOAD_FOLDER, filename)
