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

    git clone https://github.com/milancermak/tornado && cd tornado
    sudo python setup.py install 
    apt-get install mongodb python-pymongo

Installing Furnivall
--------------------

::

    python setup.py install 

This will setup a init script in /etc/init.d called "furnivall", so, we'll 
start furnivall with:

::

    invoke-rc.d furnivall start
    # or 
    service furnivall start

