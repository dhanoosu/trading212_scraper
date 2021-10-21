# -*- coding: utf-8 -*-


from __future__ import print_function
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

def wait_for_element(driver, element_type, attr):
    while True:
        # wait for page to load
        try:
            wait_time(1)
            element_present = EC.presence_of_element_located((element_type, attr))
            WebDriverWait(driver, 10).until(element_present)
            print("Page is ready!")
            break
        except Exception as e:
            print(attr + " :Loading took too much time!")
            print("Waiting ...")
            # driver.refresh()

def wait_for_element_clickable(driver, element_type, attr):
    timeout = 1

    WebDriverWait(driver, timeout * 5).until(
        EC.element_to_be_clickable((element_type, attr))
    )

class Header():

    justify_type = {
        ""      : '',
        "left" : '<',
        "right"  : '>',
        "center": '^'
    }

    def __init__(self, text, size, justify="", pad_text=False):
        self.text = text
        self.size = size

        if justify in self.justify_type:
            self.justify = justify
        else:
            print("Invalid justify keyword: only {}".format(self.justify_type.key()))
            sys.exit(1)

        if pad_text:
            self.text = "{1}{0}{1}".format(self.text, " "*2)

    def get_formatted_size(self, offset=0):

        return "{}{}".format(
            self.justify_type[self.justify],
            self.size + offset
        )

class Table():

    if sys.version_info.major > 2:
        TOP_LEFT_CORNER     = '┏'
        TOP_RIGHT_CORNER    = '┓'
        BOTTOM_LEFT_CORNER  = '└'
        BOTTOM_RIGHT_CORNER = '┘'

        TOP_SEPARATOR       = '┳'
        LEFT_SEPARATOR      = '┡'
        RIGHT_SEPARATOR     = '┩'
        MIDDLE_SEPARATOR    = '╇'
        BOTTOM_SEPARATOR    = '┴'

        VERITCAL_LINE           = '│'
        HORIZONTAL_LINE         = '─'
        HORIZONTAL_BOLD_LINE    = '━'
    else:
        TOP_LEFT_CORNER     = '+'
        TOP_RIGHT_CORNER    = '+'
        BOTTOM_LEFT_CORNER  = '+'
        BOTTOM_RIGHT_CORNER = '+'

        TOP_SEPARATOR       = '+'
        LEFT_SEPARATOR      = '+'
        RIGHT_SEPARATOR     = '+'
        MIDDLE_SEPARATOR    = '+'
        BOTTOM_SEPARATOR    = '+'

        VERITCAL_LINE           = '|'
        HORIZONTAL_LINE         = '-'
        HORIZONTAL_BOLD_LINE    = '-'



    def __init__(self, show_header=True, header_style=""):
        self.table = []
        self.header = []

    def add_column(self, col, justify=""):

        self.header.append(Header(text=col, size=(4+len(col)), justify=justify, pad_text=True))

    def add_row(self, row):
        if len(row) != len(self.header):
            print("no. row != no. header")
            sys.exit(1)
        else:
            new_row = []
            for r in row:
                new_row.append("{1}{0}{1}".format(r, " "*2))

            self.table.append(new_row)

    # def add_row_separator(self):



    def print_table(self):

        for i, col in enumerate(zip(*self.table)):
            for c in col:
                if (len(c)) > self.header[i].size:
                     self.header[i].size = (len(c))

        h0_line = ""
        h1_line = ""
        middle_line = ""
        bottom_line = ""

        for i, h in enumerate(self.header):

            if i == 0:
                h0_line += "{}{}".format(self.TOP_LEFT_CORNER, self.HORIZONTAL_BOLD_LINE*(h.size))
                h1_line += "{}{}".format(self.LEFT_SEPARATOR, self.HORIZONTAL_BOLD_LINE*(h.size))
                middle_line += "{}{}".format(self.LEFT_SEPARATOR, self.HORIZONTAL_LINE*(h.size))
                bottom_line += "{}{}".format(self.BOTTOM_LEFT_CORNER, self.HORIZONTAL_LINE*(h.size))
            elif i < (len(self.header)):
                h0_line += "{}{}".format(self.TOP_SEPARATOR, self.HORIZONTAL_BOLD_LINE*(h.size))
                h1_line += "{}{}".format(self.MIDDLE_SEPARATOR, self.HORIZONTAL_BOLD_LINE*(h.size))
                middle_line += "{}{}".format(self.MIDDLE_SEPARATOR, self.HORIZONTAL_LINE*(h.size))
                bottom_line += "{}{}".format(self.BOTTOM_SEPARATOR, self.HORIZONTAL_LINE*(h.size))


        h0_line += "{}".format(self.TOP_RIGHT_CORNER)
        h1_line += "{}".format(self.RIGHT_SEPARATOR)
        middle_line += "{}".format(self.RIGHT_SEPARATOR)
        bottom_line += "{}".format(self.BOTTOM_RIGHT_CORNER)

        print(h0_line)

        for h in self.header:

            # |{:20} or |{:>20} or |{:^20}
            format_row = "{0}{{:{1}}}".format(self.VERITCAL_LINE, h.get_formatted_size(offset=0))
            print(format_row.format(h.text), end="")

        print(self.VERITCAL_LINE)
        print(h1_line)

        for t in self.table:
            for i, r in enumerate(t):
                h = self.header[i]

                format_row = "{0}{{:{1}}}".format(self.VERITCAL_LINE, h.get_formatted_size(offset=0))
                print(format_row.format(r), end="")

            print(self.VERITCAL_LINE)

        print(bottom_line)

