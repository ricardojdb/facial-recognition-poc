from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

user = "jhuanayq@everis.com"
pasw = "Peru123_"

wakeword = "everis"

driver = 'chromedriver.exe'
page = "https://developer.amazon.com/alexa/console/ask/test/amzn1.ask.skill.98318779-2239-4375-a6ea-e55ec462a00f/development/es_MX/"

class AlexaPortal():
    def __init__(self, driver, page):
        self.driver = webdriver.Chrome(executable_path=driver)
        self.driver.get(page)

    def login(self, user=user, password=pasw):
        "Alexa login"
        elem = self.driver.find_element_by_id("ap_email")
        elem.send_keys(user)
        elem = self.driver.find_element_by_id("ap_password")
        elem.send_keys(password)
        elem.send_keys(Keys.RETURN)
    
    def wake_skill(self, wakeword=wakeword):
        elem = self.driver.find_element_by_class_name("askt-utterance__input")
        elem.send_keys(wakeword)
        elem.send_keys(Keys.RETURN)
        time.sleep(2)
    
    def send_names(self, names):
        elem = self.driver.find_element_by_class_name("askt-utterance__input")
        elem.send_keys(names)
        elem.send_keys(Keys.RETURN)

if __name__ == "__main__":
    alexa = AlexaPortal(driver, page)
    alexa.login()
    alexa.wake_skill()
    for name in ["hugo", "jaspers", "ricardo"]:
        time.sleep(5)
        alexa.send_names(name)