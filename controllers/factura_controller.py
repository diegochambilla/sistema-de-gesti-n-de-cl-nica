from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from database import db
from models.factura_model import Factura
from models.paciente_model import Paciente
from forms.factura_forms import FacturaForm

factura_bp = Blueprint('factura', __name__, url_prefix='/facturas')

@factura_bp.route('/')
@login_required
def index():
    facturas = Factura.query.all()
    return render_template('factura/index.html', facturas=facturas)

@factura_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.rol not in ['admin', 'recepcion']:
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    form = FacturaForm()
    form.paciente_id.choices = [(p.id, f"{p.nombre} {p.apellido}") for p in Paciente.query.filter_by(activo=True).all()]
    
    if form.validate_on_submit():
        factura = Factura(
            paciente_id=form.paciente_id.data,
            numero_factura=form.numero_factura.data,
            fecha_emision=form.fecha_emision.data,
            subtotal=form.subtotal.data,
            impuesto=form.impuesto.data,
            total=form.total.data,
            estado=form.estado.data,
            metodo_pago=form.metodo_pago.data
        )
        db.session.add(factura)
        db.session.commit()
        flash('Factura creada exitosamente', 'success')
        return redirect(url_for('factura.index'))
    
    return render_template('factura/create.html', form=form)

@factura_bp.route('/detalle/<int:id>')
@login_required
def detalle(id):
    factura = Factura.query.get_or_404(id)
    return render_template('factura/detalle.html', factura=factura)

@factura_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    if current_user.rol not in ['admin', 'recepcion']:
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    factura = Factura.query.get_or_404(id)
    db.session.delete(factura)
    db.session.commit()
    flash('Factura eliminada exitosamente', 'success')
    return redirect(url_for('factura.index'))