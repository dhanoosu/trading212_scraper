from selenium import webdriver
from selenium.common.exceptions     import TimeoutException
from selenium.webdriver.common.by   import By
from selenium.webdriver.support.ui  import WebDriverWait
from selenium.common.exceptions     import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from msedge.selenium_tools import Edge, EdgeOptions

from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor, as_completed

import sys, time
from datetime import date

from .utils import *
from .html_attr import Xpaths, ClassNames

class Stock (object):

    def __init__(self, ticker, name, date_created, quantity, market_value, return_percent, image):
        self.ticker         = ticker
        self.name           = name
        self.date_created   = date_created
        self.quantity       = quantity
        self.market_value   = market_value
        self.return_percent = return_percent
        self.image          = image

class AccountSummary(object):

    def __init__(self,
        total_return,
        total_div,
        deposits,
        withdrawals,
        live_result,
        free_fund,
        portfolio,
        acc_value,
        invested,
        percent_ret,
        today_date
    ):
        self.total_return = total_return
        self.total_div = total_div
        self.deposits = deposits
        self.withdrawals = withdrawals

        self.live_result = live_result
        self.free_fund = free_fund
        self.portfolio = portfolio
        self.acc_value = acc_value

        self.invested = invested
        self.percent_ret = percent_ret

        self.today_date = today_date

