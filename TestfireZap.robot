*** Settings ***
Library  RoboZap  http://127.0.0.1:8090/
Library  Collections
Library  Selenium2Library

*** Variables ***
${ZAP_PATH}  /Applications/ZAP_2.6.0.app/Contents/Java/
${TARGET}  http://demo.testfire.net/
${CONTEXT}  Testfire
${BASE_URL}  http://demo.testfire.net/
${LOGIN_URL}  http://demo.testfire.net/bank/login.aspx
${SCANPOLICY}  Minimal OWASP Policy
${APPNAME}  Testfire
${TINYPATH}  /Users/abhaybhargav/Documents/vul_db.json


*** Test Cases ***
ZAP Init
    [Tags]  zap_init
    start headless zap  ${ZAP_PATH}
    zap open url  ${TARGET}

Open App
    [Tags]  phantomjs
    ${service args}=    Create List    --proxy=127.0.0.1:8090
    Create WebDriver  PhantomJS  service_args=${service args}
    go to  ${LOGIN_URL}

Login to Testfire App
    [Tags]  login
    input text  uid  admin
    input password  passw  admin
    click button  name=btnSubmit
    set browser implicit wait  10
    location should be  ${BASE_URL}bank/main.aspx

ZAP Contextualize
    [Tags]  zap_context
    ${contextid}=  zap define context  ${CONTEXT}  ${TARGET}
    set suite variable  ${CONTEXT_ID}  ${contextid}

ZAP Crawl
    ${spider_id}=  zap start spider  ${CONTEXT}  ${TARGET}
    zap spider status  ${spider_id}

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