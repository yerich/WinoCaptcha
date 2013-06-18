"""Usage:
        >>> winolib.get_question()
        {'token': '51bee4c7XLP0eZjFBiMOjAq8xjPp714Wk7oZ520DrM458Si62go',
         'question': 'Despite the fact that they usually come pretty close to each other, Dawn won against Melissa because she had such a good start. Who had a good start?'}
        >>> winolib.check_answer('51bee4c7XLP0eZjFBiMOjAq8xjPp714Wk7oZ520DrM458Si62go','dawn') # right answer
        True
        >>> `winolib.check_answer('51bee4c7XLP0eZjFBiMOjAq8xjPp714Wk7oZ520DrM458Si62go','dawn')` # replay attempt
        'None'
        >>> winolib.get_question()
        {'token': '51bee51eFgISvqyS0SycT0lp9UWAZAeJkHe5Oif8xR2jWZJLXw',
         'question': "Erica tried to get a coffee with Andrea, but she wasn't available. Who was not available?"}
        >>> winolib.check_answer('51bee51eFgISvqyS0SycT0lp9UWAZAeJkHe5Oif8xR2jWZJLXw','bla') # wrong answer
        False
"""
LIBDIR = '/' in __file__ and __file__.rsplit('/',1)[0] or '.'
MAX_CHALLENGES = 529 # Feel free to increase if you're popular or under a DoS attack :)
DBPATH = '/'.join([LIBDIR,'challenges.db'])

import winograd,shelve,random,re,os,time

_RE_NONALPHANUM=re.compile('[^a-zA-Z0-9]+')
def _gen_token(): # monotonic yet unpredictable
    return hex(int(time.time()))[2:]+_RE_NONALPHANUM.sub('',random._urandom(32).encode('base64'))

def _register_challenge(dbpath,answer):
    token = _gen_token()
    db = shelve.open(dbpath)
    db[token] = answer
    db.sync()
    keys = sorted(db.keys())
    if len(keys)>MAX_CHALLENGES:
        for k in keys[:len(keys)-MAX_CHALLENGES]: # Trim old entries
            try:
                del db[k]
            except KeyError:
                pass
    db.close()
    return token

def _check_response(dbpath,token):
    db = shelve.open(dbpath)
    a = db.get(token)
    if a:
        try:
            del db[token]
        except KeyError:
            pass
    db.close()
    return a
        

_RE_ARTICLE=re.compile('^(a|an|the|his|her|their|our) ')
def _dearticlize(s):
    return _RE_ARTICLE.sub('',s.lower().strip())
    
def get_question(winograd_source='winograd.txt',dbpath=DBPATH):
    """Returns a  question, and a token that can be used to check the user's answer.
This token can't be reused (to avoid a replay attack)"""
    orig_dir = os.path.realpath('.')
    os.chdir(LIBDIR) # TODO: fix it so that winograd.py doesn't need this
    w = winograd.Winograd(winograd_source)
    w.generate()
    os.chdir(orig_dir)
    return {'token':_register_challenge(dbpath,map(_dearticlize,w.answer)),'question':w.question,'dbg':map(_dearticlize,w.answer)}

def check_answer(token,answer,dbpath=DBPATH):
    """Fetches the token's challenge from the db. If it exists, removes it from the db and verifies the user's answer.
Returns True/False if answer was right/wrong, None if token wasn't in the db.
The None result does not necessarily mean it's an attack. This could still be accidental (user hit reload or back button).
When None is returned, app should fail, but not display a "captcha error" message."""
    a = _check_response(dbpath,token)
    if a:
        return _dearticlize(answer) in a # True or False
    else: # Either attack or accidental (user hit reload or back button)
        return None # App should fail, but not show "captcha error"
