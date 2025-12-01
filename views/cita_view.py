from flask import render_template

def index(citas):
    return render_template('cita/index.html', citas=citas)

def create(form):
    return render_template('cita/create.html', form=form)

def edit(form, cita):
    return render_template('cita/edit.html', form=form, cita=cita)