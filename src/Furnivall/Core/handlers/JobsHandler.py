# -*- coding: utf-8 -*-

from libs.route import Route
from BaseHandler import BaseHandler
import datetime

@Route(r"/application/([a-zA-Z]+)/job/new")
class NewJobHandler(BaseHandler):
	def get(self, app_name):
		self.render("applications/jobs/new.template", app_name=app_name)

	def post(self, app_name):
		description = self.get_argument("txt-description", "")
		creation_date = datetime.datetime.now().strftime("%d/%m/%Y")

		applications = self.application.db.applications
		app_details = applications.find_one({'name': app_name})

		jobs = self.application.db.jobs
		new_job = {'applicationId': app_details['_id'],
				   'description': description,
				   'creation_date': creation_date}
		jobs.insert(new_job)

		self.redirect("/application/details/" + app_name)
