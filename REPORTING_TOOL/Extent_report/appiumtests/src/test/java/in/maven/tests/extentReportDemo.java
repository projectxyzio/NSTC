package in.maven.tests;

import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.reporter.ExtentSparkReporter;

// import com.aventstack.extentreports.ExtentReports;
// import com.aventstack.extentreports.reporter.ExtentHtmlReporter;

// import org.testng.annotations.AfterSuite;
// import org.testng.annotations.BeforeSuite;

// public class extentReportDemo {
    
//     ExtentReports extent;
//     ExtentHtmlReporter htmlReporter;

//     @BeforeSuite
//     public void reportSetup(){

//         htmlReporter = new ExtentHtmlReporter("extent.html");
    
//         // create ExtentReports and attach reporter(s)
//         extent = new ExtentReports();
//         extent.attachReporter(htmlReporter);
//     }

//     @AfterSuite
//     public void reportTearDown(){
        
//         extent.flush();
//     }
// }

public class extentReportDemo {

    
    public static ExtentReports report(){
        
    ExtentReports extent = new ExtentReports();
    ExtentSparkReporter spark = new ExtentSparkReporter("target/Spark.html");
    
    extent.attachReporter(spark);
    // extent.flush();

    return extent;
    }
    
}