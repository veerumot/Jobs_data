#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
from datetime import date
import datetime
import csv
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 800))  
display.start()

chromedriver_autoinstaller.install()


chrome_options = webdriver.ChromeOptions()
options = [
  # Define window size here
   "--window-size=1200,1200",
    "--ignore-certificate-errors"
 
    #"--headless",
    #"--disable-gpu",
    #"--window-size=1920,1200",
    #"--ignore-certificate-errors",
    #"--disable-extensions",
    #"--no-sandbox",
    #"--disable-dev-shm-usage",
    #'--remote-debugging-port=9222'
]

for option in options:
    chrome_options.add_argument(option)

    
driver = webdriver.Chrome(options = chrome_options)


# Global variables
total = None
month = None
week = None
day = None
Today_date = date.today()
list = None

def jobs_count(driver):
    global total, month, week, day, list
    max_retries = 5  # Maximum number of retries
    retry_count = 0
    while retry_count < max_retries:
        try:    
                my_list = [ 'https://www.linkedin.com/jobs/search?keywords=DevOps%20Engineer&location=United%20States', 
                            'https://www.linkedin.com/jobs/search?keywords=salesforce%20Engineer&location=United%20States', 
                            'https://www.linkedin.com/jobs/search?keywords=Data%20Engineer&location=United%20States',
                            'https://www.linkedin.com/jobs/search?keywords=fullstack%20Engineer&location=United%20States',
                            'https://www.linkedin.com/jobs/search?keywords=java%20Engineer&location=United%20States',
                            'https://www.linkedin.com/jobs/search?keywords=python%20Engineer&location=United%20States',
                            'https://www.linkedin.com/jobs/search?keywords=cloud%20Engineer&location=United%20States',
                            'https://www.linkedin.com/jobs/search?keywords=mlops%20Engineer&location=United%20States',
                            'https://www.linkedin.com/jobs/search?keywords=aiops%20Engineer&location=United%20States',
                            'https://www.linkedin.com/jobs/search?keywords=platform%20Engineer&location=United%20States',
                            'https://www.linkedin.com/jobs/search?keywords=Devsecops%20Engineer&location=United%20States',
                            'https://www.linkedin.com/jobs/search?keywords=security%20Engineer&location=United%20States',
                            'https://www.linkedin.com/jobs/search?keywords=Automation%20Engineer&location=United%20States',
                            'https://www.linkedin.com/jobs/search?keywords=python%20devloper&location=United%20States',
                            'https://www.linkedin.com/jobs/search?keywords=java%20Edevloper&location=United%20States',
                            'https://www.linkedin.com/jobs/search?keywords=QA%20Engineer&location=United%20States',
                            'https://www.linkedin.com/jobs/search?keywords=Terraform%20Engineer&location=United%20States'
                        ]
                current_hour = datetime.datetime.now().hour
                print(current_hour)
                index = current_hour % len(my_list)
                list = my_list[index]
                print(list)        
                driver.get(list)
                driver.find_element(
                    By.XPATH, '//*[@id="base-contextual-sign-in-modal"]/div/section'
                )
                close_button = driver.find_element(
                    By.XPATH, '//*[@id="base-contextual-sign-in-modal"]/div/section/button'
                )
                close_button.click()
            # except NoSuchElementException:
                posted_time = driver.find_element(
                    By.XPATH, '//*[@id="jserp-filters"]/ul/li[1]/div'
                )
                posted_time.click()
                anytime = driver.find_element(
                    By.XPATH, '//*[@id="jserp-filters"]/ul/li[1]/div/div/div/div/div/div[1]'
                )
                total = anytime.text
                total = re.sub(r"[^\d\s]", "", total)
                print(total)
                pastmonth = driver.find_element(
                    By.XPATH, '//*[@id="jserp-filters"]/ul/li[1]/div/div/div/div/div/div[2]'
                )
                month = pastmonth.text
                month = re.sub(r"[^\d\s]", "", month)
                print(month)
                pastweek = driver.find_element(
                    By.XPATH, '//*[@id="jserp-filters"]/ul/li[1]/div/div/div/div/div/div[3]'
                )
                week = pastweek.text
                week = re.sub(r"[^\d\s]", "", week)
                print(week)
                past24hrs = driver.find_element(
                    By.XPATH, '//*[@id="jserp-filters"]/ul/li[1]/div/div/div/div/div/div[4]'
                )
                day = past24hrs.text
                day = re.sub(r"[^\d\s]", "", day)
                day = day.replace("24", "", 1).strip()
                print(day)
            # with open("page.html", "a") as f:
            # #     print(driver.page_source, file=f)
                time.sleep(1)
            # driver.get_screenshot_as_file(
            #     "/Users/madhurigorantla/github/My-website/veeru-portfolio/user.png"
            # )
                break
        except WebDriverException as e:
            # Handle failure and retry
            print(f"Failed to load URL on attempt {retry_count + 1}. Retrying...")
            retry_count += 1
            time.sleep(3)
        if retry_count == max_retries:
            print("Failed to load URL after multiple attempts") 
        driver.quit()


def use_values():
    global Today_date
    print(f"month_jobs:{month}, week_jobs:{week}, day_jobs:{day}, all:{total}, list:{list}")
    month_jobs = month
    week_jobs = week
    day_jobs = day
    data = [month_jobs, week_jobs, day_jobs, list]
    print(data)
    with open("output.csv", "a", newline="") as file:
        writer = csv.writer(file)
        # writer.writerow(data[0])
        # for row in data:
        writer.writerow(data)

# roles()
jobs_count(webdriver.Chrome())
use_values()
