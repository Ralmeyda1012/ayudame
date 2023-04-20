import csv
import os
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    # Create the Chrome driver instance
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=options, port=8080)

    return driver

def close_driver(driver):
    # close the driver
    driver.quit()

def get_data(driver, url):
    # navigate to the search results page
    driver.get(url)

    # create a BeautifulSoup object from the driver page source
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # find all elements with the data-pid attribute using the 'attrs' parameter
    elements = soup.find_all(attrs={'data-pid': True})

    # extract the data-pid attribute value for each element
    # use a list comprehension for better performance
    data_pid = [element['data-pid'] for element in elements]

    # find the element using a CSS selector
    # css_value = driver.find_element(By.CSS_SELECTOR, "div.kp-hc h2 span")
    try:
        css_value_element = driver.find_element(
            By.CSS_SELECTOR, "div.kp-hc h2 span")
        css_value = css_value_element.text
    except:
        print(f"CSS Selector not found for url: {url}")
        css_value = "CSS Selector not found "
    # close the driver
    # driver.quit()

    return data_pid, css_value

filename = 'output.csv'
count = 1
while os.path.exists(filename):
    filename = f"output_{count}.csv"
    count += 1
input_path = '/Users/raul/Downloads/Testing.csv'
input_path_abs = os.path.abspath(input_path)    
with open(input_path_abs, 'r', encoding='utf-8') as infile, \
        open(filename, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # skip header row
    next(reader)

    # write header row for output file
    writer.writerow(['Deal ID', 'URL', 'Output 1', 'data-pid'])
    driver = initialize_driver()
    for row in reader:
        url = row[1]
        deal_id = row[0]
        print("URL:", url)
        data_pid, css_value = get_data(driver, url)
        driver.implicitly_wait(1.0)
        writer.writerow([deal_id, url, css_value, data_pid])
        print(deal_id, url, data_pid, css_value)

close_driver(driver)
    
