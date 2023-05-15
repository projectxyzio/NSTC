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
        driver.resetApp();

        // Creating the test
        report = extentReportDemo.report();

        while( count < 3 ){
            try{

                test = report.createTest( "Automation of Expedia - "+(count+1));
                test.log( Status.INFO, "Test just started!" );


                    try{

                        wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.AccessibilityId( "More rewarding travel" ) ) );
                        wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.className( "android.widget.Button" ) ) ).click();

                    }

                    catch( Exception e ){
                        Thread.sleep( 2000 );
                        test.log( Status.INFO, "Initial pop-up cleared " );
                    }

                try{
                    wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.id( "com.google.android.gms:id/cancel") ) ).click();

                }
                catch( Exception e ){

                    wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.AccessibilityId( "Sign in" ) ) );
                    Thread.sleep( 1000 );
                }

                String xp;
                if( count == 0 ){
                    xp = "(//android.widget.ImageButton[@content-desc=\"Sign in with ABC\"])[2]";
                }

                else{
                    xp = "//android.widget.TextView[@content-desc='Continue with Google']";
                }

                try{
                    wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.xpath( xp ) ) ).click();
                }

                catch( Exception e ){
                    test.log( Status.FAIL, "Failed!" );

                }


                Thread.sleep( 2000 );
                wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.id( "com.google.android.gms:id/account_picker_container" ) ) ).click();

                wait.until( ExpectedConditions.presenceOfElementLocated( MobileBy.className( "android.widget.LinearLayout" ) ) );

                test.log( Status.PASS, "Login successful!" );
                Thread.sleep( 3000 );
                test.log( Status.INFO, "Test ended successfully!" );

            }

            catch( Exception e ){

                // System.out.println( "The cause: " +e.getCause() );
                // System.out.println( "The message: " +e.getMessage() );
                // System.out.println( "Stack Trace: "  +e.getStackTrace());
                test.log( Status.FAIL, "Login Failed!" );
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
