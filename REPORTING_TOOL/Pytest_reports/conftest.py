import os
import sys
import pytest
import time
import pytest_html
import datetime
from appium import webdriver
from py.xml import html
import logging
import configparser


ROOT_DIR = os.path.dirname(__file__)
sys.path.append(ROOT_DIR)
SCRIPTS_DIR = os.path.join(ROOT_DIR, "scripts")
sys.path.append(SCRIPTS_DIR)
HTML_REPORTS_DIR = os.path.join(ROOT_DIR, "html_reports")
session_data = None
driver=None
import logging
from reportportal_client import RPLogger
from hs_logger import logger, setup_logger
setup_logger(logger, logging.DEBUG)

def pytest_addoption(parser):
    """
    This pytest hook is used to define additional command line arguments.
    """
    parser.addoption(
        "--appium_url",
        dest="appium_url",
        type=str,
        nargs="?",
        default="",
        required=True,
        help="appium_url",
    )

    parser.addoption(
        "--udid",
        dest="udid",
        type=str,
        nargs="?",
        default="",
        required=True,
        help="udid",
    )
    parser.addoption(
        "--html_report",
        dest="html_report",
        type=str,
        nargs="?",
        default="",
        required=False,
        help="html_report",
    )


@pytest.fixture
def driver(request):
    """
    driver fixture create a appium driver with the capabilities and
    appium_url url and returns the driver for automation.
    """
    global session_data, driver
    # creating test class object for saving test values.
    session_data = request.cls()
    request.cls.session_data = session_data
    session_data.status = "Started"
    session_data.appium_url = request.config.getoption("appium_url")
    session_data.udid = request.config.getoption("udid")
    session_data.desired_capabilities.update({"udid": session_data.udid})
    hs_caps = {
        "headspin:capture.video": True,
        "headspin:testName": session_data.test_name,
        "headspin:session.name": session_data.test_name,
    }
    if "headspin" in session_data.appium_url:
        session_data.desired_capabilities.update(hs_caps)
    session_data.start_time = datetime.datetime.utcnow()
    print(session_data.appium_url,"\n",session_data.desired_capabilities)
    driver = webdriver.Remote(
        command_executor=session_data.appium_url,
        desired_capabilities=session_data.desired_capabilities,
    )
    session_data.session_id = driver.session_id
    add_allure_enviornment(session_data.desired_capabilities)
    yield driver
    logger.info("Teardown Started")
    if "pass" in session_data.status.lower():
        status = "Passed"
    else:
        status = "Failed"
    if "headspin" in session_data.appium_url:
        driver.execute_script('headspin:quitSession', {'status': status})
    else:
        driver.quit()

# ######################################## HTML REPORT ENHANCING HOOKS ########################################
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    if config.getoption("html_report").lower()=="true":
        if not os.path.exists(HTML_REPORTS_DIR):
            os.makedirs(HTML_REPORTS_DIR)

        report_name = f"HTML_Sample_Report_{int(time.time()*1000)}.html"
        config.option.htmlpath = os.path.join(HTML_REPORTS_DIR, report_name)
        config.option.self_contained_html = True

def pytest_html_report_title(report):
    """
    By default the report title will be the filename of the report, 
    you can edit it by using the pytest_html_report_title hook:
    """
    report.title = f"Sample Report Project, ID : {report.title.strip('.html').split('_')[-1]}"

@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    """
    Modifying the environment table in html report
    """
    session.config._metadata["Additional Environment Key"] = "Additional Environment Value"

@pytest.mark.optionalhook
def pytest_html_results_summary(prefix, summary, postfix):
    ''' modifying the summary in pytest html report'''

    prefix.extend([html.h3("Adding prefix message")])
    summary.extend([html.h3("Adding summary message")])
    postfix.extend([html.h3("Adding postfix message")])

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    This hook is executed after setup, call and teardown.
    This is useful to add extra test information to the results table.
    Here screenshot added to the html report for failed test.
    """
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])
    report.start_time = session_data.start_time
    if report.when == "call":
        if report.failed and driver:
            screenshot = driver.get_screenshot_as_base64()
            extras.append(pytest_html.extras.html(f'<img src="data:image/png;base64,{screenshot}" style="width:150px;height:300px;" onclick="window.open(this.src)" align="right">'))

    if report.when == "teardown":
        if hasattr(session_data, "session_id"):
            report.url = (
                "https://verizon.headspin.io/sessions/"
                + session_data.session_id
                + "/waterfall"
            )
    report.extra = extras

def pytest_html_results_table_header(cells):
    """
    Modifying(adding/removing) the Results table header.
    """
    cells.insert(1, html.th('Start Time', class_='sortable time', col='time'))
    cells.insert(3, html.th('Description'))
    cells.insert(5, html.th('Link', class_='link', col='link'))
    cells.pop()

def pytest_html_results_table_row(report, cells):
    """
    Modifying(adding/removing) the Results table row.
    """
    cells.insert(1, html.td(report.start_time, class_='col-time'))
    cells.insert(3, html.td("A Sample Description"))
    if hasattr(report, "url"):
        cells.insert(5, html.td(html.a(report.url, href=report.url)))
    cells.pop()

def pytest_html_results_table_html(report, data):
    """
    Modifying the extra part of the results table in the html report
    """
    if report.passed:
        # del data[:] # Delete the extra section data such as log.
        data.append("Appended Sample Text For Passed Session Only")



# ######################################## END END END END END END END ########################################

#Logger for ReportPortal 
@pytest.fixture(scope="session")
def rp_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logging.setLoggerClass(RPLogger)
    return logger

#add environment for allure report
def add_allure_enviornment(data):
    config = configparser.ConfigParser()
    config['CAPS'] = {'UDID': data.get('udid'),'Platform_Name':  data.get('platformName')}
    with open('allure-report/allure-results/environment.properties', 'w') as configfile:
        config.write(configfile)

