"""
Visual Page Load Analysis VS VS Find Element Using Multiple Elements Based KPI marking

Find Element Using Multiple Elements Based KPI marking : Here element find from list of element is to confirm the availability of the page . 
Visual Page Load Analysis  : KPI marking is based on the Screen changes that will be recognized by the HS visual page load analysis 

Element find from list of element , function call can be found on line number 104,148,281 in the script 

Test Flow : 
        1. Launch 
        2.From Home Page Open Account 
        3.Click  Search from Bottom Tab 
        4.Select Thing ToDo  from Options 
        5.Select One Listed Event
        6.Click Book and Navigate to Secure Checkout page 
        7. Check Is page available and click back 


"""
#import python modules 

from appium import webdriver
import random
import unittest
import argparse
import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from lib.hs_api import hsApi

class ExpediaTest(unittest.TestCase):

    use_capture = True
    video_only = True
    no_reset = True
    autoLaunch = False
    app_name = "Expedia"
    package = "com.expedia.bookings"
    activity = "com.expedia.bookings.activity.SearchActivity"
    test_name = "Multi_elements"

    def setUp(self):
        self.desired_caps = {}
        self.desired_caps["platformName"] = "Android"
        self.desired_caps["udid"] = udid
        self.desired_caps["deviceName"] = udid
        self.desired_caps["appPackage"] = self.package
        self.desired_caps["appActivity"] = self.activity
        self.desired_caps["newCommandTimeout"] = 300
        self.desired_caps["noReset"] = True
        self.desired_caps["automationName"] = "UiAutomator2"
        self.desired_caps["autoGrantPermissions"] = True
        self.desired_caps["autoLaunch"] = False
        
        if not use_local_appium:
            # Headspin capabilities
            self.desired_caps["headspin:testName"] = self.test_name
            self.desired_caps["headspin:capture.video"] = True
            self.desired_caps["headspin:capture.network"] = False

            # Creating hs_api object
            self.hs_api_call = hsApi(udid, access_token)

        # Initializing Kpis
        self.kpi_labels = {}
        self.kpi_labels["Launch"] = {"start": None, "end": None}
        self.kpi_labels["Thing to do"] = {"start": None, "end": None}
        self.kpi_labels["Select Event"] = {"start": None, "end": None}
        self.kpi_labels["Secure Checkout"] = {"start": None, "end": None}
        self.kpi_labels["Search"] = {"start": None, "end": None}

        # Initializing KPI sensitivity for page_load analysis  (In Script default sensitivity set as 0.9,value ranges from 0-1)
        self.kpi_labels["Thing to do"]["start_sensitivity"] = 0.999
        self.kpi_labels["Search"]["end_sensitivity"] = 0.999
        self.kpi_labels["Search"]["start_sensitivity"] = 0.999
        self.kpi_labels["Thing to do"]["end_sensitivity"] = 0.8

        #Extra buffer time for visual page load analysis 
        self.kpi_labels["Thing to do"]["buffer_time"] = 1.2
        self.kpi_labels["Launch"]["buffer_time"] = 1
        self.kpi_labels["Select Event"]["buffer_time"] = 1.2

        self.status = "Failed_Driver_Creation"
        self.session_id = None 
        # Driver Creation
        print("\nScript started")
        self.driver = webdriver.Remote(url, self.desired_caps)
        print("Driver started ")

        # initializing Explicit wait for 20sec
        self.wait = WebDriverWait(self.driver, 20)
        self.short_wait = WebDriverWait(self.driver, 0.2)

        # Get session id
        self.session_id = self.driver.session_id

    def test_comparison(self):
        #Terminating the app to ensure cold launch
        self.driver.terminate_app(self.package)

        self.status = "Failed_launch"
        profile = (MobileBy.ACCESSIBILITY_ID, 'Profile. Button')
        txt_no_thanks = (MobileBy.ANDROID_UIAUTOMATOR, 'text("NO THANKS")')
        home_btn = (MobileBy.ACCESSIBILITY_ID, "Home Button")
        launch_element_list = [home_btn,profile, txt_no_thanks]

        self.kpi_labels["Launch"]["start"] = int(round(time.time() * 1000))
        # Launch App
        self.driver.launch_app()
        launch_ele, launch_loc = self.find_element_from_locator_list(
            launch_element_list
        )

        self.kpi_labels["Launch"]["end"] = int(round(time.time() * 1000))
        print("\nApp Launched")
        time.sleep(3)
        if launch_loc == txt_no_thanks:
            print("No Thanks ")
            launch_ele.click()

        account = self.wait.until(
            EC.presence_of_element_located(
                (MobileBy.ACCESSIBILITY_ID, "Profile. Button")
            )
        )
        account.click()

        self.wait.until(
            EC.presence_of_element_located(
                (MobileBy.ID, "com.expedia.bookings:id/section_title")
            )
        )
        print("Account Page ")
        time.sleep(1)
        search_button = self.wait.until(
            EC.presence_of_element_located((MobileBy.ACCESSIBILITY_ID, "Search Button"))
        )

        self.kpi_labels["Search"]["start"] = int(round(time.time() * 1000))
        search_button.click()

        stays_options = (MobileBy.ANDROID_UIAUTOMATOR, 'text("Stays")')
        flights_options = (MobileBy.ANDROID_UIAUTOMATOR, 'text("Flights")')
        cars_options = (MobileBy.ANDROID_UIAUTOMATOR, 'text("Cars")')
        thing_TODO_options = (MobileBy.ANDROID_UIAUTOMATOR, 'text("Things to do")')

        # Element list
        search_element_list = [
            stays_options,
            flights_options,
            cars_options,
            thing_TODO_options,
        ]
        # find any of the element from the list
        self.find_element_from_locator_list(search_element_list)
        
        self.kpi_labels["Search"]["end"] = int(round(time.time() * 1000))
        time.sleep(1)
        print("Search  Page")

        self.status = "Failed_Thing_TODO"
        thing_to_do = self.wait.until(
            EC.presence_of_element_located(
                (MobileBy.ANDROID_UIAUTOMATOR, 'text("Things to do")')
            )
        )

        time.sleep(0.5)
        self.status = "Failed_to_open_things_TODO"
        self.kpi_labels["Thing to do"]["start"] = int(round(time.time() * 1000))
        thing_to_do.click()
        self.wait.until(
            EC.presence_of_element_located(
                (MobileBy.ID, "com.expedia.bookings:id/sort_filter_uds_button")
            )
        )
        self.kpi_labels["Thing to do"]["end"] = int(round(time.time() * 1000))
        print("Things To_Do")
        time.sleep(2)

        options = self.wait.until(
            EC.presence_of_all_elements_located(
                (MobileBy.CLASS_NAME, "android.widget.FrameLayout")
            )
        )
        self.status = "Failed_to_select_event"

        choice = random.choice([2, 3])
        self.kpi_labels["Select Event"]["start"] = int(round(time.time() * 1000))
        options[choice].click()
        print("Event Selected")

        self.wait.until(
            EC.presence_of_all_elements_located(
                (MobileBy.ID, "com.expedia.bookings:id/info_title_text")
            )
        )
        self.kpi_labels["Select Event"]["end"] = int(round(time.time() * 1000))
        time.sleep(2)

        for _ in range(4):
            try:
                btn_book = self.short_wait.until(
                    EC.presence_of_element_located(
                        (MobileBy.ANDROID_UIAUTOMATOR, 'text("Book")')
                    )
                )
                time.sleep(0.5)
                break
            except:
                self.screen_swipe()
        self.kpi_labels["Secure Checkout"]["start"] = int(round(time.time() * 1000))
        btn_book.click()
        time.sleep(1)

        txt_try_later = (
            MobileBy.ANDROID_UIAUTOMATOR,
            'text("Sorry, we’re having a problem on our end. Please try again later.")',
        )
        txt_secure = (MobileBy.ANDROID_UIAUTOMATOR, 'textContains("Secure booking —")')

        # Element list
        element_list = [txt_try_later, txt_secure]
        # checking is any of the element in the list is on the screen
        element, locator = self.find_element_from_locator_list(element_list)

        if locator == txt_try_later:
            print("Error Message: Unable to navigate to check out Page  ")
            self.short_wait.until(
                EC.presence_of_element_located((MobileBy.ID, "android:id/button1"))
            ).click()
        else:
            print("On secure Checkout Page ")
            self.kpi_labels["Secure Checkout"]["end"] = int(round(time.time() * 1000))
        time.sleep(2)
        self.wait.until(
            EC.presence_of_element_located((MobileBy.ACCESSIBILITY_ID, "Back"))
        ).click()

        print("Script Passed")
        self.status = "Passed"

    def tearDown(self):

        print("session_status : " ,self.status)
        if not use_local_appium and self.session_id:
            # setting Session status
            state = "Passed" if "Fail" not in self.status else "Failed"

            # updating session status
            self.driver.execute_script("headspin:quitSession", {"status": state})
            session_url = (
                "https://ui-dev.headspin.io/sessions/" + self.session_id + "/waterfall"
            )
            print("\nURL :", session_url)

        try:
            # try to terminate driver
            self.driver.quit()
        except:
            pass
        print("Driver Terminated")

        if not use_local_appium and self.session_id:
            # Get Video start_timestamp and end_timestamp
            self.get_video_start_timestamp()

            # waiting until video available for post processing
            self.wait_for_session_video_becomes_available()

            if   add_element_label:
                #Function call adding labels based on appium element 
                self.add_element_based_annotation()
            if   add_vpla_label:
                # Function call for performing visual page load analysis
                self.add_visual_page_based_annotations()
            session_data = self.get_general_session_data()

            # Adding session data
            self.hs_api_call.add_session_data(session_data=session_data)

            description_string = ""
            for data in session_data["data"]:
                description_string += data["key"] + " : " + str(data["value"]) + "\n"

            # Adding session description
            self.hs_api_call.update_session_name_and_description(
                session_id=self.session_id,
                name=self.test_name,
                description=description_string,
            )

    # Get all the session details
    def get_general_session_data(self):

        session_data = {}
        session_data["session_id"] = self.session_id
        session_data["data"] = []
        # app info
        session_data["data"].append({"key": "bundle_id", "value": self.package})
        session_data["data"].append({"key": "status", "value": self.status})

        return session_data

    # KPI marikng based on elements
    def add_element_based_annotation(self):
        page_load = {"labels": []}
        label_category = "using finding multi-element"
        print("adding_element_based_session_annotations")
        for key, value in self.kpi_labels.items():
            if self.kpi_labels[key]["start"] and self.kpi_labels[key]["end"]:
                label_start_time = (
                    self.kpi_labels[key]["start"] - self.video_start_timestamp
                )
                label_end_time = (
                    self.kpi_labels[key]["end"] - self.video_start_timestamp
                )
                if label_start_time < 0:
                    label_start_time = (
                        self.video_start_timestamp - self.video_start_timestamp
                    )

                kpi_label = {"name": key, "category": label_category}
                kpi_label["start_time"] = label_start_time / 1000
                kpi_label["end_time"] = label_end_time / 1000
                page_load["labels"].append(kpi_label)

        # Calling Annotation API ( based on element find)
        self.hs_api_call.add_label(session_id=self.session_id, data_payload=page_load)

    # Headspin Visual Page load analysis
    def add_visual_page_based_annotations(self):
        page_load = {"regions": [], "wait_timeout_sec": 600}
        print("adding_visual_based_session_annotations")
        for key, value in self.kpi_labels.items():

            if self.kpi_labels[key]["start"] and self.kpi_labels[key]["end"]:
                label_start_time = (
                    self.kpi_labels[key]["start"] - self.video_start_timestamp
                )

                label_end_time = (
                    self.kpi_labels[key]["end"] - self.video_start_timestamp
                )

                if label_start_time < 0:
                    label_start_time = (
                        self.video_start_timestamp - self.video_start_timestamp
                    )
                label_item = {"name": key}
                label_item["start_time"] = label_start_time / 1000

                buffer_time = (
                    self.kpi_labels[key]["buffer_time"]
                    if self.kpi_labels[key].get("buffer_time")
                    else 0
                )

                label_item["end_time"] = (label_end_time / 1000) + buffer_time
                label_item["start_sensitivity"] = (
                    self.kpi_labels[key]["start_sensitivity"]
                    if self.kpi_labels[key].get("start_sensitivity")
                    else 0.9
                )
                label_item["end_sensitivity"] = (
                    self.kpi_labels[key]["end_sensitivity"]
                    if self.kpi_labels[key].get("end_sensitivity")
                    else 0.9
                )
                page_load["regions"].append(label_item)
        # Calling Page_load API
        page_load_response = self.hs_api_call.get_pageloadtime(
            session_id=self.session_id, data_payload=page_load
        )

        screen_change = {"labels": []}
        label_category = "using visual page load api"

        if "page_load_regions" in page_load_response:
            for kpi_item in page_load_response["page_load_regions"]:

                if "start_time" in kpi_item and "end_time" in kpi_item:
                    kpi_label = {
                        "name": kpi_item["request_name"],
                        "category": label_category,
                    }
                    kpi_label["start_time"] = kpi_item["start_time"] / 1000
                    kpi_label["end_time"] = kpi_item["end_time"] / 1000
                    label_item["end_sensitivity"] = (
                        self.kpi_labels[key]["end_sensitivity"]
                        if self.kpi_labels[key].get("end_sensitivity")
                        else 0.9
                    )
                    screen_change["labels"].append(kpi_label)

            # Adding KPI Annotation based on the result from visual page load
            self.hs_api_call.add_label(
                session_id=self.session_id, data_payload=screen_change
            )

    # Wait until Video available  for analysis
    def wait_for_session_video_becomes_available(self):
        t_end = time.time() + 1200
        while time.time() < t_end:
            status = self.hs_api_call.get_session_video_metadata(self.session_id)
            if status and ("video_duration_ms" in status):
                print("\nVideo Available for Post Processing\n")
                break

    # Get the video time stamps
    def get_video_start_timestamp(self):
        t_end = time.time() + 1000.0
        while time.time() < t_end:
            capture_timestamp = self.hs_api_call.get_capture_timestamp(self.session_id)
            self.video_start_timestamp = capture_timestamp["capture-started"] * 1000
            if "capture-complete" in capture_timestamp:
                break
            time.sleep(1)
        return capture_timestamp

    # Swipe with respect to screen ratio
    def screen_swipe(
        self,
        start_x_ratio=0.5,
        start_y_ratio=0.7,
        end_x_ratio=0.5,
        end_y_ratio=0.2,
        swipe_delay=300,
    ):
        """
        Screen Swipe
        """
        screen_size = self.driver.get_window_size()
        width = screen_size["width"]
        height = screen_size["height"]
        self.start_x = width * start_x_ratio
        self.start_y = height * start_y_ratio
        self.end_x = width * end_x_ratio
        self.end_y = height * end_y_ratio
        self.driver.swipe(
            self.start_x, self.start_y, self.end_x, self.end_y, swipe_delay
        )

    # Find element from the list
    def find_element_from_locator_list(self, locator_list, finding_time=30):
        """
        Locate element from list of elements
        """
        t_end = time.time() + finding_time
        while t_end > time.time():
            for locator in locator_list:
                try:
                    element = self.short_wait.until(
                        EC.presence_of_element_located(locator)
                    )
                    return element, locator
                except:
                    time.sleep(1)
        raise Exception(f"Could not find element from the list: {locator_list}")


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--udid",
        "--udid",
        dest="udid",
        type=str,
        nargs="?",
        default=None,
        required=False,
        help="udid",
    )
    
    parser.add_argument(
        "--url",
        "--url",
        dest="url",
        type=str,
        nargs="?",
        default=None,
        required=False,
        help="url",
    )
    
    parser.add_argument(
        "--appium_element_only",
        "--appium_element_only",
        dest="element_only",
        type=bool,
        nargs="?",
        default=False,
        required=False,
        help="only_appium_element_label",
    )

    parser.add_argument(
        "--vpla_only",
        "--vpla_only",
        dest="vpla_only",
        type=bool,
        nargs="?",
        default=False,
        required=False,
        help="only_visual_page_load_analysis_label",
    )

    parser.add_argument(
        "--use_local_appium",
        "--use_local_appium",
        dest="local_appium",
        type=bool,
        nargs="?",
        default=False,
        required=False,
        help="use_local_appium_server",
    )

    args = parser.parse_args()
    
    #Get command line arguments to Variables
    add_element_label =  not (args.vpla_only)
    add_vpla_label = not (args.element_only)
    use_local_appium = args.local_appium
    udid = args.udid
    url = args.url
    if not use_local_appium:
        access_token = url.split("/")[-3]
        # Get Bearer token for header
        headers = {"Authorization": "Bearer {}".format(access_token)}
    suite = unittest.TestLoader().loadTestsFromTestCase(ExpediaTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
