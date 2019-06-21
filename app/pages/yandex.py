
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from ..driver_wrapper import DriverWrapper
from ..exceptions import TimeoutException
import shutil
import base64
import time
from ..page import BasePage
import os
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import traceback
from selenium.common.exceptions import StaleElementReferenceException
import sys
# from ..mail_helper import get_yandex_verification_code
from ..phone_helper import get_code
import tempfile
import requests

user_dir = "/var/run/snc"

class Yandex(BasePage):

    Homepage = "https://www.yandex.com"
    WaitToEntryTimeout = 60

    def __init__(self, driver_wrapper: DriverWrapper):
        super().__init__(driver_wrapper)

    def __str__(self):
        return Yandex.Homepage

    def stop(self):
        if not "KEEP_SESSION" in os.environ:
            self.driver_wrapper.clear_cache()

    def go(self):
        self.webdriver.get(self.Homepage)
        return self

    def reg(self,first_name,last_name):
        # envs: PHONE PASS
        first_name = base64.b64decode(first_name.encode()).decode()
        last_name = base64.b64decode(last_name.encode()).decode()
        
        self.go()
        email_sel = "div.tabs__mail"
        func = EC.visibility_of_element_located( (By.CSS_SELECTOR,email_sel))
        self.wait_until(func,5)
        email_btn = self.webdriver.find_element_by_css_selector(email_sel)
        email_btn.click()


        create_sel = '//span[text()="%s"]/..' % "Create an account"
        func = EC.visibility_of_element_located( (By.XPATH,create_sel))
        self.wait_until(func,5)
        create_btn = self.webdriver.find_element_by_xpath(create_sel)
        create_btn.click()

        # reg_sel = "a.passp-auth-header-link_visible"
        # func = EC.visibility_of_element_located( (By.CSS_SELECTOR,reg_sel))
        # self.wait_until(func,5)
        # email_btn = self.webdriver.find_element_by_css_selector(reg_sel)
        # email_btn.click()

        first_name_sel = 'input[name="firstname"]'

        func = EC.visibility_of_element_located( (By.CSS_SELECTOR,first_name_sel))
        self.wait_until(func,5)
        name_ipt = self.webdriver.find_element_by_css_selector(first_name_sel)
        name_ipt.send_keys( first_name )

        last_name_sel = 'input[name="lastname"]'

        func = EC.element_to_be_clickable( (By.CSS_SELECTOR,last_name_sel))
        self.wait_until(func,5)
        name_ipt = self.webdriver.find_element_by_css_selector(last_name_sel)

        name_ipt.send_keys( last_name )

        login_name_sel = 'input[name="login"]'

        func = EC.element_to_be_clickable( (By.CSS_SELECTOR,login_name_sel))
        self.wait_until(func,5)
        login_name_ipt = self.webdriver.find_element_by_css_selector(login_name_sel)

        action = ActionChains(self.webdriver)
        action.move_to_element(login_name_ipt).click().perform()
        # login_name_ipt.click()

        name1_sel = 'div.reg-field__popup li:first-child' # li.registration__pseudo-link
        func = EC.visibility_of_element_located( (By.CSS_SELECTOR,name1_sel))
        self.wait_until(func,10)
        name1_btn = self.webdriver.find_element_by_css_selector(name1_sel)
        sys.stdout.write(name1_btn.text + "@yandex.com")
        name1_btn.click()
        

        password_sel = 'input[name="password"]'

        func = EC.visibility_of_element_located( (By.CSS_SELECTOR,password_sel))
        self.wait_until(func,5)
        password_ipt = self.webdriver.find_element_by_css_selector(password_sel)
        password_ipt.send_keys( os.environ["PASS"] )

        password_confirm_sel = 'input[name="password_confirm"]'

        func = EC.visibility_of_element_located( (By.CSS_SELECTOR,password_confirm_sel))
        self.wait_until(func,5)
        password_confirm_ipt = self.webdriver.find_element_by_css_selector(password_confirm_sel)
        password_confirm_ipt.send_keys( os.environ["PASS"] )

        phone_sel = 'input[name="phone"]' # phone

        func = EC.visibility_of_element_located( (By.CSS_SELECTOR,phone_sel))
        self.wait_until(func,5)
        phone_ipt = self.webdriver.find_element_by_css_selector(phone_sel)
        phone_ipt.send_keys( os.environ["PHONE"] )

        send_code_sel = '//span[text()="%s"]' % "Send code"
        func = EC.visibility_of_element_located( (By.XPATH,send_code_sel))
        self.wait_until(func,5)
        send_code_btn = self.webdriver.find_element_by_xpath(send_code_sel)
        # send_code_btn.click()
        action.move_to_element(send_code_btn).click().perform()

        code = None
        tmp = 0
        limit = 60 * 3
        while code == None:
            if tmp == limit:
                raise Exception('timeout for getting phone pin code')
            try:
                code = get_code(os.environ["PHONE"])
            except:
                pass
            tmp += 1
            time.sleep(1)
        # <input data-lego="react" id="phoneCode" type="tel" name="phoneCode" class="textinput__control" value="">
        code_ipt_sel = 'input[name="phoneCode"]' # phone

        func = EC.visibility_of_element_located( (By.CSS_SELECTOR,code_ipt_sel))
        self.wait_until(func,5)
        code_ipt = self.webdriver.find_element_by_css_selector(code_ipt_sel)
        code_ipt.send_keys( code )

        # <span>Your phone number successfully confirmed</span>
        code_ok_sel = '//span[text()="%s"]' % "Your phone number successfully confirmed"
        func = EC.visibility_of_element_located( (By.XPATH,code_ok_sel))
        self.wait_until(func,5)
        time.sleep(5)
        # sub_sel = 'button[type="submit"]'
        # sub_sel =  '//button/span[text()="%s"]/..' % "Register"

        # func = EC.element_to_be_clickable( (By.XPATH,sub_sel))
        # self.wait_until(func,10)
        # sub_btn = self.webdriver.find_element_by_xpath(sub_sel)
        # # current_url = self.webdriver.current_url
        # # sub_btn.click()
        # action.move_to_element(sub_btn).click().perform()
        self.webdriver.execute_script("document.querySelector('button[type=submit]').click()")

        # <span data-lego="react" class="button2__text">Accept</span>
        accept_sel = '//span[text()="%s"]' % "Accept"

        func = EC.visibility_of_element_located( (By.XPATH,accept_sel))
        self.wait_until(func,5)
        accept_btn = self.webdriver.find_element_by_xpath(accept_sel)
        current_url = self.webdriver.current_url
        # accept_btn.click()
        self.webdriver.execute_script( "document.querySelector('div.eula-popup button').click()" )
        # action.move_to_element(accept_btn).click().perform()

        wait = WebDriverWait(self.webdriver, 10)
        wait.until(lambda driver:  driver.current_url != current_url)
       
