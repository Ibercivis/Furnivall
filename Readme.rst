Furnivall
=========

Ibervicis Furnivall is an open source framework for distributed volunteer science.
It helps to organize batches of tasks, collect them form volunteers
and it does all the related housekeeping.
A popular similar work is Bossa. Also, Furnivall is heavily inspired in BOINC.

The name
---------
Dr Frederick James Furnivall organized a team of distributed volunteer work
to build the Oxford dictionary. Incidentally, he was also the founder of the
Furnivall Sculling Club.

Requeriments
------------

The first implementation of the core system is being done with Python,
either 2.7 or 3.x should work at the end.

Some parts of the software communicate via TCP/IP so it is possible to
have other languages involved, specially for the composition of Views.

See docs/Install.rst for more info

Sample APPS
-----------

Branched during summer 2011, you will find, hopefully:

- Phase 0:
    + A plain implementation of a trivial task, in the main branch.
- Phase 1
    + A system to record environmental data.
    + An APP to create a Spanish Corpus of sentiment analysis.
- Phase 2
    + other ideas: Collection of Geolocalized data (human migrations, bird migrations...) , Analysis of spread of diseases, 

See more, collaborate
---------------------

At this moment:

- Go to the wiki area, https://github.com/Ibercivis/Furnivall/wiki for more info
- Use the https://github.com/Ibercivis/Furnivall/issues?sort=created&direction=desc&state=open&page=1 issue tracker for ideas, discuss, etc or to offer yourself for some work



Expected output
----------------

Furnivall will have:

* A system of plugins separated from the core, to allow both for expansions and for customisations
* A way to distribute the core system across sites, allowing for high availability
* Whatever you want. Simply ask a Issue to the tracker, under milestone Improvements.

Development Plan
------------------

1. Ability to Run single site, with Asociative Paths.
2. Ability to Run single site, with Vivienda and Sentimiento. 
3. Multiple Site, redundancy, ...
4. Pluggable. Apps para mapeo de enfermedades (deteccion via twitter?), para migraciones de pájaros, para mapas de ermitas, ....

Work method
------------

* A public activity page is to be at http://ibercivis.github.com/Furnivall/  Yes, it is edited in the gh-pages branch. 
* Github issue tracker https://github.com/Ibercivis/Furnivall/issues  is to be used for main discussions, up to the level of user histories
* The core development will use PivotalTracker https://www.pivotaltracker.com/projects/274169 for finer work. 
* * Ideally, a Discuss issue (and most others) should move to "Assigned" only when its implications have been translated to the IceBox of Pivotal. Then the Assigned person should be reponsible for the closing in Pivotal and eventually the Closing in Github issue tracker.
* * Pivotal esta enlazado con github de forma que los commit se pueden marcar para que muevan tareas en el pivotal.
* Documentation, if not in the source code, goes here

Proposals for organization of the system
-------------------------------------------

.. image:: http://yuml.me/diagram/scruffy/class/73e07696.png
.. image:: http://yuml.me/diagram/scruffy;/class/%23%20Cool%20Class%20Diagram,%20%5BCore%7CAPI%20Exporter%5D%20%3C%20-%20Extends%20%20%5BPlugins%7CAPI%20Exporter;%20Task%20Manager;%20Administration%5D,%20%5BCore%5D%20%3C%20-%20%3E%20%5BViews%5D,%20%5BPlugins%5D%3C%20Extends%20via%20API%20-%20API%20%3E%20%5BExternal%20Plugins%7CAPI%20Exporter%5D.png
 
Interaction between objects
----------------------------

If not marked otherwise, the objects are Instances. Not to be confused with modules nor class objects.


