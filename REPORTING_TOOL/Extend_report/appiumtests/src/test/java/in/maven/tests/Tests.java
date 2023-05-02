package in.maven.tests;

// importing java packages
import java.time.Duration;

// Importing Extent Reports packages
import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.ExtentTest;
import com.aventstack.extentreports.Status;

// Importing Selenium packages
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.testng.annotations.Test;

// Importing Appium packages
import io.appium.java_client.MobileBy;
import io.appium.java_client.TouchAction;
import io.appium.java_client.touch.WaitOptions;
import io.appium.java_client.touch.offset.PointOption;
public class Tests extends BaseClass{
    
    ExtentReports report;
    ExtentTest test;

    @Test
    public void SampleTest(){

        int count = 0;
        System.out.println( "Running a test! " );

        // Creating the test
        report = extentReportDemo.report();

        while( count < 3 ){
            try{

                test = report.createTest( "Automation of Expedia - "+(count+1));
                test.log( Status.INFO, "Test just started!" );
    
                for( int i = 0; i < 2; i ++ )
                wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.id( "com.expedia.bookings:id/button_next" ) ) ).click();
    
                try{
                    wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.id( "com.expedia.bookings:id/button_final" ) ) ).click();
                    test.log( Status.PASS, "Entered!" );
                }
    
                catch( Exception e ){
                    Thread.sleep( 3000 );
                    wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.id( "com.expedia.bookings:id/button_final" ) ) ).click();
                    test.log( Status.PASS, "Waited and entered!" );
                }
    
                Thread.sleep( 5000 );
                // wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.id( "com.android.permissioncontroller:id/permission_allow_foreground_only_button" ) ) ).click();
                // test.log( Status.PASS, "Permission Granted!" );
                
                String xp;
                if( count == 0 ){
                    xp = "(//android.widget.ImageButton[@content-desc=\"Sign in with ABC\"])[2]";
                }

                else{
                    xp = "(//android.widget.ImageButton[@content-desc=\"Sign in with Google\"])[2]";
                }
                
                try{
                    wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.xpath( xp ) ) ).click();
                }

                catch( Exception e ){
                    test.log( Status.FAIL, "Failed!" );
                }
                
    
                // wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.id( "com.google.android.gms:id/account_picker_container" ) ) );
        
                // WebElement classList = wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.className( "android.widget.LinearLayout" ) ) );
                // System.out.println( classList );
    
                // for( int i = 0; i < 10; i ++ ){
                //     System.out.println( classList.text );
                // }
                // driver.findElement( MobileBy.xpath( "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[1]" ) ).click();
                // driver.findElement( MobileBy.id( "118ea4b2-2098-482d-806a-f96b770dcc97" ) ).click();
                TouchAction action = new TouchAction(driver);
            
                Thread.sleep(5000);
                // action.tap( PointOption.point(297, 717) ).perform();
                
                // wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.xpath( xp ) ) ).click();
    
                wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.AccessibilityId( "Stays Button" ) ) ).click();
                wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.id( "com.expedia.bookings:id/search_src_text" ) ) ).sendKeys( "Eiffel Tower, Paris, France" );
                Thread.sleep( 1000 );
    
                test.log( Status.PASS, "Search successful!" );
    
                wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.id( "com.expedia.bookings:id/suggestion_text_container" ) ) ).click();
                wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.id( "com.expedia.bookings:id/foreground" ) ) ).click();
    
                wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.id( "com.expedia.bookings:id/sticky_bottom_button" ) ) ).click();
    
                Thread.sleep( 5000 );
    
                action.press(PointOption.point(315, 1200))
                    .waitAction(new WaitOptions().withDuration(Duration.ofMillis(2000)))
                    .moveTo(PointOption.point(315, 750))
                    .release()
                    .perform();
    
                // wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.AccessibilityId( "Reserve, Superior Afterworks Option 2 Button" ) ) ).click();
                
                // Thread.sleep( 3000 );
                // action.press(PointOption.point(315, 1200))
                //     .waitAction(new WaitOptions().withDuration(Duration.ofMillis(2000)))
                //     .moveTo(PointOption.point(315, 750))
                //     .release()
                //     .perform();
    
                // wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.AccessibilityId( "Pay at property Button" ) ) ).click();
    
                test.log( Status.PASS, "Booking successful!" );
                Thread.sleep( 3000 );
    
                test.log( Status.INFO, "Test ended successfully!" );
    
            }
            
            catch( Exception e ){
    
                // System.out.println( "The cause: " +e.getCause() );
                // System.out.println( "The message: " +e.getMessage() );
                // System.out.println( "Stack Trace: "  +e.getStackTrace());
                System.out.println(e);
    
            }

            finally{
                count = count + 1;
                driver.resetApp();
                report.flush();
            }
        }
        
    }
}
