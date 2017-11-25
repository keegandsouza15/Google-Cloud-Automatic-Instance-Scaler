#!/usr/bin/python
import time

# function takes in an operation and waits for it to complete.
def wait (compute, project_id, zone, operation, message):
	current_operation = compute.zoneOperations().get(project=project_id, zone=zone, operation=operation).execute()
	status = current_operation['status']
	while (status != 'DONE'):
		time.sleep (1)
		print 'Still ' + message + '...'
		current_operation = compute.zoneOperations().get(project=project_id, zone=zone, operation=operation).execute()
		status = current_operation ['status']
	print 'Finished ' + message



