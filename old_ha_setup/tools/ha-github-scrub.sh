#!/bin/bash

##########################################################
## Variables
##########################################################

filename='PATH_TO_FILE_WITH_REDACTED_WORDS_redacted.txt'
directory='PATH_TO_LOCAL_GITHUB_DIRECTORY'
haconfigdir='PATH_TO_LOCAL_HA_CONFIG_DIR'
user1=USERNAME_TO_BE_REPLACED_WITH_USER1
user2=USERNAME_TO_BE_REPLACED_WITH_USER2
user1C=USERNAME_TO_BE_REPLACED_WITH_USER1
user2C=USERNAME_TO_BE_REPLACED_WITH_USER2
user1device=USERDEVICE_TO_BE_REPLACED_WITH_USERDEVICE1
user2device=USERDEVICE_TO_BE_REPLACED_WITH_USERDEVICE2

##########################################################
## Execute
##########################################################
clear
echo " "
echo "Copying Latest Configs"
echo " "
rsync -au --exclude=".*" --exclude ".*/" $haconfigdir/Config/ $directory/
echo " "
echo Scrubbing Files
echo " "
#scrub configration.yaml first to purge user accounts
cat $filename | while read redacted; do
    sed -i '' "s/"$redacted"/REDACTED/g" $directory/configuration.yaml
done
#scrub sensors.yaml second to purge user accounts
cat $filename | while read redacted; do
    sed -i '' "s/"$redacted"/REDACTED/g" $directory/sensors.yaml
done
#scrub out names
find $directory -name \*.yaml -exec sed -i '' "s/"$user1"/USER1/g" {} \;
find $directory -name \*.yaml -exec sed -i '' "s/"$user2"/USER2/g"  {} \;
#lame fix for uppercase names
find $directory -name \*.yaml -exec sed -i '' "s/"$user1C"/USER1/g"  {} \;
find $directory -name \*.yaml -exec sed -i '' "s/"$user2C"/USER2/g"  {} \;
#scrub out devices
find $directory -name \*.yaml -exec sed -i '' "s/"$user1device"/USER1DEVICE/g"  {} \;
find $directory -name \*.yaml -exec sed -i '' "s/"$user2device"/USER2DEVICE/g"  {} \;
#loop through and scrub any file with .yaml
cat $filename | while read redacted; do
find $directory -name \*.yaml -exec sed -i '' "s/"$redacted"/REDACTED/g" {} \;
done
#lame fix for butchering of Weekends
find $directory -name \*.yaml -exec sed -i '' "s/"WeeREDACTEDds"/Weekends/g" {} \;
echo "GitHub Files Scrubbed"
echo " "
exit
