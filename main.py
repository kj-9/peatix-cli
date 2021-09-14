import sys
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

    def __init__(self):

        chromedriver_path = 'C:/Users/kh03/Desktop/chromedriver_win32/chromedriver.exe'
        chromedriver = Path(chromedriver_path)

        op = Options()

        op.add_argument("--disable-gpu")
        op.add_argument("--disable-extensions")
        op.add_argument("--proxy-server='direct://'")
        op.add_argument("--proxy-bypass-list=*")
        op.add_argument("--start-maximized")
        op.add_argument("--headless")
        op.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')

        self.driver = webdriver.Chrome(chromedriver.resolve(),
                                       options=op)

    def _els_generator(self):

        url = 'https://peatix.com/search?country=JP&l.text=%E3%81%99%E3%81%B9%E3%81%A6%E3%81%AE%E5%A0%B4%E6%89%80&p=2&size=10&v=3.4&tag_ids=2796&online=1&dr=today'
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

        log.info("start fetcing results...")

        for i, els in enumerate(self._els_generator()):

            log.info(f"fetcing page {i+1}...")

            for el in els:

                texts = {k: el.find_element_by_class_name(
                    k).text for k in class_names}

                doy, time = texts.get('datetime').split(" ")[:2]

                date = f"{texts.get('month').removesuffix('月')}/{texts.get('day')}"

                href = el.find_element_by_class_name(
                    "event-thumb_link").get_attribute("href")

                out.append([
                    date,
                    doy[0],
                    time,
                    texts.get('event-thumb_name'),
                    texts.get('event-thumb_organizer').removeprefix("主催: "),
                    f"[link={href}]->[/link]"
                ])
            break

        log.info("finish fetcing results")
        self.driver.quit()

        log.info("stopped driver")

        table = Table(title="Peatix Search Result")

        table.add_column("Date", justify="center")
        table.add_column("DOW", justify="center")
        table.add_column("Time", justify="right")
        table.add_column("Name", overflow="fold")
        table.add_column("Organizer")
        table.add_column("Link", justify="center")

        out = sorted(out, key=lambda i_out: datetime.strptime(
            i_out[0] + i_out[2], '%m/%d%H:%M'))

        for i_out in out:
            table.add_row(*i_out)

        console = Console()
        console.print(table)


if __name__ == "__main__":
    Main().run()
