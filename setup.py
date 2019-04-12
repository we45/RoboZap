from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='RoboZap',
    version='1.2.6',
    packages=[''],
    package_dir={'': 'robozap'},
    url='https://www.github.com/we45/RoboZap',
    license='MIT',
    author='we45',
    author_email='info@we45.com',
    description='Robot Framework Library for the OWASP ZAP Application Vulnerability Scanner' ,
    install_requires=[
        'requests==2.18.4',
        'python-owasp-zap-v2.4==0.0.14',
        'robotframework==3.0.4',
        'boto3'
    ],
    long_description = long_description,
    long_description_content_type='text/markdown'
)
