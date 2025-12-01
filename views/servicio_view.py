from flask import render_template

def index(servicios):
    return render_template('servicio/index.html', servicios=servicios)

def create(form):
    return render_template('servicio/create.html', form=form)

def edit(form, servicio):
    return render_template('servicio/edit.html', form=form, servicio=servicio)