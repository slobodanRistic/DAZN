from selenium import webdriver
import os
import time
from selenium.common.exceptions import NoSuchElementException
import datetime
from selenium.webdriver.common.by import By
import logging
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities




def main():

    getAccount(webaddress = "https://serene-mountain-14043.herokuapp.com/")



def getAccount(webaddress):
    weatherValues = {}

    # enable browser logging
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'performance': 'ALL'}

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    dir_path = os.path.dirname(os.path.realpath(__file__))
    chromedriver = dir_path + "/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chrome_options=options, executable_path=chromedriver)

    driver.get(webaddress)

    # TEST CASE 1
    print ("TEST CASE 1")

    # Verify the page has a header “Weather Checker”
    print ("Verify the page has a header “Weather Checker”")
    element = findElement(driver, 'class_name', 'header')
    if element is not False:
        if element.text == "Weather Checker":
            print ("PASS: Header containg 'Weather Checker' is present on the screen")
        else:
            print ("ERROR: Wrong text in header")
    else:
        print("It was not possible to find Header")

    # Entry filed with text “Enter postcode”
    element = findElement(driver, 'id', 'searchLocation')
    if element is not False:
        child = findChildOfElement(element, 'tag_name', 'input')
        if child is not False:
            if child.get_attribute("placeholder") == "Enter postcode":
                print("PASS: Entry field is present and it contains text 'Enter Postcode'")
            else:
                print ("ERROR: Entry field does not contain correct text")
        else:
            print ("ERROR: Entry field is missing")
    else:
        print ("ERROR: The wholse SEARCH area is missing")


    # Button with text “Search”
    element = findElement(driver, 'id', 'searchLocation')
    if element is not False:
        child = findChildOfElement(element, 'tag_name', 'button')
        if child is not False:
            if child.text == "Search":
                print("PASS: Search button is present and it contains correct text")
            else:
                print ("ERROR: Search button does not contain correct text")
        else:
            print ("ERROR: Search button is missing")
    else:
        print ("ERROR: The wholse SEARCH area is missing")

    # TEST CASE 2
    print ("TEST CASE 2")

    # Send B99 9AA (valid non-existing post-code) > verify message displayed: “Postcode not found”
    # Write value to input field
    writeToInputFiledAndSearch(driver, "B99 9AA")

    # Verify Message for valid non-existing post-code
    element = findElement(driver, "tag_name", "h1")
    if element is not False:
        if element.text == 'Postcode not found':
            print ("PASS: Correct response when valid non-existent postcode checked")
        else:
            print("ERROR: Wrong response when valid non-existent postcode checked '" + element.text + " '")
    else:
        print("ERROR: The MESSAGE area is missing")

    # TEST CASE 3
    print("TEST CASE 3")

    # EC1A 1BB (non-valid post-code) > verify message displayed: “Postcode not valid”
    # Write value to input field
    writeToInputFiledAndSearch(driver, "EC1A 1BB")

    # Verify Message for valid non-existing post-code
    element = findElement(driver, "tag_name", "h1")
    if element is not False:
        if element.text == 'Postcode not valid':
            print("PASS: Correct response when valid non-existent postcode checked")
        else:
            print("ERROR: Wrong response when valid non-existent postcode checked '" + element.text + " '")
    else:
        print("ERROR: The MESSAGE area is missing")

    # TEST CASE 4
    print("TEST CASE 4")

    # W6 0NW (valid existing post-code) > verify table header and body is displayed

    # Write value to input field
    writeToInputFiledAndSearch(driver, "W6 0NW")

    # Verify Message for valid non-existing post-code
    element = findElement(driver, "tag_name", "table")
    if element is not False:
        # Find header and check text
        header = findChildOfElement(element, "class_name", "tableHeader")
        if header is not None:
            if header.text == "Weather details":
                print ("PASS: The table has header with correct text")
            else:
                print ("ERROR :Table's header contains wrong text")
        else:
            print ("ERROR: Tabel header can't be found")

        # Find table's body
        body = findChildOfElement(element, "tag_name", "tbody")
        if body is not None:
            print ("PASS: Table has body")
            tableContents = findElements(driver, "tag_name", "tr")
            if tableContents is not None:
                for i in tableContents:
                    weatherValues [findChildOfElement(i, "tag_name", "th").text.replace(":", "")] = findChildOfElement(i, "tag_name", "td").text

            else:
                print ("PASS: It wasn't possible to extract content of the table")

        else:
            print("ERROR: Table doesn't have body")

    else:
        print("ERROR: The Weather Table is missing")

    if len(weatherValues) > 0:
        # TEST CASE 5
        # Verify table with returned details displayed and verify that:
        #   The weather properties "Time", "Temperature" and "Humidity" need to be there;
        #   If a weather property doesn't have a value, it should not appear on the table;
        #   The current time should display in the format DD/MM/YYYY HH:mm:ss
        print ("TEST CASE 5")
        # The weather properties "Time", "Temperature" and "Humidity" need to be there
        if "Time" and "Temperature" and "Humidity" in weatherValues.keys():
            print ("PASS: Time, Temperature and Humidity are present in the table")
        else:
            print ("ERROR: Time, Temperature and Humidity are NOT present in the table")
        #   If a weather property doesn't have a value, it should not appear on the table;
        if "" in weatherValues.values():
            print ("ERROR: Weather properties without values appear in the table")
        else:
            print ("No Weather properties without values appear in the table")
        #   The current time should display in the format DD/MM/YYYY HH:mm:ss
        dateString = weatherValues["Time"]
        format = "%d/%m/%Y %H:%M:%S"
        try:
            datetime.datetime.strptime(dateString, format)
            print("PASS: Time is the correct date string format.")
        except ValueError:
            print("ERROR: This is the incorrect date string format. It should be DD/MM/YYYY HH:mm:ss")

    else:
        print ("ERROR: Contents of the table are not tested")


        #if len(weatherWalues) > 0:


