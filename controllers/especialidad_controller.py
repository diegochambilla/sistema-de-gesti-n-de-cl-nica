from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from database import db
from models.especialidad_model import Especialidad
from forms.especialidad_forms import EspecialidadForm

especialidad_bp = Blueprint('especialidad', __name__, url_prefix='/especialidades')

@especialidad_bp.route('/')
@login_required
def index():
    especialidades = Especialidad.query.all()
    return render_template('especialidad/index.html', especialidades=especialidades)

@especialidad_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.rol != 'admin':
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    form = EspecialidadForm()
    if form.validate_on_submit():
        especialidad = Especialidad(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            precio_consulta=form.precio_consulta.data,
            activa=form.activa.data
        )
        db.session.add(especialidad)
        db.session.commit()
        flash('Especialidad creada exitosamente', 'success')
        return redirect(url_for('especialidad.index'))
    
    return render_template('especialidad/create.html', form=form)

@especialidad_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if current_user.rol != 'admin':
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    especialidad = Especialidad.query.get_or_404(id)
    form = EspecialidadForm(obj=especialidad)
    
    if form.validate_on_submit():
        especialidad.nombre = form.nombre.data
        especialidad.descripcion = form.descripcion.data
        especialidad.precio_consulta = form.precio_consulta.data
        especialidad.activa = form.activa.data
        
        db.session.commit()
        flash('Especialidad actualizada exitosamente', 'success')
        return redirect(url_for('especialidad.index'))
    
    return render_template('especialidad/edit.html', form=form, especialidad=especialidad)

@especialidad_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    if current_user.rol != 'admin':
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    especialidad = Especialidad.query.get_or_404(id)
    db.session.delete(especialidad)
    db.session.commit()
    flash('Especialidad eliminada exitosamente', 'success')
    return redirect(url_for('especialidad.index'))