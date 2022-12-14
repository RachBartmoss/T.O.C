# projet_osint

## What is this?

Osint_Project is an automated tool for open source investigation. It uses 4 other tools/sources and fuses them in one command-line script. It runs the 4 tools consecutively on a list of domain and outputs the result to a separate file for each domain and tool.

## What does it do and how does it do it ?

Osint_Project takes a texte file as input and iniate 4 scans from 4 different tools on each of the domain listed.

The functions pertinent to the scan are as follows:

|Function's name|Role|
|---------------|----|
|`run_theHarvester()`|Initiate a theHarvester scan on each of the domain using the --source argument as the source|
|`run_dnscan()`|Initiate a dsncan scan on each of the domain|
