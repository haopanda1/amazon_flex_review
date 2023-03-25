# -- Created By: haoj
# -- Create date: 2022-06-02
# -- Script Type: Boilerplate Code - Set up Chromedriver
# -- Report Location: xxx
# -- Documentation Link: N/A
# -- Reviewed By: N/A
# -- Last Modified By: haoj
# -- Last Modified date: 2022-08-10
# -- Last Modified Changed: add code comment


import os
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

class ChromeLauncher:
    '''
    purpose: return a fully initialized chrome driver. use local cache and avoid detection.
    '''
    def __init__(self, chrome_driver_dir: str, *, useragent_id: str = None, headless: bool = False):
        self._local_cache_dir = os.path.join(os.path.expanduser('~'),r'AppData\Local\Google\Chrome\User Data\Default\Cache\Cache_Data')
        self._chrome_driver_dir = chrome_driver_dir

        self._useragent_id = useragent_id
        self._headless = headless

    def start_chrome_driver(self) -> WebDriver:
        '''
        :purpose: set up service & options parameters for returned chrome driver,
                 this should be the only function user call

        :return: customized chrome driver
        '''
        service = self._chrome_service()
        options = self._chrome_option(useragent=self._useragent_id, headless_mode=self._headless)
        return Chrome(service=service, options=options)

    def _chrome_service(self):
        '''
        purpose: configure service options; use in self.start_chrome_driver()
        :return: selenium.webdriver.chrome.service
        '''
        chrome_service = Service(self._chrome_driver_dir)
        return chrome_service

    def _chrome_option(self, useragent: str = None, headless_mode: bool = False):
        '''
        purpose: customize chrome driver functionalities; set configurable options of an inited WebDriver
        :return: selenium.webdriver.chrome.options
        '''
        prefs = {'credentials_enable_service': False, 'profile.password_manager_enabled': False}
        chrome_option = Options()
        chrome_option.add_argument("--disable-infobars")
        chrome_option.add_argument("start-maximized")
        chrome_option.add_argument("--disable-extensions")
        chrome_option.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
        chrome_option.add_argument('--disable-gpu')
        chrome_option.add_argument('--ignore-certificate-errors')
        chrome_option.add_argument('--disable-extensions')
        chrome_option.add_argument('--no-sandbox')
        chrome_option.add_argument('--disable-dev-shm-usage')
        chrome_option.add_argument("--proxy-server=direct://")
        chrome_option.add_argument("--proxy-bypass-list=*")
        chrome_option.add_argument("--start-maximized")
        chrome_option.add_argument('--single-process')  # this is to reduce the ram consumption for chrome
        chrome_option.add_argument('--disable-blink-features=AutomationControlled')
        chrome_option.add_argument('disable-infobars')
        chrome_option.add_argument('--window-size=1920x1080')
        chrome_option.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_option.add_experimental_option('useAutomationExtension', False)
        chrome_option.add_experimental_option('prefs', prefs)
        if useragent != None:
            chrome_option.add_argument(f"user-agent={useragent}")
        if headless_mode:
            chrome_option.add_argument("--headless")

        return chrome_option



if __name__ == '__main__':
    # how to use
    chromedriver_dir = 'supporting_files/chromedriver.exe'
    app = ChromeLauncher(chromedriver_dir).start_chrome_driver()
    # Use can use the returned chrome driver instance to do anything they want, include get to url, click element, etc
    app.get('https://www.google.com')
