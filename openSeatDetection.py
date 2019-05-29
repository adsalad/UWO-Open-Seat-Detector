import selenium
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from twilio.rest import Client

#this is where administrator Twilio credentials go
account_sid = ""
auth_token = ""
client = Client(account_sid, auth_token)

#start Chrome in headless mode so no window pops up when Selenium opens it
customOptions = Options()
customOptions.headless = True

def check_seats(course_number, class_number, student_number):

    #create a new instance of the Chrome driver
    driver = webdriver.Chrome('/Users/User/Downloads/chromedriver', options = customOptions)

    #go to the course searcher home page
    driver.get("https://studentservices.uwo.ca/secure/timetables/SummerTT/ttindex.cfm")

    #find the element that's id attribute is the following... for the search bar
    inputElement = driver.find_element_by_id("inputCatalognbr")

    #type in the search
    inputElement.send_keys(course_number)

    #submit the form 
    inputElement.submit()
    
    try:
        #extract source after entering keys, using selenium instead of requests due to page being an SPA
        #find table row with corresponding unique class number and append it as a string to a list
        siteSource = driver.page_source
        refinedSource = BeautifulSoup(siteSource, "html.parser")
        allRows = refinedSource.find_all('tr')
        userRows = [elem for elem in allRows if elem.find_all(text=re.compile(class_number))]
        dataList = [str(elem) for elem in userRows]

        #if word "Not Full" is found anywhere in the list, send a message to user's phone number
        if any("Not Full" in x for x in dataList):
           client.messages.create(to="+1" + studentNumber, from_="", body= course_number + " is not Full! "
                                                                         "Hurry and register!")
    #if course number does not return results, this exception will be thrown                        
    except selenium.common.exceptions.NoSuchElementException:
        print("Keyword Does Not Exist")
        
    #quit driver and close Chrome regardless of error
    finally:
        driver.quit()


def main():
     print("""
       __  ___       ______     ____                      _____            __     ____       __            __            
      / / / / |     / / __ \   / __ \____  ___  ____     / ___/___  ____ _/ /_   / __ \___  / /____  _____/ /_____  _____
     / / / /| | /| / / / / /  / / / / __ \/ _ \/ __ \    \__ \/ _ \/ __ `/ __/  / / / / _ \/ __/ _ \/ ___/ __/ __ \/ ___/
    / /_/ / | |/ |/ / /_/ /  / /_/ / /_/ /  __/ / / /   ___/ /  __/ /_/ / /_   / /_/ /  __/ /_/  __/ /__/ /_/ /_/ / /    
    \____/  |__/|__/\____/   \____/ .___/\___/_/ /_/   /____/\___/\__,_/\__/  /_____/\___/\__/\___/\___/\__/\____/_/     
                             /_/                                                                                     
    """)
    print("Hey! This is a tool that will automatically check and notify you when a course seat opens up.")
    print("First provide us with the 'Course Number', such as '1027' for 'CS1027', and provide us with the 'Class Number' which can be "
          "found manually by searching the timetable \n")
    courseNumber = input("Type in the Course Number here: \n")
    classNumber = input("And type in the Class Number here: \n")
    studentNumber = input("Finally, please enter your phone number, to be notified when a seat opens: \n")
    check_seats(courseNumber, classNumber, studentNumber)

 main()
