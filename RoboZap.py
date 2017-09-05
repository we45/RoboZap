import os
from zapv2 import ZAPv2 as ZAP
import time
import subprocess
from robot.api import logger
import base64
import uuid
import json

import sys

reload(sys)
sys.setdefaultencoding('UTF8')

class RoboZap(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, proxy):
        '''
        ZAP Library can be imported with one argument
        Arguments:
            - ``proxy``: Proxy is required to initialize the ZAP Proxy at that location
        Examples:
        | = Keyword Definition =  | = Description =  |
        | Library `|` RoboZap  | proxy|
        '''
        self.zap = ZAP(proxies={'http': proxy, 'https':proxy})


    def start_headless_zap(self, path):
        """
        Start OWASP ZAP without a GUI
        Examples:
        | Start Headless ZAP  | path |
        """
        try:
            cmd = path + 'zap.sh -port 8090'
            print cmd
            subprocess.Popen(cmd.split(' '), stdout = open(os.devnull, 'w'))
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




    def zap_shutdown(self):
        """
        Shutdown process for ZAP Scanner
        """
        self.zap.core.shutdown()




