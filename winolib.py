"""Usage:
    >>> winolib.get_question() # First time you call this, it would generate wino.db (can take a few seconds).
    {'token': 'SfPFU4dMZgJsamxcWFUY2cE69WbdBEpH6VBsMT0s4',
     'question': "The bus driver knows all about Bryan's dirty secrets simply because he is indiscreet. Who is indiscreet?"}
    >>> winolib.check_answer('SfPFU4dMZgJsamxcWFUY2cE69WbdBEpH6VBsMT0s4','bryan') # Case insensitive
    True
"""
LIBDIR = '/' in __file__ and __file__.rsplit('/',1)[0] or '.'

NUM_QUESTIONS = 1955 # As good as any other number ;)
NUM_ONETIME_TOKENS = 529 # Also good
WINO_DBPATH = '/'.join([LIBDIR,'wino3.db']) # So that we don't clash with legacy wino*.db instances :)
ONETIME_DBPATH = '/'.join([LIBDIR,'onetime.db']) # A small onetime token db against replay attacks
import winograd,shelve,random,re,os,time

_RE_NONALPHANUM=re.compile('[^a-zA-Z0-9]+')
def _gen_token():
    return _RE_NONALPHANUM.sub('',random._urandom(32).encode('base64'))

def _register_onetime_answer(otpath,answer):
    token = hex(int(time.time()))[2:]+_gen_token() # monotonic yet unpredictable
    db = shelve.open(otpath)
    db[token] = answer
    db.sync()
    keys = sorted(db.keys())
    if len(keys)>NUM_ONETIME_TOKENS:
        for k in keys[:len(keys)-NUM_ONETIME_TOKENS]: # Trim old entries
            try:
                del db[k]
            except KeyError:
                pass
    db.close()
    return token

def _get_onetime_answer(otpath,token):
    db = shelve.open(otpath)
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
    

def _populate_db(db,winograd_source='winograd.txt',num_questions=NUM_QUESTIONS):
    """ Generates the initial winograd database. Should normaly be run once (by makewino.py) """
    orig_dir = os.path.realpath('.')
    os.chdir(LIBDIR) # winograd.py needs this
    for i in xrange(num_questions):
        token = _gen_token()
        w = winograd.Winograd(winograd_source)
        w.generate()
        db[token] = {'q': w.question,'a':map(_dearticlize,w.answer)} 
    os.chdir(orig_dir)

def get_question(dbpath=WINO_DBPATH,otpath=ONETIME_DBPATH):
    """Returns a random question in the database, and a token that can be used to check the user's answer.
This token can't be reused (to avoid a replay attack)"""
    db = shelve.open(dbpath)
    k = db.keys()
    if not k:
        _populate_db(db)
        k = db.keys()
    qa = db[random.choice(k)]
    db.close()
    return {'token':_register_onetime_answer(otpath,qa['a']),'question':qa['q']}

def check_answer(token,answer,otpath=ONETIME_DBPATH):
    """Checks an answer supplied by the user against a onetime token
Returns True/False in answer was right/wrong, None if token wasn't in the db.
The None result does not necessarily mean it's an attack. This could still be accidental (user hit reload or back button).
When None is returned, app should fail, but not display a "captcha error" message."""
    a = _get_onetime_answer(otpath,token)
    if a:
        return _dearticlize(answer) in a # True or False
    else: # Either attack or accidental (user hit reload or back button)
        return None # App should fail, but not show "captcha error"
