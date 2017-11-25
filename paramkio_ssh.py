# File for handling ssh connections
def ssh_command(command, hostname):
	import paramiko	 
	aclient = paramiko.SSHClient()
	try:
		aclient.load_system_host_keys() #Loads ssh keys
		aclient.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #Add host keys if missing
		aclient.connect (hostname) 
		stdin, stdout, stderr = aclient.exec_command (command)
		print stdout.read()
		print stderr.read()
	except  paramiko.ssh_exception.AuthenticationException as e:
		print e
		exit (1)
	finally:
		aclient.close()

def paramiko_stuff(ip_addresses, hostname):
	ssh_command ("/scripts/./reset_ip.sh", hostname) # Resets the file that holds the ip addresses.
	for ip in ip_addresses: # Adds the ip addresses
		ssh_command ("/scripts/./add_ip.sh " + ip,hostname)
	ssh_command ('/scripts/./edit_default.sh',hostname) # Executes a command that edits the default file.

if __name__ == '__main__':
	paramiko_stuff(ip_addresses, hostname)


