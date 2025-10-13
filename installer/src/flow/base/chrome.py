from .logger import SimpleLogger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

class ChromeManager:
    def __init__(self):
        self.logger = SimpleLogger(__name__).get_logger()

    def chrome_options(self):
        opts = Options()
        opts.add_argument(f"--window-size=1280,900")
        return opts
    
    def start_chrome(self):
        service = Service()
        opts = self.chrome_options()
        self.logger.info(f"Chrome起動開始")
        chrome = webdriver.Chrome(service=service, options=opts)
        self.logger.info(f"Chrome起動できました")
        return chrome
    
