# -*- coding: utf-8 -*-

from libs.route import Route
from BaseHandler import BaseHandler
from bson import json_util
import json

@Route(r"/api/task/get")
class GetTask(BaseHandler):
	def get(self):
		pass
