from functools import wraps
from flask import request, Response
from settings import APP_ROOT
#from eeros_mock import EEROS
import os

def check_auth(username, password):

    fobj = open(os.path.join(APP_ROOT, 'users.txt'), "r")
    for line in fobj:
        userlist = line.split(',')
        head, sep, tail = userlist[0].partition('username: ')
        u_name = tail
        head, sep, tail = userlist[1].partition('password: ')
        u_pwd = tail
        head, sep, tail = userlist[2].partition('full name: ')
        u_fullname = tail        
        if username == u_name and password == u_pwd:
            return username == u_name and password == u_pwd

    fobj.close()
    """No valid user"""
    return username == 'username' and password == 'secret'

def authenticate():
    return Response(
    'Could not verify your access level for EEROS. ', 401,
    {'WWW-Authenticate': 'Basic realm="EEROS Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()

        #e = EEROS("/dev/eeduro")
        #e.open()
        return f(*args, **kwargs)
    return decorated


