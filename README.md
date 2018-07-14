RoboZap
=======
Documentation for test library ``RoboZap``.

Installing
----------
- Install RoboZap libraries into the virtualenv with `pip install RoboZap`

Importing
---------
Arguments:  [proxy]

ZAP Library can be imported with one argument

Arguments:
    - ``proxy``: Proxy is required to initialize the ZAP Proxy at that location. Must include PortSpec
    - ``port``: Port is required to be set as a global/suite variable for the rest of the suite to access
location


Examples:

| = Keyword Definition =  | = Description =  |

`| Library `|` RoboZap  | proxy| port | `


Major Keywords
================

Start Headless Zap
------------------
Arguments:  [path]

Start OWASP ZAP without a GUI

Examples:

`| start headless zap  | path |`

Start GUI Zap
------------------
Arguments:  [path]

Start OWASP ZAP without a GUI

Examples:

`| start gui zap  | path |`

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
Arguments:  [scan_id]

Fetches all the results from zap.core.alerts() and writes to json file.

Examples:

`| zap write to json  | scan_id |`


Zap Generate Report  (Export Report Plugin)
----------------------
Arguments:  [file_path, report_format, report_title, report_author]

Uses the `Export Report` from ZAP to generate reports in multiple formats.
- file_path: needs to be an absolute path and include the file name with extension.
- format: can be `json|xml|xhtml|pdf|doc`
- report title: Any title you deem fit for the exported report
- report auhor: Any name you want for the author of the report

Examples:

`| zap export report | file_path | format | report title | report author`