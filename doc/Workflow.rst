Usage workflow
================

Let's say we want to start developing one of the previously exposed ideas, we'd had to go trought the following steps:

- Create a plugin/view with the later described properties
- Add a researcher via the administration page (if it doesn't exist)
- Assign a plugin/view to a job (can be multiple jobs) 
- TODO: Maybe in a future we can make some plugin/view stuff in the web interface

Plugin / views structure
........................
A view must have:

- The view class name specified in config or web interface wich contains:
- At constructor:
    + The view's associated plugin filename (see later), wich we'll load on request.
    + The view's plugin class (wich allows us to have multiple views for a single plugin), description and name
    + Number of workunits it should produce by Default (one, by default)
    + A dictionary of view templates/urls to export. They'll be exported in the form view/viewName/url
    + View urls, wich will be later parsed by tornado.

::

    class SampleView(object):
        def __init__(self, creator):
            self.plugin="sample"
            self.class_="SamplePlugin"
            self.name="Sample_View"
            self.description="Sample View"
            self.workunits=1
            self.templates={'foobar': 'SampleView'} # This will be http://localhost/view/Sample_View/foobar and will render Templates/SampleView

And about the plugin:

- It must have a validate_task and consolidate_result class. 
- task_executor class gets the parent, it's where all main code should reside.

::

    class SamplePlugin(object):
        def __init__(self):
            """
                Sample plugin, containing validation and consolidation functions
            """
            self.description="Test plugin"


        def task_executor(self, parent):
            """
                This is where the main code should be
            """
            while True:
                logging.info("Foobar")

        def validate_task(self, result, async):
            """
                Validate task.
            """
            return True

        def consolidate_result(self, results):
            """
                Make results consolidation for a workunit here.
            """
            return results


After we've developed the plugin, our researcher will have to go trought the following steps to get it working.

Admin page
+++++++++++

.. image:: images/admin.png

* Initialize a view, selecting it from the users' views selectbox.
* Create a job based on that initialized view object, after reloading the page (this will be done with ajax at some point)
    - This creates the number of workunits provided in the plugins' initialization code. (this will be done manually)
    - Each workunit creats a predefined number of tasks, wich we can increase from the admin panel, clicking on the workunit's link.
        * Researcher assigns as much tasks as he wants to workunit
    - Tasks are automatically assigned as future objects, thus being in a separate thread.
        * Tasks objects automatically assign this object to its parent (workunit)

From now on, the plugin itself have to define part of the workflow, the part involving the volunteer, wich will have to look like this:

If the plugin defines a minium tasks to be being executed, it will have to deal with user re-asignment (as they're created with the user object pointing to the researcher), this applyes too if we create them via the current root admin page, while it's planned for it to have a user administration page where you could manually assign tasks to the user, it's not initially. Note that you'll have to mark the task as assigned if you don't want any other user to steal it.

Otherwise you just have to call the url with assign_task_to_user and the object will end being that user's object.

Random ideas
+++++++++++++

- You can define your plugin handler to be a XMLRPCHandler subclass instead of just a RequestHandler, this will allow you to easily write an xmlrpc interface wich can be used later by another kind of interfaces. XMLRPCHandler is not loaded by default, as we're not using any application that requires it right now.
- Inserting a new plugin requires, sadly, a server restart, I hope this will be corrected in a future.
- 

* Volunteer asks for a task via the task's assigned view, wich, right now, requires the server to restart after the plugin has been inserted.
* Get the task's future object via get_free_task and assign it a user object.
* Then, the plugin is responsible for waiting for user-input events and updating task's status.


Notice
-------

Some of this is still being developed, information may vary from lastest versions
