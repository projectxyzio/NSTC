"""
Document Ready VS Element Based KPI marking 

Document Ready KPI marking  : KPI marking is based on the Document Ready State 
Visual Page Load Analysis  : KPI marking is based on the Screen changes that will be recognized by the HS visual page load analysis 

Test Flow : 
        1.Launch Chrome Browser 
        2.Open Amazon.in
        3.Search for Apple iPhone 13 
        4.Select First phone from the list 
        5.Click Menu Option 
        6.Open PC & Computer Sections 

"""
# import python modules
import unittest
import argparse
import time
from appium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


from lib.hs_api import hsApi


class AmazonTest(unittest.TestCase):

    no_reset = False
    autoLaunch = True
    app_name = "Chrome_Amazon"
    test_name = "Document_ready_labelling"
    browser_name = "chrome"

    def setUp(self):
        self.desired_caps = {}
        self.desired_caps["platformName"] = "Android"
        self.desired_caps["udid"] = udid
        self.desired_caps["deviceName"] = udid
        self.desired_caps["newCommandTimeout"] = 300
        self.desired_caps["noReset"] = self.no_reset
        self.desired_caps["automationName"] = "UiAutomator2"
        self.desired_caps["autoGrantPermissions"] = True
        self.desired_caps["autoLaunch"] = self.autoLaunch
        self.desired_caps["browserName"] = self.browser_name

        if not use_local_appium:
            # Headspin capabilities
            self.desired_caps["headspin:testName"] = self.test_name
            self.desired_caps["headspin:capture.video"] = True
            self.desired_caps["headspin:capture.network"] = False

            # Creating hs_api object
            self.hs_api_call = hsApi(udid, access_token)

        # Initializing Kpis
        self.visual_labels = {}
        self.document_ready_labels = {}

        self.visual_labels["Search Result Page"] = {"start": None, "end": None}
        self.document_ready_labels["Search Result Page"] = {"start": None, "end": None}
        self.visual_labels["PC Page"] = {"start": None, "end": None}
        self.document_ready_labels["PC Page"] = {"start": None, "end": None}
        self.visual_labels["Device Details"] = {"start": None, "end": None}
        self.document_ready_labels["Device Details"] = {"start": None, "end": None}

        # Initializing KPI sensitivity for page_load analysis  (In Script default sensitivity set as 0.9 , value ranges from 0-1 )
        self.visual_labels["Device Details"]["end_sensitivity"] = 0.8
        self.visual_labels["Search Result Page"]["end_sensitivity"] = 0.999
        self.visual_labels["PC Page"]["start_sensitivity"] = 0.999

        self.status = "Failed_Driver_Creation"
        self.session_id = None
        # Driver Creation
        print("\nScript started")
        self.driver = webdriver.Remote(url, self.desired_caps)
        print("Driver started")

        # initializing Explicit wait for 20sec
        self.wait = WebDriverWait(self.driver, 20)

        # Get session id
        self.session_id = self.driver.session_id

    def test_comparison(self):
        self.status = "Failed_launch"
        print("\nOpen Amazon.com")

        # Open the amazon site in chrome
        self.driver.get("https://www.amazon.com/")

        self.status = "Failed_Open_Amazon.com"
        search_filed = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    'input[data-aria-clear-label="Clear search keywords"]',
                )
            )
        )
        print("Amazon Home Page")
        search_filed.click()
        time.sleep(1)
        search_filed.send_keys("iphone 13")
        self.status = "Failed_get_search_result"
        time.sleep(1)
        GO_button = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@class="nav-search-submit"]/input[@aria-label="Go"]')
            )
        )
        current_url = self.driver.current_url
        self.visual_labels["Search Result Page"]["start"] = int(
            round(time.time() * 1000)
        )
        self.document_ready_labels["Search Result Page"]["start"] = int(
            round(time.time() * 1000)
        )
        GO_button.click()
        self.document_ready_labels["Search Result Page"]["end"] = self.get_time_stamp(
            url=current_url
        )

        print("Search Result Page")

        # select thr first phone from the Search Result
        mobile = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//div[@class="sg-col-inner"]/div/div/div/span[@data-action="detail-page-link-tap"]',
                )
            )
        )

        self.visual_labels["Search Result Page"]["end"] = int(round(time.time() * 1000))

        self.status = "Failed_Select_Device"
        time.sleep(1)
        current_url = self.driver.current_url
        self.visual_labels["Device Details"]["start"] = int(round(time.time() * 1000))
        self.document_ready_labels["Device Details"]["start"] = int(
            round(time.time() * 1000)
        )
        mobile.click()
        self.document_ready_labels["Device Details"]["end"] = self.get_time_stamp(
            url=current_url
        )

        share_button = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'i[title="Share"]'))
        )
        time.sleep(1)
        self.visual_labels["Device Details"]["end"] = int(round(time.time() * 1000))

        menu_options = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'a[id="nav-hamburger-menu"]')
            )
        )
        menu_options.click()
        time.sleep(1)

        PC = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//a[text()="PC"]'))
        )

        self.status = "Failed_Open_PC_Page "
        current_url = self.driver.current_url
        self.visual_labels["PC Page"]["start"] = int(round(time.time() * 1000))
        self.document_ready_labels["PC Page"]["start"] = int(round(time.time() * 1000))
        PC.click()
        self.document_ready_labels["PC Page"]["end"] = self.get_time_stamp(
            url=current_url
        )
        PC = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//h1[text()="Computers, Tablets, &    Accessories"]')
            )
        )
        time.sleep(1)
        self.visual_labels["PC Page"]["end"] = int(round(time.time() * 1000))

        self.driver.close()

        print("Script Passed ")
        self.status = "Passed"

    def tearDown(self):
        print("session_status : ", self.status)
        if not use_local_appium and self.session_id:
            state = "Passed" if "Fail" not in self.status else "Failed"

            # updating session status
            self.driver.execute_script("headspin:quitSession", {"status": state})
            print("Driver Terminated")

            session_url = (
                "https://ui-dev.headspin.io/sessions/" + self.session_id + "/waterfall"
            )
            print("\nURL :", session_url)

            # Function call to get start and end video timestamp
            self.get_video_start_timestamp()

            # waiting until video available for post processing
            self.wait_for_session_video_becomes_available()

            if add_doc_label:
                # Function call for adding labels based on document ready state
                self.add_document_ready_based_annotations()

            if add_vpla_label:
                # Function call for performing visual page load analysis
                self.add_visual_page_based_annotations()

            # Get all the session data
            session_data = self.get_general_session_data()

            # API call to add data to the session
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
            self.kpi_data()
        else:
            try:
                # try to terminate driver
                self.driver.quit()
                print("Driver Terminated")
            except:
                pass

    def kpi_data(self):
        category_one = "using visual page load api"
        category_two = "using document ready state"
        
        if add_vpla_label:
            data_list_one = self.hs_api_call.get_labels(category=category_one,session_id = self.session_id)
            data_set_one = {}
            for x in data_list_one:
                data_set_one[x['name']] = round(x['end_time']-x['start_time'])/1000
        if add_doc_label:
            data_list_two = self.hs_api_call.get_labels(category=category_two,session_id = self.session_id)
            data_set_two = {}
            for x in data_list_two:
                data_set_two[x['name']] = round(x['end_time']-x['start_time'])/1000
        print("\n")
        
        if add_vpla_label:
            keys = data_set_one.keys()
        elif add_doc_label:
            keys = data_set_two.keys()
        for x  in keys:
            print("KPI : ",x)
            if add_vpla_label:
                print(f"{category_one} : ",data_set_one[x], "Seconds")
            if add_doc_label:
                print(f"{category_two} : ",data_set_two[x], "Seconds")
            if add_vpla_label and add_doc_label:
                pass
                # print(f"Percentage Difference between {category_two} and {category_one} (Accuracy) :",( abs((data_set_two[x] - data_set_one[x])/(data_set_two[x] + data_set_one[x])) * 100) / data_set_one[x],"%")
            print("\n")
       
    # Get all the session details
    def get_general_session_data(self):

        session_data = {}
        session_data["session_id"] = self.session_id
        session_data["data"] = []
        # app info
        session_data["data"].append({"key": "browser", "value": self.browser_name})
        session_data["data"].append({"key": "status", "value": self.status})

        return session_data

    # KPI marikng based on Document ready state
    def add_document_ready_based_annotations(
        self,
    ):
        page_load = {"labels": []}
        label_category = "using Document Ready State"
        print("adding_annotations_based_document_ready")
        for key, value in self.document_ready_labels.items():
            if (
                self.document_ready_labels[key]["start"]
                and self.document_ready_labels[key]["end"]
            ):
                label_start_time = (
                    self.document_ready_labels[key]["start"]
                    - self.video_start_timestamp
                )
                label_end_time = (
                    self.document_ready_labels[key]["end"] - self.video_start_timestamp
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
        for key, value in self.visual_labels.items():

            if self.visual_labels[key]["start"] and self.visual_labels[key]["end"]:
                label_start_time = (
                    self.visual_labels[key]["start"] - self.video_start_timestamp
                )

                label_end_time = (
                    self.visual_labels[key]["end"] - self.video_start_timestamp
                )

                if label_start_time < 0:
                    label_start_time = (
                        self.video_start_timestamp - self.video_start_timestamp
                    )
                label_item = {"name": key}
                label_item["start_time"] = label_start_time / 1000

                buffer_time = (
                    self.visual_labels[key]["buffer_time"]
                    if self.visual_labels[key].get("buffer_time")
                    else 0
                )

                label_item["end_time"] = (label_end_time / 1000) + buffer_time
                label_item["start_sensitivity"] = (
                    self.visual_labels[key]["start_sensitivity"]
                    if self.visual_labels[key].get("start_sensitivity")
                    else 0.9
                )
                label_item["end_sensitivity"] = (
                    self.visual_labels[key]["end_sensitivity"]
                    if self.visual_labels[key].get("end_sensitivity")
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
                        self.visual_labels[key]["end_sensitivity"]
                        if self.visual_labels[key].get("end_sensitivity")
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

    # scroll to web element to visibility
    def scroll_to_web_element(self, element):
        """
        Scroll to the element in Web View
        """
        try:
            desired_y = (element.size["height"] / 2) + element.location["y"]
            current_y = (
                self.driver.execute_script("return window.innerHeight") / 2
            ) + self.driver.execute_script("return window.pageYOffset")
            scroll_y_by = desired_y - current_y
            self.driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
            time.sleep(1)
        except:
            print("Scroll to web element failed")

    # Get the video time stamps
    def get_time_stamp(self, url=None):
        t_end = time.time()
        # Wait for 30 sec
        while time.time() < t_end + 30:
            # Check if the URL changed
            if url != self.driver.current_url:
                break
        t_end = time.time()
        # Check ready state
        while time.time() < t_end + 30:
            state = self.driver.execute_script("return document.readyState")
            if state == "complete":  # or state == 'interactive':
                return int(round(time.time() * 1000))


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
        "--vpla_only",
        dest="vpla_only",
        type=bool,
        default=False,
        required=False,
        help="only_visual_page_load_analysis",
    )

    parser.add_argument(
        "--document_ready_state_only",
        dest="document_only",
        type=bool,
        default=False,
        required=False,
        help="only_document_ready",
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
    add_doc_label = not (args.vpla_only)
    add_vpla_label = not (args.document_only)
    use_local_appium = args.local_appium
    udid = args.udid
    url = args.url
    if not use_local_appium:
        access_token = url.split("/")[-3]
        # Get Bearer token for header
        headers = {"Authorization": "Bearer {}".format(access_token)}
    suite = unittest.TestLoader().loadTestsFromTestCase(AmazonTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
