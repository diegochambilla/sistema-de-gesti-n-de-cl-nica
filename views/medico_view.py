from flask import render_template

def index(medicos):
    return render_template('medico/index.html', medicos=medicos)

def create(form):
    return render_template('medico/create.html', form=form)

def edit(form, medico):
    return render_template('medico/edit.html', form=form, medico=medico)

def horarios(form, medico, horarios):
    return render_template('medico/horarios.html', form=form, medico=medico, horarios=horarios)