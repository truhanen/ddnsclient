
from setuptools import setup

setup(
    name='dynamic-dns-updater',
    version='0.1.0',
    author='Tuukka Ruhanen',
    author_email='tuukka.t.ruhanen@gmail.com',
    description=('A simple service for updating the dynamic IP\'s of a host to '
                 'a dynamic DNS service. Currently supports only the DNS '
                 'hosting service of namecheap.com.'),
    install_requires=['requests', 'bs4', 'lxml'],
    python_requires='>=3.6',
    py_modules=['dynamic_dns_updater'],
    scripts=['scripts/dynamic_dns_updater'],
)
