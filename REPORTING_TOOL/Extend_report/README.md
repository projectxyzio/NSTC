# Automation of Expedia application in Java and integrating the same with Extent Reports.

##  Prerequisites
### a. Installing JDK and initialising $JAVA_HOME:
1. Download JDK from the link: [https://www.oracle.com/in/java/technologies/javase/javase-jdk8-downloads.html](https://www.oracle.com/in/java/technologies/javase/javase-jdk8-downloads.html) and install it.
2. Now the environmental variable JAVA_HOME should be initialised.

Now initialising the $JAVA_HOME variable. This can be done by executing the below commands.

```
nano .zprofile
export JAVA_HOME = "$(/usr/libexec/java_home)"
```

Example

```
# Setting PATH for Python 3.9
# The original version is saved in .zprofile.pysave
export JAVA_HOME="/Library/Java/JavaVirtualMachines/jdk-
11.0.10.jdk/Contents/Ho$
```

### b. Installing Appium Desktop App:
1. Download the Appium Desktop app from the link: [https://appium.io/downloads.html](https://appium.io/downloads.html) and install it.
This can be used to create the automation script.

### c. Installing Code Editor:

1. Download IntelliJ IDEA code from the link: [https://www.jetbrains.com/idea/download/](https://www.jetbrains.com/idea/download/)
and install it.

**Any other code editor can also be used.**

**Once all the above steps are completed, the setup is ready.**


## Test Execution

- Open **`appiumtests`** Directory in IntelliJ (File -> Open -> Select Directory )  

-  Update the device id and Appium url  of the device which your performing the test  in **`BaseClass.java`** (path : `appiumtests/src/test/java/in/maven/tests` ) .

- Execut the test file . ( right click on Tests.java -> Run 'Tests' )

-  Now if you execute the automation test code, a HTML report will be created in the path you have specified in the above code. In my case the report will be generated in the same directory (target directory)and will be named as **`Spark.html`**.

![Not Loading](./readme_images/report1.png)

![Not Loading](./readme_images/report2.png)

This will be the end product. This is how the report will be generated after the test is executed.
