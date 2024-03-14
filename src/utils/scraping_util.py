from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def browserDriver(url:str):
    browser = webdriver.Firefox()
    browser.get(url)
    return browser;

def getTextByCssSelector(webDriver,selector:str):
    element = webDriver.find_element(By.CSS_SELECTOR,selector)
    elementText = element.text
    return elementText;

def clickButton(webDriver,selector:str):
        wait = WebDriverWait(webDriver, 5) 
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        button.click();

def getElements(webDriver,locatorType:str,locator):
    elements = webDriver.find_elements(locatorType, locator)
    return elements;




    
