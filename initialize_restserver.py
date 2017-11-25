#!/usr/bin/python
import json
import wait_to_complete 

# Creates a restserver and puts a startup script conatining the fibonacci file into the new server.
def create_restserver (compute, project_id, zone, name):
	
	image_response = compute.images().getFromFamily(project='ubuntu-os-cloud',family='ubuntu-1604-lts').execute()
    	source_disk_image = image_response['selfLink']	

	# Configure the machine
	machine_type = "zones/%s/machineTypes/f1-micro" % zone
	startup_script = open ('restserver_startup.sh', 'r').read()

	config = {
		'name' : name,
		'machineType' : machine_type,

		 # Specify the boot disk and the image to use as a source.
        	'disks': [
            		{
			'boot': True,
			'autoDelete': True,
			'initializeParams': {
			    'sourceImage': source_disk_image,
				}
            		}
        	],
		
		# Specify a network interface with NAT to access the public
		# internet.
		'networkInterfaces': [{
		    'network': 'global/networks/default',
		    'accessConfigs': [
			{'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
		    ]
		}],

		# Allow the instance to access cloud storage and logging.
		'serviceAccounts': [{
		    'email': 'default',
		    'scopes': [
			'https://www.googleapis.com/auth/devstorage.read_write',
			'https://www.googleapis.com/auth/logging.write'
		    ]
		}],
		
		'metadata' : {
			'items' : [{
				'key': 'startup-script',
				'value': startup_script
				}
			]
		}
	}
	# Waits for the operation to complete.
       	operation = compute.instances().insert(project=project_id,zone=zone,body=config).execute()
	wait_to_complete.wait(compute, project_id,zone, operation['name'], 'creating ' + name)

	
	# Sets the http and https tags to allow traffic
	data = compute.instances().get(project=project_id,zone=zone,instance=name).execute()
	tags = data ['tags']
	fingerprint = tags['fingerprint']
	
	body = {
		'items':[
			'http-server',
			'https-server'
			],
		'fingerprint': fingerprint
	}	
	# Waits for the operation to complete.
	request = compute.instances().setTags(project=project_id, zone=zone, instance=name, body=body).execute()
	wait_to_complete.wait(compute, project_id, zone, request['name'], 'enabling http and https traffic for ' + name)

# Creates a load balancer and with a start that puts file in place and the ssh-keys
def create_load_balancer (compute, project_id, zone):
	
	image_response = compute.images().getFromFamily(project='ubuntu-os-cloud',family='ubuntu-1604-lts').execute()
    	source_disk_image = image_response['selfLink']	

	# Configure the machine
	machine_type = "zones/%s/machineTypes/f1-micro" % zone
	startup_script = open ('load_balancer_startup.sh', 'r').read()
	ssh_key = open('id_rsa.pub').read()
	ssh_key = 'keegan:'+ssh_key
	
	name = 'loadbalancer-1'

	config = {
		'name' : name,
		'machineType' : machine_type,

		 # Specify the boot disk and the image to use as a source.
        	'disks': [
            		{
			'boot': True,
			'autoDelete': True,
			'initializeParams': {
			    'sourceImage': source_disk_image,
				}
            		}
        	],
		
		# Specify a network interface with NAT to access the public
		# internet.
		'networkInterfaces': [{
		    'network': 'global/networks/default',
		    'accessConfigs': [
			{'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
		    ]
		}],

		# Allow the instance to access cloud storage and logging.
		'serviceAccounts': [{
		    'email': 'default',
		    'scopes': [
			'https://www.googleapis.com/auth/devstorage.read_write',
			'https://www.googleapis.com/auth/logging.write'
		    ]
		}],
		
		'metadata' : {
			'items' : [{
				'key': 'startup-script',
				'value': startup_script
				},{
				'key': 'ssh-keys',
				'value' : ssh_key
				}
			]
		}
	}
	thing = compute.instances().insert(project=project_id,zone=zone,body=config).execute()
	wait_to_complete.wait(compute, project_id,zone, thing['name'], 'creating ' + name)

	
	# Sets the http and https tags to allow traffic
	data = compute.instances().get(project=project_id,zone=zone,instance=name).execute()
	tags = data ['tags']
	fingerprint = tags['fingerprint']
	
	body = {
		'items':[
			'http-server',
			'https-server'
			],
		'fingerprint': fingerprint
	}	
	# Waits for the operation to complete.
	request = compute.instances().setTags(project=project_id, zone=zone, instance=name, body=body).execute()
	wait_to_complete.wait(compute, project_id, zone, request['name'], 'enabling http and https traffic for ' + name)
