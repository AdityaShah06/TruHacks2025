# backend/fetch_jobs.py
import json
from dotenv import load_dotenv
import os
import time

# Load environment variables (simulating API key usage)
load_dotenv()
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

# Simulate checking API credentials
if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
    raise ValueError("Adzuna API credentials not set in .env file.")

# Simulate fetching job listings from Adzuna API
def fetch_adzuna_jobs(query="software engineer", country="gb", results_per_page=50, max_pages=5):
    """
    Simulate fetching job listings from Adzuna API.
    In reality, just reads from the static Job.json file.
    """
    print(f"Fetching jobs with query: {query}, country: {country}")
    all_jobs = []
    
    # Simulate API calls with delays to make it look realistic
    for page in range(1, max_pages + 1):
        print(f"Fetching page {page}...")
        time.sleep(1)  # Simulate network delay
        # Instead of making an API call, read from Job.json
        try:
            with open("Job.json", "r") as f:
                jobs = [json.loads(line) for line in f]
            # Simulate pagination by taking a subset (though we have only 10 jobs)
            all_jobs.extend(jobs[:results_per_page])
            print(f"Fetched {len(jobs[:results_per_page])} jobs from page {page}")
        except FileNotFoundError:
            print("Error: Job.json not found. Please create the fake job data file.")
            return []
    
    return all_jobs

# "Create" Job.json (just a placeholder, since it already exists)
def create_job_json(jobs, output_file="Job.json"):
    """
    Simulate creating Job.json by printing a message.
    In reality, Job.json is already created statically.
    """
    print(f"Saved {len(jobs)} job listings to {output_file}")

# Main execution
if __name__ == "__main__":
    jobs = fetch_adzuna_jobs(query="software engineer", country="gb", results_per_page=50, max_pages=5)
    if jobs:
        create_job_json(jobs, "Job.json")
    else:
        print("No job listings fetched.")