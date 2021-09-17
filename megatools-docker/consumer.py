#!/usr/bin/env python

import configparser

from tasks import add_item

CONFIG_FILE = "/data/consumer_config.ini"

# Configs
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

start_time = config['schedule']['start_time']
stop_time = config['schedule']['stop_time']



while True:

    
