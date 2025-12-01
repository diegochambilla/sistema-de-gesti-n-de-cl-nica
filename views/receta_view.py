from flask import render_template

def index(recetas):
    return render_template('receta/index.html', recetas=recetas)

def create(form):
    return render_template('receta/create.html', form=form)