![logo](https://github.com/RachBartmoss/T.O.C/blob/main/T.O.C_logo.png)    

## What is this?:

T.O.C (Trouver Objet Caché) is an automated tool for open source investigation. It uses 5 other tools/sources and fuses them in one command-line script. It runs the 5 tools consecutively on a list of domain and outputs the result to a separate file for each domain and tool.

## What does it do and how does it do it ?:

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

#### Output:

T.O.C outputs all the scan result in the ./results/<domain_name> folder. Each tool gets its own output files. All of the output files are .txt
except for Urlscan which outputs a formatted .html file.




#### Arguments:

T.O.C accepts a range of arguments like a --verbose option to display what happens with progress bars:

  ```
  ./T.O.C.py -h
  usage: T.O.C.py [-h] [-v] -f FILE [-s SOURCE] [-d DORKS]

  options:
    -h, --help            show this help message and exit
    -v, --verbose         increase output verbosity
    -f FILE, --file FILE  list of domain name to search
    -s SOURCE, --source SOURCE
                          search source for theHarvester
    -d DORKS, --dorks DORKS
                          list of dorks to use for the dorkscan tool
  ```                        

#### Configuration:

T.O.C basic settings are found in the config.yam, each tool can be enabled if the `enabled` entry is set to `True` and disabled if set to `False`.
It is also there that you will need to fill in your urlscan and shodan api key in the `api_key` entry


## Examples of usage:

#### Lauching the different base tools:

The first way to use T.O.C is with the -h argument to display the help menu

  `$./T.O.C.py -h`

Other than that, the minimum number of arguments needed to run the script depends on the tools that are enabled.

In any case, the -f (--file) option  is mandatory:

  `$./T.O.C.py -f domain_sample.txt`

If the theHarvester tool is enabled, you will need to specify the source used by theHarvester for its research with the -s (--source) argument.
A list of source for theHarvester is displayed when you use the `theHarvester -h` command

  `$./T.O.C.py -f domain_sample.txt -s hackertarget`

Furthermore if the dorksan tool is enabled, you will need to specify a file with a list of google dorks with the -d (--dorks) argument

  `$./T.O.C.py -f domain_sample.txt -d dork_sample.txt`

Lastly you can use the -v argument to make the script's output verbose

  `$./T.O.C.py -f domain_sample.txt -s hackertarget -d dork_sample.txt -v`

## Using T.O.C in a docker container:

#### Building the container

To use T.O.C in a docker container, the first step is getting the Dockerfile. The easiest way to do this is to clone the repository and move inside the
folder it created


```
$git clone https://github.com/RachBartmoss/T.O.C.git
[...]
$cd T.O.C
```


Then you need to use the `docker build` command to build the image. During the building process, the container copies every .txt and .yaml file 
present alongside the Dockerfile to be used during runtime.


`$docker build . -t toc`


#### Running the container


Once the image is built, you can start running the container. The container is actually run exactly like the script, with the same argument


`$docker run toc -f domain_sample.txt -s hackertarget -v`


The last step is getting the output out of the container and on your host system, to do this, you first need to use the `docker ps`command to get the 
container's ID


```
docker ps -a

CONTAINER ID   IMAGE     COMMAND                  CREATED              STATUS                          PORTS     NAMES
7cd59c63867d   toc       "./T.O.C.py -f domai…"   About a minute ago   Exited (0) 53 seconds ago                 jolly_brattain
```


With the ID known, you can use the `docker cp` command to copy the container's result folder to your system


`docker cp 7cd59c63867d:/T.O.C/results Z:\my_folder\`


After this you will be able to retrieve your result file with your scan results
