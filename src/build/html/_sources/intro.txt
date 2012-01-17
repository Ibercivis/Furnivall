Introduction
============
Furnivall is an open source framework for distributed volunteer science. 
It helps to organize batches of tasks, collect them form volunteers and it does all the related housekeeping.

Currently Furnivall consists on a series of plugins + views and an integrated webserver, using threadspoolexecution
to make tasks asynchronous.

Inner workings
----------------


Furnivall does not difference between volunteers and researchers, they're the same objects.
The only thing that makes them different is their rights, a volunteer does not have right to
creater jobs, anyway, if needed by some project, a volunteer can eventually be given permission,
as well as a researcher can have their permissions dropped by the root administrator.

There's not yet an administrative interface for edition rights nor any other information about a
user, so we have to manually create it (wich takes seconds) in the database. This is planned to be
fixed before end of january 2012

After that, the researcher needs to have an initialized_view assigned for each project it wants to
create jobs for. Then, the jobs will create workunits and a minium amount of tasks.
The plugin will have in account the number of correct tasks needed to consider the workunit as done.
This is represented by a property "status" of workunit object, wich will be true when correctly finished,
false if failed, and "-1" if still running.

Workunits and tasks both have function calls to plugins and views personaliced stuff,
wich, in a future, will probably have defaults to fit most requeriments for standard 
collaborative works.
