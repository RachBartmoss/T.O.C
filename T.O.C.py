#!/usr/bin/python3

import os
import argparse
import json
import requests
import yaml
import time
from datetime import date
from json2html import *
from tqdm import tqdm
import yagooglesearch

 
                     


def print_banner(banner_file):
    with open(banner_file,'r') as file:
        for line in file:
            print(f"\033[0;32m{line}\033[00m",end="")
            time.sleep(0.05)
    



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
    parser.add_argument('-d', '--dorks',help = 'list of dorks to use for the dorkscan tool')
    args = parser.parse_args()
    return args


#opening the .txt file containing the targets and onverting them into a python list
def get_targetlist(target_file):
    target_list = []
    with open(target_file,'r') as file:
        for line in file:
            target_list.append(line.strip())
    return target_list

def get_dorkslist(dorks_file):
    dorks_list = []
    with open(dorks_file,'r') as file:
        for line in file:
            dorks_list.append(line.strip())
    return dorks_list

#reading the yaml config file
def get_config(config_file):
    with open(config_file,'r') as file:
        configuration = yaml.safe_load(file)
    return configuration


#Function to run thHarvester over the domain list
def run_theHarvester(target):
    if arguments.verbose:
        target = tqdm(target)
    for domain in target:
        if arguments.verbose:
            target.set_description(f"Runnning \033[01m\033[91m theHarvester \033[00m on \033[01m\033[91m{domain}\033[00m")
            #print(f"running a \033[01m\033[91m theHarvester \033[00m scan on the {domain} domain using {arguments.source} as a source\n")

        os.system(f"theHarvester -d {domain} -b {arguments.source} > results/{domain}/{today}-theHarvester")
        if arguments.verbose:
            target.update()

#Function to run shodan over the domain list
def run_shodan(target):
    if arguments.verbose:
        target = tqdm(target)
    for domain in target:
        if arguments.verbose:
            target.set_description(f"Runnning \033[01m\033[91m Shodan \033[00m on \033[01m\033[91m{domain}\033[00m")
        #print(f"\033[01m\033[91mshodan\033[00m is running on domain {domain}\n")
    if arguments.verbose:
        target.update()    
        
    

#Function to run dnscan over the domain list
def run_dnscan(target):
    if arguments.verbose:
        target = tqdm(target)
    for domain in target:
        if arguments.verbose:
            target.set_description(f"Runnning \033[01m\033[91m Shodan \033[00m on \033[01m\033[91m{domain}\033[00m")
            #print(f"running a \033[01m\033[91mdnscan\033[00m scan on the {domain} domain\n")
        os.system(f"./dnscan/dnscan.py -d {domain} > results/{domain}/{today}-dnscan")
    if arguments.verbose:
        target.update()



'''
The following 2 functions are used to make a url request on the domain list and then 
making a request for the result and then formatting the .JSON result to a more readable
.HTML format
'''

def probe_urlscan(target, api_key):
    if arguments.verbose:
        target = tqdm(target)
    request_uuid_list = []
    for domain in target:
        if arguments.verbose:
            target.set_description(f"making a request to \033[01m\033[91murlscan.io\033[00m for a scan of the {domain} domain")
            #print(f"making a request to \033[01m\033[91murlscan.io\033[00m for a scan of the {domain} domain\n")
        headers = {'API-Key':api_key,'Content-Type':'application/json'}
        data = {"url": f"https://{domain}", "visibility": "public"}
        response = requests.post('https://urlscan.io/api/v1/scan/',headers=headers, data=json.dumps(data))
        request_uuid_list.append(response.json()['uuid'])
        if arguments.verbose:
            target.update()
    return request_uuid_list

def fetch_urlscan_result(domain_list, uuid_list):
    if arguments.verbose:
        domain_list = tqdm(domain_list)
    for domain in domain_list:
        uuid_count = 0
        if arguments.verbose:
            domain_list.set_description(f"getting the \033[01m\033[91murlscan.io\033[00m scan results for the {domain} domain")
            #print(f"getting the \033[01m\033[91murlscan.io\033[00m scan results for the {domain} domain\n")
        query = (requests.get(f"https://urlscan.io/api/v1/result/{uuid_list[uuid_count]}"))
        formatted_query = json2html.convert(json = query.text)
        with open(f"results/{domain}/{today}-urlscan.html","w") as file:
            file.write(formatted_query)
        if arguments.verbose:
            domain_list.update()
        uuid_count+=1    
              

def run_dorkscan(target,dorks):
    
    if arguments.verbose:
        target = tqdm(target)
    
    for domain in target:
        
        if arguments.verbose:
            target.set_description(f"Runnning \033[01m\033[91m Dorkscan \033[00m on \033[01m\033[91m{domain}\033[00m")

        result_list = []
        
        for dork in dorks:
            query = f"inurl:{domain} {dork}"
            result_list.append(f"-inurl:{query} :\n")
            client = yagooglesearch.SearchClient(query,verbosity = 0, max_search_result_urls_to_return=10, yagooglesearch_manages_http_429s=False)
            client.assign_random_user_agent()
            urls = client.search()
            
            if "HTTP_429_DETECTED" in urls:
                print("IP address detected by google, wait for 1H before making new requests with dorkscan\n")
                return

            for url in urls:
                result_list.append(url)
            result_list.append("\n")
            
            time.sleep(10)
            
        with open(f"results/{domain}/{today}-dorkscan","w") as file:
            for line in result_list:
                file.write(f"{line}\n")
        
        if arguments.verbose:
            target.update()


arguments = build_argumentparser()

configuration = get_config("config.yaml")

target_list = get_targetlist(arguments.file)

#creating a variable with today's date to help name the OSINT function output's file
today = date.today()

create_resultdirectories(target_list)

#print(header)
print_banner("banner.txt")


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
    print("\n")
    if arguments.verbose:
        for i in tqdm(range(30),desc=("Waiting 30 seconds for the Urlscan.io's result to be available")):
            time.sleep(1)
    else :
        time.sleep(30)
    print("\n")
    fetch_urlscan_result(target_list,uuid_list)
else:
	print("urlscan is disabled in config file\n")

print("\n")
    
if configuration['dorkscan']['enabled']:
    dorks_list = get_dorkslist(arguments.dorks)
    run_dorkscan(target_list, dorks_list)
else:
	print("dor is disabled in config file\n")
