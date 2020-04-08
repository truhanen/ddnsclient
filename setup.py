
from setuptools import setup

setup(
    name='dynamic_dns_updater',
    version='0.1.0',
    description=('Simple service for updating dynamic IP\'s of a host '
                 'to the dynamic DNS service of namecheap.com'),
    install_requires=['requests', 'bs4', 'lxml'],
    python_requires='>=3.6',
    py_modules=['dynamic_dns_updater'],
    scripts=['dynamic_dns_updater.py'],
)
