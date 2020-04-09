
# truhanen.ddnsclient

A simple DDNS client for updating the dynamic IP addresses of a host to a dynamic DNS service. Currently supports only the DNS hosting service of [Namecheap](https://www.namecheap.com/).

## Installation

In the project root directory, run
```
pip install --user .
```

## Usage

To configure the domains to update, create a configuration file of the form
```
# Domain name as the section header
[mydomain.com]
# Password to the dynamic DNS service
password = mypassword
# Comma-separated sequence of subdomain names
subdomains = @, subdomain1, subdomain2
# IP to be set when the service is interrupted
lastip = 1.1.1.1

# Another domain
[mydomain2.org]
password = mypassword2
subdomains = @
lastip = 1.1.1.1
```

To start the service, use the installed script `truhanen_ddnsclient_service`,
```
$ truhanen_ddnsclient_service --help
usage: truhanen_ddnsclient_service [-h] [-d] domain_path

positional arguments:
  domain_path    The file that lists the credentials and the domains to update.
                 See README.md for example.

optional arguments:
  -h, --help     show this help message and exit
  -d, --dry-run  Dry-run. Don't really request any IP updates, only check.
```
