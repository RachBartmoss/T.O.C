#!/usr/bin/python3

import os
import argparse
import json
import requests
import yaml
import time


#building the argument parser for the script
def build_argumentparser():
    global parser
    parser = argparse.ArgumentParser()
    parser.parse_args()


#opening the .txt file containing the targets and onverting them into a python list
def get_targetlist(target_file):
    global target_list
    target_list = []
    with open(target_file) as file:
        for line in file:
            target_list.append(line.strip())

#reading the yaml config file
def get_config(config_file):
    global configuration
    with open(config_file,'r') as file:
        configuration = yaml.safe_load(file)



def run_theHarvester(target):
    for domain in target:
        os.system(f"theHarvester -d {domain} -b hackertarget")

def run_shodan(target):
    for domain in target:
        print(f"shodan is running on domain {domain}")

def run_dnscan(target):
    for domain in target:
        os.system(f"./dnscan.py -d {domain}")

def run_urlscan(target, api_key):
    global request_uuid_list
    request_uuid_list = []
    for domain in target:
        headers = {'API-Key':api_key,'Content-Type':'application/json'}
        data = {"url": f"https://{domain}", "visibility": "public"}
        response = requests.post('https://urlscan.io/api/v1/scan/',headers=headers, data=json.dumps(data))
        request_uuid_list.append(response.json()['uuid'])

    time.sleep(30)

    for uuid in request_uuid_list:
        os.system(f"curl https://urlscan.io/api/v1/result/{uuid}")


build_argumentparser()

get_config("config.yaml")

get_targetlist("domain.txt")

urlscan_api_key = configuration['tools']['urlscan.io']['api_key']


if configuration['tools']['theHarvester'] == "enabled":
    run_theHarvester(target_list)
else:
	print("theHarvester is disabled in config file")



if configuration['tools']['dnscan'] == "enabled":
    run_dnscan(target_list)
else:
	print("dnscan is disabled in config file")


if configuration['tools']['shodan'] == "enabled":
    run_shodan(target_list)
else:
	print("shodan is disabled in config file")


if configuration['tools']['urlscan.io'] == "enabled":
    run_urlscan(target_list,urlscan_api_key)
else:
	print("urlscan is disabled in config file")
