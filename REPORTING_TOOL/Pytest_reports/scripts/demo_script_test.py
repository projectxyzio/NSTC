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

    @allure.step
    @allure.label("DM1TC")
    @allure.title("First TC")  # TC title
    # @allure.description(
    #     """This is test_demo running on Mobile device"""
    # )  # TC Description
    @allure.severity(allure.severity_level.MINOR)
    # mark.issue :  Adds the details to ReportPortal if the test fails
    @pytest.mark.issue(issue_id="111111", reason="Some bug", issue_type="AB")
    def test_demo(self, driver):
        """
        This will be added as test description for ReportPortal/Allure Report
        """
        self.HOME_BUTTON = (MobileBy.ANDROID_UIAUTOMATOR, 'text("Homes")')
        self.SHORTS_BUTTON = (MobileBy.ANDROID_UIAUTOMATOR, 'text("Shorts")')
        self.LIBRARY_BUTTON = (MobileBy.ANDROID_UIAUTOMATOR, 'text("Library")')
        driver.find_element(*self.HOME_BUTTON)
        driver.find_element(*self.LIBRARY_BUTTON).click()
        logger.info("Test Passed")

    # mark.issue :  Adds the details to ReportPortal if the test fails
    pytest.mark.issue(issue_id="111111", reason="Locator bug", issue_type="AB")

    @allure.step
    @allure.title("Second TC")
    # @allure.description("""This is test_demo2 running on Mobile device """)
    @allure.severity(allure.severity_level.BLOCKER)
    def test_demo2(self, driver):
        """
        This will be added as test description for ReportPortal/Allure Report
        """
        self.HOME_BUTTON = (MobileBy.ANDROID_UIAUTOMATOR, 'text("Home")')
        self.SHORTS_BUTTON = (MobileBy.ANDROID_UIAUTOMATOR, 'text("Shorts")')
        self.LIBRARY_BUTTON = (MobileBy.ANDROID_UIAUTOMATOR, 'text("Library")')
        driver.find_element(*self.HOME_BUTTON)
        driver.find_element(*self.LIBRARY_BUTTON).click()
        logger.info("Test Passed")
