from .window import Console
from selenium import webdriver
from os import path, makedirs, umask,environ
from selenium.common.exceptions import WebDriverException
from pathlib import Path
# from .extension import disable_transition_extension
from .mixins import DatetimeMixin
from urllib.parse import urlparse
import sys
import json
import shutil
import hashlib
cur = path.dirname(__file__)
default_download_dir = "/tmp/chrome_download"
default_chromedriver_path = path.normpath(
    path.join(cur, "../bin/chromedriver"))

if not "KEEP_SESSION" in environ:
    default_user_dir = "/tmp/chrome_user_data"
else:
    ha = hashlib.md5(environ["EMAIL"].encode()).hexdigest()
    default_user_dir = path.join("/var/run/snc","yandex-%s" % ha)

class DriverWrapper(DatetimeMixin):
    def __init__(self, user_dir=default_user_dir, download_dir=default_download_dir, chromedriver_path=default_chromedriver_path):
        if not path.exists(download_dir):
            makedirs(download_dir)
        if not path.exists(user_dir):
            makedirs(user_dir)
        self.options = self.get_options(user_dir, download_dir)
        self.user_dir = user_dir
        if not "KEEP_SESSION" in environ:
            try:
                self.clear_cache()
            except:
                pass
        try:
            driver = webdriver.Chrome(
                chromedriver_path, chrome_options=self.options)
        except WebDriverException as e:
            sys.stderr.write( str(e))
            exit(1)
            # remove user dir,close all chrome controlled by webdriver
        except Exception as e:
            sys.stderr.write( str(e))
            exit(1)
        
        self.driver = driver
        self.driver.set_page_load_timeout(60)
        
        self.console = Console(self.driver)

    def clear_cache(self):
        shutil.rmtree(self.user_dir,ignore_errors=True)
        
    def get_options(self, user_dir, download_dir):

        driver_options = webdriver.ChromeOptions()
        driver_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36")
        if "CHROME" in environ:
            chrome_bin = environ.get('CHROME')
            driver_options.binary_location = chrome_bin
        driver_options.add_argument(
            "user-data-dir={0}".format(str(Path(user_dir))))
        driver_options.add_experimental_option("prefs", {
            "download.default_directory": str(Path(download_dir)),
            "download.directory_upgrade": True,
            "download.extensions_to_open": "",
            "download.prompt_for_download": 2,
            "intl.accept_languages": "en",
            "profile.content_settings.pattern_pairs.*.multiple-automatic-downloads": 1,
            "profile.default_content_settings.automatic": 1,
            "profile.default_content_settings.multiple-automatic-downloads": 1,
            "profile.default_content_setting_values.automatic_downloads": 1,
            "profile.default_content_setting_values.notifications":1 # allow notification by default
        })

        driver_options.add_argument("--lang=en")
        # Works on mine mac High Sierra 10.13.5 (17F77) without docker
        # Chrome Version 68.0.3440.106 (Official Build) (64-bit)
        # driver_options.add_argument("--homepage='%s'" % HOMEPAGE) 
        
        # browser wait for response but failure
        # driver_options.add_argument("--google-base-url=%s" % HOMEPAGE) 

        # current url:chrome-search://local-ntp/local-ntp.html
        # without this will be:https://www.google.com/_/chrome/newtab?ie=UTF-8
        driver_options.add_argument("--google-base-url=%s" % "about:blank") 

        ss = path.normpath(path.join(cur, "../shadowsocks.json"))
    

        if path.exists(ss):
            with open(ss,"r") as f:
                data = json.load(f)
                driver_options.add_argument("--proxy-server=socks5://127.0.0.1:%d" % data["local_port"]) 
                driver_options.add_argument("--host-resolver-rules=MAP * 0.0.0.0 , EXCLUDE 127.0.0.1")
        elif "HTTPS_PROXY" in environ:
            driver_options.add_argument('--ignore-certificate-errors')
            driver_options.add_argument("--proxy-server=%s" % environ["HTTPS_PROXY"]) 
            if  environ["HTTPS_PROXY"].find("socks5://") != -1:
                parsed = urlparse(environ["HTTPS_PROXY"])
                driver_options.add_argument("--host-resolver-rules=MAP * ~NOTFOUND , EXCLUDE %s" % parsed.hostname )

        if "DN" in environ:
            driver_options.add_argument("--disable-notifications")
        driver_options.add_argument("--mute-audio")
        driver_options.add_argument("--no-sandbox")
        # driver_options.add_argument("--disable-notifications")
        driver_options.add_argument("--silent")
        # driver_options.add_argument("--disable-dev-shm-usage")
        # driver_options.add_argument("--remote-debugging-port=19222")
        driver_options.add_argument("--no-first-run")
        # driver_options.add_argument("--start-maximized")
        # driver_options.add_argument("--force-device-scale-factor=2")
        driver_options.add_argument("disable-infobars")
        if "HEADLESS" in environ:
            driver_options.add_argument('--headless')
            driver_options.add_argument("--disable-extensions")
        driver_options.add_argument('--cap-add=SYS_ADMIN')
        # driver_options.add_argument("--disable-extensions")
        # driver_options.add_argument("--disable-gpu")
        driver_options.add_argument("--enable-logging=stderr")
 
        
        # driver_options.add_experimental_option("useAutomationExtension", False)

        return driver_options

    # def __del__(self):
    #     self.db.close()
