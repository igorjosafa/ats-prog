# -*- coding: utf-8 -*-

import os
import os.path
import tempfile
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from .exceptions import MrhException

class Browser:
 
    IMPLICITLY_WAIT = 3
 
    def __init__(self, chrome_options=None, remote=None, download_dir=''):
        """
        If download_dir is None, no downloads will occur.
        If download_dir is '', a temporary directory will be created.
        """

        if download_dir == '':
            download_dir = tempfile.mkdtemp()
        
        self.download_dir = download_dir

        if chrome_options is None:
            chrome_options = Options()
        
        profile = {
            "plugins.plugins_list": [
                {"enabled": False, "name": "Chrome PDF Viewer"},
            ],
            "download.extensions_to_open": "applications/pdf",
            "download.directory_upgrade": True,
            "download.prompt_for_download": False,
            "plugins.always_open_pdf_externally": True,
        }
        if download_dir is not None:
            profile["download.default_directory"] = download_dir
        chrome_options.add_experimental_option("prefs", profile)

        if remote:
            self.driver = webdriver.Remote(
                command_executor=remote,
                desired_capabilities=DesiredCapabilities.CHROME,
                options=chrome_options
            )
        else:
            self.driver = webdriver.Chrome(options=chrome_options)
        
        self.driver.implicitly_wait(self.IMPLICITLY_WAIT)
 
    def fill(self, name:str, value:str|None, tab=False, enter=False, ignore_if_none=False):
        """Clears the element and sends keys to set its value. If value is None and 
        ignore_if_none is True, does nothing.

        """
        if value is None and ignore_if_none:
            return
        el = self.driver.find_element(By.NAME, name)
        el.clear()
        if value:
            el.send_keys(value)
        if tab:
            el.send_keys(Keys.TAB)
        if enter:
            el.send_keys(Keys.ENTER)
 
    def double_click(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        actionChains = ActionChains(self.driver)
        actionChains.double_click(element).perform()
 
    def check(self, name, value:bool, by_id=False):
        if by_id:
            el = self.driver.find_element(By.ID, name)
        else:
            el = self.driver.find_element(By.NAME, name)
        if ((el.get_attribute('checked') or 'false').lower() == 'true') != value:
            self.driver.execute_script("arguments[0].click();", el)  # el.click()
    
    def select_radio(self, name, value):
        if value is None:
            return
        el = self.driver.find_element(By.CSS_SELECTOR, 
            "input[type='radio'][name='{}'][value='{}']".format(name, str(value))
        )
        el.click()

    def select(self, name:str, value:str, ignore_if_none=True, by_text=False):
        """Selects OPTION value in SELECT identified by name.
        If ignore_if_none is True, do nothing if value is None.
        If by_text is True, value should be option's text instead of value.

        """
        if value is None and ignore_if_none:
            return

        select = Select(self.driver.find_element(By.NAME, name))
        if by_text:
            select.select_by_visible_text(value)
        else:
            select.select_by_value(value)
 
    def close(self):
        self.driver.quit()

    def save_file(self, fname, timeout=60*2, watch_file='file.pdf'):
        rfile = os.path.join(self.download_dir, watch_file)
        t = 0
        while t <= timeout:
            if os.path.exists(rfile):
                time.sleep(1)
                dest_file = os.path.join(self.download_dir, fname)
                os.rename(rfile, dest_file)
                return
            time.sleep(1)
            t += 1
        raise MrhException("Timeout waiting for file: {}.".format(rfile))

    def save_text(self, text, fname):
        with open(os.path.join(self.download_dir, fname), 'wt') as f:
            f.write(text)

    def raise_if_alert(self, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present(),
                'Alert significa erro!')
            alert = self.driver.switch_to.alert
            emsg = alert.text
            alert.dismiss()
            raise MrhException(emsg)
        except TimeoutException:
            pass

    def handle_alert(self, timeout=60*2):
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present(),
                'Alert missing!')
            alert = self.driver.switch_to.alert
            msg = alert.text
            alert.dismiss()
            return msg
        except TimeoutException:
            raise MrhException("Timeout")
        
    def click(self, element):
        self.driver.execute_script("arguments[0].click();", element)
