import os
from zapv2 import ZAPv2 as ZAP
import time
import subprocess
from robot.api import logger
import base64
import uuid
import json
import requests
from datetime import datetime

import sys

reload(sys)
sys.setdefaultencoding('UTF8')

class RoboZap(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, proxy, port):
        '''
        ZAP Library can be imported with one argument

        Arguments:
            - ``proxy``: Proxy is required to initialize the ZAP Proxy at that location. This MUST include the port specification as well
            - ``port``: This is a portspecification that will be used across the suite


        Examples:

        | = Keyword Definition =  | = Description =  |

        | Library `|` RoboZap  | proxy | port |
        '''
        self.zap = ZAP(proxies={'http': proxy, 'https':proxy})
        self.port = port


    def start_headless_zap(self, path):
        """
        Start OWASP ZAP without a GUI

        Examples:

        | start gui zap  | path | port |

        """
        try:
            cmd = path + 'zap.sh -daemon -config api.disablekey=true -port {0}'.format(self.port)
            print cmd
            subprocess.Popen(cmd.split(' '), stdout = open(os.devnull, 'w'))
            time.sleep(10)
        except IOError as e:
            print 'ZAP Path is not configured correctly'


    def start_gui_zap(self, path):
        """
        Start OWASP ZAP with a GUI

        Examples:

        | start gui zap  | path | port |

        """
        try:
            cmd = path + 'zap.sh -config api.disablekey=true -port {0}'.format(self.port)
            print cmd
            subprocess.Popen(cmd.split(' '), stdout=open(os.devnull, 'w'))
            time.sleep(10)
        except IOError as e:
            print 'ZAP Path is not configured correctly'

    def zap_open_url(self, url):
        """
        Invoke URLOpen with ZAP

        Examples:

        | zap open url  | target |

        """
        self.zap.urlopen(url)
        time.sleep(4)

    def zap_define_context(self, contextname, url):
        """
        Add Target to a context and use the context to perform all scanning/spidering operations

        Examples:

        | zap define context  | contextname  | target |

        """
        regex = "{0}.*".format(url)
        context_id = self.zap.context.new_context(contextname=contextname)
        time.sleep(1)
        self.zap.context.include_in_context(contextname, regex=regex)
        time.sleep(5)
        return context_id

    def zap_start_spider(self, target, url):
        """
        Start ZAP Spider with ZAP's inbuilt spider mode

        Examples:

        | zap start spider  | target  | url |

        """
        try:

            spider_id = self.zap.spider.scan(url=url, contextname=target)
            time.sleep(2)
            return spider_id
        except Exception as e:
            print str(e.message)
        #return spider #this is the spider id
    #
    def zap_spider_status(self, spider_id):
        """
        Fetches the status for the spider id provided by the user
        Examples:
        | zap spider status  | spider_id |
        """
        while int(self.zap.spider.status(spider_id)) < 100:
            logger.info('Spider running at {0}%'.format(int(self.zap.spider.status(spider_id))))
            time.sleep(10)


    def zap_start_ascan(self, context, url, policy = "Default Policy"):
        """
        Initiates ZAP Active Scan on the target url and context

        Examples:

        | zap start ascan  | context  | url |

        """
        try:
            scan_id = self.zap.ascan.scan(contextid=context, url=url, scanpolicyname=policy)
            time.sleep(2)
            return scan_id
        except Exception as e:
            print str(e.message)

    def zap_scan_status(self, scan_id):
        """
        Fetches the status for the spider id provided by the user

        Examples:

        | zap scan status  | scan_id |

        """
        while int(self.zap.ascan.status(scan_id)) < 100:
            logger.info('Scan running at {0}%'.format(int(self.zap.ascan.status(scan_id))))
            time.sleep(10)


    def zap_write_to_json_file(self, base_url):
        """

        Fetches all the results from zap.core.alerts() and writes to json file.

        Examples:

        | zap write to json  | scan_id |

        """
        core = self.zap.core
        all_vuls = []
        for i, na in enumerate(core.alerts(baseurl=base_url)):
            vul = {}
            vul['name'] = na['alert']
            vul['confidence'] = na.get('confidence', '')
            if na.get('risk') == 'High':
                vul['severity'] = 3
            elif na.get('risk') == 'Medium':
                vul['severity'] = 2
            elif na.get('risk') == 'Low':
                vul['severity'] = 1
            else:
                vul['severity'] = 0

            vul['cwe'] = na.get('cweid', 0)
            vul['uri'] = na.get('url', '')
            vul['param'] = na.get('param', '')
            vul['attack'] = na.get('attack', '')
            vul['evidence'] = na.get('evidence', '')
            message_id = na.get('messageId', '')
            message = core.message(message_id)
            if isinstance(message, dict):
                request = base64.b64encode("{0}{1}".format(message['requestHeader'], message['requestBody']))
                response = base64.b64encode("{0}{1}".format(message['responseHeader'], message['responseBody']))
                vul['request'] = request
                vul['response'] = response
                vul['rtt'] = int(message['rtt'])
            all_vuls.append(vul)

        filename = "{0}.json".format(str(uuid.uuid4()))
        with open(filename, 'wb') as json_file:
            json_file.write(json.dumps(all_vuls))

        return filename


    def zap_write_to_orchy(self, report_file, token, hook_uri):
        """
                Generates an XML Report and writes said report to orchestron over a webhook.

                Mandatory Fields:
                - Report_file: Absolute Path of Report File - JSON or XML
                - Token: Webhook Token
                - hook_uri: the unique URI to post the XML Report to

                Examples:

                | zap write to orchy  | report_file_path | token | hook_uri

        """
        # xml_report = self.zap.core.xmlreport()
        # with open('zap_scan.xml','w') as zaprep:
        #     zaprep.write(xml_report)
        try:
            files = {'file': open(report_file,'rb')}
            auth = {'Authorization': 'Token {0}'.format(token)}
            r = requests.post(hook_uri, headers = auth, files = files)
            if r.status_code == 200:
                return "Successfully posted to Orchestron"
            else:
                raise Exception("Unable to post successfully")
        except Exception as e:
            print(e)


    def zap_export_report(self, export_file, export_format, report_title, report_author):
        """
        This functionality works on ZAP 2.7.0 only. It leverages the Export Report Library to generate a report.
        Currently ExportReport doesnt have an API endpoint in python. We will be using the default ZAP REST API for this

        :param export_file: location to which the export needs to happen. Absolute path with the export file name and extension
        :param export_format: file extension of the exported file. Can be XML, JSON, HTML, PDF, DOC
        :param report_title: Title of the exported report
        :param report_author: Name of the Author of the report
        Examples:

        | zap export report | export_path | export_format |

        """

        url = 'http://localhost:{0}/JSON/exportreport/action/generate/'.format(self.port)
        export_path = export_file
        extension = export_format
        report_time = datetime.now().strftime("%I:%M%p on %B %d, %Y")
        source_info = '{0};{1};ZAP Team;{2};{3};v1;v1;{4}'.format(report_title, report_author, report_time, report_time, report_title)
        alert_severity = 't;t;t;t'  # High;Medium;Low;Info
        alert_details = 't;t;t;t;t;t;t;t;t;t'  # CWEID;#WASCID;Description;Other Info;Solution;Reference;Request Header;Response Header;Request Body;Response Body
        data = {'absolutePath': export_path, 'fileExtension': extension, 'sourceDetails': source_info,
                'alertSeverity': alert_severity, 'alertDetails': alert_details}

        r = requests.post(url, data=data)
        if r.status_code == 200:
            pass
        else:
            raise Exception("Unable to generate report")




    def zap_shutdown(self):
        """
        Shutdown process for ZAP Scanner
        """
        self.zap.core.shutdown()




