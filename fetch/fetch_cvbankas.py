import requests
from bs4 import BeautifulSoup
import json
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add the parent directory to sys.path (for log_config)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from log_config import logger
from config import (
    CVBANKAS_IGNORE_WORDS_IN_JOB_TITLE,
    CVBANKAS_IGNORE_WORDS_IN_JOB_COMPANY,
)


load_dotenv()


def fetch_cvbankas_jobs(keyword, pages, salary, filter_to):
    logger.info("Fetching CVBankas jobs...")
    jobs = []

    for page in range(1, pages):
        url = f"https://en.cvbankas.lt/?keyw={keyword}&page={page}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            job_listings = soup.find_all("article", class_="list_article")

            for job in job_listings:
                job_data = {
                    "title": job.find("h3", class_="list_h3").text.strip(),
                    "company": job.find("span", class_="dib mt5 mr5").text.strip(),
                    "salary": extract_salary(job),
                    "keyword": keyword,
                    "job_posted": extract_job_posted(job),
                    "city": extract_city(job),
                    "href": job.find("a")["href"],
                }
                jobs.append(job_data)

        except Exception as e:
            logger.error(f"Error fetching data for {keyword} page {page}: {e}")

    logger.info(f"Fetched {len(jobs)} job listings for keyword: '{keyword}'")
    filtered_jobs = filter_cvbankas_jobs(jobs, salary, filter_to)

    # Move jobs with "kokyb" in the title to the top of the list
    kokyb_jobs = [job for job in filtered_jobs if "kokyb" in job["title"].lower()]
    other_jobs = [job for job in filtered_jobs if "kokyb" not in job["title"].lower()]
    filtered_jobs = kokyb_jobs + other_jobs

    return filtered_jobs


def extract_salary(job):
    salary_elem = job.find("span", class_="salary_amount")
    if not salary_elem:
        return "N/A"

    salary = salary_elem.text.strip()
    salary_period = job.find("span", class_="salary_period")
    salary_type = job.find("span", class_="salary_calculation")

    if salary_period and salary_type:
        return f"{salary} {salary_period.text.strip()} ({salary_type.text.strip()})"
    return salary


def extract_job_posted(job):
    time_elem = job.find("span", class_="txt_list_2")
    if time_elem:
        return time_elem.text.strip()
    else:
        important_elem = job.find("span", class_="txt_list_important")
        return important_elem.text.strip() if important_elem else None


def extract_city(job):
    city_elem = job.find("span", class_="list_city")
    return city_elem.text.strip() if city_elem else "N/A"


def filter_cvbankas_jobs(jobs, salary, filter_to):
    def is_valid_job(job):
        if job["salary"] == "N/A":
            return False
        try:
            salary_value = float(
                "".join(filter(str.isdigit, job["salary"].split("-")[0]))
            )
            return (
                salary_value >= salary
                and not any(
                    keyword.lower() in job["title"].lower()
                    for keyword in CVBANKAS_IGNORE_WORDS_IN_JOB_TITLE
                )
                and not any(
                    keyword.lower() in job["company"].lower()
                    for keyword in CVBANKAS_IGNORE_WORDS_IN_JOB_COMPANY
                )
            )
        except ValueError:
            return False

    filtered_jobs = list(filter(is_valid_job, jobs))
    logger.info(
        f"Filtered those {len(jobs)} to {len(filtered_jobs)} jobs, returned first {filter_to} according to:min. {salary}eur salary requirements and ignored words in job title:{CVBANKAS_IGNORE_WORDS_IN_JOB_TITLE} as well as ignored words in job company:{CVBANKAS_IGNORE_WORDS_IN_JOB_COMPANY} "
    )
    return filtered_jobs[:filter_to]


def save_cvbankas_jobs(jobs):
    data_to_save = {
        "fetch_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "jobs": jobs,
    }

    file_path = os.path.join(os.getenv("BASE_DIR"), "data/data_cvbankas.json")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)
        logger.info(f"Data saved to {file_path}")
    except IOError as e:
        logger.error(f"Failed to save data: {e}")


def main():
    jobs = fetch_cvbankas_jobs(keyword="vadovas", pages=2, salary=3000, filter_to=5)
    save_cvbankas_jobs(jobs)


if __name__ == "__main__":
    main()
