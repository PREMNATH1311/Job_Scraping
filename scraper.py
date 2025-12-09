import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from db import insert_unique_job

file_path = "job_url.txt"
links = []

def scrape_jobs_from_file(file_path=file_path):

    # ------------------------------
    # Read links from file
    # ------------------------------
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("http"):
                links.append(line)

    print(f"Total links found: {len(links)}")

    # ------------------------------
    # Selenium Setup (HEADLESS)
    # ------------------------------
    options = Options()

    # Headless required for GitHub Actions
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    # Optional flags (good for stability)
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

    # IMPORTANT: Chromedriver path in GitHub Actions
    service = Service("/usr/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)

    driver.get("https://www.google.com")  # dummy homepage

    # ------------------------------
    # Scrape each job URL
    # ------------------------------
    new_job_count = 0

    for index, url in enumerate(links, start=1):
        print(f"\n[{index}] Opening: {url}")

        # Open in new tab
        driver.execute_script("window.open(arguments[0], '_blank');", url)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)

        def safe_find(xpath):
            try:
                return driver.find_element(By.XPATH, xpath).text.strip()
            except:
                return "N/A"

        title = safe_find('//div[@class="job-role  padding-none"]')
        company = safe_find('//div[@class=" padding-none company-name"]')
        salary = safe_find('//span[@style="margin-top: 2px;"]')
        location = safe_find('//a[@class="bold_font"]')
        education = safe_find('(//span[@class="elig_pos bold_font"]/a)[1]')
        experience = safe_find('//span[@style="margin-top: 3px;"]')
        hiring_process = safe_find('//span[@style="margin-left:52px;"]')
        employment_type = safe_find('//span[@style="margin-left:28px;"]')
        locality = safe_find('//span[@style="margin-left:35px;"]')
        state = safe_find('(//span[@style="margin-left:112px;"]//a)[1]')

        job_data = {
            "job_url": url,
            "title": title,
            "company": company,
            "salary": salary,
            "location": location,
            "education": education,
            "experience": experience,
            "hiring_process": hiring_process,
            "employment_type": employment_type,
            "locality": locality,
            "state": state
        }

        print(job_data)

        if insert_unique_job(job_data):
            print("→ New job added to MongoDB")
            new_job_count += 1
        else:
            print("→ Job already exists, skipped")

        # Close tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    driver.quit()

    print(f"\nDONE. Total NEW jobs inserted: {new_job_count}")
    return new_job_count
