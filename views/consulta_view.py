from flask import render_template

def crear(form):
    return render_template('consulta/crear.html', form=form)

def detalle(consulta):
    return render_template('consulta/detalle.html', consulta=consulta)

def agregar_receta(form, consulta_id):
    return render_template('consulta/agregar_receta.html', form=form, consulta_id=consulta_id)