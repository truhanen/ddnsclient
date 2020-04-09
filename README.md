
# ddnsclient

A simple dynamic DNS (DDNS) client for updating the IP address of a host to a DDNS service. Currently supports only the DNS hosting service of [Namecheap](https://www.namecheap.com/).

## Requirements

- Python 3.6+
- Enabled DDNS service at [Namecheap](https://www.namecheap.com/)

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
# Password to the DDNS service
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

To start updating the listed domains with the current IP address every time it changes, use the installed script `truhanen_ddnsclient_service`,
```
$ truhanen_ddnsclient_service mydomains.conf
```
