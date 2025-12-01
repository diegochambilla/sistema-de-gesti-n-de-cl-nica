from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from database import db
from models.configuracion_model import Configuracion

configuracion_bp = Blueprint('configuracion', __name__, url_prefix='/configuracion')

@configuracion_bp.route('/')
@login_required
def index():
    if current_user.rol != 'admin':
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    configuraciones = Configuracion.query.all()
    return render_template('configuracion/index.html', configuraciones=configuraciones)

@configuracion_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.rol != 'admin':
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        try:
            clave = request.form.get('clave')
            valor = request.form.get('valor')
            descripcion = request.form.get('descripcion')
            
            if not clave or not valor:
                flash('Clave y valor son obligatorios', 'danger')
                return render_template('configuracion/create.html')
            
            # Verificar si la clave ya existe
            if Configuracion.query.filter_by(clave=clave).first():
                flash('La clave ya existe', 'danger')
                return render_template('configuracion/create.html')
            
            configuracion = Configuracion(
                clave=clave,
                valor=valor,
                descripcion=descripcion
            )
            db.session.add(configuracion)
            db.session.commit()
            flash('Configuración creada exitosamente', 'success')
            return redirect(url_for('configuracion.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la configuración: {str(e)}', 'danger')
            return render_template('configuracion/create.html')
    
    return render_template('configuracion/create.html')

@configuracion_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if current_user.rol != 'admin':
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    configuracion = Configuracion.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            clave = request.form.get('clave')
            valor = request.form.get('valor')
            descripcion = request.form.get('descripcion')
            
            if not clave or not valor:
                flash('Clave y valor son obligatorios', 'danger')
                return render_template('configuracion/edit.html', configuracion=configuracion)
            
            # Verificar si la clave ya existe (excluyendo la actual)
            existing = Configuracion.query.filter_by(clave=clave).first()
            if existing and existing.id != configuracion.id:
                flash('La clave ya existe', 'danger')
                return render_template('configuracion/edit.html', configuracion=configuracion)
            
            configuracion.clave = clave
            configuracion.valor = valor
            configuracion.descripcion = descripcion
            
            db.session.commit()
            flash('Configuración actualizada exitosamente', 'success')
            return redirect(url_for('configuracion.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la configuración: {str(e)}', 'danger')
            return render_template('configuracion/edit.html', configuracion=configuracion)
    
    return render_template('configuracion/edit.html', configuracion=configuracion)

@configuracion_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    if current_user.rol != 'admin':
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    try:
        configuracion = Configuracion.query.get_or_404(id)
        db.session.delete(configuracion)
        db.session.commit()
        flash('Configuración eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la configuración: {str(e)}', 'danger')
    
    return redirect(url_for('configuracion.index'))