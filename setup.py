from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


install_dependencies = (
    'python-owasp-zap-v2.4==0.0.14',
    'requests==2.18.4',
    'robotframework==3.0.4',
)

setup(
    name='RoboZap',
    version='1.1',
    packages=[''],
    package_dir={'': 'robozap'},
    url='http://www.we45.com/',
    license='MIT License',
    author='Abhay Bhargav',
    install_requires = [
    'python-owasp-zap-v2.4==0.0.14',
    'requests==2.18.4',
    'robotframework==3.0.4',
    ],
    description='Robot Framework Library for OWASP ZAP 2.7',
    long_description = long_description,
    long_description_content_type='text/markdown'
)
