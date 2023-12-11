import time

import tools
from selenium.webdriver.common import by

driver = tools.get_chrome_client()

driver.get('https://58.com')

driver.find_element(by.By.XPATH,
                    '''//a[@tongji_tag="pc_home_dh_zf"]''').click()
driver.switch_to.window(driver.window_handles[-1])

for filter_box in driver.find_elements(by.By.XPATH, '//div[@class="filter-wrap"]/div[@class="search_nav"]/a'):
    if filter_box.text.find('地铁线路') > -1:
        filter_box.click()


def enter_stations():
    pass


for index in range(len(driver.find_elements(by.By.XPATH,
                                            '//div[@class="search_bd"]//dl[@class="secitem secitem_fist subway"]/dd/a'))):
    dd = driver.find_elements(by.By.XPATH,
                              '//div[@class="search_bd"]//dl[@class="secitem secitem_fist subway"]/dd/a')[index]
    if dd.text.find('不限'):
        continue

    print(dd.text)
    dd.click()
    enter_stations()
    break

time.sleep(100)
driver.close()
driver.quit()
