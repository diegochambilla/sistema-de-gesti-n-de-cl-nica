from flask import render_template

def index(especialidades):
    return render_template('especialidad/index.html', especialidades=especialidades)

def create(form):
    return render_template('especialidad/create.html', form=form)

def edit(form, especialidad):
    return render_template('especialidad/edit.html', form=form, especialidad=especialidad)