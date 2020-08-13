The [Home Assistant Management Tool](https://github.com/geekofweek/homeassistant/blob/master/tools/ha-mgmt-docker.sh) is something I built for my personal use, but can easily be modified to suite different setups.  Adjust the variables to your settings and setup shared SSH keys (if desired).  Probably a million other more efficient ways to do this, but it has worked out so far for me.  I had a previous version that I was using before converting to a Docker based installation. That one works with a more traditional installation.  You can check out that version [here]( https://github.com/geekofweek/homeassistant/blob/master/tools/ha-mgmt-bash.sh)

#### Overview:

- Bash Shell script, should work anywhere you can use Bash
- All HA configs are stored on my local workstation within Dropbox (doesn’t have to be but I like the versioning and access to it from any machine).
- Edit locally with Text Editor.  Currently using [Visual Studio Code](https://code.visualstudio.com) and VIM

#### Options:

1.	Deploy Home Assistant Configs
    - Creates tar file of current configs
    - Backs up tar file to local workstation (I use a Dropbox Folder)
    - rsyncs config directory from local workstation (Dropbox Folder)
2.	Restart Home Assistant
    - Restarts the Home Assistant Docker container, thus restarting Home Assistant
3. 	Stop Home Assistant
    - Stops the Home Assistant Docker Container
4.	Start Home Assistant
    - Starts the Home Assistant Docker Container
5.	Upgrade Home Assistant
    - Does a docker pull for the latest version of Home Assistant
    - Stops the Home Assistant Docker Container
    - Deletes the Home Assistant Docker Container
    - Creates a new Home Assistant Docker Container
6.	Check Database Size
    - Check the size of the MySQL Database
7. 	Validate Home Assistant Config
    - Runs a config check using a Docker Container
8. 	Backup Home Assistant
    - Creates tar file of current configs
    - Backs up tar file to local workstation (Dropbox Folder)
9. 	Copy Configs to GitHub
    - Copy’s current config to local workstation Github, scrubs any data that is listed in [redacted.txt]( https://github.com/geekofweek/homeassistant/blob/master/tools/redacted.txt) using [ha-github-scrub.sh]( https://github.com/geekofweek/homeassistant/blob/master/tools/ha-github-scrub.sh).  
10.	Renew SSL Certificate
    - Runs a certbot (Let's Encrypt) Docker container that generates a new SSL certificate

x)  Exit
    – I shouldn’t need to explain that one

#### Variables:

hauser=“USER_ACCOUNT” **<-- Home Assistant User Account**

habin="/usr/local/bin/hass" **<-- Home Assistant Binary**

haconfigdir="/home/USER/.homeassistant" **<-- Home Assistant Config Directory**

hahost=“HOSTNAME/IP” **<-- Home Assistant Hostname or IP address**

localuser=“USER_ACCOUNT” **<-- Local Computer Username, account from where this shell script will run**

localhost=“HOSTNAME/IP” **<-- Local Computer Hostname or IP address**

localpath=“PATH_TO_LOCAL_HA_CONFIGS” **<-- Where I store my local HA configs and backups**

docker="/PATH/TO/DOCKER/bin " **<-- Docker Binary**


Within the local folder, variable localpath="PATH_TO_LOCAL_HA_CONFIGS", I have two folders:

**Config:** All of the .yaml files for Home Assistant

**Backup:** Place for backup tar file
