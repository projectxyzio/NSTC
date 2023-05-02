// Automation test to run a tourist app called 'Expedia using java'

package in.maven.tests;

// importing java packages
import java.net.URL;

// Importing Selenium packages
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.annotations.AfterTest;
import org.testng.annotations.BeforeTest;

// Importing Appium packages
import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileElement;
import io.appium.java_client.remote.MobileCapabilityType;

public class BaseClass extends extentReportDemo{
    
    // Global variables
    static AppiumDriver<MobileElement> driver;
    WebDriverWait wait;
    
    @BeforeTest
    public void setup(){

        try{
            // The url in which the appium server is running
            URL url = new URL("https://in-bgl.headspin.io:3010/v0/da8072ab2ea94d239bfa9854089a9708/wd/hub");

            // The location of the app which should be launched in the android device
            // String myApp = "/Users/keer/Documents/Java/Expedia.apk";

            // Declaring desired capabilities
            DesiredCapabilities capabilities = new DesiredCapabilities();
            capabilities.setCapability(MobileCapabilityType.PLATFORM_NAME, "Android");
            capabilities.setCapability(MobileCapabilityType.PLATFORM_VERSION, "8.1.0");
            capabilities.setCapability(MobileCapabilityType.DEVICE_NAME, " 1724");
            capabilities.setCapability(MobileCapabilityType.UDID, "94c0d2f7");
            // capabilities.setCapability(MobileCapabilityType.APP, myApp);
            capabilities.setCapability("autoAcceptAlerts", true);
            capabilities.setCapability("autoGrantPermissions", true);
            capabilities.setCapability("appPackage", "com.expedia.bookings");
            capabilities.setCapability("appActivity", "com.expedia.bookings.activity.RouterActivity");

            // Initialising driver
            driver = new AppiumDriver<MobileElement>( url, capabilities);

            // Initialising wait
            wait = new WebDriverWait( driver, 10 );
        }

        catch( Exception e ){
            // System.out.println( "The cause is: " +e.getCause() );
            // System.out.println( "The message is: " +e.getMessage() );
            // System.out.println( "Stack Trace: " +e.getStackTrace() );
            System.out.println(e);
        }
    }

    @AfterTest
    public void TearDown(){

        driver.quit();

    }
}
