import pytest
import allure
from logging import Logger
from hs_logger import logger
from allure_commons.types import AttachmentType
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestDemoScript:
    test_name = "Demo Test"
    package = "com.google.android.youtube"
    activity = "com.google.android.apps.youtube.app.WatchWhileActivity"

    desired_capabilities = {
        "automationName": "uiautomator2",
        "appPackage": package,
        "platformName": "android",
        "appActivity": activity,
        "newCommandTimeout": 60,
    }

    @allure.step
    @allure.label("DM1TC")
    @allure.title("First TC")  # TC title
    @allure.description(
        """This is test_demo running on Mobile device"""
    )  # TC Description
    @allure.severity(allure.severity_level.MINOR)
    # mark.issue :  Adds the details to ReportPortal if the test fails
    @pytest.mark.issue(issue_id="111111", reason="Some bug", issue_type="AB")
    def test_demo(self, driver, rp_logger: Logger):
        # This will be added as test description for ReportPortal
        """
        This is test_demo running on Mobile device
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)
        try:
            self.HOME_BUTTON = (MobileBy.ANDROID_UIAUTOMATOR, 'text("Homes")')
            self.SHORTS_BUTTON = (MobileBy.ANDROID_UIAUTOMATOR, 'text("Shorts")')
            self.LIBRARY_BUTTON = (MobileBy.ANDROID_UIAUTOMATOR, 'text("Library")')
            self.wait.until(EC.presence_of_element_located(self.HOME_BUTTON))
            self.wait.until(EC.presence_of_element_located(self.LIBRARY_BUTTON)).click()
            self.session_data.status = "Passed"
            logger.info("Test Passed")
        except Exception as e:
            self.add_screenshot_to_report(rp_logger)

            raise e

    # mark.issue :  Adds the details to ReportPortal if the test fails
    pytest.mark.issue(issue_id="111111", reason="Locator bug", issue_type="AB")

    @allure.step
    @allure.title("Second TC")
    @allure.description("""This is test_demo2 running on Mobile device """)
    @allure.severity(allure.severity_level.BLOCKER)
    def test_demo2(self, driver, rp_logger: Logger):
        # This will be added as test description for ReportPortal
        """
        This is test_demo2 running on Mobile device
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)
        try:
            self.HOME_BUTTON = (MobileBy.ANDROID_UIAUTOMATOR, 'text("Home")')
            self.SHORTS_BUTTON = (MobileBy.ANDROID_UIAUTOMATOR, 'text("Shorts")')
            self.LIBRARY_BUTTON = (MobileBy.ANDROID_UIAUTOMATOR, 'text("Library")')
            self.wait.until(EC.presence_of_element_located(self.HOME_BUTTON))
            self.wait.until(EC.presence_of_element_located(self.LIBRARY_BUTTON)).click()
            self.session_data.status = "Passed"
            logger.info("Test Passed")
        except Exception as e:
            self.add_screenshot_to_report(rp_logger)
            raise e

    def add_screenshot_to_report(self, rp_logger, name="ScreenShot"):
        logger.info("Test Failed")
        logger.info("Taking Failed screenshot")
        with allure.step("Take screenshot"):
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name=name,
                attachment_type=AttachmentType.PNG,
            )
        try:
            screenshot = (
                self.driver.get_screenshot_as_png()
            )  # Capture screenshot and attach to Allure Report if test fails
            rp_logger.info(
                "Some Text Here",
                attachment={
                    "name": "test_name_screenshot.ini",
                    "data": screenshot,
                    "mime": "application/octet-stream",
                },
            )  # Capture screenshot and attach to ReportPortal if test fails
        except:
            pass
