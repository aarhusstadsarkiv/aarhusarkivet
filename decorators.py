from functools import wraps

from flask import session
from flask import redirect

import constants


# Base-authentication decorator
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if constants.SESSION_KEY not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated


def employee_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if constants.SESSION_KEY not in session:
            return redirect('/login')
        elif 'employee' not in session[constants.SESSION_KEY].get('roles', ['user']):
            return redirect('/')
        else:
            return f(*args, **kwargs)
    return decorated


# Use only with all three of my logins
def tester_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if constants.SESSION_KEY not in session:
            return redirect('/login')
        elif 'tester' not in session[constants.SESSION_KEY].get('roles', ['user']):
            return redirect('/')
        else:
            return f(*args, **kwargs)
    return decorated


# Admin-authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if constants.SESSION_KEY not in session:
            return redirect('/login')
        elif 'admin' not in session[constants.SESSION_KEY].get('roles', ['user']):
            return redirect('/')
        else:
            return f(*args, **kwargs)
    return decorated
