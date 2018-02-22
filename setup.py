from setuptools import setup

install_dependencies = (
    'certifi==2017.7.27.1',
    'chardet==3.0.4',
    'decorator==4.1.2',
    'idna==2.6',
    'python-owasp-zap-v2.4==0.0.11',
    'requests==2.18.4',
    'robotframework==3.0.2',
    'robotframework-requests==0.4.7',
    'robotframework-selenium2library==1.8.0',
    'selenium==3.5.0',
    'six==1.10.0',
    'tinydb==3.5.0',
    'urllib3==1.22',
)

setup(
    name='RoboZap',
    version='0.1',
    packages=[''],
    package_dir={'': 'robozap'},
    url='www.we45.com',
    license='MIT License',
    author='Abhay Bhargav',
    author_email='Twitter: @abhaybhargav',
    install_requires = [
    'certifi==2017.7.27.1',
    'chardet==3.0.4',
    'decorator==4.1.2',
    'idna==2.6',
    'python-owasp-zap-v2.4==0.0.11',
    'requests==2.18.4',
    'robotframework==3.0.2',
    'robotframework-requests==0.4.7',
    'robotframework-selenium2library==1.8.0',
    'selenium==3.5.0',
    'six==1.10.0',
    'tinydb==3.5.0',
    'urllib3==1.22',
    ],
    description='Robot Framework Library for OWASP ZAP 2.6'
)
