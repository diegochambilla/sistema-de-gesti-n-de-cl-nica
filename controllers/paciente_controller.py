from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from database import db
from models.paciente_model import Paciente
from forms.paciente_forms import PacienteForm

paciente_bp = Blueprint('paciente', __name__, url_prefix='/pacientes')

@paciente_bp.route('/')
@login_required
def index():
    pacientes = Paciente.query.all()
    return render_template('paciente/index.html', pacientes=pacientes)

@paciente_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.rol not in ['admin', 'recepcion']:
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    form = PacienteForm()
    if form.validate_on_submit():
        paciente = Paciente(
            dni=form.dni.data,
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            genero=form.genero.data,
            telefono=form.telefono.data,
            email=form.email.data,
            direccion=form.direccion.data,
            alergias=form.alergias.data,
            enfermedades_cronicas=form.enfermedades_cronicas.data,
            activo=form.activo.data
        )
        db.session.add(paciente)
        db.session.commit()
        flash('Paciente creado exitosamente', 'success')
        return redirect(url_for('paciente.index'))
    
    return render_template('paciente/create.html', form=form)

@paciente_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if current_user.rol not in ['admin', 'recepcion']:
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    paciente = Paciente.query.get_or_404(id)
    form = PacienteForm(obj=paciente)
    
    if form.validate_on_submit():
        paciente.dni = form.dni.data
        paciente.nombre = form.nombre.data
        paciente.apellido = form.apellido.data
        paciente.fecha_nacimiento = form.fecha_nacimiento.data
        paciente.genero = form.genero.data
        paciente.telefono = form.telefono.data
        paciente.email = form.email.data
        paciente.direccion = form.direccion.data
        paciente.alergias = form.alergias.data
        paciente.enfermedades_cronicas = form.enfermedades_cronicas.data
        paciente.activo = form.activo.data
        
        db.session.commit()
        flash('Paciente actualizado exitosamente', 'success')
        return redirect(url_for('paciente.index'))
    
    return render_template('paciente/edit.html', form=form, paciente=paciente)

@paciente_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    if current_user.rol not in ['admin', 'recepcion']:
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    paciente = Paciente.query.get_or_404(id)
    db.session.delete(paciente)
    db.session.commit()
    flash('Paciente eliminado exitosamente', 'success')
    return redirect(url_for('paciente.index'))
