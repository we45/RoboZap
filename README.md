RoboZap
=======
Documentation for test library ``RoboZap``.

Please refer to the sample Zap Test in ``TestfireZap.robot`` that uses the RoboZap library and Selenium Library with it to perform "parameterized scanning"/authenticated scanning of the app. 

Installing
----------
- Please install all requirements in requirements.txt with `pip install requirements.txt`
- Install RoboZap libraries into the virtualenv with `python setup.py install`

Importing
---------
Arguments:  [proxy]

ZAP Library can be imported with one argument

Arguments:
    - ``proxy``: Proxy is required to initialize the ZAP Proxy at that
location


Examples:

| = Keyword Definition =  | = Description =  |

`| Library `|` RoboZap  | proxy|`

Start Headless Zap
------------------
Arguments:  [path]

Start OWASP ZAP without a GUI

Examples:

`| Start Headless ZAP  | path |`

Zap Define Context
------------------
Arguments:  [contextname, url]

Add Target to a context and use the context to perform all scanning/spidering
operations

Examples:

`| zap define context  | contextname  | target |`

Zap Open Url
------------
Arguments:  [url]

Invoke URLOpen with ZAP

Examples:

`| zap open url  | target |`

Zap Scan Status
---------------
Arguments:  [scan_id]

Fetches the status for the spider id provided by the user

Examples:

`| zap scan status  | scan_id |`

Zap Shutdown
------------
Arguments:  []

Shutdown process for ZAP Scanner

Zap Spider Status
-----------------
Arguments:  [spider_id]

Fetches the status for the spider id provided by the user
Examples:
`| zap spider status  | spider_id |`

Zap Start Ascan
---------------
Arguments:  [context, url, policy=Default Policy]

Initiates ZAP Active Scan on the target url and context

Examples:

`| zap start ascan  | context  | url |`

Zap Start Spider
----------------
Arguments:  [target, url]

Start ZAP Spider with ZAP's inbuilt spider mode

Examples:

`| zap start spider  | target  | url |`

Zap Write To Json File
----------------------
Arguments:  [base_url]

Fetches all the results from zap.core.alerts() and writes to json file.

Examples:

`| zap write to json  | scan_id |`

Zap Write To Tiny
-----------------
Arguments:  [base_url, db_name, app_name]

Fetches all the results from zap.core.alerts() and writes to json file.

Examples:

`| zap write to json  | scan_id |`