
from setuptools import setup

setup(
    name='dyndns_service',
    version='0.1',
    description=('Simple service for updating dynamic IP\'s of a host '
                 'to the dynamic DNS service of namecheap.com'),
    install_requires=['requests', 'bs4', 'lxml'],
    python_requires='>=3.6',
    py_modules=['dyndns_service'],
    scripts=['dyndns_service.py'],
)