def writeToInputFiledAndSearch(driver, value):
    element = findElement(driver, 'id', 'searchLocation')
    if element is not False:
        child = findChildOfElement(element, 'tag_name', 'input')
        if child is not False:
            child.clear()
            child.send_keys(value)
        else:
            print("ERROR: Search button is missing")
    else:
        print("ERROR: The wholse SEARCH area is missing")

    time.sleep(5)

    # Click on “Search” button
    element = findElement(driver, 'id', 'searchLocation')
    if element is not False:
        child = findChildOfElement(element, 'tag_name', 'button')
        if child is not False:
            child.click()
        else:
            print("ERROR: Search button is missing")
    else:
        print("ERROR: The wholse SEARCH area is missing")

    time.sleep(20)

def findElement(driver, selector, value):

    try:
        if selector.lower()== 'id':
            element = driver.find_element(By.ID, value)
        elif selector.lower()== 'xpath':
            element = driver.find_element(By.XPATH, value)
        elif selector.lower()== 'link_text':
            element = driver.find_element(By.LINK_TEXT, value)
        elif selector.lower()== 'partial link text':
            element = driver.find_element(By.PARTIAL_LINK_TEXT, value)
        elif selector.lower()== 'name':
            element = driver.find_element(By.NAME, value)
        elif selector.lower()== 'tag_name':
            element = driver.find_element(By.TAG_NAME, value)
        elif selector.lower()== 'class_name':
            element = driver.find_element(By.CLASS_NAME, value)
        elif selector.lower()== 'css_selector':
            element = driver.find_element(By.CSS_SELECTOR, value)
    except NoSuchElementException:
        element is False
    return element

def findElements(driver, selector, value):

    try:
        if selector.lower()== 'id':
            elementList = driver.find_elements(By.ID, value)
        elif selector.lower()== 'xpath':
            elementList = driver.find_elements(By.XPATH, value)
        elif selector.lower()== 'link_text':
            elementList = driver.find_elements(By.LINK_TEXT, value)
        elif selector.lower()== 'partial link text':
            elementList = driver.find_elements(By.PARTIAL_LINK_TEXT, value)
        elif selector.lower()== 'name':
            elementList = driver.find_elements(By.NAME, value)
        elif selector.lower()== 'tag_name':
            elementList = driver.find_elements(By.TAG_NAME, value)
        elif selector.lower()== 'class_name':
            elementList = driver.find_elements(By.CLASS_NAME, value)
        elif selector.lower()== 'css_selector':
            elementList = driver.find_elements(By.CSS_SELECTOR, value)
    except NoSuchElementException:
        elementList is False
    return elementList

def findChildOfElement(element, selector, value):
    try:
        if selector.lower()== 'id':
            child = element.find_element(By.ID, value)
        elif selector.lower()== 'xpath':
            child = element.find_element(By.XPATH, value)
        elif selector.lower()== 'link_tex:':
            child = element.find_element(By.LINK_TEXT, value)
        elif selector.lower()== 'partial link text':
            child = element.find_element(By.PARTIAL_LINK_TEXT, value)
        elif selector.lower()== 'name':
            child = element.find_element(By.NAME, value)
        elif selector.lower()== 'tag_name':
            child = element.find_element(By.TAG_NAME, value)
        elif selector.lower()== 'class_name':
            child = element.find_element(By.CLASS_NAME, value)
        elif selector.lower()== 'css selector':
            child = element.find_element(By.CSS_SELECTOR, value)
    except NoSuchElementException:
        child is False
    return child


if __name__ == "__main__":
    main()