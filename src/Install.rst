Installation instructions
=========================

Dependences
------------
tornado-sessions
mongodb
python mongodb support ( python-pymongo package on debian ) 

Currently, furnivall only depends on tornado-sessions web server, the tornado
fork by milancemark wich adds sessions to tornado, mongodb to store the 
sessions and its python libs.

Installing deps
----------------

::

    easy_install tornado

You should carefully consider installing David Francos' branch at http://www.github.com/XayOn/tornado

Installing Furnivall
--------------------

::

    python setup.py install 

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


