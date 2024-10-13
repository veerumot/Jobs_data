#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
from datetime import date
import psycopg2
from selenium.common.exceptions import WebDriverException
import os
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



#Global variables
total = None
month = None
week = None
day = None
Today_date = date.today()


def jobs_count(driver):
    global total, month, week, day
    max_retries = 5  # Maximum number of retries
    retry_count = 0
    while retry_count < max_retries: 
        try: 
            path = f"https://www.linkedin.com/jobs/search?keywords=DevOps%20Engineer&location=United%20States"
            driver.get(path)
            time.sleep(5)
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
        time.sleep(2)
    if retry_count == max_retries:
        print("Failed to load URL after multiple attempts")
    driver.quit()



def use_values():
    global Today_date
    print(f"month_jobs:{month}, week_jobs:{week}, day_jobs:{day}, all:{total}")
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    month_jobs = month
    week_jobs = week
    day_jobs = day
    conn = psycopg2.connect(
        database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )
    print("Database connected successfully")
    cur = conn.cursor()
    query = """
                INSERT INTO time_data (date, month_jobs, week_jobs, day_jobs)
                VALUES (%s, %s, %s, %s)
            """
    cur.execute(query, (Today_date, month_jobs, week_jobs, day_jobs))

    conn.commit()
    cur.close()
    conn.close()


def main():
    jobs_count(webdriver.Chrome())
    use_values()

if _name_ == '__main__':
   main()
