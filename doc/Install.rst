Installation instructions
=========================

Dependences
------------
ZODB
tornado


Installing deps
----------------

::

    easy_install tornado ZODB

You should carefully consider installing David Francos' branch at http://www.github.com/XayOn/tornado

Or, if you prefer the PIP method (for wich you'll need to have PIP installed), it will automatically read
dependences from the deps file with this command:

::
    
    pip install -r deps


Installing Furnivall
--------------------

::

    python setup.py install 

Since version 1.0 you can also install it from pypi:

::
    easy_install furnivall

Wich will take care of deps for you.


Packaging furnivall
-------------------
Furnivall's setup.py (got from http://github.com/XayOn/Digenpy ) has 
some nice configurations to allow it to generate debian packages.

::

    python setup.py bdist_deb

eggs

::

    python setup.py bdist_egg


tgz

::

    python setup.py bdist_tgz

Launching Furnivall
-------------------

::

    python Furnivall.py --port=80

TODO
-------------------
This will setup a init script in /etc/init.d called "furnivall", so, we'll 
start furnivall with:

::

    invoke-rc.d furnivall start
    # or 
    service furnivall start


