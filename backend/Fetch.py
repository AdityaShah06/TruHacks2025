import requests
import json
import base64
from dotenv import load_dotenv
import os
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")
ENABLE_LOCAL_TESTING = os.getenv("ENABLE_LOCAL_TESTING", "false").lower() == "true"

def fetch_repo_info(owner, repo):
    if ENABLE_LOCAL_TESTING:
        logger.info(f"Using sample response for {owner}/{repo} (ENABLE_LOCAL_TESTING=true)")
        return {
            "name": repo,
            "description": "A hackathon project to automate resume creation from GitHub repositories.",
            "topics": ["fastapi", "github-api", "resume-automation"],
            "created_at": "2023-01-01T00:00:00Z",
            "pushed_at": "2023-12-31T23:59:59Z",
        }
    
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Authorization": f"token {github_token}"} if github_token else {}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return {
            "name": data.get("name"),
            "description": data.get("description", "No description available."),
            "topics": data.get("topics", []),
            "created_at": data.get("created_at"),
            "pushed_at": data.get("pushed_at"),
        }
    logger.error(f"Error fetching repo info for {owner}/{repo}: {response.status_code}")
    return None

def fetch_repo_files(owner, repo, path=""):
    if ENABLE_LOCAL_TESTING:
        logger.info(f"Using sample response for {owner}/{repo} files (ENABLE_LOCAL_TESTING=true)")
        return ["main.py", "README.md", "requirements.txt", "utils.py"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Authorization": f"token {github_token}"} if github_token else {}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        items = response.json()
        file_list = []
        for item in items:
            if item["type"] == "file":
                file_list.append(item["path"])
            elif item["type"] == "dir":
                time.sleep(0.1)  # Avoid rate limits
                file_list.extend(fetch_repo_files(owner, repo, item["path"]))
        return file_list
    logger.error(f"Error fetching files for {owner}/{repo} at path '{path}': {response.status_code}")
    return []

def fetch_repo_languages(owner, repo):
    if ENABLE_LOCAL_TESTING:
        logger.info(f"Using sample response for {owner}/{repo} languages (ENABLE_LOCAL_TESTING=true)")
        return {"Python": 80.0, "JavaScript": 20.0}
    
    url = f"https://api.github.com/repos/{owner}/{repo}/languages"
    headers = {"Authorization": f"token {github_token}"} if github_token else {}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        total_bytes = sum(data.values())
        return {lang: round((bytes / total_bytes) * 100, 2) for lang, bytes in data.items()}
    logger.error(f"Error fetching languages for {owner}/{repo}: {response.status_code}")
    return {}

def fetch_readme(owner, repo):
    if ENABLE_LOCAL_TESTING:
        logger.info(f"Using sample response for {owner}/{repo} README (ENABLE_LOCAL_TESTING=true)")
        return "This is a sample README for the TruHacks project."
    
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/README.md"
    headers = {"Authorization": f"token {github_token}"} if github_token else {}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        readme_data = response.json()
        return base64.b64decode(readme_data["content"]).decode("utf-8")
    logger.info(f"README not found for {owner}/{repo}: {response.status_code}")
    return "No README available."

def fetch_commit_messages(owner, repo, limit=100):
    if ENABLE_LOCAL_TESTING:
        logger.info(f"Using sample response for {owner}/{repo} commits (ENABLE_LOCAL_TESTING=true)")
        return ["Initial commit", "Added FastAPI backend", "Integrated GitHub API", "Updated README"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    headers = {"Authorization": f"token {github_token}"} if github_token else {}
    messages = []
    page = 1
    per_page = min(100, limit)
    
    while len(messages) < limit and page <= (limit // per_page) + 1:
        params = {"per_page": per_page, "page": page}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            logger.error(f"Error fetching commits for {owner}/{repo}: {response.status_code}")
            break
        commits = response.json()
        if not commits:
            break
        messages.extend(commit["commit"]["message"] for commit in commits)
        page += 1
    
    return messages[:limit]

def aggregate_repo_data(owner, repo, commit_limit=100):
    if ENABLE_LOCAL_TESTING:
        logger.info(f"Using sample response for {owner}/{repo} (ENABLE_LOCAL_TESTING=true)")
        return {
            "Repository Name": repo,
            "Description": "A hackathon project to automate resume creation from GitHub repositories.",
            "Topics": ["fastapi", "github-api", "resume-automation"],
            "Languages": {"Python": 80.0, "JavaScript": 20.0},
            "Files": ["main.py", "README.md", "requirements.txt", "utils.py"],
            "README": "This is a sample README for the TruHacks project.",
            "Recent Commit Messages": ["Initial commit", "Added FastAPI backend", "Integrated GitHub API", "Updated README"],
            "Start Date": "2023-01-01T00:00:00Z",
            "Last Updated": "2023-12-31T23:59:59Z",
        }
    
    repo_info = fetch_repo_info(owner, repo)
    if not repo_info:
        raise ValueError(f"Failed to fetch repo info for {owner}/{repo}")
    
    repo_languages = fetch_repo_languages(owner, repo) or {}
    readme_content = fetch_readme(owner, repo) or "No README available."
    all_files = fetch_repo_files(owner, repo) or []
    recent_commit_messages = fetch_commit_messages(owner, repo, limit=commit_limit) or []

    return {
        "Repository Name": repo_info.get("name", "Unknown Repository"),
        "Description": repo_info.get("description", "No description available."),
        "Topics": repo_info.get("topics", []),
        "Languages": repo_languages,
        "Files": all_files,
        "README": readme_content,
        "Recent Commit Messages": recent_commit_messages,
        "Start Date": repo_info.get("created_at", "Unknown Start Date"),
        "Last Updated": repo_info.get("pushed_at", "Unknown Last Updated"),
    }

def save_to_file(data, filename="repo_data.json"):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    logger.info(f"Data saved to {filename}")

if __name__ == "__main__":
    owner = "Aditya Shah"
    repo = "TruHacks"
    try:
        repo_data = aggregate_repo_data(owner, repo, commit_limit=100)
        save_to_file(repo_data)
    except Exception as e:
        logger.error(f"Failed to aggregate data: {e}")