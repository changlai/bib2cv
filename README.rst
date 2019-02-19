Converting your bib file to cv section
===============

This project enables you to convert your bib database (if you collect your
publications in a bib file as me) into a latex cv subsection. After your bib
database is updated, recompile your cv and it's updated automatically. 

This tool is in the very initial version with limited bibtex entry and field
types, as well as limited publication types. And only IEEE citation style is
supported now. More features will be supported later or per request.

Installing
----------

bib2cv is based on biblib. Please install it first.
https://github.com/aclements/biblib

Copy `bib2cv.py` to  any convenient local place.

If you want to compile python code inside your latex file, please install
python.sty at 
https://github.com/changlai/python-sty

Using
-----

In a terminal, input::

    python bib2cv.py example.bib

Make sure example.bib is accessible.

To show your name in bold, add the --user(-u) argument::

    python bib2cv.py -u last,first example.bib

The user name format is "last,first".

Package content
---------------

bib2cv.py
    A python tool that enables you to convert your bib database to your cv
    subsection.    

example.bib
    Example bib database.

example.tex 
    Example cv tex file. Install python.sty first to compile this example.
