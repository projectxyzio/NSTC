import pytest
import allure
import time
from appium.webdriver.common.mobileby import MobileBy
from hs_logger import logger


class TestDemoScript:
    test_name = "Demo Test"
    package = "com.google.android.youtube"
    activity = "com.google.android.apps.youtube.app.WatchWhileActivity"

    @allure.step
    @allure.label("DM1TC")
    @allure.title("First TC")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.issue(issue_id="111111", reason="Locator bug", issue_type="AB")
    def test_youtube_live_streaming(self, driver):
        """
        This will be added as test description for ReportPortal/Allure Report
        """

        driver.find_element(by=MobileBy.ANDROID_UIAUTOMATOR, value='text("Home")')
        logger.info("Home Screen loaded")
        driver.find_element(by=MobileBy.ACCESSIBILITY_ID, value="Create").click()
        logger.info("Taped on Create icon")
        driver.find_element(by=MobileBy.ACCESSIBILITY_ID, value="Go live").click()
        logger.info("Taped on Go live")
        driver.find_element(by=MobileBy.ID, value="com.google.android.youtube:id/title_edit_text").send_keys("My Live Stream")
        logger.info("Entered live stream title")
        driver.find_element(by=MobileBy.ID, value="com.google.android.youtube:id/go_live_button").click()
        logger.info("Started live stream")
        # Wait for the live stream to start
        time.sleep(10)
        logger.info("Test Passed")

    @allure.step
    @allure.title("Second TC")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.issue(issue_id="111112", reason="Some bug", issue_type="AB")
    def test_library_loading(self, driver):
        """
        This will be added as test description for ReportPortal/Allure Report
        """
        driver.find_element(by=MobileBy.ANDROID_UIAUTOMATOR, value='text("Home")')
        logger.info("Home Screen loaded")
        driver.find_element(by=MobileBy.ANDROID_UIAUTOMATOR, value='text("Library")').click()
        logger.info("Taped on Library button")
        try:
            driver.find_element(by=MobileBy.ANDROID_UIAUTOMATOR, value='descriptionContains("History")')
            logger.info("Library screen loaded")
        except:
            assert False, "Library screen did not load"

        assert True, "Library screen loaded successfully"
        logger.info("Test Passed")
