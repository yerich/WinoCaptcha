"""Usage:
    >>> winolib.get_question() # First time you call this, it would generate wino.db (can take a few seconds).
    {'token': 'SfPFU4dMZgJsamxcWFUY2cE69WbdBEpH6VBsMT0s4',
     'question': "The bus driver knows all about Bryan's dirty secrets simply because he is indiscreet. Who is indiscreet?"}
    >>> winolib.check_answer('SfPFU4dMZgJsamxcWFUY2cE69WbdBEpH6VBsMT0s4','bryan') # Case insensitive
    True
"""
LIBDIR = '/' in __file__ and __file__.rsplit('/',1)[0] or '.'

NUM_QUESTIONS = 1955 # As good as any other number ;)
WINO_DBPATH = '/'.join([LIBDIR,'wino3.db']) # So that we don't clash with legacy wino*.db instances :)
import winograd,shelve,random,re,os

_RE_NONALPHANUM=re.compile('[^a-zA-Z0-9]+')
def _gen_token():
    return _RE_NONALPHANUM.sub('',random._urandom(32).encode('base64'))
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

def get_question(dbpath=WINO_DBPATH):
    """ Returns a random question in the database, and a token that can be used to check the user's answer """
    db = shelve.open(dbpath)
    k = db.keys()
    if not k:
        _populate_db(db)
        k = db.keys()
    t = random.choice(k)
    qa = db[t]
    db.close()
    return {'token':t,'question':qa['q']}

def check_answer(token,answer,dbpath=WINO_DBPATH):
    """ Checks an answer supplied by the user against a question token """
    db = shelve.open(dbpath)
    qa = db.get(token)
    db.close()
    if qa and _dearticlize(answer) in qa['a']:
        return True
    return False
