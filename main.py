import time
import datetime as dt

from selenium.webdriver import Remote, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as ec

from calc_fibonachi import fib_number
from csv_output import write_to_csv


# Variables
DEFAULT_TIME_WAIT = 5
WALLET = fib_number
OUTPUT_METHOD = write_to_csv


# Mixins
class WaitElementMixin:
    def wait_element(self, timer=DEFAULT_TIME_WAIT, method=By.XPATH, value=None):
        return WebDriverWait(self.driver, timer).until(ec.presence_of_element_located((method, value)))


# Page Objects
class MainPage(WaitElementMixin):
    def __init__(self, driver):
        self.driver = driver

    def start(self):
        self.driver.get('https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login')
        if self.driver.title == 'XYZ Bank':
            print('Connection complete!')

        button_login = self.wait_element(value='//button[@ng-click="customer()"]')
        button_login.click()

        assert "No results found." not in self.driver.page_source


class LoginPage(WaitElementMixin):
    def __init__(self, driver):
        self.driver = driver

    def login(self, username):
        username_field = self.wait_element(timer=1, value='//select[@name="userSelect"]')
        select_username = Select(username_field)
        select_username.select_by_visible_text(username)

        button_submit = self.wait_element(timer=1, value='//button[@type="submit"]')
        button_submit.click()


class ActionPage(WaitElementMixin):
    def __init__(self, driver):
        self.driver = driver

    def procedure_input_submit(self, amount):  # DRY Principle
        # input cash
        amount_field = self.wait_element(timer=1, value='//input[@ng-model="amount"]')
        amount_field.send_keys(amount)

        # click submit
        button_deposit = self.driver.find_element(by=By.XPATH, value='//button[@type="submit"]')
        button_deposit.click()

    def deposit(self):
        select_deposit = self.wait_element(timer=1, value='//button[@ng-click="deposit()"]')
        select_deposit.click()
        self.procedure_input_submit(WALLET)

    def withdrawal(self):
        select_withdrawal = self.driver.find_element(by=By.XPATH, value='//button[@ng-click="withdrawl()"]')
        select_withdrawal.click()
        time.sleep(1)  # Necessary for correct switching field/button
        self.procedure_input_submit(WALLET)

    def check_balance(self):
        balance = self.driver.find_element(by=By.XPATH, value='//strong[2][@class="ng-binding"]')
        message = 'Balance is empty.' if balance.text == '0' else 'ERROR!'
        print(message)

    def get_transactions(self):
        transaction_button = self.driver.find_element(by=By.XPATH, value='//button[@ng-click="transactions()"]')
        transaction_button.click()

        time.sleep(1)  # Necessary for correct download table
        self.driver.refresh()


class TransactionsPage(WaitElementMixin):
    def __init__(self, driver):
        self.driver = driver

    def transactions(self):
        data = []
        table = self.wait_element(method=By.TAG_NAME, timer=2, value='tbody')
        rows = table.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            current_row = {}
            cells = row.find_elements(By.TAG_NAME, "td")

            raw_date = dt.datetime.strptime(cells[0].text, '%B %d, %Y %I:%M:%S %p')
            # May 7, 2024 8:34:43 PM __to__ "ДД Месяц ГГГГ ЧЧ:ММ:СС"
            current_row['Дата-времяТранзакции'] = raw_date.strftime('%d %B %Y %H:%M:%S')
            current_row['Сумма'] = int(cells[1].text)
            current_row['ТипТранзакции'] = cells[2].text

            data.append(current_row)

        print(data)
        OUTPUT_METHOD(data)


if __name__ == '__main__':
    used_driver = Remote(
        command_executor="http://localhost:4444/wd/hub",
        options=FirefoxOptions()
    )

    main_page = MainPage(used_driver)
    main_page.start()

    login_page = LoginPage(used_driver)
    login_page.login('Harry Potter')

    action_page = ActionPage(used_driver)
    action_page.deposit()
    action_page.withdrawal()
    action_page.check_balance()
    action_page.get_transactions()

    transactions_page = TransactionsPage(used_driver)
    transactions_page.transactions()

    used_driver.quit()
