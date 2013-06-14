### WinoCaptcha

A Captcha Alternative, based on Winograd Schemas. `python winograd.py` for a demo.

#### The winolib wrapper

This wrapper uses `winograd.py` to generate a `shelve` db of preset questions.
It provides access to questions and verification of answers in a way that is practical for stateless web applications:

        >>> from WinoCaptcha import winolib
        >>> winolib.get_question() # First time you call this, it would generate wino.db (can take a few seconds).
            {'token': 'SfPFU4dMZgJsamxcWFUY2cE69WbdBEpH6VBsMT0s4',
             'question': "The bus driver knows all about Bryan's dirty secrets simply because he is indiscreet. Who is indiscreet?"}
        >>> winolib.check_answer('SfPFU4dMZgJsamxcWFUY2cE69WbdBEpH6VBsMT0s4','bryan') # Case insensitive
            True
