#!/usr/bin/env python
"""
    Ibervicis Furnivall is an open source framework for distributed user science.
    It helps to organize batches of tasks, collect them form users and do all the related housekeeping.

"""
from tornadorpc.json import JSONRPCHandler
from tornadorpc.xml import XMLRPCHandler
from tornadorpc import private
import logging, os, daemon, lockfile
from Furnivall.Core.Handlers import MainHandler, LoginHandler, ObjectManager
from Furnivall import data_dir
import tornado.httpserver, tornado.database, tornado.ioloop, tornado.web
import Furnivall.Views as Views
from ZODB.DB import DB
from ZODB.FileStorage import FileStorage

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)
define("daemonize", default=False, help="Run as daemon")

class StaticInterfaceProvider(tornado.web.RequestHandler):
    """
        Renders templates dinamically to build static interfaces to be used with rpc handlers
    """
    def get(self, template, place):
        return self.render(template + "_" + place, xsrf=self.xsrf_token,user_name=self.get_secure_cookie('username'))

def get_task_from_user(application, job, user, researcher):
    """
        Implement me, I have to search on all tasks from the job to see if one belongs to a determinate user
        if i cant find it first looking for user's tasks.
    """
    for wk in job.tasks:
        for task in wk.tasks:
            if task.user == user: # TODO Check if we're dealing with ids here correctly.
                return [researcher, job, wk, task.id_ ]
    return False 

def get_researcher_job(application, job, researcher=False):
    """
        Returns the job path for a specific job name.
        If researcher is specified it will filter jobs from that researcher
    """
    if researcher:
        logging.debug(application.db['users'][researcher])
        return application.db['users'][researcher].jobs[job] # TODO Test me
    else:
        for user_ in application.db['users']:
            user=application.db['users'][user_]
            for job_ in user.jobs.keys():
                if user.jobs[job_].name == job:
                    return ( user_, job_)

class DynamicUrlHandler(tornado.web.RequestHandler):
    """
        Manages views' urls.
    """
    def get(self, researcher, view, askfor):
        viewfile, viewclass = self.application.extra_urls[view]
        researcher = researcher # TODO: Get researcher.
        view = getattr(getattr(Views, view),viewfile)(False) # TODO: make this with a initialized object from somewhere
        return self.write(getattr(view, viewclass)(askfor))

class RPCxmlDynamicUrlHandler(XMLRPCHandler):
    def get_task(self, job, researcher=False):
        if not researcher:
            logging.info("Error: no researcher provided")
        user_, job = get_researcher_job(self.application, job, researcher)
        workunit, task = self.application.db['users'][user_].jobs[job].get_free_task()
        logging.info(task.id_)
        return [user_, job, workunit, task.id_ ]

    def send_command(self, user=False, job=False, workunit=False, task=False, method=False, values=False):
        task = self.application.db['users'][user].jobs[job].workunits[workunit].tasks[task]
        return getattr(getattr(task, 'job_plugin'), method)(values)

class RPCDynamicUrlHandler(JSONRPCHandler):
    def get_task(self, job, user, researcher=False):
        """
            Create task and return its full path
        """
        researcher, job = get_researcher_job(self.application, job, researcher)
        workunit, task = get_task_from_user(self.application, job, researcher)
        if not workunit and task:
            workunit, task = self.application.db['users'][researcher].jobs[job].get_free_task()
        return [researcher, job, workunit, task.id_ ]

    def get_or_create_task(self, job, user, researcher = False):
        """
            return the full path of a task if exists, creates a new one and returns its path if not
        """
        task = get_task_from_user(self.application, job, user)
        if not task: 
            return self.get_task(job, user, researcher)

    def send_command(self, user=False, job=False, workunit=False, task=False, method=False, values=False):
        """
            Send a command to a view object.
        """
        task = self.application.db['users'][user].jobs[job].workunits[workunit].tasks[task]
        return getattr(getattr(task, 'job_plugin'), method)(values)

class Application(tornado.web.Application):
    def __init__(self):
        """
            Sets up the tornado web server and loads needed data from db
        """
        conn = DB(FileStorage('Data.fs')).open()
        self.db  = conn.root()
        self.initialize_db()
        self.extra_urls = {}
        self.researchers = self.db['users']
        for a in self.get_all_urls():
            for template in a.keys():
                self.extra_urls[template] = a[template]

        urls = [
                ('/', MainHandler),
                ('/([^/]+)', MainHandler),
                ('/new/([^/]+)', ObjectManager),
                ('/Login/([^/]+)', LoginHandler),
                ('/RPC/', RPCDynamicUrlHandler),
                ('/RPCXML/', RPCxmlDynamicUrlHandler),
                ('/View/([^/]+)/([^/]+)/([^/]+)', DynamicUrlHandler),
                ('/([^/]+)/(.+)', StaticInterfaceProvider ),
                ]

        settings = dict(
                static_path=os.path.join(data_dir, "static"),
                template_path=os.path.join(data_dir, "templates"),
                xsrf_cookies = False,
                cookie_secret = "11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1ao/Vo=",
        )

        self.special_login_slugs = {
                'root': '/Admin',
                'researcher': '/Admin/Researcher',
                'user': '/User/Home'
        }

        logging.debug('Starting server with urls: %s', urls)

        tornado.web.Application.__init__(self, urls, **settings)

    def get_all_urls(self):
        """
            generator returning a dict of url: (file, class) list for the url building
        """
        views = Views.ViewClasses 
        return ( getattr(getattr(Views, viewfile), views[viewfile][0])(None).templates\
            for viewfile in views.keys() )

    def initialize_db(self):
        try:
            self.db['users']
        except KeyError:
            from Furnivall.Core.Personality import User
            self.db['users'] = {
                    'anonymous' : User(self),
                    'root' : User(self)
                    }
            self.db['users']['anonymous'].set_password("anonymous")
            self.db['users']['root'].set_password("root")
            self.db['users']['root'].grant_permission('root')

def do_main_program():
    """
        DO: All objects must be saved and reloaded from the database.
    """
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    if options.daemonize:
        log_file = 'furnivall.%s.log' % options.port
        log = open(os.path.join('/var/log', log_file), 'a+')
        with daemon.DaemonContext(
            working_directory='/var/lib/furnivall',
            umask=0o002,
            pidfile=lockfile.FileLock('/var/run/furnivall.pid'),
            stdout=log,
            stderr=log
        ):
            do_main_program()
    else:
        do_main_program()
