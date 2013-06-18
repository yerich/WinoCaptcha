### WinoCaptcha

A Captcha Alternative, based on [Winograd Schemas](http://www.cs.toronto.edu/~hector/Papers/winograd.pdf). `python winograd.py` for a demo.

Question and answer generator written by [Richard Ye](http://www.github.com/yerich), winolib wrapper and web integration written by [The Dod](https://dubiousdod.org/thedod).

#### The winolib wrapper

This wrapper uses `winograd.py` to generate a challenge and verify a user's answer to such a challenge in a way that is practical for stateless web applications.

Each challenge has a token that can only be used once (to avoid replay and brute-force attacks),
but since a replay can also happen by accident (reload, back button, etc.), there's a distinct failure mode
for an "attack or honest mistake" where winolib returns `None` (as opposed to the `False` it returns when the user fails the captcha test).

When `None` is returned, best is to fail (e.g. redisplays the form) *without* displaying a [confusing and untrue] "captcha failed" error.

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

#### License

The MIT License (MIT)

Copyright (c) 2013 [Richard Ye](http://www.github.com/yerich) and [The Dod](https://dubiousdod.org/thedod).

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
