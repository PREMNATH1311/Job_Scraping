# main.py
from scrap1 import collect_links
from scraper import scrape_jobs_from_file
from email_alert import send_email


def main():
    print("Collecting job links...")
    total_links = collect_links()
    print(f"Collected {total_links} job links.")

    print("Scraping job details...")
    new_jobs = scrape_jobs_from_file()
    print(f"New jobs found: {new_jobs}")

    if new_jobs > 0:
        send_email(new_jobs)
        print("Email alert sent.")

    print("Task completed.")


if __name__ == "__main__":
    main()
