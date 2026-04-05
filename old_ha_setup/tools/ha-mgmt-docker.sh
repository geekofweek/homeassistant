#!/bin/bash

#################################################################
## Home Assistant Managment Tool
#################################################################

##########################################################
## Variables
##########################################################

hauser="SERVER_DOCKER_USER_ACCOUNT"
haconfigdir="/PATH/TO/SERVER/HA/CONFIG"
hahost="HA_SERVER_HOSTNAME/IP"
localuser="LOCAL_USER_ACCOUNT"
localhost="LOCAL_HOSTNAME/IP"
localpath="PATH_TO_LOCAL_HA_CONFIGS"
scripts="/SERVER/SCRIPTS/DIRECTORY"
mgmtscripts='/LOCAL/SCRIPTS/DIRECTORY'

##########################################################
## Execute
##########################################################

answer=1
while [ "$answer" = 1 ]
do

 clear
 echo "This Script Will Modify Home Assistant"
 echo "Proceed with Caution!"
 echo "Home (LOCATION)"
 echo ""
 echo "What would you like to do?"
 echo " "
 echo "1) Deploy Home Assistant Configs"
 echo "2) Restart Home Assistant"
 echo "3) Stop Home Assistant"
 echo "4) Start Home Assistant"
 echo "5) Upgrade Home Assistant"
 echo "6) Check Database Size"
 echo "7) Validate Home Assistant Config"
 echo "8) View Logs"
 echo "9) Backup Home Assistant"
 echo "10) Copy Configs to GitHub"
 echo "11) Renew SSL Certificate"
 echo "x) Exit"
 echo " "
 read action

 if [ "$action" != "1" -a "$action" != "2" -a "$action" != "3" -a "$action" != "4" -a "$action" != "5" -a "$action" != "6" \
 -a "$action" != "7" -a "$action" != "8" -a "$action" != "9" -a "$action" != "10" -a "$action" != "11" -a "$action" != "x" ];then
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
   ssh -t $hauser@$hahost "mkdir $haconfigdir/temp; cd $haconfigdir/config; tar -czf $haconfigdir/temp/ha-backup-`date +"%m-%d-%Y-%H-%M"`.tar.gz ."
   echo " "
   echo "Moving Backup to Local Host"
   echo " "
   ssh -t $hauser@$hahost "scp $haconfigdir/temp/*.tar.gz $localuser@$localhost:$localpath/Backups"
   echo " "
   echo "Deploying Home Assistant Configs..."
   echo " "
   rsync -rzvu --exclude=".*" --exclude ".*/" $localpath/Config/ $hauser@$hahost:/$haconfigdir/config
   echo " "
   echo "Cleaning Up..."
   echo " "
   ssh -t $hauser@$hahost "rm -rf $haconfigdir/temp;"
   echo " "
   echo "Home Assistant Config Deployment Complete"
   echo " "
   echo "Choose Option 7 to Validate Configs"
   echo " "
 fi

 if [ "$action" == "2" ];then
   clear
   echo "Restarting Home Assistant..."
   echo " "
   ssh -t $hauser@$hahost "$scripts/restart/ha-docker-restart.sh"
   echo " "
   echo "Home Assistant Restart Complete"
   echo " "
 fi

 if [ "$action" == "3" ];then
   clear
   echo "Stopping Home Assistant..."
   echo " "
   ssh -t $hauser@$hahost "$scripts/stop/ha-docker-stop.sh"
   echo " "
   echo "Home Assistant Stop Complete"
   echo " "
 fi

 if [ "$action" == "4" ];then
   clear
   echo "Starting Home Assistant..."
   echo " "
   ssh -t $hauser@$hahost "$scripts/start/ha-docker-start.sh"
   echo " "
   echo "Home Assistant Start Complete"
   echo " "
 fi

 if [ "$action" == "5" ];then
   clear
   echo "Upgrading Home Assistant..."
   echo " "
   echo " "
   echo "Downloading Latest Docker Image"
   echo " "
   ssh -t $hauser@$hahost "$scripts/update/ha-docker-update.sh"
   echo " "
   echo "Stopping Home Assistant Container"
   echo " "
   ssh -t $hauser@$hahost "$scripts/stop/ha-docker-stop.sh"
   echo " "
   echo "Deleting Home Assistant Container"
   echo " "
   ssh -t $hauser@$hahost "$scripts/remove/ha-docker-remove.sh"
   echo " "
   echo "Initializing Home Assistant Container"
   echo " "
   ssh -t $hauser@$hahost "$scripts/create/ha-docker-create.sh"
   echo " "
   echo "Upgrade Complete"
   echo " "
 fi

 if [ "$action" == "6" ];then
   clear
   echo "Checkign Size of Home Assistant Databae..."
   echo " "
   ssh -t $hauser@$hahost "du -sh /data/containers/mysql/data | cut -c -5"
   echo " "
   echo "Home Assistant Size Check Complete"
   echo " "
 fi

 if [ "$action" == "7" ];then
   clear
   echo "Validating Home Assistant Configs..."
   echo " "
   ssh -t $hauser@$hahost "$scripts/other/ha-docker-validate.sh"
   echo " "
   echo "Home Assistant Config Validation Complete"
   echo " "
 fi

 if [ "$action" == "8" ];then
   clear
   echo "Tailing Home Assistant Logs ctrl+c to Exit..."
   echo " "
   ssh -t $hauser@$hahost "tail -f $haconfigdir/config/home-assistant.log"
   echo " "
 fi

 if [ "$action" == "9" ];then
   clear
   echo "Backing Up Home Assistant..."
   echo "Creating Tar File..."
   echo " "
   ssh -t $hauser@$hahost "mkdir $haconfigdir/temp; cd $haconfigdir/config; tar -czf $haconfigdir/temp/ha-backup-`date +"%m-%d-%Y-%H-%M"`.tar.gz ."
   echo " "
   echo "Moving Backup to Local Host"
   echo " "
   ssh -t $hauser@$hahost "scp $haconfigdir/temp/*.tar.gz $localuser@$localhost:$localpath/Backups"
   echo " "
   echo "Cleaning Up..."
   echo " "
   ssh -t $hauser@$hahost "rm -rf $haconfigdir/temp;"
   echo " "
   echo "Backup Complete"
   echo " "
 fi

 if [ "$action" == "10" ];then
   clear
   echo "Copy Files for GitHub Publishing"
   echo " "
   $mgmtscripts/ha-github-scrub.sh
   echo " "
   echo "Files Copied to GitHub Directory"
   echo " "
 fi

 if [ "$action" == "11" ];then
   clear
   echo "Renewing SSL Certificate..."
   echo " "
   ssh -t $hauser@$hahost "$scripts/create/certbot-docker-create.sh"
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
   sleep .4
   exit
 fi

echo " "
echo "Do You Want to Perform Another Task?"
echo " "
echo "1) Yes"
echo "2) No"
echo " "
read answer

done

clear
echo " "
echo ":-("
echo "Exiting"
echo " "
sleep .4
