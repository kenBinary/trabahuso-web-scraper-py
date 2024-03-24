from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


def browserDriver(url: str):

    service = Service(
        r"C:\Users\Kenneth\Downloads\Compressed\geckodriver-v0.34.0-win64\geckodriver.exe"
    )

    driver_options = webdriver.FirefoxOptions()
    driver_options.add_argument("-profile")
    driver_options.set_preference("dom.webdriver.enabled", False)
    driver_options.add_argument(
        r"C:\Users\Kenneth\AppData\Roaming\Mozilla\Firefox\Profiles\ael5r3vy.second profile"
    )

    browser = webdriver.Firefox(service=service, options=driver_options)
    browser.get(url)
    return browser


def getTextByCssSelector(webDriver, selector: str):
    element = webDriver.find_element(By.CSS_SELECTOR, selector)
    elementText = element.text
    return elementText


def clickButton(webDriver, selector: str):
    wait = WebDriverWait(webDriver, 5)
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
    button.click()


def getElements(webDriver, locatorType: str, locator):
    elements = webDriver.find_elements(locatorType, locator)
    return elements


def getElement(webDriver, locatorType: str, locator):
    element = webDriver.find_element(locatorType, locator)
    return element
