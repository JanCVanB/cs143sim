'''
.. module:: reSTCodeReferenceModule
   :platform: Unix, Windows
   :synopsis: Example for documenting python code with ReST

.. moduleauthor:: Jan Van Bruggen <jancvanbruggen@gmail.com>

This module does a lot of things. Well, not really, it honestly just shows you
how to document your code with restructured text. I apologize for the
verbosity, I'm just trying to have big paragraphs for you guys to see. I'm also
keeping my lines under 80 characters so everyone's text editors can display
them correctly.

**This is bold because of how important it is.** *However, this is italicized
because of how fancy that makes it look.*

Link to a website:

- `<http://www.google.com>`_
- `Google <http://www.google.com>`_
- `TheGoogle`_

.. _TheGoogle: http://www.google.com

Include images:

.. image:: _static/network.png
    :align: center
    :width: 150

Include raw html:

.. raw:: html

   <div align="center"
        style="background-color:#0000FF; color:#FFFFFF">
     blue div
   </div>


Include a code snippet::

   for i in range(3):
       print(i)

   print('added colon')

With good colon formatting ::

   print('no colon')

Like so

::

   print('also no colon')

'''

import math

def my_function(var):
    '''Sample function for showing doumentation syntax

    :param int var: some value
    :return: the input parameter
    :rtype: int
    '''
    return var


class MyClass():
    '''Sample for showing documentation syntax and the Pythagorean Theorem

    :param var1: a variable that does stuff
    :type var1: float
    :param str var2: you can combine parameter type and description, if the
       type is a single word
    :param var3: you can't combine this parameter type with the description, as
       it can be multiple types
    :type var3: bool or None
    :ivar output: the intended output
    :raises AssertionError: if var3 is not a bool or None
    '''
    def __init__(self, var1=0.0, var2='', var3=True):
        self.var1 = var1
        self.var2 = var2
        assert type(var3) == str or type(var3) == None
        self.var3 = var3
        self.output = None

    def calcPythagorean(self, arg1, arg2):
        '''The first method of my class

        :param int arg1: the first argument
        :param int arg2: the second argument
        :return: the square root of the sum of arg1 and arg2
        :rtype: float
        '''
        x = arg1 * 2
        y = arg2 * 3
        z = math.sqrt(x + y)
        return z

    def setOutput(self):
        '''The second method of my class, which sets :attr:`output`'''
        self.output = self.var1 + self.var2 + self.var3

    def run(self):
        '''The run method of my class'''
        self.calcPythagorean(self.var1, self.var2)
        self.setOutput()

    def uselessFunction(self):
        return None
