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
It provides access to questions and verification of answers in a way that is practical for stateless web applications.
Captcha questions get a onetime token to avoid replay attacks.

        >>> from WinoCaptcha import winolib
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
