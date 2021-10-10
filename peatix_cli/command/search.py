import re
from datetime import datetime

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from rich.console import Console
from rich.table import Table

from peatix_cli.command.root import RootCmd, logger


class SearchCmd(RootCmd):

    def _next_page(self):

        url = f'https://peatix.com/search?country=JP&p=1&size=10&v=3.4&tag_ids={"" if self.args.tag_id is None else self.args.tag_id}&online=1&dr={self.args.period}'
        target_selector = '#results-table > div.event-search-results.col-main > ul > li'
        next_selector = '#app > div > ul > li.next'

        logger.info(f'fetching url: {url}')

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

        logger.info(
            f"start fetcing results until {self.args.max_page} pages at max...")

        for i, els in enumerate(self._next_page()):

            logger.info(f"fetcing page {i+1}...")

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
                logger.info("reached max page.")
                break

        logger.info("finish fetcing results")

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
