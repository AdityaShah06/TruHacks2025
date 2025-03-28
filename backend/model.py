import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
from Fetch import aggregate_repo_data

# Load environment variables
load_dotenv()

# Load Gemini API key from environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

def generate_star_resume_section(repo_data):
    """
    Generate a STAR-based project section for a resume using Gemini API.
    :param repo_data: Dictionary containing GitHub repository details.
    :return: A dictionary with Name, Date, and Descriptions.
    """
    try:
        # Prepare the prompt with the repo data
        prompt = f"""
        Generate a professional and concise project description for a resume using the STAR (Situation, Task, Action, Result) method. 
        Each component must consist of a single, concise sentence written in formal, action-oriented language without personal pronouns or references.

        Repository Details:
        - Repository Name: {repo_data['Repository Name']}
        - Description: {repo_data['Description']}
        - Topics: {', '.join(repo_data.get('Topics', []))}
        - Languages: {json.dumps(repo_data['Languages'], indent=2)}
        - Recent Commit Messages: {', '.join(repo_data['Recent Commit Messages'][:50])}  # First 50 commit messages

        Format the response exactly as:
        - Situation: [Your sentence here]
        - Task: [Your sentence here]
        - Action: [Your sentence here]
        - Result: [Your sentence here]

        Ensure the output is concise, professional, and directly applicable to a resume.
        """

        # Call Gemini API to generate content
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        # Parse the result
        result_text = response.text.strip()
        descriptions = [line.split(": ", 1)[1].strip() for line in result_text.split("\n") if ": " in line]

        # Return the structured data
        return {
            "Name": repo_data["Repository Name"],
            "Date": f"{repo_data['Start Date']} - {repo_data['Last Updated']}",
            "Languages": list(repo_data["Languages"].keys()),
            "Descriptions": descriptions[:4]  # Ensures 4 sentences (one for each STAR component)
        }

    except Exception as e:
        print(f"Error generating resume section: {e}")
        return None

if __name__ == "__main__":
    # Define GitHub repository details
    owner = "Aditya Shah"
    repo = "TruHacks"

    # Fetch repository data dynamically using Fetch.py
    repo_data = aggregate_repo_data(owner, repo, commit_limit=100)

    if repo_data:
        # Generate STAR-based resume section
        star_section = generate_star_resume_section(repo_data)

        # Print the result
        print("Generated STAR Resume Section:")
        print(star_section)
    else:
        print("Failed to fetch repository data.")