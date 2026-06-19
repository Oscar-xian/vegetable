from flask import g,redirect
from functools import wraps

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if g.user :
            return func(*args, **kwargs)
        else:
            return redirect('/login')
    return wrapper

