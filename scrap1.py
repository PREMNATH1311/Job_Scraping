import pandas as pd
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

Start_url="https://www.freshersworld.com/jobs/category/it-software-job-vacancies"

def collect_links(output_file="job_url.txt"):
    options=webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")

    # prefs = {
    #     "profile.default_content_setting_values.notifications": 2,  # block notifications
    #     "profile.default_content_setting_values.geolocation": 2,     # block location popup
    #     "profile.default_content_setting_values.media_stream": 2     # block mic/camera
    # }

    # options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=Service(),options=options)
    wait=WebDriverWait(driver,10)
    sleep=time.sleep(2)

    #Main URL
    driver.get(Start_url)

    # link_container=driver.find_elements(By.XPATH,'//div[@class="col-md-12 col-lg-12 col-xs-12 padding-none job-container jobs-on-hover top_space"]')


    
    page_number=1
    while page_number<=15:
        
        link_contains=wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="col-md-12 col-lg-12 col-xs-12 padding-none job-container jobs-on-hover top_space"]')))
        page_link=[]
        ##Get job url on this page
        for card in link_contains:
            job_url=card.get_attribute("job_display_url")
            if job_url:
                page_link.append(job_url)
        # print(f"Collected {len(page_link)} job links so page {page_number}")
        # Append to text file
        with open(output_file, "a", encoding="utf-8") as f:
            # f.write(f"\n# Page {page_number}\n")
            for url in page_link:
                f.write(url + "\n")

        print(f"Saved Page {page_number} links.\n")
        
        #check if "Next" page exists
        
        try:
            next_button=driver.find_element(By.XPATH,'//a[@title="Next Page"]')
            next_page_url=next_button.get_attribute("href")
            if next_page_url:
                driver.get(next_page_url)
                page_number+=1
                time.sleep(2)
            else:
                break
        except:
            print("No more pages")
            break
        
    # print(f"total job Urls {len(page_link)}")
    driver.quit()
    return len(page_link)