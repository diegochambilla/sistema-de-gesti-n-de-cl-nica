from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from database import db
from models.cita_model import Cita
from models.paciente_model import Paciente
from models.medico_model import Medico
from models.consulta_model import Consulta
from datetime import datetime

cita_bp = Blueprint('cita', __name__, url_prefix='/citas')

@cita_bp.route('/')
@login_required
def index():
    citas = Cita.query.order_by(Cita.fecha_cita.desc()).all()
    return render_template('cita/index.html', citas=citas)

@cita_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.rol not in ['admin', 'recepcion']:
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    # Obtener pacientes y médicos activos
    pacientes = Paciente.query.filter_by(activo=True).all()
    medicos = Medico.query.filter_by(activo=True).all()
    
    if request.method == 'POST':
        try:
            paciente_id = request.form.get('paciente_id')
            medico_id = request.form.get('medico_id')
            fecha_cita_str = request.form.get('fecha_cita')
            duracion = request.form.get('duracion', 30)
            tipo_consulta = request.form.get('tipo_consulta')
            notas = request.form.get('notas')
            
            # Validaciones
            if not paciente_id or not medico_id or not fecha_cita_str or not tipo_consulta:
                flash('Todos los campos marcados con * son obligatorios', 'danger')
                return render_template('cita/create.html', pacientes=pacientes, medicos=medicos)
            
            # Convertir fecha
            fecha_cita = datetime.fromisoformat(fecha_cita_str)
            
            # Verificar que la fecha no sea en el pasado
            if fecha_cita < datetime.now():
                flash('No se pueden programar citas en fechas pasadas', 'danger')
                return render_template('cita/create.html', pacientes=pacientes, medicos=medicos)
            
            # Crear la cita
            cita = Cita(
                paciente_id=int(paciente_id),
                medico_id=int(medico_id),
                fecha_cita=fecha_cita,
                duracion=int(duracion),
                tipo_consulta=tipo_consulta,
                notas=notas,
                estado='programada'
            )
            
            db.session.add(cita)
            db.session.commit()
            flash('Cita programada exitosamente', 'success')
            return redirect(url_for('cita.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al programar la cita: {str(e)}', 'danger')
            return render_template('cita/create.html', pacientes=pacientes, medicos=medicos)
    
    return render_template('cita/create.html', pacientes=pacientes, medicos=medicos)

@cita_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if current_user.rol not in ['admin', 'recepcion']:
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    cita = Cita.query.get_or_404(id)
    pacientes = Paciente.query.filter_by(activo=True).all()
    medicos = Medico.query.filter_by(activo=True).all()
    
    if request.method == 'POST':
        try:
            paciente_id = request.form.get('paciente_id')
            medico_id = request.form.get('medico_id')
            fecha_cita_str = request.form.get('fecha_cita')
            duracion = request.form.get('duracion')
            tipo_consulta = request.form.get('tipo_consulta')
            notas = request.form.get('notas')
            estado = request.form.get('estado')
            
            # Validaciones
            if not paciente_id or not medico_id or not fecha_cita_str or not tipo_consulta or not estado:
                flash('Todos los campos marcados con * son obligatorios', 'danger')
                return render_template('cita/edit.html', cita=cita, pacientes=pacientes, medicos=medicos)
            
            # Convertir fecha
            fecha_cita = datetime.fromisoformat(fecha_cita_str)
            
            # Actualizar la cita
            cita.paciente_id = int(paciente_id)
            cita.medico_id = int(medico_id)
            cita.fecha_cita = fecha_cita
            cita.duracion = int(duracion)
            cita.tipo_consulta = tipo_consulta
            cita.notas = notas
            cita.estado = estado
            
            db.session.commit()
            flash('Cita actualizada exitosamente', 'success')
            return redirect(url_for('cita.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la cita: {str(e)}', 'danger')
            return render_template('cita/edit.html', cita=cita, pacientes=pacientes, medicos=medicos)
    
    return render_template('cita/edit.html', cita=cita, pacientes=pacientes, medicos=medicos)

@cita_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    if current_user.rol not in ['admin', 'recepcion']:
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    try:
        cita = Cita.query.get_or_404(id)
        
        # Verificar si la cita tiene una consulta asociada
        consulta_asociada = Consulta.query.filter_by(cita_id=id).first()
        if consulta_asociada:
            flash('No se puede eliminar la cita porque tiene una consulta asociada. Elimine la consulta primero.', 'danger')
            return redirect(url_for('cita.index'))
        
        # Si no hay consulta asociada, eliminar la cita
        db.session.delete(cita)
        db.session.commit()
        flash('Cita eliminada exitosamente', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la cita: {str(e)}', 'danger')
    
    return redirect(url_for('cita.index'))

@cita_bp.route('/cancelar/<int:id>')
@login_required
def cancelar(id):
    if current_user.rol not in ['admin', 'recepcion']:
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    try:
        cita = Cita.query.get_or_404(id)
        
        # Verificar si la cita ya tiene una consulta
        consulta_asociada = Consulta.query.filter_by(cita_id=id).first()
        if consulta_asociada:
            flash('No se puede cancelar la cita porque ya tiene una consulta asociada', 'danger')
            return redirect(url_for('cita.index'))
        
        # Solo se pueden cancelar citas programadas o confirmadas
        if cita.estado not in ['programada', 'confirmada']:
            flash('Solo se pueden cancelar citas programadas o confirmadas', 'danger')
            return redirect(url_for('cita.index'))
        
        cita.estado = 'cancelada'
        db.session.commit()
        flash('Cita cancelada exitosamente', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cancelar la cita: {str(e)}', 'danger')
    
    return redirect(url_for('cita.index'))

@cita_bp.route('/completar/<int:id>')
@login_required
def completar(id):
    if current_user.rol not in ['admin', 'recepcion', 'medico']:
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    try:
        cita = Cita.query.get_or_404(id)
        
        # Solo se pueden completar citas programadas o confirmadas
        if cita.estado not in ['programada', 'confirmada']:
            flash('Solo se pueden completar citas programadas o confirmadas', 'danger')
            return redirect(url_for('cita.index'))
        
        cita.estado = 'completada'
        db.session.commit()
        flash('Cita marcada como completada', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al completar la cita: {str(e)}', 'danger')
    
    return redirect(url_for('cita.index'))
@cita_bp.route('/eliminar_con_consulta/<int:id>')
@login_required
def eliminar_con_consulta(id):
    if current_user.rol not in ['admin', 'recepcion']:
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    try:
        cita = Cita.query.get_or_404(id)
        
        # Verificar si la cita tiene una consulta asociada
        consulta_asociada = Consulta.query.filter_by(cita_id=id).first()
        
        if consulta_asociada:
            # Eliminar la consulta asociada primero
            db.session.delete(consulta_asociada)
            flash('Consulta asociada eliminada', 'info')
        
        # Luego eliminar la cita
        db.session.delete(cita)
        db.session.commit()
        flash('Cita y consulta asociada eliminadas exitosamente', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar: {str(e)}', 'danger')
    
    return redirect(url_for('cita.index'))