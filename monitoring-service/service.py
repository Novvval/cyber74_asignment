from collections.abc import Callable
import contextlib
import re
import time

from pyvirtualdisplay import Display
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from undetected_chromedriver import Chrome, WebElement

RE_FLOAT = re.compile(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?')
RE_DIGIT = re.compile(r'\d')


class ScraperService:
    def __init__(self, driver):
        self._driver: Callable = driver
        self._display: Display | None = None
        self.driver: Chrome | None = None

    @contextlib.contextmanager
    def driver_context(self):
        driver, display = self._driver()
        self._display = display
        self.driver = driver
        try:
            yield
        finally:
            self.driver.close()
            self.driver.quit()
            self._display.stop()
            self._display = None
            self.driver = None

    def find_product(self, link: str) -> dict | None:
        self.driver.get(link)
        cookies = self.driver.get_cookies()
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.get(link)
        time.sleep(3)
        self.driver.execute_script('window.scrollTo(0, 3000)')

        description = self.try_to_find('//mvid-seo-text-pdp')
        title = self.try_to_find('//div[contains(@class, "title-brand flex ng-star-inserted")]')
        price = self.try_to_find('//span[contains(@class, "price__main-value")]')
        rating = self.try_to_find('//mvid-reviews-rating')

        if price is not None and title is not None:
            return self.convert(link, price.text, title.text, rating, description)
        return None

    def try_to_find(self, xpath: str) -> WebElement | None:
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return element
        except Exception:
            return None

    @staticmethod
    def convert(*args) -> dict:
        link, price, title, rating, description = args

        link = link.split('//')[1]

        price = int(''.join(RE_DIGIT.findall(price)))

        if rating is not None:
            rating = float(''.join(RE_FLOAT.findall(rating.text)))

        if description is not None:
            description = description.text.split('\n')
            if description[-1] in ('Читать полностью', 'Скрыть'):
                description.pop()
            if description[0] == 'О товаре':
                description = description[1:]
            description = '\n'.join(description)

        return {
            'link': link,
            'title': title,
            'description': description,
            'rating': rating,
            'value': price
        }
