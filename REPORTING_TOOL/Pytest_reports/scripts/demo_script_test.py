import pytest
import allure
from appium.webdriver.common.mobileby import MobileBy
from hs_logger import logger


class TestDemoScript:
    test_name = "Demo Test"
    package = "com.google.android.youtube"
    activity = "com.google.android.apps.youtube.app.WatchWhileActivity"

    @allure.step
    @allure.label("DM1TC")
    @allure.title("First TC")  # TC title
    @allure.severity(allure.severity_level.MINOR)

    # mark.issue :  Adds the details to ReportPortal if the test fails
    @pytest.mark.issue(issue_id="111111", reason="Locator bug", issue_type="AB")
    def test_demo(self, driver):
        """
        This will be added as test description for ReportPortal/Allure Report
        """

        driver.find_element(MobileBy.ANDROID_UIAUTOMATOR, 'text("Home ")')
        driver.find_element(MobileBy.ANDROID_UIAUTOMATOR, 'text("Library")').click()
        logger.info("Test Passed")

    @allure.step
    @allure.title("Second TC")
    @allure.severity(allure.severity_level.BLOCKER)

    # mark.issue :  Adds the details to ReportPortal if the test fails
    @pytest.mark.issue(issue_id="111112", reason="Some bug", issue_type="AB")
    def test_demo2(self, driver):
        """
        This will be added as test description for ReportPortal/Allure Report
        """

        driver.find_element(MobileBy.ANDROID_UIAUTOMATOR, 'text("Home")')
        driver.find_element(MobileBy.ANDROID_UIAUTOMATOR, 'text("Library")').click()
        logger.info("Test Passed")