class Scrape():

    def __init__(self, username, password, headless, account_types=[]):

        self.options = EdgeOptions()
        self.options.use_chromium = True
        self.options.headless = headless
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.username = username
        self.password = password

        self.has_login = False
        self.has_setup = False
        self.driver = None

    def setup(self):
        self.driver = Edge(options=self.options)
        self.load_mainpage()

        wait = WebDriverWait(self.driver, 1)

        if not self.has_login:
            self.login()

        self.has_setup = True


    def scape(self, account):


        print("Starting scaping..")

        if not self.has_setup:
            self.setup()

        wait_for_element_clickable(self.driver, By.CLASS_NAME, ClassNames.ACCOUNT_MENU_HEADER)

        try:
            self.driver.find_element_by_xpath(Xpaths.SPLASH_SCREEN_X_BUTTON).click()
        except Exception as e:
            pass

        print("Switching account of {}".format(account))
        self.switch_account(acc=account)

        wait_for_element_clickable(self.driver, By.CLASS_NAME, "status-bar")

        while(1):
            try:
                live_result = self.driver.find_element_by_xpath(Xpaths.LIVE_RESULT).text
                free_fund   = self.driver.find_element_by_xpath(Xpaths.FREE_FUND).text
                portfolio   = self.driver.find_element_by_xpath(Xpaths.PORTFOLIO).text
                acc_value   = self.driver.find_element_by_class_name(ClassNames.ACCOUNT_VALUE).text

                self.live_val        = float(live_result.split('\n')[1].replace(u'\xa3', '').replace(',', ''))
                self.free_fund_val   = float(free_fund.split('\n')[1].replace(u'\xa3', '').replace(',', ''))
                self.portfolio_val   = float(portfolio.split('\n')[1].replace(u'\xa3', '').replace(',', ''))
                self.acc_value_val   = float(acc_value.split('\n')[1].replace(u'\xa3', '').replace(',', ''))

                self.invested = (self.portfolio_val - self.live_val)
                self.percent_ret = (self.live_val/self.invested) * 100

                self.today = date.today()
                self.date_frmt = self.today.strftime("%d/%m/%Y")

                break
            except Exception as e:
                pass


        print("Clicking account button")
        self.driver.find_element_by_class_name(ClassNames.ACCOUNT_MENU_HEADER).click()
        time.sleep(3)
        print("Clicking history")
        self.driver.find_element_by_xpath(Xpaths.HISTORY_BUTTON).click()

        wait_for_element_clickable(self.driver, By.CLASS_NAME, "history-header")
        # wait_for_element(self.driver, By.CLASS_NAME, "reports-footer-wrapper")

        while True:
            try:
                report_footer = self.driver.find_element_by_xpath(Xpaths.HISTORY_REPORT_FOOTER)
                break
            except Exception as e:
                pass

        total_return    = report_footer.find_element_by_xpath('.//div[1]/div[2]').text
        total_div       = report_footer.find_element_by_xpath('.//div[2]/div[2]').text
        deposits        = report_footer.find_element_by_xpath('.//div[3]/div[2]').text
        withdrawals      = report_footer.find_element_by_xpath('.//div[4]/div[2]').text

        self.total_return    = float(total_return.replace(u'\xa3', '').replace(' ', ''))
        self.total_div       = float(total_div.replace(u'\xa3', '').replace(' ', ''))
        self.deposits        = float(deposits.replace(u'\xa3', '').replace(' ', ''))
        self.withdrawals      = float(withdrawals.replace(u'\xa3', '').replace(' ', ''))

        print("total_return: {}".format(self.total_return))
        print("total_div:    {}".format(self.total_div))
        print("deposits:     {}".format(self.deposits))
        print("withdrawals:  {}".format(self.withdrawals))

        self.account_summary = None
        self.account_summary = AccountSummary(
            total_return    = self.total_return,
            total_div       = self.total_div,
            deposits        = self.deposits,
            withdrawals     = self.withdrawals,
            live_result     = self.live_val,
            free_fund       = self.free_fund_val,
            portfolio       = self.portfolio_val,
            acc_value       = self.acc_value_val,
            invested        = self.invested,
            percent_ret     = self.percent_ret,
            today_date      = self.date_frmt

        )

        # close the history window
        self.driver.find_element_by_xpath(Xpaths.HISTORY_WINDOW_X_BUTTON).click()


        self.stocks = []

        stocks_rows = set()
        stocks_names = set()

        while(1):

            stocks_table = self.driver.find_element_by_xpath(Xpaths.POSITION_TABLE_CONTENT)
            stop_flag = 0

            for row in stocks_table.find_elements_by_xpath(Xpaths.POSITION_TABLE_ITEM):
                if not row in stocks_rows:
                    stop_flag = 1
                    break

            if (stop_flag == 0): break

            stocks_table = self.driver.find_element_by_xpath(Xpaths.POSITION_TABLE_CONTENT)

            for row in stocks_table.find_elements_by_xpath(Xpaths.POSITION_TABLE_ITEM):

                stocks_rows.add(row)
                name = row.find_element_by_xpath(Xpaths.POSITION_NAME).get_attribute("textContent")

                if not name in stocks_names:

                    stocks_names.add(name)

                    self.name            = row.find_element_by_xpath(Xpaths.POSITION_NAME).get_attribute("textContent")
                    self.ticker          = row.find_element_by_xpath(Xpaths.POSITION_TICKER).get_attribute("textContent")
                    self.image           = row.find_element_by_xpath(Xpaths.POSITION_IMAGE).get_attribute("src")
                    dateCreated          = row.find_element_by_xpath(Xpaths.POSITION_DATECREATED).get_attribute("textContent")
                    self.dateCreated     = '/'.join(dateCreated.split()[0].split('.')[::-1]) + ' ' + dateCreated.split()[1]

                    self.quantity        = row.find_element_by_xpath(Xpaths.POSITION_QUANTITY).get_attribute("textContent")

                    self.marketVal       = row.find_element_by_xpath(Xpaths.POSITION_MARKETVAL).get_attribute("textContent")
                    self.returnPercent   = row.find_element_by_xpath(Xpaths.POSITION_RETURNPERCENT).get_attribute("textContent")

                    s = Stock(self.ticker, self.name, self.dateCreated, self.quantity, self.marketVal, self.returnPercent, image=self.image)
                    self.stocks.append(s)

            time.sleep(2.5)
            stocks_table.find_elements_by_xpath(Xpaths.POSITION_TABLE_ITEM)[-1].location_once_scrolled_into_view

        self.print_account_summary()
        self.print_stock_summary()

    def load_mainpage(self):
        self.driver.get("https://live.trading212.com")

    def login(self):

        wait_for_element_clickable(self.driver, By.CLASS_NAME, "submit-button")

        self.driver.find_element_by_xpath("//*[@id='__next']/main/div[2]/div/div[2]/div/div[2]/div/form/div[2]/div/div/input").send_keys(self.username)
        self.driver.find_element_by_xpath("//*[@id='__next']/main/div[2]/div/div[2]/div/div[2]/div/form/div[3]/div/div/input").send_keys(self.password)

        self.driver.find_element_by_class_name('submit-button').click()

        self.has_login = True

    def switch_account(self, acc):

        self.driver.find_element_by_class_name('account-menu-header').click()
        time.sleep(3)

        if acc in ["INVESTING"]:

            print("Selecting INVESTING")

            try:
                self.driver.find_element_by_xpath('//*[@id="app"]/div[11]/div/div/div/div/div[1]/div/div[1]/div[2]').click()
            except Exception as e:
                print(e)
                self.driver.find_element_by_class_name('account-menu-header').click()

        elif acc in ["ISA"]:

            print("Selecting ISA")

            try:
                self.driver.find_element_by_xpath('//*[@id="app"]/div[11]/div/div/div/div/div[1]/div/div[1]/div[3]').click()
            except Exception as e:
                print (e)
                self.driver.find_element_by_class_name('account-menu-header').click()
        else:
            print("ERR: unknown account")
            sys.exit(1)


        time.sleep(5)

    def get_account_summary(self):
        return self.account_summary

    def get_stocks(self):
        return self.stocks

    def print_account_summary(self):

        print ("")
        print ("--------------------------")
        print ("DATE: {}".format(self.today))
        print ("--------------------------")
        print ("LIVE RESULT   : {}".format(self.live_val))
        print ("FREE FUND     : {}".format(self.free_fund_val))
        print ("PORTFOLIO     : {}".format(self.portfolio_val))
        print ("ACCOUNT VALUE : {}".format(self.acc_value_val))
        print ("--------------------------")
        print ("Invested      : {}".format(self.invested))
        print ("Return        : {}".format(self.live_val))
        print ("\n")

    def print_stock_summary(self):

        table = Table(show_header=True, header_style="bold magenta")

        header = ["NAME", "DATE CREATED", "QUANTITY", "MARKET VALUE", "RETURN PERCENTAGE"]

        table.add_column("NAME", justify="right")
        table.add_column("DATE CREATED")
        table.add_column("QUANTITY")
        table.add_column("MARKET VALUE", justify="right")
        table.add_column("RETURN PERCENTAGE", justify="right")

        for s in self.stocks:
            table.add_row([s.name, s.date_created, s.quantity, s.market_value, s.return_percent])

        table.print_table()

    def close_driver(self):

        if self.driver is not None:
            self.driver.quit()

if __name__ == "__main__":

    S = Scrape(
        username="",
        password="",
        headless=False
    )

    S.scape(account='INVESTING')
    S.scape(account='ISA')