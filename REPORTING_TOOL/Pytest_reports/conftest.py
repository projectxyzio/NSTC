import os
import sys
import pytest
import time
import pytest_html
import datetime
import allure
import base64
from appium import webdriver
from allure_commons.types import AttachmentType
from reportportal_client import RPLogger, RPLogHandler
from py.xml import html
import logging
import configparser


ROOT_DIR = os.path.dirname(__file__)
sys.path.append(ROOT_DIR)
SCRIPTS_DIR = os.path.join(ROOT_DIR, "scripts")
sys.path.append(SCRIPTS_DIR)
HTML_REPORTS_DIR = os.path.join(ROOT_DIR, "html_reports")
ALLURE_REPORTS_DIR = os.path.join(ROOT_DIR, "allure-report")
ALLURE_RESULTS_DIR = os.path.join(ALLURE_REPORTS_DIR, "allure-results")

from hs_logger import logger, setup_logger

setup_logger(logger, logging.DEBUG)
session_data = None
driver = None


def pytest_addoption(parser):
    """
    allows you to add custom command line options to your tests.
    """
    parser.addoption(
        "--appium_url",
        dest="appium_url",
        type=str,
        default="",
        required=True,
        help="appium_url",
    )
    parser.addoption(
        "--udid",
        dest="udid",
        type=str,
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
    parser.addoption(
        "--allure_report",
        dest="allure_report",
        type=str,
        nargs="?",
        default="",
        required=False,
        help="allure_report",
    )


@pytest.fixture
def driver(request):
    """
    driver fixture create a appium driver with the capabilities and
    appium_url url and returns the driver for automation.
    """

    print()
    logger.info(f"{'<'*10} Starting Test: {request.node.name} {'>'*10}")

    global session_data, driver
    # creating test class object for saving test variables.
    session_data = request.cls()

    session_data.status = "Test Started"
    session_data.appium_url = request.config.getoption("appium_url")
    session_data.udid = request.config.getoption("udid")

    session_data.desired_capabilities = {
        "appPackage": session_data.package,
        "appActivity": session_data.activity,
        "udid": session_data.udid,
        "newCommandTimeout": 60,
        "platformName": "android",
        "automationName": "uiautomator2",
        "autoGrantPermissions" : True,
    }

    # Adding headspin capabilities, when headspin appium url is used.
    if "headspin" in session_data.appium_url:
        session_data.desired_capabilities.update(
            {
                "headspin:capture.video": True,
                "headspin:testName": session_data.test_name,
                "headspin:session.name": session_data.test_name,
            }
        )

    session_data.start_time = datetime.datetime.utcnow()
    # Connect to Appium server and launch the YouTube app
    driver = webdriver.Remote(
        command_executor=session_data.appium_url,
        desired_capabilities=session_data.desired_capabilities,
    )

    session_data.session_id = driver.session_id

    # updating Environment section in allure report
    if request.config.getoption("allure_report_dir"):
        add_allure_environment(session_data.desired_capabilities)

    yield driver
    logger.info("Teardown Started")

    if "pass" in session_data.status.lower():
        status = "Passed"
    else:
        status = "Failed"

    # Quit driver and set session status when headspin webdriver url is used
    if "headspin" in session_data.appium_url:
        driver.execute_script("headspin:quitSession", {"status": status})
    else:
        driver.quit()

    logger.info("Teardown Ended")


# ######################################## HTML REPORT ENHANCING HOOKS ########################################
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """
    allows you to configure the testing environment and add custom functionality to your tests.
    """

    # Enable Allure report
    if config.getoption("allure_report").lower() == "true":
        config.option.allure_report_dir = ALLURE_RESULTS_DIR
        logger.info("Allure Report enabled for this execution")

    # Enable HTML report
    if config.getoption("html_report").lower() == "true":
        if not os.path.exists(HTML_REPORTS_DIR):
            os.makedirs(HTML_REPORTS_DIR)

        report_name = f"HTML_Sample_Report_{int(time.time()*1000)}.html"
        config.option.htmlpath = os.path.join(HTML_REPORTS_DIR, report_name)
        config.option.self_contained_html = True
        logger.info("Pytest HTML Report enabled for this execution")

    # logging Enable report portal
    if config.getoption("rp_enabled"):
        logger.info("Report Portal enabled for this execution")


def pytest_html_report_title(report):
    """
    allows you to update the HTML Report title
    """
    report.title = (
        f"Sample Report Project, ID : {report.title.strip('.html').split('_')[-1]}"
    )


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    """
    allows you to perform custom actions at the end of a test session.
    Here we are updating the environment table in html report
    """
    session.config._metadata[
        "Additional Environment Key"
    ] = "Additional Environment Value"


@pytest.mark.optionalhook
def pytest_html_results_summary(prefix, summary, postfix):
    """
    allows you to customize the summary information that is displayed in the HTML report.
    """

    prefix.extend([html.h3("Adding prefix message")])
    summary.extend([html.h3("Adding summary message")])
    postfix.extend([html.h3("Adding postfix message")])


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    This is useful to add extra test information to the results table.
    Here screenshot added to the html report for failed test.
    """
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])
    report.start_time = session_data.start_time if session_data else ""
    if report.when == "call":
        if report.failed:
            logger.info("Test Failed")
            add_screenshot_to_report(item, extras)
        else:
            session_data.status = "Passed"

    if report.when == "teardown":
        if hasattr(session_data, "session_id"):
            report.url = (
                "https://ui-dev.headspin.io/sessions/"
                + session_data.session_id
                + "/waterfall"
            )
    report.extra = extras


def pytest_html_results_table_header(cells):
    """
    Modifying(adding/removing) the Results table header.
    """
    cells.insert(1, html.th("Start Time", class_="sortable time", col="time"))
    cells.insert(3, html.th("Description"))
    cells.insert(5, html.th("Link", class_="link", col="link"))
    cells.pop()


def pytest_html_results_table_row(report, cells):
    """
    Modifying(adding/removing) the Results table row.
    """
    cells.insert(1, html.td(report.start_time, class_="col-time"))
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


def pytest_terminal_summary(terminalreporter, config):
    """
    Adding additional information to the terminal summary section.
    """
    try:
        if config.option.html_report.lower() == "true":
            terminalreporter.write_line(
                "Note: To view the html report, open the file at the above location."
            )
    except:
        pass

    try:
        if config.option.rp_enabled:
            terminalreporter.write_line(
                "- report generated: To view this report, please open this link (https://demo.reportportal.io/ui/#default_personal/launches/19).\nNote: When you are not logged in, just click the login button."
            )
    except:
        pass

    try:
        if config.option.allure_report_dir:
            terminalreporter.write_line(
                "- report generated: The report will be opened in a web browser once the command(allure serve allure-report/allure-results) is run."
            )
    except:
        pass


def add_screenshot_to_report(item, extras, name="ScreenShot"):
    """
    Adding failed screenshot to the reports
    """
    # Capturing Failed screenshot
    screenshot = driver.get_screenshot_as_png()

    # Adding Failed screenshot to html report
    if item.config.option.html_report.lower() == "true":
        logger.info("Screenshot adding to html report")
        base_64_screenshot = base64.b64encode(screenshot).decode("utf-8")
        extras.append(
            pytest_html.extras.html(
                f'<img src="data:image/png;base64,{base_64_screenshot}" style="width:150px;height:300px;" onclick="window.open(this.src)" align="right">'
            )
        )

    # Adding Failed screenshot to report portal
    if item.config.option.rp_enabled:
        logging.setLoggerClass(RPLogger)
        logger.addHandler(RPLogHandler())
        logger.info(
            "Screenshot adding to report portal",
            attachment={
                "name": "test_name_screenshot.ini",
                "data": screenshot,
                "mime": "application/octet-stream",
            },
        )

    # Adding Failed screenshot to allure report
    if item.config.option.allure_report_dir:
        logger.info("Screenshot adding to allure report")
        with allure.step("Screenshot adding to report"):
            allure.attach(
                screenshot,
                name=name,
                attachment_type=AttachmentType.PNG,
            )


def add_allure_environment(data):
    """
    Adding environment info to allure report
    """
    config = configparser.ConfigParser()
    config["CAPS"] = {
        "UDID": data.get("udid"),
        "Platform_Name": data.get("platformName"),
    }
    allure_results_dir = os.path.join(ALLURE_REPORTS_DIR, "allure-results")
    with open(
        os.path.join(allure_results_dir, "environment.properties"), "w"
    ) as configfile:
        config.write(configfile)
