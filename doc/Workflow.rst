
* Researcher or root creates Job
    - Initialize view (Once a view is initialized, every researcher can use it)
    - Create a job based on that initialized view object
    - It creates the number of workunits provided in the plugins' initialization code. (I'm planning a manual create-workunit button, will take a few minutes)
    - Each workunit creats a predefined number of tasks, wich we can increase from the admin panel.
        * Researcher assigns as much tasks as he wants to workunit
* Tasks are assigned as future objects
* Volunteer asks for a task via the task's assigned view.
* Wich returns a future object and assigns it to the user.
* Then, the plugin is responsible for waiting for user-input events and updating task's status.
