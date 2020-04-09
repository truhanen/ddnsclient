
# dynamic-dns-updater

A simple service for updating the dynamic IP's of a host to a dynamic DNS service. Currently supports only the DNS hosting service of [namecheap.com](https://www.namecheap.com/).

## Installation

In the project root directory, run
```
pip install --user .
```

## Usage

To start the service, use the installed script `dynamic_dns_updater`,
```
$ dynamic_dns_updater --help
usage: dynamic_dns_updater [-h] [-d] domain_path

positional arguments:
  domain_path    The file that lists the credentials and the domains to update.
                 See the example.conf file for example.

optional arguments:
  -h, --help     show this help message and exit
  -d, --dry-run  Dry-run. Don't really request any IP updates, only check.
```

Contents of `example.conf`
```
# Domain name as the section header
[mydomain.com]
# Password to the dynamic DNS service
password = mypassword
# Comma-separated sequence of subdomain names
subdomains = @, subdomain1, subdomain2
# IP to be set when the service is interrupted
lastip = 1.1.1.1

[mydomain2.org]
password = mypassword2
subdomains = @
lastip = 1.1.1.1
```
