from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from database import db
from models.consulta_model import Consulta
from models.cita_model import Cita
from datetime import datetime

consulta_bp = Blueprint('consulta', __name__, url_prefix='/consultas')

@consulta_bp.route('/')
@login_required
def index():
    """Lista todas las consultas"""
    consultas = Consulta.query.order_by(Consulta.fecha_consulta.desc()).all()
    return render_template('consulta/index.html', consultas=consultas)

@consulta_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    if current_user.rol not in ['admin', 'medico']:
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    # Obtener citas disponibles para consulta
    citas_disponibles = Cita.query.filter_by(estado='programada').all()
    
    if request.method == 'POST':
        try:
            cita_id = request.form.get('cita_id')
            fecha_consulta_str = request.form.get('fecha_consulta')
            sintomas = request.form.get('sintomas')
            diagnostico = request.form.get('diagnostico')
            tratamiento = request.form.get('tratamiento')
            observaciones = request.form.get('observaciones')
            peso = request.form.get('peso')
            altura = request.form.get('altura')
            presion_arterial = request.form.get('presion_arterial')
            temperatura = request.form.get('temperatura')
            costo = request.form.get('costo')
            
            # Validaciones básicas
            if not cita_id or not fecha_consulta_str or not costo:
                flash('Cita, fecha y costo son obligatorios', 'danger')
                return render_template('consulta/crear.html', citas=citas_disponibles)
            
            # Convertir fecha
            fecha_consulta = datetime.fromisoformat(fecha_consulta_str)
            
            # Obtener la cita para obtener paciente y médico
            cita = Cita.query.get(int(cita_id))
            if not cita:
                flash('Cita no encontrada', 'danger')
                return render_template('consulta/crear.html', citas=citas_disponibles)
            
            # Crear la consulta
            consulta = Consulta(
                cita_id=int(cita_id),
                paciente_id=cita.paciente_id,
                medico_id=cita.medico_id,
                fecha_consulta=fecha_consulta,
                sintomas=sintomas,
                diagnostico=diagnostico,
                tratamiento=tratamiento,
                observaciones=observaciones,
                peso=float(peso) if peso else None,
                altura=float(altura) if altura else None,
                presion_arterial=presion_arterial,
                temperatura=float(temperatura) if temperatura else None,
                costo=float(costo)
            )
            
            # Actualizar estado de la cita
            cita.estado = 'completada'
            
            db.session.add(consulta)
            db.session.commit()
            flash('Consulta creada exitosamente', 'success')
            return redirect(url_for('consulta.detalle', id=consulta.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la consulta: {str(e)}', 'danger')
            return render_template('consulta/crear.html', citas=citas_disponibles)
    
    return render_template('consulta/crear.html', citas=citas_disponibles)

@consulta_bp.route('/detalle/<int:id>')
@login_required
def detalle(id):
    consulta = Consulta.query.get_or_404(id)
    return render_template('consulta/detalle.html', consulta=consulta)

@consulta_bp.route('/agregar_receta/<int:consulta_id>', methods=['GET', 'POST'])
@login_required
def agregar_receta(consulta_id):
    if current_user.rol not in ['admin', 'medico']:
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    consulta = Consulta.query.get_or_404(consulta_id)
    
    if request.method == 'POST':
        medicamento = request.form.get('medicamento')
        dosis = request.form.get('dosis')
        frecuencia = request.form.get('frecuencia')
        duracion = request.form.get('duracion')
        instrucciones = request.form.get('instrucciones')
        
        if not medicamento:
            flash('El medicamento es obligatorio', 'danger')
            return render_template('consulta/agregar_receta.html', consulta=consulta)
        
        from models.receta_model import Receta
        receta = Receta(
            consulta_id=consulta_id,
            medicamento=medicamento,
            dosis=dosis,
            frecuencia=frecuencia,
            duracion=duracion,
            instrucciones=instrucciones
        )
        db.session.add(receta)
        db.session.commit()
        flash('Receta agregada exitosamente', 'success')
        return redirect(url_for('consulta.detalle', id=consulta_id))
    
    return render_template('consulta/agregar_receta.html', consulta=consulta)
# NUEVA RUTA PARA ELIMINAR CONSULTA
@consulta_bp.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    """Eliminar una consulta y sus recetas asociadas"""
    if current_user.rol not in ['admin', 'medico']:
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    consulta = Consulta.query.get_or_404(id)
    
    try:
        # Verificar si tiene recetas asociadas
        from models.receta_model import Receta
        recetas_asociadas = Receta.query.filter_by(consulta_id=id).all()
        
        # Eliminar recetas asociadas primero
        for receta in recetas_asociadas:
            db.session.delete(receta)
        
        # Restaurar el estado de la cita a "programada" si existe
        if consulta.cita:
            consulta.cita.estado = 'programada'
        
        # Eliminar la consulta
        db.session.delete(consulta)
        db.session.commit()
        
        flash(f'Consulta eliminada exitosamente. Se eliminaron {len(recetas_asociadas)} receta(s) asociadas.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la consulta: {str(e)}', 'danger')
    
    return redirect(url_for('consulta.index'))