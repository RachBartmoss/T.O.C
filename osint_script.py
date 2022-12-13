#!/usr/bin/python3

import os
import argparse
import json
import requests
import yaml
import time
from datetime import date
from json2html import *

#function to check and create the folders to store the tool's results
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
    with open(target_file,'r') as file:
        for line in file:
            target_list.append(line.strip())
    return target_list

#reading the yaml config file
def get_config(config_file):
    with open(config_file,'r') as file:
        configuration = yaml.safe_load(file)
    return configuration


#Function to run thHarvester over the domain list
def run_theHarvester(target):
    for domain in target:
        if arguments.verbose:
            print(f"running a \033[01m\033[91m theHarvester \033[00m scan on the {domain} domain using {arguments.source} as a source\n")
        os.system(f"theHarvester -d {domain} -b {arguments.source} > results/{domain}/{today}-theHarvester")

#Function to run shodan over the domain list
def run_shodan(target):
    for domain in target:
        print(f"\033[01m\033[91mshodan\033[00m is running on domain {domain}\n")

#Function to run dnscan over the domain list
def run_dnscan(target):
    for domain in target:
        if arguments.verbose:
            print(f"running a \033[01m\033[91mdnscan\033[00m scan on the {domain} domain\n")
        os.system(f"./dnscan/dnscan.py -d {domain} > results/{domain}/{today}-dnscan")

'''
The following 2 functions are used to make a url request on the domain list and then 
making a request for the result and then formatting the .JSON result to a more readable
.HTML format
'''

def probe_urlscan(target, api_key):
    request_uuid_list = []
    for domain in target:
        if arguments.verbose:
            print(f"making a request to \033[01m\033[91murlscan.io\033[00m for a scan of the {domain} domain\n")
        headers = {'API-Key':api_key,'Content-Type':'application/json'}
        data = {"url": f"https://{domain}", "visibility": "public"}
        response = requests.post('https://urlscan.io/api/v1/scan/',headers=headers, data=json.dumps(data))
        request_uuid_list.append(response.json()['uuid'])
    return request_uuid_list

def seek_urlscan_result(domain_list, uuid_list):
    for (domain,uuid) in zip (domain_list,uuid_list):
        if arguments.verbose:
            print(f"getting the \033[01m\033[91murlscan.io\033[00m scan results for the {domain} domain\n")
        query = (requests.get(f"https://urlscan.io/api/v1/result/{uuid}"))
        formatted_query = json2html.convert(json = query.text)
        with open(f"results/{domain}/{today}-urlscan.html","w") as file:
            file.write(formatted_query)
        '''
        object = os.system(f"curl https://urlscan.io/api/v1/result/{uuid}")
        object = json2html.convert(json = object)
        print(object)
        with open(f"results/{domain}/{today}-urlscan","w") as file :
            file.write(str(object))
        '''
            
              



arguments = build_argumentparser()

configuration = get_config("config.yaml")

target_list = get_targetlist(arguments.file)

#creating a variable with today's date to help name the OSINT function output's file
today = date.today()

create_resultdirectories(target_list)

if configuration['theHarvester']['enabled']:
    run_theHarvester(target_list)
else:
	print("theHarvester is disabled in config file\n")
print

print("\n")

if configuration['dnscan']['enabled']:
    run_dnscan(target_list)
else:
	print("dnscan is disabled in config file\n")

print("\n")

if configuration['shodan']['enabled']:
    run_shodan(target_list)
else:
	print("shodan is disabled in config file\n")

print("\n")

if configuration['urlscan.io']['enabled']:
    uuid_list=probe_urlscan(target_list,configuration['urlscan.io']['api_key'])
    time.sleep(30)
    if arguments.verbose:
        print("Waiting for the \033[01m\033[91murlscan.io\033[00m request to be processed\n")
    seek_urlscan_result(target_list,uuid_list)
else:
	print("urlscan is disabled in config file\n")
