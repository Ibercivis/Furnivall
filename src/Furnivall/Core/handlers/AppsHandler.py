# -*- coding: utf-8 -*-

from libs.route import Route
from BaseHandler import BaseHandler

@Route(r"/application/new")
class NewApplicationHandler(BaseHandler):
	def get(self):
		self.render("applications/new.template")

	def post(self):
		name = self.get_argument("txt-name", "")
		description = self.get_argument("txt-description", "")

		applications = self.application.db.applications
		already_created = applications.find_one({'name': name})
		if already_created:
			error_message = u'El nombre de la aplicación ya esta siendo usado.'
			self.render("applications/new.template")

		## FIXME: [JUANJO] Hacer validaciones
		new_application = { 'name': name,
							'description': description }
		applications.insert(new_application)

		self.redirect(u"/")

@Route(r"/application/details/([a-zA-Z]+)")
class ApplicationDetails(BaseHandler):
	def get(self, app_name):
		applications = self.application.db.applications
		app_details = applications.find_one({'name': app_name})

		if app_details:
			jobs = self.application.db.jobs
			application_jobs = jobs.find({'applicationId': app_details['_id']})
			self.render("applications/details.template", app_details = app_details, jobs = application_jobs)
		else:
			error_message = u'No existe ninguna aplicación con el nombre seleccionado.'
			self.render("error.template", message = error_message)
