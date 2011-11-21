"""
    Ibervicis Furnivall is an open source framework for distributed volunteer science.
    It helps to organize batches of tasks, collect them form volunteers and do all the related housekeeping.

"""
import daemon, logging
from Core.core import *
from tornado.options import define, options
import tornado.httpserver
import tornado.database
import tornado.ioloop

define("port", default=8888, help="run on the given port", type=int)
define("db_host", default="localhost", help="database host")
define("db_user", default="root", help="database username")
define("db_db", default="furnivall", help="database name")
define("db_password", default="root", help="database password")
db = tornado.database.Connection(options.db_host, options.db_db ,options.db_user, options.password)

"""
    TODO: 
        All objects must be saved and reloaded from the database.
"""
def do_main_program(self):
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
                     
if __name__ == "__main__":
    with daemon.DaemonContext(
        working_directory='/var/lib/furnivall',
        umask=0o002,
        pidfile=lockfile.FileLock('/var/run/furnivall.pid'),
    ):
        logging.info("Starting daemon")
        do_main_program()
