from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .driver_wrapper import DriverWrapper
from .exceptions import NoSuchElementException, StaleElementReferenceException,TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from typing import List
import re

class BasePage:
    Homepage = None
    WaitToEntryTimeout = 10

    def __init__(self, driver_wrapper: DriverWrapper):
        self.driver_wrapper = driver_wrapper
        self.webdriver = driver_wrapper.driver

    def go(self):
        self.webdriver.get(self.Homepage)
        return self

    def wait_to_entry(self):
        wait = WebDriverWait(self.webdriver, self.WaitToEntryTimeout)
        wait.until(self)

    def wait_until(self, func, timeout):
        wait = WebDriverWait(self.webdriver, timeout)
        wait.until(func)
    
    def move_to_and_click(self,ele):
        a = ActionChains(self.webdriver)
        a.move_to_element(ele).click().perform()

    def locate(self,ele):
        ele.location_once_scrolled_into_view

