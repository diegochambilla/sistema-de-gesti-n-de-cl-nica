from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import time
from database import db
from models.medico_model import Medico
from models.usuario_model import Usuario
from models.especialidad_model import Especialidad
from models.horario_medico_model import HorarioMedico
from forms.medico_forms import MedicoForm, HorarioMedicoForm

medico_bp = Blueprint('medico', __name__, url_prefix='/medicos')

@medico_bp.route('/')
@login_required
def index():
    medicos = Medico.query.all()
    return render_template('medico/index.html', medicos=medicos)

@medico_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.rol not in ['admin', 'recepcion']:
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    form = MedicoForm()
    form.usuario_id.choices = [(u.id, u.username) for u in Usuario.query.filter_by(rol='medico', activo=True).all()]
    form.especialidad_id.choices = [(e.id, e.nombre) for e in Especialidad.query.filter_by(activa=True).all()]
    
    if form.validate_on_submit():
        medico = Medico(
            usuario_id=form.usuario_id.data,
            especialidad_id=form.especialidad_id.data,
            numero_colegiado=form.numero_colegiado.data,
            telefono=form.telefono.data,
            direccion=form.direccion.data,
            fecha_contratacion=form.fecha_contratacion.data,
            activo=form.activo.data
        )
        db.session.add(medico)
        db.session.commit()
        flash('Médico creado exitosamente', 'success')
        return redirect(url_for('medico.index'))
    
    return render_template('medico/create.html', form=form)

@medico_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if current_user.rol not in ['admin', 'recepcion']:
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    medico = Medico.query.get_or_404(id)
    form = MedicoForm(obj=medico)
    form.usuario_id.choices = [(u.id, u.username) for u in Usuario.query.filter_by(rol='medico', activo=True).all()]
    form.especialidad_id.choices = [(e.id, e.nombre) for e in Especialidad.query.filter_by(activa=True).all()]
    
    if form.validate_on_submit():
        medico.usuario_id = form.usuario_id.data
        medico.especialidad_id = form.especialidad_id.data
        medico.numero_colegiado = form.numero_colegiado.data
        medico.telefono = form.telefono.data
        medico.direccion = form.direccion.data
        medico.fecha_contratacion = form.fecha_contratacion.data
        medico.activo = form.activo.data
        
        db.session.commit()
        flash('Médico actualizado exitosamente', 'success')
        return redirect(url_for('medico.index'))
    
    return render_template('medico/edit.html', form=form, medico=medico)

@medico_bp.route('/horarios/<int:medico_id>', methods=['GET', 'POST'])
@login_required
def horarios(medico_id):
    medico = Medico.query.get_or_404(medico_id)
    form = HorarioMedicoForm()
    
    if form.validate_on_submit():
        # Convertir strings a objetos time
        hora_inicio_str = form.hora_inicio.data
        hora_fin_str = form.hora_fin.data
        
        # Convertir 'HH:MM' a objeto time
        hora_inicio_time = time(int(hora_inicio_str.split(':')[0]), int(hora_inicio_str.split(':')[1]))
        hora_fin_time = time(int(hora_fin_str.split(':')[0]), int(hora_fin_str.split(':')[1]))
        
        horario = HorarioMedico(
            medico_id=medico_id,
            dia_semana=form.dia_semana.data,
            hora_inicio=hora_inicio_time,
            hora_fin=hora_fin_time,
            activo=form.activo.data
        )
        db.session.add(horario)
        db.session.commit()
        flash('Horario agregado exitosamente', 'success')
        return redirect(url_for('medico.horarios', medico_id=medico_id))
    
    horarios = HorarioMedico.query.filter_by(medico_id=medico_id).all()
    return render_template('medico/horarios.html', form=form, medico=medico, horarios=horarios)

@medico_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    if current_user.rol != 'admin':
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    medico = Medico.query.get_or_404(id)
    
    # Verificar si tiene citas o consultas antes de eliminar
    from models.cita_model import Cita
    from models.consulta_model import Consulta
    
    citas_count = Cita.query.filter_by(medico_id=id).count()
    consultas_count = Consulta.query.filter_by(medico_id=id).count()
    
    if citas_count > 0 or consultas_count > 0:
        flash(f'No se puede eliminar el médico porque tiene {citas_count} cita(s) y {consultas_count} consulta(s) asociadas. Use "Desasociar" primero.', 'danger')
        return redirect(url_for('medico.index'))
    
    db.session.delete(medico)
    db.session.commit()
    flash('Médico eliminado exitosamente', 'success')
    return redirect(url_for('medico.index'))

# NUEVA RUTA PARA DESASOCIAR
@medico_bp.route('/disassociate/<int:id>')
@login_required
def disassociate(id):
    """Desasociar médico de su usuario (quitar relación usuario_id)"""
    if current_user.rol != 'admin':
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    medico = Medico.query.get_or_404(id)
    
    try:
        # Guardar el usuario_id antes de desasociar para mostrar en el mensaje
        usuario_anterior = medico.usuario_id
        
        # Desasociar estableciendo usuario_id a None
        medico.usuario_id = None
        
        db.session.commit()
        
        if usuario_anterior:
            flash('Médico desasociado exitosamente del usuario', 'success')
        else:
            flash('El médico ya no tenía usuario asociado', 'info')
            
    except Exception as e:
        db.session.rollback()
        flash(f'Error al desasociar médico: {str(e)}', 'danger')
    
    return redirect(url_for('medico.index'))