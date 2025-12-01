from flask import render_template

def dashboard(stats):
    return render_template('admin/dashboard.html', stats=stats)

def estadisticas():
    return render_template('admin/estadisticas.html')