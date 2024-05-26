import utils.scraping_util as scraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import logging
import uuid
import time
from datetime import datetime
import re
import sqlite3
from selenium.webdriver.remote.webdriver import WebDriver
from utils.helpers import (
    is_location_remote,
    is_location_unspecified,
    get_province,
    normalize_scraped_salary,
    determine_job_level,
    normalize_job_level,
    determine_tech_stack,
)
import os


def scrape_page(browser: WebDriver) -> list[dict]:

    # left pane job list
    jobCardSelector = "#mosaic-provider-jobcards > ul > li"

    # information from header
    job_title_locator = ".jobsearch-JobInfoHeader-title > span:nth-child(1)"
    job_location_locator = "[data-testid='inlineHeader-companyLocation']"
    job_salary_locator_id = "salaryInfoAndJobType"

    # bakcup
    # information from body
    job_location_locator_backup = (
        "[data-testid='jobsearch-JobInfoHeader-companyLocation']"
    )
    job_description_id = "jobDescriptionText"

    job_list: list[dict] = []
    job_cards = scraper.getElements(browser, By.CSS_SELECTOR, jobCardSelector)
    for index, job in enumerate(job_cards):

        job_data_id = str(uuid.uuid4())
        job_detail: dict = {
            "job_data_id": job_data_id,
            "title": None,
            "location": None,
            "salary": None,
            "job_level": None,
            "date_scraped": datetime.today().strftime("%Y-%m-%d"),
            "tech_stack": [],
        }

        tech_stack_list: list[str] = []

        fresh_job_cards = scraper.getElements(browser, By.CSS_SELECTOR, jobCardSelector)
        fresh_card = fresh_job_cards[index]
        if len(fresh_card.text) > 0 and fresh_card.is_enabled():

            job_title: str = scraper.getElement(
                browser, By.CSS_SELECTOR, job_title_locator
            ).text
            job_location = scraper.getElement(
                browser, By.CSS_SELECTOR, job_location_locator
            ).text

            job_detail["title"] = job_title.splitlines()[0]

            # LOCATION
            if is_location_remote(job_location):
                job_detail["location"] = "remote"
            elif is_location_unspecified(job_location):
                job_detail["location"] = "unspecified"
            elif "•" in job_location:
                job_detail["location"] = get_province(
                    job_location[: job_location.index("•")]
                )
            else:
                job_detail["location"] = get_province(job_location)

            # SALARY
            try:
                job_salary = scraper.getElement(
                    browser, By.ID, job_salary_locator_id
                ).text

                pattern = r"\d+,\d+"
                matches = re.findall(pattern, job_salary)
                if len(matches) == 2:
                    base_salary = matches[0].replace(",", "")
                    max_salary = matches[1].replace(",", "")
                    job_detail["salary"] = normalize_scraped_salary(
                        int(base_salary), int(max_salary)
                    )
                elif len(matches) == 1:
                    base_salary = matches[0].replace(",", "")
                    job_detail["salary"] = int(base_salary)

            except NoSuchElementException:
                pass

            # JOB LEVEL
            raw_job_level = determine_job_level(job_title.splitlines()[0])
            if bool(raw_job_level):
                job_level = normalize_job_level(raw_job_level)
                job_detail["job_level"] = job_level

            # TECH STACK
            try:
                job_description = scraper.getElement(
                    browser, By.ID, job_description_id
                ).text

                tech_list = determine_tech_stack(job_description)
                for tech in tech_list:
                    tech_skill: dict = {
                        "tech_stack_id": str(uuid.uuid4()),
                        "job_data_id": job_data_id,
                        "tech_type": tech,
                    }
                    tech_stack_list.append(tech_skill)

            except NoSuchElementException:
                pass
            finally:
                job_detail["tech_stack"] = tech_stack_list

            job_list.append(job_detail)

            fresh_card.click()
            time.sleep(3)
    return job_list


def scrape_indeed():

    browser = scraper.browserDriver()
    # baseUrl = rf"https://ph.indeed.com/jobs?q=software%20developer&fromage=7&sort=date&start={page}"
    baseUrl = rf"https://ph.indeed.com/jobs?q=software%20developer&fromage=7&sort=date&start=0"
    browser.get(baseUrl)
    dbPath = os.getenv("DB_FILE_PATH")

    is_end_of_page = True
    while is_end_of_page:
        page = 0
        time.sleep(2)

        scraped_data: list[dict] = []
        if page == 1:
            break

        try:
            scraped_data = scrape_page(browser)
        except BaseException as e:
            logging.basicConfig(
                filename="./logs/page_scraping.log",
                filemode="a",
                format="[%(asctime)s - %(levelname)s]: %(message)s",
            )
            logging.warning(f"Could not scrape at page: {page} on INDEED")
            logging.error(f"Error Type: {e}")
            break

        try:
            # connection = sqlite3.connect("../../db/job_record.db")
            connection = sqlite3.connect(dbPath)
            cursor = connection.cursor()

            for data in scraped_data:

                cursor.execute(
                    "INSERT INTO job_data VALUES (?,?,?,?,?,?);",
                    (
                        data["job_data_id"],
                        data["title"],
                        data["location"],
                        data["salary"],
                        data["job_level"],
                        data["date_scraped"],
                    ),
                )

                tech_stack = data["tech_stack"]
                for tech in tech_stack:
                    cursor.execute(
                        "INSERT INTO tech_skill VALUES (?,?,?);",
                        (
                            tech["tech_stack_id"],
                            tech["job_data_id"],
                            tech["tech_type"],
                        ),
                    )

            connection.commit()
        except BaseException as e:

            logging.basicConfig(
                filename="./logs/insert_records_to_db.log",
                filemode="a",
                format="[%(asctime)s - %(levelname)s]: %(message)s",
            )
            logging.error(f"Error Occured while inserting data to db: {e}")
        finally:
            connection.close()

        try:
            next_page_button_locator = "[data-testid='pagination-page-next']"
            x = scraper.getElement(browser, By.CSS_SELECTOR, next_page_button_locator)
            x.click()
        except NoSuchElementException:
            is_end_of_page = False
            break

        page += 1