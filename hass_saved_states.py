#!/usr/bin/env python

import sys
import ConfigParser
import os
import argparse
import urllib2
import json

"""
BEGIN CUSTOMIZE
"""
path = "/home/_REDACTED_/.homeassistant/ha_saved_states.out"
host = "_REDACTED_"
api_key = "_REDACTED_"

"""
END CUSTOMIZE
"""

parser = argparse.ArgumentParser()
parser.add_argument("-act")
parser.add_argument("-sec")
parser.add_argument("-set")
parser.add_argument("-val")
args = parser.parse_args()

def create_config():
    """
    Create a config file
    """
    config = ConfigParser.ConfigParser()
    config.add_section("boolean")
    config.add_section("select")
    config.add_section("slider")
    config.add_section("tracker")

    with open(path, "wb") as config_file:
        config.write(config_file)


def get_config():
    """
    Returns the config object
    """
    if not os.path.exists(path):
        create_config()

    config = ConfigParser.ConfigParser()
    config.read(path)
    return config


def get_setting(section, setting):
    """
    Print out a setting
    """
    config = get_config()
    value = config.get(section, setting)
    #print "{section} {setting} is {value}".format(
    #    section=section, setting=setting, value=value)
    return value


def update_setting(section, setting, value):
    """
    Update a setting
    """
    config = get_config()
    config.set(section, setting, value)
    with open(path, "wb") as config_file:
        config.write(config_file)


def delete_setting(section, setting):
    """
    Delete a setting
    """
    config = get_config()
    config.remove_option(section, setting)
    with open(path, "wb") as config_file:
        config.write(config_file)

def update_hass_post(section, setting, value):
    """
    Post to Hass
    """
    if section == "boolean":

        url = 'https://'+ host +'/api/services/input_boolean/turn_on'
        data = json.dumps({"entity_id": ""+ setting +""})
        cont_len = len(data)

    elif section == "select":

        url = 'https://'+ host +'/api/services/input_select/select_option'
        data = json.dumps({"entity_id": ""+ setting +"", "option": ""+ value +""})
        cont_len = len(data)

    elif section == "slider":

        url = 'https://'+ host +'/api/services/input_slider/select_value'
        data = json.dumps({"entity_id": ""+ setting +"", "value": value})
        cont_len = len(data)

    elif section == "tracker":

        url = 'https://'+ host +'/api/services/device_tracker/see'
        data = json.dumps({"dev_id": ""+ setting.split(".")[1] +"", "location_name": value})
        cont_len = len(data)


    req = urllib2.Request(url, data, {'Content-Type': 'application/json', 'Content-Length': cont_len})
    req.add_header('x-ha-access', api_key)
    f = urllib2.urlopen(req)

    response = f.read()
    f.close()


def update_hass(section):
    """
    Compare values to default & then send to post
    """
    config = get_config()
    for (setting, value) in config.items(section):

        if section == "boolean":

            if value != "off":
                #print setting
               # print value
                update_hass_post(section, setting, value)

        elif section == "select":

            if value != "None" and value != "PowerOff":
                update_hass_post(section, setting, value)

        elif section == "slider":

            if value != "0":
                update_hass_post(section, setting, value)

        elif section == "tracker":

            if value != "not_home":
                update_hass_post(section, setting, value)


if args.act == 'update_settings':

    args.sec = args.sec.split("_")[1]
    update_setting(args.sec.split(".")[0], args.set, args.val)

elif args.act == 'update_hass':

    update_hass("boolean")
    update_hass("select")
    update_hass("slider")
    update_hass("tracker")
