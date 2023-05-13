package in.maven;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileBy;
import io.appium.java_client.MobileElement;
import io.appium.java_client.TouchAction;
// import io.appium.java_client.android.Activity;
import io.appium.java_client.remote.MobileCapabilityType;
import io.appium.java_client.touch.WaitOptions;
import io.appium.java_client.touch.offset.PointOption;

import java.net.URL;
import java.time.Duration;

import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class expendia {
    
    static AppiumDriver<MobileElement> driver;
    public static void main(String[] args) {
    
        try{
            test();
        }

        catch( Exception e ){
            // System.out.println( e.getCause() );
            // System.out.println( e.getMessage() );
            // System.out.println( e.getStackTrace() );
            System.out.println(e);
        }
        
    }

    public static void test() throws Exception{

        URL url = new URL("https://in-bgl.headspin.io:3010/v0/<TOKEN>/wd/hub");
        // String myApp = "/Users/keer/Documents/Java/Expedia.apk";

        // DesiredCapabilities capabilities = new DesiredCapabilities();
        DesiredCapabilities capabilities = new DesiredCapabilities();
        capabilities.setCapability(MobileCapabilityType.PLATFORM_NAME, "Android");
            // capabilities.setCapability(MobileCapabilityType.PLATFORM_VERSION, "11");
        capabilities.setCapability(MobileCapabilityType.DEVICE_NAME, "1724");
        capabilities.setCapability(MobileCapabilityType.UDID, "94c0d2f7");
            // capabilities.setCapability(MobileCapabilityType.APP, myApp);
        capabilities.setCapability("appPackage", "com.expedia.bookings");
        capabilities.setCapability("appActivity", "com.expedia.bookings.activity.RouterActivity");

        driver = new AppiumDriver<MobileElement>( url, capabilities);
        WebDriverWait wait;
        wait = new WebDriverWait( driver, 10 );

        // driver.startActivity(new Activity("com.example", "ActivityName"));
        // driver.activi

        System.out.println("Hello");
        for( int i = 0; i < 2; i ++ )
            wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.id( "com.expedia.bookings:id/button_next" ) ) ).click();
        System.out.println("Hello");

        try{
            wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.id( "com.expedia.bookings:id/button_final" ) ) ).click();
        }
        
        catch( Exception e ){
            Thread.sleep( 3000 );
            wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.id( "com.expedia.bookings:id/button_final" ) ) ).click();
        }
        System.out.println("Hello");

        Thread.sleep( 5000 );
        wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.id( "com.android.permissioncontroller:id/permission_allow_foreground_only_button" ) ) ).click();

        String xp = "(//android.widget.ImageButton[@content-desc=\"Sign in with Google\"])[2]";

        wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.xpath( xp ) ) ).click();
        System.out.println("Hello");

        wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.AccessibilityId( "Stays Button" ) ) ).click();
        wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.id( "com.expedia.bookings:id/search_src_text" ) ) ).sendKeys( "Eiffel Tower, Paris, France" );
        Thread.sleep( 5000 );
        System.out.println("Hello");

        wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.id( "com.expedia.bookings:id/suggestion_text_container" ) ) ).click();
        wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.id( "com.expedia.bookings:id/foreground" ) ) ).click();

        wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.id( "com.expedia.bookings:id/sticky_bottom_button" ) ) ).click();
        
        Thread.sleep( 5000 );

        TouchAction action = new TouchAction(driver);

        action.press(PointOption.point(537, 1777))
            .waitAction(new WaitOptions().withDuration(Duration.ofMillis(2000)))
            .moveTo(PointOption.point(537, 1000))
            .release()
            .perform();

        wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.AccessibilityId( "Reserve, Superior Afterworks Option 2 Button" ) ) ).click();
        
        Thread.sleep( 3000 );
        action.press(PointOption.point(537, 1777))
            .waitAction(new WaitOptions().withDuration(Duration.ofMillis(2000)))
            .moveTo(PointOption.point(537, 1000))
            .release()
            .perform();

        wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.AccessibilityId( "Pay at property Button" ) ) ).click();

        Thread.sleep( 3000 );    

    }
}

