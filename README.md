### WinoCaptcha

A Captcha Alternative, based on [Winograd Schemas](http://www.cs.toronto.edu/~hector/Papers/winograd.pdf). `python winograd.py` for a demo.

#### License

The MIT License (MIT)

Copyright (c) 2013 Richard Ye and Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

#### The winolib wrapper

This wrapper uses `winograd.py` to generate a `shelve` db of preset questions.
It provides access to questions and verification of answers in a way that is practical for stateless web applications:

        >>> from WinoCaptcha import winolib
        >>> winolib.get_question() # First time you call this, it would generate wino.db (can take a few seconds).
            {'token': 'SfPFU4dMZgJsamxcWFUY2cE69WbdBEpH6VBsMT0s4',
             'question': "The bus driver knows all about Bryan's dirty secrets simply because he is indiscreet. Who is indiscreet?"}
        >>> winolib.check_answer('SfPFU4dMZgJsamxcWFUY2cE69WbdBEpH6VBsMT0s4','bryan') # Case insensitive
            True
