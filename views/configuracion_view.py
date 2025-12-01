from flask import render_template

def index(configuraciones):
    return render_template('configuracion/index.html', configuraciones=configuraciones)

def create(form):
    return render_template('configuracion/create.html', form=form)

def edit(form, configuracion):
    return render_template('configuracion/edit.html', form=form, configuracion=configuracion)