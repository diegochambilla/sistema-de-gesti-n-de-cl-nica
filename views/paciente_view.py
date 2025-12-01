from flask import render_template

def index(pacientes):
    return render_template('paciente/index.html', pacientes=pacientes)

def create(form):
    return render_template('paciente/create.html', form=form)

def edit(form, paciente):
    return render_template('paciente/edit.html', form=form, paciente=paciente)