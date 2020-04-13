import pytest
from robozap.RoboZap import RoboZap
import time

context = ""
spider_id = ""
scan_id = ""

def test_start_gui_zap():
    robo = RoboZap("http://127.0.0.1:8090/", "8090")
    robo.start_gui_zap("/Applications/ZAP_29.app/Contents/Java/")

def test_zap_open_url():
    robo = RoboZap("http://127.0.0.1:8090/", "8090")
    robo.zap_open_url('http://localhost:5050')

def test_zap_define_context():
    robo = RoboZap("http://127.0.0.1:8090/", "8090")
    global context
    context = robo.zap_define_context("test", "http://localhost:5050")
    print("context", context)

def test_zap_spider():
    robo = RoboZap("http://127.0.0.1:8090/", "8090")
    global spider_id
    spider_id = robo.zap_start_spider("test", 'http://localhost:5050')
    print(spider_id)

def test_zap_spider_status():
    robo = RoboZap("http://127.0.0.1:8090/", "8090")
    robo.zap_spider_status(spider_id)

def test_zap_active_scan():
    robo = RoboZap("http://127.0.0.1:8090/", "8090")
    global scan_id
    scan_id = robo.zap_start_ascan(context, "http://localhost:5050/")
    print("scan_id", scan_id)

def test_zap_active_scan_status():
    time.sleep(4)
    robo = RoboZap("http://127.0.0.1:8090/", "8090")
    robo.zap_scan_status(scan_id)


def test_zap_export_report():
    time.sleep(3)
    robo = RoboZap("http://127.0.0.1:8090/", "8090")
    robo.zap_export_report("/Users/abhaybhargav/Downloads/hello.json", "json", "Test Report", "Abhay Bhargav")



def test_zap_shutdown():
    robo = RoboZap("http://127.0.0.1:8090/", "8090")
    robo.zap_shutdown()
