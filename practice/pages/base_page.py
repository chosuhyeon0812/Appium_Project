# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver, timeout=10):
        self.d = driver
        self.wait = WebDriverWait(driver, timeout)

    def find(self, by, locator):
        return self.d.find_element(by, locator)

    def finds(self, by, locator):
        return self.d.find_elements(by, locator)

    def click_when_clickable(self, by, locator):
        el = self.wait.until(EC.element_to_be_clickable((by, locator)))
        el.click()
        return el
