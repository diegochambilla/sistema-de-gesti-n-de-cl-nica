from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from database import db
from models.receta_model import Receta
from models.consulta_model import Consulta

receta_bp = Blueprint('receta', __name__, url_prefix='/recetas')

@receta_bp.route('/')
@login_required
def index():
    recetas = Receta.query.all()
    return render_template('receta/index.html', recetas=recetas)

@receta_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.rol not in ['admin', 'medico']:
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    consultas = Consulta.query.all()
    
    if request.method == 'POST':
        try:
            consulta_id = request.form.get('consulta_id')
            medicamento = request.form.get('medicamento')
            dosis = request.form.get('dosis')
            frecuencia = request.form.get('frecuencia')
            duracion = request.form.get('duracion')
            instrucciones = request.form.get('instrucciones')
            
            if not consulta_id or not medicamento:
                flash('Consulta y medicamento son obligatorios', 'danger')
                return render_template('receta/create.html', consultas=consultas)
            
            receta = Receta(
                consulta_id=int(consulta_id),
                medicamento=medicamento,
                dosis=dosis,
                frecuencia=frecuencia,
                duracion=duracion,
                instrucciones=instrucciones
            )
            db.session.add(receta)
            db.session.commit()
            flash('Receta creada exitosamente', 'success')
            return redirect(url_for('receta.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la receta: {str(e)}', 'danger')
            return render_template('receta/create.html', consultas=consultas)
    
    return render_template('receta/create.html', consultas=consultas)
# NUEVA RUTA PARA ELIMINAR RECETA
@receta_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    if current_user.rol not in ['admin', 'medico']:
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    receta = Receta.query.get_or_404(id)
    
    try:
        db.session.delete(receta)
        db.session.commit()
        flash('Receta eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la receta: {str(e)}', 'danger')
    
    return redirect(url_for('receta.index'))