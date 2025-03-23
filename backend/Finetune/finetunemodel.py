import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def generate_star_resume_section(repo_data):
    """
    Generate a professional and concise STAR-based project description for a resume using Gemini API.
    :param repo_data: Dictionary containing GitHub repository details.
    :return: A dictionary with Name, Date, Languages, and Descriptions.
    """
    try:
        # Prepare the prompt with STAR structure
        prompt = f"""
        Generate a professional and concise project description for a resume using the STAR (Situation, Task, Action, Result) method.
        Each component must consist of a single, concise sentence written in formal, action-oriented language without personal pronouns or references.

        Repository Details:
        - Repository Name: {repo_data['Repository Name']}
        - Description: {repo_data['Description']}
        - Topics: {', '.join(repo_data.get('Topics', []))}
        - Languages: {json.dumps(repo_data['Languages'], indent=2)}
        - Recent Commit Messages: {', '.join(repo_data.get('Recent Commit Messages', [])[:5])}

        Format the response exactly as:
        - Situation: [Your sentence here]
        - Task: [Your sentence here]
        - Action: [Your sentence here]
        - Result: [Your sentence here]

        Ensure the output is concise, professional, and directly applicable to a resume.
        """

        # Call Gemini API
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        result_text = response.text.strip()

        # Parse STAR components
        descriptions = []
        for line in result_text.split("\n"):
            if ": " in line:
                try:
                    component = line.split(": ", 1)[1].strip()
                    descriptions.append(component)
                except IndexError:
                    continue

        # Validate 4 STAR components
        if len(descriptions) != 4:
            print(f"Warning: Expected 4 STAR components, got {len(descriptions)}. Response: {result_text}")
            return None

        # Return structured data
        return {
            "Name": repo_data["Repository Name"],
            "Date": f"{repo_data['Start Date']} - {repo_data['Last Updated']}",
            "Languages": list(repo_data["Languages"].keys()),
            "Descriptions": descriptions  # List for FastAPI compatibility
        }

    except genai.GenerationError as e:
        print(f"Gemini API error: {e}")
        raise ValueError("Failed to generate content from Gemini API")
    except KeyError as e:
        print(f"Missing key in repo_data: {e}")
        raise ValueError(f"Invalid repository data: missing {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise RuntimeError("Internal error generating resume section")

if __name__ == "__main__":
    # Example test data
    repo_data = {
        "Repository Name": "TruHacks",
        "Description": "A hackathon project",
        "Topics": ["python", "ai"],
        "Languages": {"Python": 80, "JavaScript": 20},
        "Recent Commit Messages": ["Initial commit", "Add AI feature", "Fix bugs"],
        "Start Date": "2023-01-01",
        "Last Updated": "2023-12-31"
    }
    result = generate_star_resume_section(repo_data)
    print(result)