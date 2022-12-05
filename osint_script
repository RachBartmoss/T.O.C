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
    os.system(f"theHarveser -d {target} -b hackertarget")

def run_shodan(target):
    print("shodan is running")

def run_dnscan(target):

def run_urlscan(target, api_key):
    
    headers = {'API-Key':api_key,'Content-Type':'application/json'}
    data = {"url": f"https://{target}", "visibility": "public"}
    response = requests.post('https://urlscan.io/api/v1/scan/',headers=headers, data=json.dumps(data))
    uuid = response.json()['uuid']

    time.sleep(30)

    os.system(f"curl https://urlscan.io/api/v1/result/{uuid}")


build_argumentparser()

get_config("config.yaml")

get_targetlist("domain.txt")
