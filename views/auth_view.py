from flask import render_template

def login(form):
    return render_template('auth/login.html', form=form)

def register(form):
    return render_template('auth/register.html', form=form)