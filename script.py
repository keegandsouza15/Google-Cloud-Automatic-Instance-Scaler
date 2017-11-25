#!/usr/bin/python


import time
import sys, os
import googleapiclient.discovery 
import json 

from oauth2client.client import GoogleCredentials
from googleapiclient.discovery import build




instance_count = 0
running_instance_count = 0
non_running_instances = []
running_instances = []
generic_restserver = None


	
# Configures the loadbalancer with the new ip addresses.
def configure_loadbalancer (compute, project_id, zone, internal_IPs):
	request = compute.instances().get(project=project_id, zone=zone, instance='loadbalancer-1').execute()
	network_interfaces = request['networkInterfaces']
	more_network = network_interfaces[0]
	hostname = more_network ['networkIP']
	paramkio_ssh.paramiko_stuff(internal_IPs, hostname)


# Lists all the instances that are running and not-running.	
def list_instances (compute, project_id, zone):
	global instance_count
	global running_instance_count
	global non_running_instances 
	global running_instances
	global generic_restserver 

	instance_count = 0
	running_instance_count = 0
	non_running_instances = []
	running_instances = []
	result = compute.instances().list(project=project_id, zone=zone).execute()
	instances = result['items']

	
	
	print '{:*^41}'.format('Here are a list of instances')
	for instance in instances:
		name = instance ['name']
		if (name [0:11] == 'restserver-'):
			instance_count += 1
			network_array = instance ['networkInterfaces']
			more_network = network_array[0]
			status = instance ['status']
			rest_id = instance ['id']

			internal_ip = more_network['networkIP']
			if (status == 'RUNNING'):
				time = '0.1'
				running_instance_count+=1
				running_instances.append([name, internal_ip, time])
			else:
				non_running_instances.append([name, internal_ip])
			data = [name,status]
			print '{0[0]:<20} {0[1]:>20}'.format (data)



def start_instandces (compute, count, project_id, zone):

	# Partition new instances
	if ((instance_count - running_instance_count) < count):
		a = count - (instance_count - running_instance_count)
		print 'Need to add: '  +  str(a) + ' instances.'
		for i in range (a):
			name = 'restserver-'+ str(i+ instance_count)
			print 'Created new instance: '+  name
			initialize_restserver.create_restserver (compute, project_id, zone, name)
			count-=1
	
	started_instance_list = []
	i = 0
	# Starts already created instances.
	while count != 0:
		operation = compute.instances().start (project=project_id, zone=zone, instance=non_running_instances[i][0]).execute()
		wait_to_complete.wait(compute,project_id,zone, operation['name'], 'starting ' + non_running_instances [i][0])
		started_instance_list.append (non_running_instances [i][0])
		count -=1
		i+=1
	
# Stops already created instances.
def stop_instances (compute, count, project_id, zone):
	operation_list = []
	i = 0
	while count != 0:
		operation = compute.instances().stop (project=project_id, zone=zone, instance=running_instances [i][0]).execute()
		operation_list.append(operation)
		count -=1
		i += 1
	# Puts the last operation first.
	operation_list.reverse()
	for operation in operation_list:
		wait_to_complete.wait(compute,project_id,zone,operation['name'], 'stopping multiple instances')



def main ():

	project_id = raw_input ("Enter the project_id: ")
	zone = raw_input ("Enter the zone")
	
	credentials = GoogleCredentials.get_application_default()
	compute = googleapiclient.discovery.build('compute','v1')


	# Checks if the project was found
	try:
		compute.projects().get(project=project_id).execute()
	except googleapiclient.errors.HttpError as e:
		print e
		print 'Project not found.'
		exit(1)		
	# Checks if the zone was found
	try :
		compute.zones().get(project=project_id, zone=zone).execute()
	except googleapiclient.errors.HttpError:
		print 'Zone not found.'
		exit (1)
	
	
	expected_instance_count = input ("Enter the node count: ")
	



	# Gets the current instance status
	list_instances (compute, project_id, zone)
	
	a = expected_instance_count - running_instance_count
	b = running_instance_count - expected_instance_count
	if (running_instance_count < expected_instance_count):
		start_instandces (compute, a, project_id, zone)		
	if (running_instance_count > expected_instance_count):
		stop_instances (compute, b, project_id, zone)

	list_instances (compute, project_id, zone)
	
	# Updates the load balances
	if (expected_instance_count != 0):
		# Checks if the load balancer is created and if not creates it. 
		try:
			result = compute.instances().get (project=project_id, zone=zone, instance='loadbalancer-1').execute()
			status = result ['status']
			if (status == 'TERMINATED'):
				operation = compute.instances().start (project=project_id, zone=zone, instance='loadbalancer-1').execute()
				wait_to_complete.wait(compute,project_id,zone, operation['name'], 'starting ' + 'loadbalancer-1')
		except googleapiclient.errors.HttpError:
			print 'Called:'
			initialize_restserver.create_load_balancer (compute,project_id,zone)
		# Gets the interal ips of the nodes
		internal_IPs = []
		for instance in running_instances:
			internal_IPs.append(instance [1])
		configure_loadbalancer (compute, project_id, zone,internal_IPs)

if __name__ == "__main__":
	import initialize_restserver
	import wait_to_complete
	import paramkio_ssh
	main()
