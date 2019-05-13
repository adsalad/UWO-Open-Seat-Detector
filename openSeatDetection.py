import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from twilio.rest import Client

account_sid = ""
auth_token = ""
client = Client(account_sid, auth_token)

# Create a new instance of the Firefox driver
driver = webdriver.Chrome('/Users/User/Downloads/chromedriver')

# go to the google home page
driver.get("https://studentservices.uwo.ca/secure/timetables/SummerTT/ttindex.cfm")

# find the element that's name attribute is q (the google search box)
inputElement = driver.find_element_by_id("inputCatalognbr")

# type in the search
inputElement.send_keys("")

# submit the form (although google automatically searches now without submitting)
inputElement.submit()

try:
    siteSource = driver.page_source
    refinedSource = BeautifulSoup(siteSource, "html.parser")
    table = refinedSource.find("table", {"class": "table table-striped"})

    dataList = []
    for sibling in table.tbody.tr.td.next_siblings:
        dataList.append(sibling)
    dataList = [str(elem) for elem in dataList]
    dataList = [x.replace(' ', '') for x in dataList]

    if any("NotFull" in x for x in dataList):
        message = client.messages.create(to="+", from_="+", body="Course is not Full!")

except selenium.common.exceptions.NoSuchElementException:
    print("Keyword Does Not Exist")
finally:
    driver.quit()

# why does it check first row only????
# research lists
