from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class Main():

    url = 'https://peatix.com/search?country=JP&l.text=%E3%81%99%E3%81%B9%E3%81%A6%E3%81%AE%E5%A0%B4%E6%89%80&p=2&size=10&v=3.4&tag_ids=2796&online=1&dr=today'
    chromedriver_path = 'C:/Users/kh03/Desktop/chromedriver_win32/chromedriver.exe'
    target_selector = '#results-table > div.event-search-results.col-main > ul > li'
    next_selector = '#app > div > ul > li.next'
    chromedriver = Path(chromedriver_path)

    def __init__(self):

        self.driver = webdriver.Chrome(self.chromedriver.resolve(),
                                       options=self._set_option())

    def _set_option(self):
        op = Options()

        op.add_argument("--disable-gpu")
        op.add_argument("--disable-extensions")
        op.add_argument("--proxy-server='direct://'")
        op.add_argument("--proxy-bypass-list=*")
        op.add_argument("--start-maximized")
        op.add_argument("--headless")
        op.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')
        return op

    def _page_generator(self):
        while True:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self.target_selector))
            )

            els = self.driver.find_elements_by_css_selector(
                self.target_selector)

            yield els

            next_el = self.driver.find_element_by_css_selector(
                self.next_selector)

            if next_el.is_displayed():
                next_el.click()
            else:
                break

    def run(self):

        self.driver.get(self.url)

        class_names = [
            'month', 'day', 'datetime', 'event-thumb_name', 'event-thumb_organizer'
        ]

        for els in self._page_generator():
            for el in els:

                texts = {k: el.find_element_by_class_name(
                    k).text for k in class_names}

                doy, time = texts.get('datetime').split(" ")[:2]

                date = f"{texts.get('month')}{texts.get('day')}日({doy[0]}){time}"

                print(*[
                    date,
                    texts.get('event-thumb_name'),
                    texts.get('event-thumb_organizer').removeprefix("主催: "),
                ], sep='\t', end='\n'
                )

        self.driver.quit()


if __name__ == "__main__":
    Main().run()
