*** Settings ***
Library  /Users/abhaybhargav/Documents/Code/Python/RoboZap/RoboZap.py  http://127.0.0.1:8090/
Library  Collections
Library  Selenium2Library

*** Variables ***
${ZAP_PATH}  /Applications/ZAP_2.6.0.app/Contents/Java/
${TARGET}  http://104.236.85.150/
${CONTEXT}  CTF2
${BASE_URL}  http://104.236.85.150/
${LOGIN_URL}  http://104.236.85.150/login/
${SCANPOLICY}  Minimal OWASP Policy
${APPNAME}  weCare
${TINYPATH}  /Users/abhaybhargav/Documents/vul_db.json


*** Test Cases ***
ZAP Init
    [Tags]  zap_init
    start headless zap  ${ZAP_PATH}
    zap open url  ${TARGET}

Open Healthcare App
    [Tags]  phantomjs
    ${service args}=    Create List    --proxy=127.0.0.1:8090
    Create WebDriver  PhantomJS  service_args=${service args}
    go to  ${LOGIN_URL}

Login to Healthcare App
    [Tags]  login
    input text  email_id  betty.ross@we45.com
    input password  password  secdevops
    click button  id=submit
    set browser implicit wait  10
    location should be  ${BASE_URL}dashboard/

Visit Random Pages
    [Tags]  visit
    go to  ${BASE_URL}tests/
    input text  search  something
    click button  name=look
    go to  ${BASE_URL}secure_tests/

ZAP Contextualize
    [Tags]  zap_context
    ${contextid}=  zap define context  ${CONTEXT}  ${TARGET}
    set suite variable  ${CONTEXT_ID}  ${contextid}

#ZAP Crawl
#    ${spider_id}=  zap start spider  ${CONTEXT}  ${TARGET}
#    zap spider status  ${spider_id}

ZAP Active Scan
    [Tags]  zap_scan
    ${scan_id}=  zap start ascan  ${CONTEXT_ID}  ${TARGET}  ${SCANPOLICY}
    set suite variable  ${SCAN_ID}  ${scan_id}
    zap scan status  ${scan_id}
    zap write to json file  ${BASE_URL}
    zap write to tiny  ${BASE_URL}  ${TINYPATH}  ${APPNAME}


ZAP Die
    [Tags]  zap_kill
    zap shutdown

Close App
    [Tags]  browser_close
    close browser