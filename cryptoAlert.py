import smtplib
import time
import random
import difflib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

                #"https://www.binance.com/en/copy-trading/lead-details?portfolioId=3680006230067031297&timeRange=30D", #jasmine tmp                

profileLinks = [
                #"https://www.binance.com/en/copy-trading/lead-details?portfolioId=3674416448692723201&timeRange=30D",
                #"https://www.binance.com/en/copy-trading/lead-details?portfolioId=3606613603928673025&timeRange=30D",
                "https://www.binance.com/en/copy-trading/lead-details?portfolioId=3698665844371141377&timeRange=30D",
                "https://www.binance.com/en/copy-trading/lead-details?portfolioId=3641706115175816705&timeRange=30D",
                ]

def searchLoop(driver):
    tmpList = []
    for link in profileLinks:
        if checkPageLoaded(driver , link):
            tmpList.append(runScraper(driver))
    
    writeToTmp(tmpList)
    compareLists()

    time.sleep(random.randint(120, 180)) # timer
    searchLoop(driver)

def writeToTmp(inputList):
    file_path = "tmp.txt"
    with open(file_path, 'w') as file:
        for item in inputList:
            if(item):
                file.write(item + '\n')

def compareLists():

    # File paths for the two text files
    file1_path = "main.txt"
    file2_path = "tmp.txt"

    # Read the contents of the two files
    with open(file1_path, 'r') as file1:
        file1_contents = file1.readlines()

    with open(file2_path, 'r') as file2:
        file2_contents = file2.readlines()

    # Use difflib to compare the contents
    differ = difflib.Differ()
    diff = list(differ.compare(file1_contents, file2_contents))

    # Process and display the differences
    for line in diff:
        if line.startswith(" "):
            continue   
        elif line.startswith("- "):
            emailPosition(line[2:],"Position Closed")
        elif line.startswith("+ "):
            emailPosition(line[2:],"Position Opened")

    # put the text from tmp file to main file
    # Read the contents of the source file
    with open(file2_path, 'r') as source_file:
        source_contents = source_file.read()

    # Write the contents of the source file to the destination file
    with open(file1_path, 'w') as destination_file:
        destination_file.write(source_contents)

def emailPosition(emailBody , emailSubject ):
    # formating
    text = emailBody
    words = text.strip().split()
    if words:
        first_word = words[0]



    # Email configuration
    sender_email = 'davistom408@gmail.com'
    receiver_email = 'besniknurshaba@gmail.com'
    subject = first_word + " " + emailSubject
    body = emailBody

    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # You can attach files if needed
    # attachment = open('file.txt', 'rb')
    # part = MIMEApplication(attachment.read(), Name='file.txt')
    # part['Content-Disposition'] = f'attachment; filename=file.txt'
    # message.attach(part)

    # Establish a connection to the SMTP server (in this case, Gmail)
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # For Gmail, you might need to enable "Less secure apps" or use an "App Password"
    # Go to your Google Account settings: https://myaccount.google.com/security
    # Generate an App Password: https://myaccount.google.com/apppasswords
    smtp_username = 'davistom408@gmail.com'
    smtp_password = 'etnh nmfz jhfs hwlj'

    # Connect to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    # Send the email
    server.sendmail(sender_email, receiver_email, message.as_string())

    # Close the connection
    server.quit()

def checkPageLoaded(driver , urlLink):
    driver.get(urlLink)
    wait = WebDriverWait(driver, 100)  # Set a timeout of 100 seconds
    xpath = "/html/body/div[3]"  # Replace with the desired XPath
    time.sleep(5)
    try:
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        time.sleep(5)
        if(element):
            return True
        else:
            checkPageLoaded(driver , urlLink)
    except:
            checkPageLoaded(driver , urlLink)

def runScraper(driver):
    try:
        # Read the contents of the JavaScript file
        with open("scraperJS.js", "r") as script_file:
            javascript_code = script_file.read()

        # Execute the JavaScript code from the external file and capture the result
        result = driver.execute_script(javascript_code)

        return result
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    driver = webdriver.Chrome()
    searchLoop(driver)


