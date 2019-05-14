import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from twilio.rest import Client

account_sid = ""
auth_token = ""
client = Client(account_sid, auth_token)

def check_seats(course_number, class_number):

    # Create a new instance of the Firefox driver
    driver = webdriver.Chrome('/Users/User/Downloads/chromedriver')

    # go to the google home page
    driver.get("https://studentservices.uwo.ca/secure/timetables/SummerTT/ttindex.cfm")

    # find the element that's name attribute is q (the google search box)
    inputElement = driver.find_element_by_id("inputCatalognbr")

    # type in the search
    inputElement.send_keys(course_number)

    # submit the form (although google automatically searches now without submitting)
    inputElement.submit()

    try:
        siteSource = driver.page_source
        refinedSource = BeautifulSoup(siteSource, "html.parser")
        allRows = refinedSource.find_all('tr')
        userRows = [t for t in alRrows if t.find_all(text=re.compile(class_number))]
        dataList = [str(elem) for elem in userRows]

        if any("Not Full" in x for x in dataList):
            message = client.messages.create(to="+", from_="+", body="Course is not Full!")

    except selenium.common.exceptions.NoSuchElementException:
        print("Keyword Does Not Exist")
    finally:
        driver.quit()


def main():
    print("Hey! This is a tool that will automatically check and notify you when a course seat opens up /n")
    print("First provide us with the 'Course Number', such as '1027' for 'CS1027', and provide us with the 'Class Number' which can be"
          "found manually by searching the timetable")
    courseNumber = input("Type in the Course Number here: ")
    classNumber = input("And type in the Class Number here: ")
    check_seats(courseNumber, classNumber)

 main()
