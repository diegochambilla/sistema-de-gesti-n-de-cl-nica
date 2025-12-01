from flask import render_template

def index(usuarios):
    return render_template('usuario/index.html', usuarios=usuarios)

def create(form):
    return render_template('usuario/create.html', form=form)

def edit(form, usuario):
    return render_template('usuario/edit.html', form=form, usuario=usuario)