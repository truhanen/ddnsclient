
from setuptools import setup

setup(
    name='truhanen.ddnsclient',
    version='0.1.0',
    author='Tuukka Ruhanen',
    author_email='tuukka.t.ruhanen@gmail.com',
    description=('A simple dynamic DNS (DDNS) client for updating the IP '
                 'address of a host to a DDNS service. Currently supports only '
                 'the DNS hosting service of Namecheap.'),
    install_requires=['requests', 'bs4'],
    python_requires='>=3.6',
    packages=['truhanen.ddnsclient'],
    scripts=['scripts/truhanen_ddnsclient_service'],
)
