Introduction
============
Furnivall is an open source framework for distributed volunteer science. 
It helps to organize batches of tasks, collect them form volunteers and it does all the related housekeeping.

Currently Furnivall consists on a series of plugins + views and an integrated webserver, using threadspoolexecution
to make tasks asynchronous.

Inner workings
----------------
First of all, you need to create a researcher object foreach real researcher 
(who can have more than one project). 

Then, a job foreach project, indicating min and max workunits for the job
Min workunits will be the ones to be executed when job starts.
Max workunits are the neccesary workunits for the work to be considered finished.

Each workunit contains a set of tasks, when the minimun tasks for a workunit to be
completed is completed, the tasks is ended (wich is represented by property status of 
the workunit object).

Workunits and tasks both have function calls to plugins and views personaliced stuff,
wich, in a future, will probably have defaults to fit most requeriments for standard 
collaborative works.
