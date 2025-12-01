from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from database import db
from models.servicio_model import Servicio
from models.especialidad_model import Especialidad
from forms.servicio_forms import ServicioForm

servicio_bp = Blueprint('servicio', __name__, url_prefix='/servicios')

@servicio_bp.route('/')
@login_required
def index():
    servicios = Servicio.query.all()
    return render_template('servicio/index.html', servicios=servicios)

@servicio_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.rol != 'admin':
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    form = ServicioForm()
    form.especialidad_id.choices = [(e.id, e.nombre) for e in Especialidad.query.filter_by(activa=True).all()]
    
    if form.validate_on_submit():
        servicio = Servicio(
            especialidad_id=form.especialidad_id.data,
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            precio=form.precio.data,
            duracion_estimada=form.duracion_estimada.data,
            activo=form.activo.data
        )
        db.session.add(servicio)
        db.session.commit()
        flash('Servicio creado exitosamente', 'success')
        return redirect(url_for('servicio.index'))
    
    return render_template('servicio/create.html', form=form)

@servicio_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if current_user.rol != 'admin':
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    servicio = Servicio.query.get_or_404(id)
    form = ServicioForm(obj=servicio)
    form.especialidad_id.choices = [(e.id, e.nombre) for e in Especialidad.query.filter_by(activa=True).all()]
    
    if form.validate_on_submit():
        servicio.especialidad_id = form.especialidad_id.data
        servicio.nombre = form.nombre.data
        servicio.descripcion = form.descripcion.data
        servicio.precio = form.precio.data
        servicio.duracion_estimada = form.duracion_estimada.data
        servicio.activo = form.activo.data
        
        db.session.commit()
        flash('Servicio actualizado exitosamente', 'success')
        return redirect(url_for('servicio.index'))
    
    return render_template('servicio/edit.html', form=form, servicio=servicio)

@servicio_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    if current_user.rol != 'admin':
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    servicio = Servicio.query.get_or_404(id)
    db.session.delete(servicio)
    db.session.commit()
    flash('Servicio eliminado exitosamente', 'success')
    return redirect(url_for('servicio.index'))