'''

    a session wrapper for beaker.session

    usage:

        session.get('key')

        session.set('key', 'value')
        
        #beaker will persist automatically, should not call the function in your code.
        session.save()


'''

from bottle import request

def _session():
    return request.environ.get('beaker.session')

def exist():
    session_obj = _session()
    return session_obj != None and session_obj.has_key("user")

def has_key(key):
    return _session().has_key(key)

def get(key):
    return _session()[key] if _session().has_key(key) else ''

def put(key, value):
    _session()[key] = value

def save():
    _session().save()

def delete():
    _session().delete()










