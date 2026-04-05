#!/bin/bash

#################################################################
## Home Assistant Managment Tool Old
#################################################################

##########################################################
## Variables
##########################################################

hauser="HA_USER_ACCOUNT"
habin="/usr/local/bin/hass"
haconfigdir="/home/USER/.homeassistant"
hahost="HOSTNAME/IP"
localuser="LOCAL_USER_ACCOUNT"
localhost="LOCAL_HOSTNAME/IP"
localpath="PATH_TO_LOCAL_HA_CONFIGS"


##########################################################
## Execute
##########################################################

answer=1
while [ "$answer" = 1 ]
do

 clear
 echo "This Script Will Modify Home Assistant"
 echo "Proceed with Caution!"
 echo ""
 echo "What would you like to do?"
 echo " "
 echo "1) Deploy Home Assistant Configs"
 echo "2) Restart Home Assistant - (sudo Required)"
 echo "3) Stop Home Assistant - (sudo Required)"
 echo "4) Start Home Assistant - (sudo Required)"
 echo "5) Upgrade Home Assistant - (sudo Required)"
 echo "6) Check Database Size - (sudo Required)"
 echo "7) Validate Home Assistant Config"
 echo "8) Backup Home Assistant"
 echo "9) Copy Configs to GitHub"
 echo "10) Renew SSL Certificate"
 echo "x) Exit"
 echo " "
 read action

 if [ "$action" != "1" -a "$action" != "2" -a "$action" != "3" -a "$action" != "4" -a "$action" != "5" -a "$action" != "6" -a "$action" != "7" -a "$action" != "8" -a "$action" != "9" -a "$action" != "10" -a "$action" != "x" ];then
 		echo ":-("
 		echo "Error!"
 		echo "Invalid Option Stupid"
    exit
 fi

 if [ "$action" == "1" ];then
   clear
   echo "Backing Up Home Assistant..."
   echo "Creating Tar File..."
   echo " "
   ssh -t $hauser@$hahost "mkdir /home/$hauser/temp; cd $haconfigdir; tar -czf /home/$hauser/temp/ha-backup-`date +"%m-%d-%Y-%H-%M"`.tar.gz *"
   echo " "
   echo "Moving Backup to Local Host"
   echo " "
   ssh -t $hauser@$hahost "scp /home/$hauser/temp/*.tar.gz $localuser@$localhost:$localpath/Backups"
   echo " "
   echo "Deploying Home Assistant Configs..."
   echo " "
   rsync -au --exclude=".*" --exclude ".*/" $localpath/Config/ $hauser@$hahost:/$haconfigdir
   echo " "
   echo "Validating Home Assistant Configs..."
   echo " "
   ssh -t $hauser@$hahost "$habin --script check_config"
   echo " "
   echo "Home Assistant Config Validation Complete"
   echo " "
   echo "Cleaning Up..."
   echo " "
   ssh -t $hauser@$hahost "rm -rf /home/$hauser/temp;"
   echo " "
   echo "Home Assistant Config Deployment Complete"
 fi

 if [ "$action" == "2" ];then
   clear
   echo "Restarting Home Assistant..."
   echo " "
   ssh -t $hauser@$hahost "sudo systemctl restart home-assistant@ha"
   echo " "
   echo "Home Assistant Restart Complete"
   echo " "
 fi

 if [ "$action" == "3" ];then
   clear
   echo "Stopping Home Assistant..."
   echo " "
   ssh -t $hauser@$hahost "sudo systemctl stop home-assistant@ha"
   echo " "
   echo "Home Assistant Stop Complete"
   echo " "
 fi

 if [ "$action" == "4" ];then
   clear
   echo "Starting Home Assistant..."
   echo " "
   ssh -t $hauser@$hahost "sudo systemctl start home-assistant@ha"
   echo " "
   echo "Home Assistant Start Complete"
   echo " "
 fi

 if [ "$action" == "5" ];then
   clear
   echo "Upgrading Home Assistant..."
   echo " "
   ssh -t $hauser@$hahost "sudo pip3 install --upgrade homeassistant"
   echo " "
   echo "Upgrade Complete"
   echo " "
 fi

 if [ "$action" == "6" ];then
   clear
   echo "Checking Size of Home Assistant Database..."
   echo " "
   ssh -t $hauser@$hahost "sudo du -sh /var/lib/mysql | cut -c -5"
   echo " "
   echo "Home Assistant Size Check Complete"
   echo " "
 fi

 if [ "$action" == "7" ];then
   clear
   echo "Validating Home Assistant Configs..."
   echo " "
   ssh -t $hauser@$hahost "$habin --script check_config"
   echo " "
   echo "Home Assistant Config Validation Complete"
   echo " "
 fi

 if [ "$action" == "8" ];then
   clear
   echo "Backing Up Home Assistant..."
   echo "Creating Tar File..."
   echo " "
   ssh -t $hauser@$hahost "mkdir /home/$hauser/temp; cd $haconfigdir; tar -czf /home/$hauser/temp/ha-backup-`date +"%m-%d-%Y-%H-%M"`.tar.gz *"
   echo " "
   echo "Moving Backup to Local Host"
   echo " "
   ssh -t $hauser@$hahost "scp /home/$hauser/temp/*.tar.gz $localuser@$localhost:$localpath/Backups"
   echo " "
   echo "Cleaning Up..."
   echo " "
   ssh -t $hauser@$hahost "rm -rf /home/$hauser/temp;"
   echo " "
   echo "Backup Complete"
   echo " "
 fi

 if [ "$action" == "9" ];then
   clear
   echo "Copy Files for GitHub Publishing"
   echo " "
   ./ha-github-scrub.sh
   echo " "
   echo "Files Copied to GitHub Directory"
   echo " "
 fi

 if [ "$action" == "10" ];then
   clear
   echo "Renewing SSL Certificate..."
   echo " "
   ssh -t $hauser@$hahost "./certbot/certbot-auto renew --quiet --no-self-upgrade --standalone \
                     --standalone-supported-challenges http-01"
   echo " "
   echo "Home Assistant SSL Ceretificate Renewal Complete"
   echo " "
 fi

 if [ "$action" == "x" ];then
   clear
   echo " "
   echo ":-("
   echo "Exiting"
   echo " "
   exit
 fi

echo " "
echo "Do You Want to Perform Another Task?"
echo " "
echo "1) Yes"
echo "2) No"
echo " "
read answer

if [ "$answer" = 1 ]
then "run script again"
fi

done

clear
echo " "
echo ":-("
echo "Exiting"
echo " "
