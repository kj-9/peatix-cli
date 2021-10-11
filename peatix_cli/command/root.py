import sys
import logging
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from rich.logging import RichHandler

sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger("rich")


class ChromeDriverCmd():

    def __init__(self, args):

        self.args = args

        options = Options()

        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument("--headless")
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option(
            'prefs', {'intl.accept_languages': 'ja'})

        logger.info("starting chromedriver")
        if self.args.chromedriver:
            self.driver = webdriver.Chrome(
                Path(self.args.chromedriver).resolve(),
                options=options,
                chrome_options=chrome_options)
        else:
            self.driver = webdriver.Chrome(
                options=options,
                chrome_options=chrome_options)

    def __del__(self):

        if hasattr(self, "driver"):
            self.driver.quit()
            logger.info("stopped chromedriver")
