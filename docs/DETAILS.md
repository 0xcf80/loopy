# Target Parsing
Loopy is supposed to support lists of targets in different formats. In converts a supported file type into a list of `Target` classes that you can operate on.

## Target Class Attributes
Currently only host, port and service attributes are supported:
* host: IP address or domain
* port: the port of the service
* service: the service name (will become optional) such as http or ftp

URLs will likely be supported as well in the nearer future. Specifically, the idea is to build an URL generator that builds URLs of the form service://host:port automatically (e.g. for dirbusting).

I thought of implementing IP ranges as well, but I don't see any reason for this (despite for port scanners who do this natively. And the whole idea is that loopy is used to post-process the results of such scanners for individual services). 

## Filtering
You can currently filter targets by:
* host (regex)
* port, or list of ports
* service (regex)

This is extremely useful if you do not use a target list, but scanner results. You can then execute your tool against only those services that match your filter conditions (e.g. only on services where the service name contains the string http). 

Example:
```python
parser.add_filters(
    hostfilter='127.*',
    portfilter=[22,34835],
    servicefilter='(ss.*)|rpcbind'
)

targets_filter = parser.parse('./tests/targets_filter.csv')
```
## File Formats
### Nmap
Nmap's XML scan results can be parsed using the `NmapTargetParser` class. 

Depending on whether you set `use_ips` or `use_hosts` either the IP or hostname is scanned. You can provide both, so that targets added by nmap (e.g. when a hostname is resolved to an IP), are scanned automatically. Please note however, that if you provide your target in one form (e.g. IP), but specify to scan only hostnames (`use_ips = False`, `use_hosts = True`), your target may not be scanned if nmap could not identify any hostname. 

Default: `use_ips = True`, `use_hosts = False`

Example:
```python
parser = NmapTargetParser(use_hosts=True)
targets = parser.parse('./tests/nmap/nmap_localhost.xml')
```
### CSV (CHARACTER Seperated Value)
Despite the seperator, the CSV column order can be specified (defaults to host,port,service). You can also specify whether the first line of the file should be ignored. 

Example (service;host;port):
```python
parser = CSVTargetParser(
    skip_header=True,
    format = [
        TARGET_LAYOUT_ID_SERVICE, 
        TARGET_LAYOUT_ID_HOST, 
        TARGET_LAYOUT_ID_PORT
    ],
    seperator=';'
)
targets = parser.parse('./tests/targets_format2.csv')
```

Todo: 
* implement optional columns (service)
* Testcase (unknown columns are in place)
* Testcase (crucial columns are missing)

# Executors
Currently only shell exec is supported. 

Example:
```python
parser = CSVTargetParser(skip_header=True)
targets = parser.parse('./tests/targets.csv')

se = ShellExecutor()

args_nmap = ['-vvv', '-p{}'.format(ARGUMENT_ID_PORT), ARGUMENT_ID_HOST]

for t in targets:
    logging.info('Executing nmap for target {}'.format(t.prettify()))
    logging.info('Result {}'.format(se.exec_cmd('nmap', args_nmap, t)))
```

# Next steps (priority may change ;) )
* verify whether it is required to add reverse/forward lookup entries as new targests (see nmap parser)
* report generation
    * defining custom report directory / filename tructure [DONE]
    * writing simple strings [DONE]
    * writing stdout [DONE]
    * writing stderr [DONE]
    * writing stderr/stdout/string depending on success/failure [DONE] 
        * with default reporting directory for errors [DONE]
        * with custom reporting directory for errors [DONE]
    * custom logfile placeholder for tools that produce logs themselves 
* nmap parser [DONE]
    * supports `use_ips` and `use_hosts` parameters
        * depending on which one of the both is set, new targets are automatically added for hosts/ips (e.g. localhost for 127.0.0.1)
        * Default: `use_ips = True`, `use_hosts = False`
* target list generator (conversion from one format to another to just feed it into a different tool; e.g. nmap to file containing host:port entries)
* URL generator

# Example Tools TODO
* nikto
* dirsearch
* IKE / VPN
* ssh
* bruteforcer
* ldap

# Parsing Todo
* nmap [DONE]
* url building
* sqlite?
* nessus?

# Reporting Todo
* Generic CSV output class
* Log which command was issued for which host/port/service (and result code) 
* logging of raw tool output
    * custom file name generation scheme (e.g. service_host_port_tool_timestamp.csv)
* grep-like functionality (postprocessing)
* output target lists in different formats, so that you can use loopy as a converter for other tools
* sqlite output?
* metasploit output?
