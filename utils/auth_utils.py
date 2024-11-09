# auth_utils.py
from functools import wraps
from flask import session, flash, redirect, url_for, request

def login_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Debes iniciar sesión para acceder a esta página.', 'warning')
            # Guardar la URL actual a la que el usuario intentaba acceder
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorador