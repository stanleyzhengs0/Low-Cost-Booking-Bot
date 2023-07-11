from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import booking.constants as const
import os
from selenium import webdriver
from booking.booking_filtration import BookingFiltration


# options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)
# driver = webdriver.Chrome(options=options)


class Booking(webdriver.Chrome):

    # acts as ta constructor in java
    # def __init__(self, teardown=False):
    #     self.driver = driver
    #     self.teardown = teardown
    #     self.driver.implicitly_wait(15)
    #     self.driver.maximize_window()
    #     super().__init__()

    def __init__(self,
                 driver_path=r"C:\SeleniumDrivers"):
        self.driver_path = driver_path
        os.environ['PATH'] += self.driver_path

        options = Options()
        options.add_argument('--incognito')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("detach", True)
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(10)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # if self.teardown:
        self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def clear_popup(self):
        pop_up = self.find_element(By.XPATH,
                                   "//button[@class='fc63351294 a822bdf511 e3c025e003 fa565176a8 f7db01295e c334e6f658 ae1678b153']")
        pop_up.click()

    def change_currency(self, currency=None):
        currency_element = self.find_element(By.XPATH, "//span[@class='e57ffa4eb5']")
        currency_element.click()

        selected_currency_element = self.find_element(By.XPATH, "//span[contains(text(),'U.S. Dollar')]")
        selected_currency_element.click()

    def select_place_to_go(self, place_to_go):
        search_field = self.find_element(By.NAME, 'ss')
        search_field.clear()
        search_field.send_keys(place_to_go)

        first_result = self.find_element(By.XPATH, "//div[contains(text(),'Tokyo')]")
        first_result.click()

    def select_dates(self, check_in_date, check_out_date):
        check_in_element = self.find_element(By.CSS_SELECTOR, f'span[data-date="{check_in_date}"]')
        check_in_element.click()

        check_out_element = self.find_element(By.CSS_SELECTOR, f'span[data-date="{check_out_date}"]')
        check_out_element.click()

    def select_adults(self, count=1):
        select_occupancy = self.find_element(By.XPATH, "//button[@data-testid='occupancy-config']")
        select_occupancy.click()

        # saftey locgic (for selecting occupancy number), set the number of adults to 1, getting rid of the default number provided by the website
        while True:
            decrease_adult_element = self.find_element(By.XPATH,
                                                       "//button[@class='fc63351294 a822bdf511 e3c025e003 fa565176a8 f7db01295e c334e6f658 e1b7cfea84 cd7aa7c891']")
            decrease_adult_element.click()

            adult_value_element = self.find_element(By.XPATH, "//input[@id='group_adults']")
            adult_value = adult_value_element.get_attribute('aria-valuenow')

            if int(adult_value) == 1:
                break

        # from the reset, given a number of adults as a param, we increment the loop and click increase button accordingly
        increase_button_element = self.find_element(By.XPATH,
                                                    "//button[@class='fc63351294 a822bdf511 e3c025e003 fa565176a8 f7db01295e c334e6f658 e1b7cfea84 d64a4ea64d']")
        for _ in range(count - 1):
            increase_button_element.click()

    def click_search(self):
        search_button = self.find_element(By.CSS_SELECTOR, 'button[type = "submit"]')
        search_button.click()

    def apply_filtration(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(3, 4, 5)
        filtration.sort_price_lowest_first()


