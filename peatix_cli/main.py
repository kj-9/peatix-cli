import sys
import re
import logging
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from rich.console import Console
from rich.table import Table
from rich.logging import RichHandler

sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

log = logging.getLogger("rich")


class Main():

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
            log.info("stopped chromedriver")

    def _els_generator(self):

        url = f'https://peatix.com/search?country=JP&l.text=%E3%81%99%E3%81%B9%E3%81%A6%E3%81%AE%E5%A0%B4%E6%89%80&p=1&size=10&v=3.4&tag_ids=2796&online=1&dr={self.args.filter}'
        target_selector = '#results-table > div.event-search-results.col-main > ul > li'
        next_selector = '#app > div > ul > li.next'

        self.driver.get(url)

        while True:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, target_selector))
            )

            els = self.driver.find_elements_by_css_selector(
                target_selector)

            yield els

            next_el = self.driver.find_element_by_css_selector(
                next_selector)

            if next_el.is_displayed():
                next_el.click()
            else:
                break

    def run(self):

        class_names = [
            'month', 'day', 'datetime', 'event-thumb_name', 'event-thumb_organizer'
        ]

        out = []

        log.info(
            f"start fetcing results until {self.args.max_page} pages at max...")

        for i, els in enumerate(self._els_generator()):

            log.info(f"fetcing page {i+1}...")

            for el in els:

                texts = {k: el.find_element_by_class_name(
                    k).text for k in class_names}

                date = f"{re.sub('月', '', texts.get('month'))}/{texts.get('day')}"
                doy, time = texts.get('datetime').split(" ")[:2]

                href = el.find_element_by_class_name(
                    "event-thumb_link").get_attribute("href")
                # this part of href is enough to access event pages
                link = re.sub('\?utm.+$', '', href)

                out.append([
                    date,
                    doy[0],
                    time,
                    texts.get('event-thumb_name'),
                    texts.get('event-thumb_organizer').removeprefix("主催: "),
                    link if self.args.show_link else f"[link={link}]->[/link]"
                ])

            if (i+1) == self.args.max_page:
                log.info("reached max page.")
                break

        log.info("finish fetcing results")

        table = Table(title="Peatix Search Result")

        table.add_column("Date", justify="center")
        table.add_column("DOW", justify="center")
        table.add_column("Time", justify="right")
        table.add_column("Name", overflow="fold")
        table.add_column("Organizer")

        if self.args.show_link:
            table.add_column("Link", justify="left", overflow="fold")
        else:
            table.add_column("Link", justify="center")

        out = sorted(out, key=lambda i_out: datetime.strptime(
            i_out[0] + ' ' + i_out[2], '%m/%d %H:%M'))

        for i_out in out:
            table.add_row(*i_out)

        console = Console()
        console.print(table)
