<h1 align="center">  Readme </h1>

<br/>

# Annotation Comparison  
The KPI (Key Performance Indicator) has been evaluated using diverse approaches, and the script will conduct a comparison among them.
## 📝 Table of Contents

-  [Requirements](#req)
- [Visual Page Load Analysis (VPLA) VS  Find Element ](#fe)
- [ Visual Page Load Analysis (VPLA) VS Document Ready](#dr)
- [Visual Page Load Analysis (VPLA) VS Find Element Using Multiple Elements](#me)
- [Run Test On Local Appium Server ](#as)
- [Reference](#rf)

# :ballot_box_with_check: Requirements<a name = "req"></a>
- Device Platfrom  - Andoid 
- Test Application  - Expedia , Chrome Browser  
- Python  - Version 3.8 or above 
- Install all python packages before executing to avoid import errors.

		#Execute from root Directory 
		pip3 install -r requirements.txt
-  Local Appium Server for test : [Steps to setup Appium Server ](#as)  (*Optional requirement*)

## Note  :

-  To perform the Test Setup on Linux and Mac OS, you can run the `setup.sh` bash script located in the root directory. The script carries out the subsequent actions:

	- Verify whether python3 is pre-installed or not, and if it is not installed, proceed with its installation.
	- Set up a python virtual environment named **`env3`** and install all the necessary python packages within it.   
-  To run the **`setup.sh`** bash script, it is necessary to grant executable permission by using the command **`chmod +x setup.sh`** beforehand.
- Execute the setup.sh with command :  **`bash setup.sh`**  
- python virtual environment can be activate with the command : **`source env3/bin/activate `**
- *The `setup.sh` script is not compatible with Windows operating systems and cannot be executed on them.*

# :radio_button:  Visual Page Load Analysis (VPLA) VS  Find Element <a name = "fe"></a>

## Testing App 

- Expedia Android ([App Link](https://play.google.com/store/apps/details?id=com.expedia.bookings&hl=en&gl=US))



## Run Command 

**Run Command** : `python3 VPLA_Appium_Element.py  --udid {Device UDID}  --url  {Appium URL}` 


**Example** : 

```
python3 VPLA_Appium_Element.py  --udid RZ8NA0Z723M --url https://dev-in-blr-0.headspin.io:3012/v0/<TOKEN>/wd/hub 
```
    


 ` Note : Before running the  test,  make sure Expedia App is installed and loggedIn.`

**Command line Arguments** 
	
	

- `--udid` : Device id of the device you wish to start the run.Can be obtained from headspin UI  or locally conected device .

- `--url` : Appium URL of the device you wish to start the run. Can be obtained from the headspin UI or local appium url 

**Optional Arguments** 


- `--vpla_only` : ```True``` If only visual page load analysis needed 

- `--appium_element_only` : ```True``` If only Element Based label   needed 

- `--use_local_appium` : ```True``` If  need to use local appium server for test 
	
	*Note : Value should be boolean type (True/ False) for optional arguments  ,Default value for optional argument is False* 
	
## Sample Sessions 
    
- Sample Session : [ https://ui-dev.headspin.io/sessions/b0a83e42-ddae-11ed-b52a-06f0589e70dd/waterfall
](https://ui-dev.headspin.io/sessions/b0a83e42-ddae-11ed-b52a-06f0589e70dd/waterfall)    
- Sample Session with appium_element_only : [ https://ui-dev.headspin.io/sessions/af25d956-e37d-11ed-b9cb-06f0589e70dd/waterfall
](https://ui-dev.headspin.io/sessions/af25d956-e37d-11ed-b9cb-06f0589e70dd/waterfall)    
- Sample Session with vpla_only : [https://ui-dev.headspin.io/sessions/37091c26-e422-11ed-ba76-06f0589e70dd/waterfall
](https://ui-dev.headspin.io/sessions/37091c26-e422-11ed-ba76-06f0589e70dd/waterfall)
  



<br/>

# :radio_button:  Visual Page Load Analysis (VPLA) VS Document Ready <a name = "dr"></a> 

## Testing  Website 

- Amazon Mobile ([Link]( https://www.amazon.com/))

## Run command 

**Run Command** : `python3 VPLA_Doccument_Ready_State.py  --udid {Device UDID}  --url  {Appium URL}`


**Example** : 
```
python3 VPLA_Doccument_Ready_State.py --udid RZ8NA0Z723M --url https://dev-in-blr-0.headspin.io:3012/v0/<TOKEN>/wd/hub
```
   
**Command line Arguments** 
	
-	`--udid` : Device id of the device you wish to start the run.Can be obtained from headspin  UI or  or locally conected device . 

-	`--url` : Appium URL of the device you wish to start the run. Can be obtained from the headspin UI or local appium url 
	
**Optional Arguments** 

-	`--vpla_only` : ```True``` If only visual page load analysis needed 

-	`--document_ready_state_only` : ```True``` If only Document  Ready labels  needed   

-	`--use_local_appium` : ```True``` If  need to use local appium server for test 

	*Note : Value should be boolean type (True/ False) for optional arguments  ,Default value for optional argument is False* 


## Sample Sessions 

-  Sample Session : [https://ui-dev.headspin.io/sessions/08e597ee-ddaf-11ed-b52b-06f0589e70dd/waterfall](https://ui-dev.headspin.io/sessions/08e597ee-ddaf-11ed-b52b-06f0589e70dd/waterfall)

- Sample Session with document_ready_state_only : [ https://ui-dev.headspin.io/sessions/eb5d5c5e-e37e-11ed-b9cc-06f0589e70dd/waterfall](https://ui-dev.headspin.io/sessions/eb5d5c5e-e37e-11ed-b9cc-06f0589e70dd/waterfall)  

- Sample Session with vpla_only : [https://ui-dev.headspin.io/sessions/341695be-e424-11ed-ba79-06f0589e70dd/waterfall
](https://ui-dev.headspin.io/sessions/341695be-e424-11ed-ba79-06f0589e70dd/waterfall)


    
<br/>

#  :radio_button: Visual Page Load Analysis (VPLA) VS Find Element Using Multiple Elements <a name = "me"></a>

## Testing  App 

- Expedia Android ([App Link](https://play.google.com/store/apps/details?id=com.expedia.bookings&hl=en&gl=US))



## Run Command

**Run Command** : `python3 VPLA_Multiple_Appium_Element.py --udid {Device UDID}  --url  {Appium URL}`



**Example** : 
```
python3 VPLA_Multiple_Appium_Element.py --udid RZ8NA0Z723M --url https://dev-in-blr-0.headspin.io:3012/v0/<TOKEN>/wd/hub 
```
  ` Note : Before running the  test,  make sure Expedia App is installed and loggedIn.`
    


**Command line Arguments**
	
	

-	`--udid` : Device id of the device you wish to start the run.Can be obtained from headspin UI  or locally conected device .

-	`--url` : Appium URL of the device you wish to start the run. Can be obtained from the headspin UI or local appium url 
**Optional Arguments** 

-	`--vpla_only` : ```True``` If only visual page load analysis needed 

-	`--appium_element_only` : ```True``` If only Element Based label   needed 

-	`--use_local_appium` : ```True``` If  need to use local appium server for test 
	
	*Note : Value should be boolean type (True/ False) for optional arguments  ,Default value for optional argument is False* 
  
 ## Sample Sessions 
 
- Sample Session : [ https://ui-dev.headspin.io/sessions/2848212a-e420-11ed-ba70-06f0589e70dd/waterfall
](https://ui-dev.headspin.io/sessions/2848212a-e420-11ed-ba70-06f0589e70dd/waterfall)    

- Sample Session with appium_element_only : [https://ui-dev.headspin.io/sessions/9d3b2482-e420-11ed-ba72-06f0589e70dd/waterfall
](https://ui-dev.headspin.io/sessions/9d3b2482-e420-11ed-ba72-06f0589e70dd/waterfall)

- Sample Session with vpla_only : [https://ui-dev.headspin.io/sessions/b7665bd2-e421-11ed-ba73-06f0589e70dd/waterfall
](https://ui-dev.headspin.io/sessions/b7665bd2-e421-11ed-ba73-06f0589e70dd/waterfall)


<br/>

# Run Test On Local Appium Server <a name = "as"></a>
 
 * Install and Setup the Appium Server in  the local  ( [Installation Setp ](https://appium.io/docs/en/2.0/quickstart/install/)) , Start the server with command `appium` and get the Appium url. (Example url : `http://0.0.0.0:4723/wd/hub` )
* Make device available locally and get the device id with command `adb dveices`
* Pass the Appium url and Device id as argument for test run along with making the flag --local_appium True  for running test on local appium server

  *Note : All Headspin Capabilities will be disabled while running test on local appium server* 
<br/>

# :books: References <a name = "rf"></a>

1. Document ready state :   [https://developer.mozilla.org/en-US/docs/Web/API/Document/readyState](https://developer.mozilla.org/en-US/docs/Web/API/Document/readyState)
2. Headspin VIsual page load : [https://ui.headspin.io/docs/visual-loading-metrics#page-load](https://ui.headspin.io/docs/visual-loading-metrics#page-load)
3. Appium find elements based: [https://www.headspin.io/blog/capturing-app-launch-metrics-on-android](https://www.headspin.io/blog/capturing-app-launch-metrics-on-android)

<br/>

# :iphone: Tested On  

            ORG : Headspin_APAC_Shared
            Device :SAMSUNG SM-M317  
            UDID : RZ8NA0Z723M
