from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from database import db
from models.usuario_model import Usuario
from models.medico_model import Medico
from models.paciente_model import Paciente
from models.cita_model import Cita
from models.consulta_model import Consulta
from models.factura_model import Factura

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    stats = {
        'total_usuarios': Usuario.query.count(),
        'total_medicos': Medico.query.filter_by(activo=True).count(),
        'total_pacientes': Paciente.query.filter_by(activo=True).count(),
        'citas_hoy': Cita.query.filter(
            db.func.date(Cita.fecha_cita) == db.func.current_date()
        ).count(),
        'consultas_mes': Consulta.query.filter(
            db.func.strftime('%Y-%m', Consulta.fecha_consulta) == db.func.strftime('%Y-%m', 'now')
        ).count(),
        'ingresos_mes': db.session.query(
            db.func.sum(Factura.total)
        ).filter(
            db.func.strftime('%Y-%m', Factura.fecha_emision) == db.func.strftime('%Y-%m', 'now'),
            Factura.estado == 'pagada'
        ).scalar() or 0
    }
    
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/estadisticas')
@login_required
def estadisticas():
    if current_user.rol != 'admin':
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/estadisticas.html')