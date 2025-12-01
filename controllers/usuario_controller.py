from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from database import db
from models.usuario_model import Usuario
from forms.usuario_forms import UsuarioForm
from werkzeug.security import generate_password_hash

# Asegúrate de que esta línea esté correcta - sin espacios extra
usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuarios')

# Importar todos los modelos relacionados
try:
    from models.medico_model import Medico
except ImportError:
    Medico = None

try:
    from models.cita_model import Cita
except ImportError:
    Cita = None

try:
    from models.consulta_model import Consulta
except ImportError:
    Consulta = None

try:
    from models.receta_model import Receta
except ImportError:
    Receta = None

try:
    from models.factura_model import Factura
except ImportError:
    Factura = None

@usuario_bp.route('/')
@login_required
def index():
    if current_user.rol != 'admin':
        flash('No tienes permisos para ver esta página', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    usuarios = Usuario.query.all()
    return render_template('usuario/index.html', usuarios=usuarios)

@usuario_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.rol != 'admin':
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    form = UsuarioForm()
    if form.validate_on_submit():
        # Verificar si el username ya existe
        existing_user = Usuario.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('El nombre de usuario ya existe', 'danger')
            return render_template('usuario/create.html', form=form)
        
        # Verificar si el email ya existe
        existing_email = Usuario.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('El email ya está registrado', 'danger')
            return render_template('usuario/create.html', form=form)
        
        hashed_password = generate_password_hash(form.password.data) if form.password.data else ''
        usuario = Usuario(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            rol=form.rol.data,
            activo=form.activo.data
        )
        db.session.add(usuario)
        db.session.commit()
        flash('Usuario creado exitosamente', 'success')
        return redirect(url_for('usuario.index'))
    
    return render_template('usuario/create.html', form=form)

@usuario_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if current_user.rol != 'admin':
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    usuario = Usuario.query.get_or_404(id)
    form = UsuarioForm(obj=usuario)
    
    if form.validate_on_submit():
        # Verificar si el username ya existe (excluyendo el usuario actual)
        existing_user = Usuario.query.filter(
            Usuario.username == form.username.data,
            Usuario.id != id
        ).first()
        if existing_user:
            flash('El nombre de usuario ya existe', 'danger')
            return render_template('usuario/edit.html', form=form, usuario=usuario)
        
        # Verificar si el email ya existe (excluyendo el usuario actual)
        existing_email = Usuario.query.filter(
            Usuario.email == form.email.data,
            Usuario.id != id
        ).first()
        if existing_email:
            flash('El email ya está registrado', 'danger')
            return render_template('usuario/edit.html', form=form, usuario=usuario)
        
        usuario.username = form.username.data
        usuario.email = form.email.data
        if form.password.data:
            usuario.password = generate_password_hash(form.password.data)
        usuario.rol = form.rol.data
        usuario.activo = form.activo.data
        
        db.session.commit()
        flash('Usuario actualizado exitosamente', 'success')
        return redirect(url_for('usuario.index'))
    
    return render_template('usuario/edit.html', form=form, usuario=usuario)

@usuario_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    if current_user.rol != 'admin':
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    usuario = Usuario.query.get_or_404(id)
    
    # Verificar si es el usuario actual
    if usuario.id == current_user.id:
        flash('No puedes eliminar tu propio usuario', 'danger')
        return redirect(url_for('usuario.index'))
    
    # Contar dependencias antes de eliminar
    dependencias = []
    
    # Verificar relaciones con médicos
    if Medico is not None:
        medicos_count = Medico.query.filter_by(usuario_id=usuario.id).count()
        if medicos_count > 0:
            dependencias.append(f"{medicos_count} médico(s)")
    
    # Si hay dependencias, mostrar advertencia
    if dependencias:
        flash(f'No se puede eliminar el usuario porque está asociado a: {", ".join(dependencias)}. Primero desasocia estas relaciones.', 'danger')
        return redirect(url_for('usuario.index'))
    
    try:
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuario eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar usuario: {str(e)}', 'danger')
    
    return redirect(url_for('usuario.index'))
# ... (todo tu código existente)

# AGREGAR ESTAS RUTAS NUEVAS AL FINAL DEL ARCHIVO

@usuario_bp.route('/disassociate/<int:id>')
@login_required
def disassociate(id):
    """Desasociar médico del usuario antes de eliminar"""
    if current_user.rol != 'admin':
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    usuario = Usuario.query.get_or_404(id)
    
    # Verificar si es el usuario actual
    if usuario.id == current_user.id:
        flash('No puedes desasociar tu propio usuario', 'danger')
        return redirect(url_for('usuario.index'))
    
    try:
        # Desasociar médicos
        if Medico is not None:
            medicos = Medico.query.filter_by(usuario_id=usuario.id).all()
            for medico in medicos:
                medico.usuario_id = None  # Desasociar sin eliminar el médico
            
            db.session.commit()
            flash(f'Se desasociaron {len(medicos)} médico(s) del usuario', 'success')
        else:
            flash('No hay médicos para desasociar', 'info')
            
    except Exception as e:
        db.session.rollback()
        flash(f'Error al desasociar: {str(e)}', 'danger')
    
    return redirect(url_for('usuario.index'))

@usuario_bp.route('/force-delete/<int:id>')
@login_required
def force_delete(id):
    """Eliminar usuario incluso si tiene dependencias"""
    if current_user.rol != 'admin':
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    usuario = Usuario.query.get_or_404(id)
    
    # Verificar si es el usuario actual
    if usuario.id == current_user.id:
        flash('No puedes eliminar tu propio usuario', 'danger')
        return redirect(url_for('usuario.index'))
    
    try:
        # Primero desasociar médicos
        if Medico is not None:
            medicos = Medico.query.filter_by(usuario_id=usuario.id).all()
            for medico in medicos:
                medico.usuario_id = None
        
        # Luego eliminar el usuario
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuario eliminado exitosamente (médicos desasociados)', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar usuario: {str(e)}', 'danger')
    
    return redirect(url_for('usuario.index'))