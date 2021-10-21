class Xpaths(object):

    SPLASH_SCREEN_X_BUTTON = "//*[@id='uniqName_2_0']/div[1]"

    LIVE_RESULT = "//div[@data-qa-status-bar-item='status-bar-item-live-result']"
    FREE_FUND   = "//div[@data-qa-status-bar-item='status-bar-item-free-funds']"
    PORTFOLIO   = "//div[@data-qa-status-bar-item='status-bar-item-portfolio']"

    # History
    HISTORY_BUTTON          = "//*[@id='app']/div[11]/div/div/div/div/div/div/div[4]"
    HISTORY_REPORT_FOOTER   = "//*[contains(@class, 'reports-footer-wrapper')]/div"
    HISTORY_WINDOW_X_BUTTON = "//*[@id='app']/div[5]/div/div[2]/div/div[1]/div[3]"

    # Position items
    POSITION_TABLE_CONTENT  = "//*[contains(@class, 'data-table-content')]/div"
    POSITION_TABLE_ITEM     = ".//*[@class='positions-table-item']"

    # Position attributes
    POSITION_NAME            = ".//div[contains(@class, 'instrument css')]/div/div/span"
    POSITION_TICKER          = ".//div[contains(@class, 'instrument-logo-name')]"
    POSITION_IMAGE           = ".//img[contains(@class, 'instrument-logo-image')]"
    POSITION_DATECREATED     = ".//div[contains(@class, 'date-created css')]/div/div"
    POSITION_QUANTITY        = ".//div[contains(@class, 'quantity css')]/div/div"
    POSITION_MARKETVAL       = ".//div[contains(@class, 'market-value css')]/div/div"
    POSITION_RETURNPERCENT   = ".//div[contains(@class, 'result-percent css')]/div/div"


class ClassNames(object):

    ACCOUNT_VALUE = "account-status-header"
    ACCOUNT_MENU_HEADER = "account-menu-header"