"""
Visual Page Load Analysis VS Element Based KPI marking 

Element Based KPI marking  : KPI marking is based on the Apppium find Element 
Visual Page Load Analysis  : KPI marking is based on the Screen changes that will be recognized by the HS visual page load analysis 

Test Flow : 
        1. Launch 
        2.From Home Page Open Account
        3.Click  Profile Options  , Verify and get back to Account page 
        4.Click  Coupons and credits options , Verify and get back to Account page 
        5.Click  Search from Bottom Tab , Verify with Thing ToDo option
        
"""

# import python modules
import unittest
import argparse
import time
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from lib.hs_api import hsApi


class ExpediaTest(unittest.TestCase):

    no_reset = True
    autoLaunch = False
    package = "com.expedia.bookings"
    activity = "com.expedia.bookings.activity.SearchActivity"
    test_name = "Appium_element_labelling"

    def setUp(self):
        self.desired_caps = {}
        self.desired_caps["platformName"] = "Android"
        self.desired_caps["udid"] = udid
        self.desired_caps["deviceName"] = udid
        self.desired_caps["appPackage"] = self.package
        self.desired_caps["appActivity"] = self.activity
        self.desired_caps["newCommandTimeout"] = 300
        self.desired_caps["noReset"] = self.no_reset
        self.desired_caps["automationName"] = "UiAutomator2"
        self.desired_caps["autoGrantPermissions"] = True
        self.desired_caps["autoLaunch"] = self.autoLaunch

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
        self.kpi_labels["Search"] = {"start": None, "end": None}
        self.kpi_labels["Account"] = {"start": None, "end": None}
        self.kpi_labels["Profile"] = {"start": None, "end": None}
        self.kpi_labels["Coupons and Credit"] = {"start": None, "end": None}

        # Initializing KPI sensitivity for page_load analysis  (In Script default sensitivity set as 0.9,value ranges from 0-1)
        self.kpi_labels["Account"]["end_sensitivity"] = 0.999
        self.kpi_labels["Account"]["start_sensitivity"] = 0.99
        self.kpi_labels["Search"]["end_sensitivity"] = 0.99
        self.kpi_labels["Search"]["start_sensitivity"] = 0.999
        self.kpi_labels["Profile"]["start_sensitivity"] = 0.99
        self.kpi_labels["Coupons and Credit"]["start_sensitivity"] = 0.99

        # Extra buffer time for visual page load analysis (in seconds)
        self.kpi_labels["Account"]["buffer_time"] = 1
        self.kpi_labels["Search"]["buffer_time"] = 1
        self.kpi_labels["Launch"]["buffer_time"] = 1

        self.status = "Failed_Driver_Creation"
        self.session_id = None
        # Driver Creation
        print("\nScript started")
        self.driver = webdriver.Remote(url, self.desired_caps)
        print("Driver started ")

        # initializing Explicit wait for 20sec
        self.wait = WebDriverWait(self.driver, 20)

        # Get session id
        self.session_id = self.driver.session_id

    def test_comparison(self):
        # Terminating the app to ensure cold launch
        self.driver.terminate_app(self.package)

        self.status = "Failed_launch"

        self.kpi_labels["Launch"]["start"] = int(round(time.time() * 1000))

        # Launch App
        self.driver.launch_app()
        account = self.wait.until(
            EC.presence_of_element_located(
                (MobileBy.ACCESSIBILITY_ID, "Profile. Button")
            )
        )
        self.kpi_labels["Launch"]["end"] = int(round(time.time() * 1000))
        print("\nApp Launched")
        time.sleep(3)

        self.status = "Failed_Account"

        self.kpi_labels["Account"]["start"] = int(round(time.time() * 1000))
        account.click()
        self.wait.until(
            EC.presence_of_element_located(
                (MobileBy.ID, "com.expedia.bookings:id/section_title")
            )
        )
        self.kpi_labels["Account"]["end"] = int(round(time.time() * 1000))
        print("Account  Page")
        time.sleep(2)

        profile_option = self.wait.until(
            EC.presence_of_element_located(
                (
                    MobileBy.XPATH,
                    '//android.widget.LinearLayout[@content-desc="Profile. Update personal details and customise preferences. Button"]/android.widget.TextView',
                )
            )
        )
        self.status = "Failed_to_profile"
        self.kpi_labels["Profile"]["start"] = int(round(time.time() * 1000))
        profile_option.click()
        self.wait.until(
            EC.presence_of_element_located(
                (MobileBy.ANDROID_UIAUTOMATOR, 'text("My Travel Details")')
            )
        )

        self.kpi_labels["Profile"]["end"] = int(round(time.time() * 1000))
        print("Profile  Page")

        time.sleep(2)
        self.wait.until(
            EC.presence_of_element_located(
                (MobileBy.ACCESSIBILITY_ID, "Close My account")
            )
        ).click()
        self.wait.until(
            EC.presence_of_element_located(
                (MobileBy.ID, "com.expedia.bookings:id/section_title")
            )
        )

        coupon_and_credit = self.wait.until(
            EC.presence_of_element_located(
                (
                    MobileBy.XPATH,
                    '//android.widget.LinearLayout[@content-desc="Coupons and credits. See coupons and credits available for your next trip. Button"]/android.widget.TextView',
                )
            )
        )
        self.status = "Failed_to_coupon_and_credit"
        self.kpi_labels["Coupons and Credit"]["start"] = int(round(time.time() * 1000))
        coupon_and_credit.click()
        self.wait.until(
            EC.presence_of_element_located(
                (
                    MobileBy.XPATH,
                    '//android.view.View[@content-desc="How to use coupons"]/android.widget.TextView',
                )
            )
        )

        self.kpi_labels["Coupons and Credit"]["end"] = int(round(time.time() * 1000))
        print("Coupons & Credit Page")

        time.sleep(2)
        self.wait.until(
            EC.presence_of_element_located(
                (MobileBy.ACCESSIBILITY_ID, "Close My account")
            )
        ).click()

        search_button = self.wait.until(
            EC.presence_of_element_located((MobileBy.ACCESSIBILITY_ID, "Search Button"))
        )
        time.sleep(1)
        self.status = "Failed_to_open_search"

        self.kpi_labels["Search"]["start"] = int(round(time.time() * 1000))
        search_button.click()
        thing_to_do = self.wait.until(
            EC.presence_of_element_located(
                (MobileBy.ANDROID_UIAUTOMATOR, 'text("Things to do")')
            )
        )
        self.kpi_labels["Search"]["end"] = int(round(time.time() * 1000))
        print("Search  Page")

        time.sleep(2)

        print("Script Passed")
        self.status = "Passed"

    def tearDown(self):
        print("session_status : ", self.status)
        if not use_local_appium and self.session_id:
            # setting Session status
            state = "Passed" if "Fail" not in self.status else "Failed"

            # updating session status
            self.driver.execute_script("headspin:quitSession", {"status": state})
            print("Driver Terminated")

            self.session_id = self.session_id
            session_url = (
                "https://ui-dev.headspin.io/sessions/" + self.session_id + "/waterfall"
            )
            print("\nURL :", session_url)

            # Get Video start_timestamp and end_timestamp
            self.get_video_start_timestamp()

            # waiting until video available for post processing
            self.wait_for_session_video_becomes_available()

            if add_element_label:
                # Function call adding labels based on appium element
                self.add_element_based_annotation()

            if add_vpla_label:
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
        else:
            try:
                # try to terminate driver
                self.driver.quit()
                print("Driver Terminated")
            except:
                pass
        self.kpi_data()
        
        
        
    def kpi_data(self):
        category_one = "using visual page load api"
        category_two = "using finding element"
        
        if add_vpla_label:
            data_list_one = self.hs_api_call.get_labels(category=category_one,session_id = self.session_id)
            data_set_one = {}
            for x in data_list_one:
                data_set_one[x['name']] = round(x['end_time']-x['start_time'])/1000
        if add_element_label:
            data_list_two = self.hs_api_call.get_labels(category=category_two,session_id = self.session_id)
            data_set_two = {}
            for x in data_list_two:
                data_set_two[x['name']] = round(x['end_time']-x['start_time'])/1000
        print("\n")
        
        if add_vpla_label:
            set_selection = data_set_one
        elif add_element_label:
            set_selection = data_list_two
        for x  in set_selection.keys():
            print("KPI : ",x)
            if add_vpla_label:
                print(f"{category_one} : ",data_set_one[x], "Seconds")
            if add_element_label:
                print(f"{category_two} : ",data_set_two[x], "Seconds")
            if add_vpla_label and add_element_label:
                pass
                # print(f"Percentage Difference between {category_two} and {category_one} (Accuracy) :",( abs((data_set_two[x] - data_set_one[x])/(data_set_two[x] + data_set_one[x])) * 100) / data_set_one[x],"%")
            print("\n")
            

    # Get all the session details
    def get_general_session_data(self):

        session_data = {}
        session_data["session_id"] = self.session_id
        session_data["data"] = []
        # app info
        session_data["data"].append({"key": "bundle_id", "value": self.package})
        session_data["data"].append({"key": "status", "value": self.status})

        return session_data

    # KPI marking based on elements
    def add_element_based_annotation(self):
        page_load = {"labels": []}
        label_category = "using finding element"
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
    
            


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--udid",
        dest="udid",
        type=str,
        default=None,
        required=True,
        help="udid",
    )

    parser.add_argument(
        "--url",
        dest="url",
        type=str,
        default=None,
        required=True,
        help="url",
    )

    parser.add_argument(
        "--appium_element_only",
        dest="element_only",
        type=bool,
        default=False,
        required=False,
        help="only_appium_element_label",
    )

    parser.add_argument(
        "--vpla_only",
        dest="vpla_only",
        type=bool,
        default=False,
        required=False,
        help="only_visual_page_load_analysis_label",
    )

    parser.add_argument(
        "--use_local_appium",
        dest="local_appium",
        type=bool,
        default=False,
        required=False,
        help="use_local_appium_server",
    )

    # Get command line arguments to Variables
    args = parser.parse_args()
    add_element_label = not (args.vpla_only)
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
