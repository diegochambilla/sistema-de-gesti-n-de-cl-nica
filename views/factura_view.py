from flask import render_template

def index(facturas):
    return render_template('factura/index.html', facturas=facturas)

def create(form):
    return render_template('factura/create.html', form=form)

def detalle(factura):
    return render_template('factura/detalle.html', factura=factura)