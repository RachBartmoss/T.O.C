![logo](https://github.com/RachBartmoss/T.O.C/blob/main/T.O.C_logo.png)                                         
                     

## What is this?

T.O.C (Trouver Objet Caché) is an automated tool for open source investigation. It uses 5 other tools/sources and fuses them in one command-line script. It runs the 5 tools consecutively on a list of domain and outputs the result to a separate file for each domain and tool.

## What does it do and how does it do it ?

T.O.C takes a texte file as input and iniate 5 scans from 5 different tools on each of the domain listed.

#### The 5 tools used in T.O.C are:

[theHarvester](https://github.com/laramies/theHarvester) : A simple yet powerful OSINT tool that gathers informations from multiple public resource  
[Dnscan](https://github.com/rbsec/dnscan) : A python wordlist-based DNS subdomain scanner  
[Shodan](https://www.shodan.io/) : The world's first search engine for Internet-connected devices  
[urlscan.io](https://urlscan.io/) : A free service to scan and analyse websites  
Dorkscan : A simple google dorks script using the [yagooglesearch](https://github.com/opsdisk/yagooglesearch) module


#### The functions pertinent to the scan are as follows:

|Function's name|Role|
|---------------|----|
|`run_theHarvester()`|Initiate a theHarvester scan on each of the domain using the --source argument as the source|
|`run_dnscan()`|Initiate a dsncan scan on each of the domain|
|`run_shodan()`|Initiate a shodan scan on each of the domain|
|`run_dorkscan()`|Initiate a google dorks search on the domain the list of dorks provided with the -d argument|

The case of urlscan.io is a little bit different, it makes a request on the urlscan.io API in one function and then fetches the results in another


|Function's name|Role|
|---------------|----|
|`probe_urlscan`|Sends a request to urlscan.io to scan each of the domain, recuperating a list of request IDs (called uuid)|
|`fetch_urlscan_result`|Fetches the result from urlscan.io using the request ID (uuid) we get from the first function|


#### Arguments

T.O.C accepts a range of arguments like a --verbose option to display what happens in beautiful progress bars:

```
./osint.py -h
usage: osint.py [-h] [-v] -f FILE [-s SOURCE]

options:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -f FILE, --file FILE  list of domain name to search
  -s SOURCE, --source SOURCE
                        search source for theHarvester
```                        
                        
                                                                                                                                                                      
