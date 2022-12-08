#!/usr/bin/python3

import os
import argparse
import json
import requests
import yaml
import time
from datetime import date

def create_resultdirectories(target):
    for domain in target:
        if os.path.exists(f"results/{domain}"):
            continue
        os.system(f"mkdir -p results/{domain}")


#uilding the argument parser for the script
def build_argumentparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help='increase output verbosity',action='store_true')
    parser.add_argument('-f', '--file', help = 'list of domain name to search',required='true' )
    parser.add_argument('-s', '--source',help = 'search source for theHarvester')
    args = parser.parse_args()
    return args


#opening the .txt file containing the targets and onverting them into a python list
def get_targetlist(target_file):
    target_list = []
    with open(target_file) as file:
        for line in file:
            target_list.append(line.strip())
    return target_list

#reading the yaml config file
def get_config(config_file):
    with open(config_file,'r') as file:
        configuration = yaml.safe_load(file)
    return configuration


#
def run_theHarvester(target):
    for domain in target:
        if arguments.verbose:
            print(f"running a theHarvester scan on the {domain} domain using {arguments.source} as a source")
        os.system(f"theHarvester -d {domain} -b {arguments.source} > results/{domain}/{today}-theHarvester")

def run_shodan(target):
    for domain in target:
        print(f"shodan is running on domain {domain}")

def run_dnscan(target):
    for domain in target:
        os.system(f"./dnscan/dnscan.py -d {domain} > results/{domain}/{today}-dnscan")

def run_urlscan(target, api_key):
    request_list = []
    request_uuid_list = []
    for domain in target:
        headers = {'API-Key':api_key,'Content-Type':'application/json'}
        data = {"url": f"https://{domain}", "visibility": "public"}
        response = requests.post('https://urlscan.io/api/v1/scan/',headers=headers, data=json.dumps(data))
        #request_uuid_list.append(response.json()['uuid'])
        request_list.append(f"curl https://urlscan.io/api/v1/result/{response.json()['uuid']} > results/{domain}/{today}-urlscan")
    time.sleep(30)

    for request in request_list:
        os.system(f"{request}")


arguments = build_argumentparser()




configuration = get_config("config.yaml")

target_list = get_targetlist(arguments.file)

urlscan_api_key = configuration['urlscan.io']['api_key']

today = date.today()

create_resultdirectories(target_list)

if configuration['theHarvester']['enabled']:
    run_theHarvester(target_list)
else:
	print("theHarvester is disabled in config file")


if configuration['dnscan']['enabled']:
    run_dnscan(target_list)
else:
	print("dnscan is disabled in config file")


if configuration['shodan']['enabled']:
    run_shodan(target_list)
else:
	print("shodan is disabled in config file")


if configuration['urlscan.io']['enabled']:
    run_urlscan(target_list,urlscan_api_key)
else:
	print("urlscan is disabled in config file")
