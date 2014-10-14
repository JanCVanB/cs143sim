***************************************
reStructuredText Code Reference Example
***************************************

   Auto-documentation example for :download:`reSTCodeReferenceModule.py`

   This is something I want to say that is not in my my_function docstring,
   because I'm about to auto-document ONLY that.

   IF YOU LEAVE MEMBERS BLANK IT WILL AUTODOCUMENT EVERYTHING.
   The ":noindex:" is only for if you've indexed your module with ".. module::"

   *Below this is documentation from reSTCodeReferenceModule.my_function*

-----

   .. automodule:: reSTCodeReferenceModule
      :members: my_function
      :noindex:

-----

   *Above this is documentation from reSTCodeReferenceModule.my_function*

   This is something I want to say that is not in some MyClass docstrings,
   because I'm about to auto-document ONLY some MyClass methods.

   *Below this is documentation from reSTCodeReferenceModule.MyClass*

-----

   .. autoclass:: MyClass
      :members: calcPythagorean, run
      :exclude-members: uselessFunction
      :noindex:

-----

   *Above this is documentation from reSTCodeReferenceModule.MyClass*
