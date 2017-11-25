#!/bin/sh

sudo apt-get update
sudo apt-get install -y nginx

sudo mkdir /etc/systemd/system/nginx.service.d
sudo bash -c 'echo -e "[Service]nLimitNOFILE=65536" > /etc/systemd/system/nginx.service.d/local.conf'
sudo systemctl daemon-reload
sudo systemctl restart nginx

sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup


#Directory to hold all the scripts
sudo mkdir /scripts

#Creats an empty default file
sudo cp /etc/nginx/sites-available/default /scripts/empty_default
sudo sed -i '0,/^/s//upstream fibonacci{\n\n\n\n\n\n\n\n}/' /scripts/empty_default 
sudo sed -i 's/# First attempt to serve request as file, then/proxy_pass http:\/\/fibonacci;/g' /scripts/empty_default 

#File holds all the ip addresses to be added.
sudo touch /scripts/add.txt
sudo chmod 777 /scripts/add.txt

# Script to add servers ips
sudo touch /scripts/add_ip.sh
sudo chmod 777 /scripts/add_ip.sh
echo '
#!/bin/sh
ip=$1
echo " server "$ip";" >> /scripts/add.txt
echo Added $ip to file'> /scripts/add_ip.sh

# Script to clear add.txt
sudo touch /scripts/reset_ip.sh
sudo chmod 777 /scripts/reset_ip.sh
echo '
#!/bin/sh
sudo rm /scripts/add.txt
sudo touch /scripts/add.txt
sudo chmod 777 /scripts/add.txt
echo Rest File.'> /scripts/reset_ip.sh

#Script to edit default
sudo touch /scripts/edit_default.sh
sudo chmod 777 /scripts/edit_default.sh
echo '
#!/bin/sh
sudo cp /scripts/empty_default /scripts/temp.txt
sudo sed -i "/upstream/r /scripts/add.txt" /scripts/temp.txt
sudo sed -i "s/try_files/#/g" /scripts/temp.txt
sudo cp /scripts/temp.txt ../../etc/nginx/sites-available/default
sudo service nginx reload
echo Edited default file and reloaded nginx' > /scripts/edit_default.sh
