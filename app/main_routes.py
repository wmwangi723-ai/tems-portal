import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, abort, request, session, redirect, url_for, flash, current_app
from .models import Level, Module, Unit, User, Material, Flashcard, db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def dashboard():
    levels = Level.query.order_by(Level.level_number).all()
    return render_template('dashboard.html', levels=levels)

@main_bp.route('/unit/<int:unit_id>')
def view_unit(unit_id):
    unit = Unit.query.get_or_404(unit_id)
    return render_template('unit_view.html', unit=unit)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            return redirect(url_for('main.admin_dashboard'))
        else:
            flash('Invalid credentials. Access denied.')
    return render_template('login.html')

@main_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.dashboard'))

@main_bp.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    # Security Check: Kick out anyone without an admin session
    if not session.get('is_admin'):
        abort(403) 

    if request.method == 'POST':
        action_type = request.form.get('action_type')
        unit_id = request.form.get('unit_id')
        
        if not unit_id:
            flash('Please select a unit.')
            return redirect(url_for('main.admin_dashboard'))

        # 1. Handle Text Material Upload
        if action_type == 'upload_material':
            material_type = request.form.get('material_type')
            content = request.form.get('content')
            if content:
                new_material = Material(material_type=material_type, content=content, unit_id=unit_id)
                db.session.add(new_material)
                db.session.commit()
                flash('Text material successfully added!')

        # 2. Handle File Uploads (PDFs/Images)
        elif action_type == 'upload_file':
            file = request.files.get('file_upload')
            if file and file.filename != '':
                # Secure the filename
                filename = secure_filename(file.filename)
                # Save it to the static/uploads folder
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Save the filename to the database
                new_material = Material(material_type='File', content=filename, unit_id=unit_id)
                db.session.add(new_material)
                db.session.commit()
                flash(f'File {filename} successfully uploaded!')

        # 3. Handle Flashcard Generation
        elif action_type == 'add_flashcard':
            question = request.form.get('question')
            answer = request.form.get('answer')
            if question and answer:
                new_card = Flashcard(question=question, answer=answer, unit_id=unit_id)
                db.session.add(new_card)
                db.session.commit()
                flash('Flashcard successfully added!')
                
        return redirect(url_for('main.admin_dashboard'))
        
    # GET request - load the page
    units = Unit.query.all()
    return render_template('admin_dashboard.html', units=units)