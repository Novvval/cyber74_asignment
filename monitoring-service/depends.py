from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

from service import ScraperService
from config import Config


def get_driver() -> tuple[uc.Chrome, Display]:
    display = Display(visible=False, size=(1080, 1920))
    display.start()
    options = Options()
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-default-browser-check')
    options.add_argument('--no-first-run')
    options.add_argument('--no-proxy-server')
    options.add_argument('--no-service-autorun')
    options.add_argument('--password-store=basic')
    options.add_argument(f'user-agent={Config.USER_AGENT}')
    options.binary_location = Config.BROWSER_BIN
    driver = uc.Chrome(headless=False, use_subprocess=False, options=options)
    return driver, display


def get_service() -> ScraperService:
    return ScraperService(get_driver)
