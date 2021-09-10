from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import csv

collection = 'Domestic Traffic Ads'
csvfile = open(collection+'.csv', 'w', newline='')
writer = csv.writer(csvfile)
headers_written = False

def save_record(pageno, trs):
    global headers_written, writer
    if headers_written == False:
        writer.writerow([x.find_element_by_tag_name('b').text for x in trs])
        headers_written = True
    data = [x.find_elements_by_tag_name('td')[1].text for x in trs]
    try:
        data[6] = trs[6].find_element_by_tag_name('a').get_attribute('href')
    except NoSuchElementException:
        pass
    writer.writerow(data)

driver = webdriver.Firefox()
driver.get("http://slavery2.msa.maryland.gov/pages/Search.aspx")
driver.find_element_by_name('ctl00$main$btnTabCollections').click()
driver.find_element_by_link_text(collection).click()
driver.find_element_by_id('main_rblDisplayMode_1').click()

pageno = 1
staleness_check = None
while True:
    #if pageno > 1:
    #    break
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "main_lblDetails")))
        if staleness_check != None:
            element = WebDriverWait(driver, 10).until(
                EC.staleness_of(staleness_check))
        table = driver.find_element_by_css_selector('span#main_lblDetails + table')
        trs = table.find_elements_by_tag_name('tr')
        staleness_check = trs[0]
        save_record(pageno, trs)
        try:
            pageno += 1
            driver.find_element_by_id("main_imgButtonNext").click()
        except NoSuchElementException:
            break
    except TimeoutException:
        print('timeout waiting for page '+pageno)
        exit()

csvfile.close()
driver.close()
