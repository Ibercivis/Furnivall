# -*- coding: utf-8 -*-

from libs.route import Route
from BaseHandler import BaseHandler
from bson import json_util
import json

@Route(r"/api/application/list")
class ApplicationList(BaseHandler):
	def get(self):
		applications = self.application.db.applications
		application_list = []
		for app in applications.find():
			application_list.append({'id': app['_id'],
									 'name': app['name'],
									 'description': app['description']})

		self.write(json.dumps({'status': 'OK',
							   'applications': application_list}, default=json_util.default))
