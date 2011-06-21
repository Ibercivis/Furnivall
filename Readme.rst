Furnivall
=========
Ibervicis Furnivall is an open source framework for distributed volunteer science. It helps to organize batches of tasks, collect them form volunteers and do all the related housekeeping.

Requeriments
============

The first implementation of the core system is being done under Python, either 2.7 or 3.x should work at the end.
Some parts of the software communicate via TCP/IP so it is possible to have other languages involved, specially for the composition of Views.
See docs/Install.rst for more info

Sample APPS
===========

Branched during summer 2011, you will find, hopefully:

phase 0:
- A plain implementation of a trivial task, in the main branch.
phase 1:
- A system to record environmental data.
- An APP to create a Spanish Corpus of sentiment analysis.
phase 2:
-other ideas: Collection of Geolocalized data (human migrations, bird migrations...) , Analysis of spread of diseases, 


Ideas
=====
- Expansible via plugins
  - Plugin-personalized API
  - After the summer, volunteers will be drafted to create new plugins
- Views
  - Connecting to core via API
- Core
  - Task execution


See more, collaborate
=====================

At this moment:

- Go to the wiki area, https://github.com/Ibercivis/Furnivall/wiki for more info
- Use the https://github.com/Ibercivis/Furnivall/issues?sort=created&direction=desc&state=open&page=1 issue tracker for ideas, discuss, etc or to offer yourself for some work

Use case howto
===============

Let's say we want to start developing one of the previously exposed ideas, we'd had to go trought the following steps:
    - Create a plugin/view with the later described properties
    - Add a researcher via the administration page (if it doesn't exist)
    - Assign a plugin/view to a job (can be multiple jobs) 
    - TODO: Maybe in a future we can make some plugin/view stuff in the web interface

Plugin / views structure
========================
A view must have:
    - The view class name specified in config or web interface
      wich contains:
        At constructor:
            The view's associated plugin filename (see later)
            The view's plugin class, description and name
            Number of workunits it should produce by Default
            View template 
            View urls, wich will be later parsed by tornado.

Example: 

class SampleView(object):
    def __init__(self, creator):
        self.plugin="sample"
        self.class_="SamplePlugin"
        self.name="Sample_View"
        self.description="Sample View"
        self.workunits=3
        self.templates=['SampleView']
        self.urls=[( '/sample/', creator.Scheduler ),] # Only scheduler can manage created jobs!

And about the plugin:
    
