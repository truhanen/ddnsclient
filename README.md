
# dynamic-dns-updater

A simple service for updating the dynamic IP's of a host to a dynamic DNS service. Currently supports only the DNS hosting service of [namecheap.com](https://www.namecheap.com/).

## Installation

In the project root directory, run
```
pip install --user .
```

## Usage

To start the service, use the installed script `dynamic_dns_updater.py`,
```
$ dynamic_dns_updater.py --help
usage: dynamic_dns_updater.py [-h] [-d] domain_path

positional arguments:
  domain_path    The file that lists the credentials and the domains to update.
                 The file must be readable by configparser.ConfigParser,
                 and contain sections of the form

                 [mydomain.com]
                 password = mypassword
                 subdomains = mysubdomains
                 lastip = mylastip

                 where subdomains is a comma separated list of subdomain names.
                 The value of lastip is requested to be set when the service is
                 interrupted with SIGINT.

optional arguments:
  -h, --help     show this help message and exit
  -d, --dry-run  Dry-run. Don't really request any IP updates, only check.
```
