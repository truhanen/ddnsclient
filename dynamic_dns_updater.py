#! /usr/bin/env python3

import logging
import time
import re
from typing import NamedTuple, List
from argparse import ArgumentParser, FileType, RawTextHelpFormatter
from pathlib import Path
from configparser import ConfigParser

import requests
import bs4


FORMAT = '%(asctime)-15s|%(name)s|%(levelname)s|%(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


class UpdateError(RuntimeError):
    pass


def get_current_ip() -> str:
    ip = requests.get('http://api.ipify.org').content.decode(
        'utf-8')

    ip_pattern = '^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    if not re.match(ip_pattern, ip):
        error = RuntimeError(f'Got invalid IP {ip}.')
        logging.error(str(error))
        raise error

    return ip


def request_namecheap_dyndns_update(*, host: str, domain: str, password: str,
                                    ip: str, dry_run: bool = False):
    # The URL of the dynamic DNS service by Namecheap
    dyndns_url = 'https://dynamicdns.park-your-domain.com/update'

    url = (f'{dyndns_url}'
           f'?host={host}'
           f'&domain={domain}'
           f'&password={password}'
           f'&ip={ip}')

    logger.info(f'Updating {host}.{domain} with {ip}')

    if not dry_run:
        response = requests.get(url)

        if response.status_code != 200:
            error = UpdateError(f'Update failed with error status {response.status}')
            logger.error(str(error))
            raise error

        errors = bs4.BeautifulSoup(response.content, 'xml').find('errors')
        if errors:
            error = UpdateError(f'Update failed with error {errors}')
            logger.error(str(error))
            raise error
    else:
        logger.info(f'Dry-run \'request_namecheap_dyndns_update(...)\'. '
                    'Nothing was really updated.')


class Domain(NamedTuple):
    name: str
    password: str
    subdomains: str
    last_ip: str

    @classmethod
    def read_from_file(cls, path):
        """Read a list of domains to update from the given file."""
        config = ConfigParser()
        config.read(path)
        domains = []
        try:
            for domain_name in config.sections():
                values = config[domain_name]
                last_ip = values['lastip'] if 'lastip' in values else None
                domains.append(Domain(
                    domain_name, values['password'], values['subdomains'],
                    last_ip))
        except Exception:
            raise RuntimeError(f'Error reading domain info from {path}.')

        return domains

    def update(self, current_ip, dry_run : bool = False):
        subdomains = [s.strip() for s in self.subdomains.split(',')]
        for subdomain in subdomains:
            request_namecheap_dyndns_update(
                host=subdomain, domain=self.name, password=self.password,
                ip=current_ip, dry_run=dry_run)

    def update_last(self, dry_run : bool = False):
        if self.last_ip:
            self.update(self.last_ip, dry_run=dry_run)


class Updater:
    def __init__(self, domains: List[Domain], dry_run: bool = False):
        self.domains = domains
        self.dry_run = dry_run

    def run(self):
        """Update dynamic IP's to the DNS in an infinite loop."""
        try:
            self._run_update_loop()
        except KeyboardInterrupt:
            self._set_last_ip()

    def _run_update_loop(self):
        previous_ip = None

        while True:
            try:
                current_ip = get_current_ip()
            except Exception as e:
                logger.exception(
                    f'Checking failed due to {e}. Trying again in a minute.')
                time.sleep(60)
                continue

            logger.debug(f'Current IP is {current_ip}')

            if previous_ip == current_ip:
                logger.debug('IP not changed. Checking again after a minute.')
                time.sleep(60)
                continue

            logger.info(
                f'IP changed from {previous_ip} to {current_ip}. Updating it to DNS.')

            try:
                for domain in self.domains:
                    domain.update(current_ip, dry_run=self.dry_run)
            except Exception as e:
                logger.exception(
                    f'Updating failed due to {e}. Trying again in a minute.')
                time.sleep(60)
                continue

            previous_ip = current_ip

            logger.info('Checking again after 5 minutes.')
            time.sleep(300)

    def _set_last_ip(self):
        while True:
            try:
                for domain in self.domains:
                    domain.update_last(dry_run=self.dry_run)
                break
            except Exception as e:
                logger.exception(f'Updating failed due to {e}. '
                                 'Trying updating again after 1 minute.')
                time.sleep(60)
                continue


def main():
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        'domain_path', type=FileType('r'),
        help=('The file that lists the credentials and the domains to update. '
              'The file must be readable by configparser.ConfigParser,'
              'and contain sections of the form\n \n'
              '[mydomain.com]\npassword = mypassword\nsubdomains = mysubdomains\n'
              'lastip = mylastip\n'
              'where subdomains is a comma separated '
              'list of subdomain names. The value of lastip is requested '
              'to be set when the service is interrupted with SIGINT.'))
    parser.add_argument('-d', '--dry-run', action='store_true', dest='dry',
                        help='Dry-run. Don\'t really request any IP updates, only check.')

    args = parser.parse_args()
    dry_run = args.dry
    domain_path = Path(args.domain_path.name)

    domains = Domain.read_from_file(domain_path)
    updater = Updater(domains, dry_run=dry_run)
    updater.run()


if __name__ == '__main__':
    main()
