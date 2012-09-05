import random
from yapsy.IPlugin import IPlugin
from bson.objectid import ObjectId

class Sumar(IPlugin):
	def task_executor(self):
		print "Task executor"

	def validate_task(self):
		print "Validate task"

	def consolidate_result(self):
		print "Consolidate result"

	def generate_workunits(self, job_id):
		workunits = []
		for i in range(10):
			new_workunit = {'job_id': ObjectId(job_id),
							'validated': False,
							'all_assigned': False,
							'tasks': [{'A': random.randint(1, 100), 'B': random.randint(1, 100), 'assigned': False},
									  {'A': random.randint(1, 100), 'B': random.randint(1, 100), 'assigned': False}]}
			workunits.append(new_workunit)

		return workunits

	def get_client_data(self, task):
		return {'A': task['A'],
				'B': task['B']}
