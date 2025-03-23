from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import logging
from Fetch import aggregate_repo_data  # Import aggregate_repo_data from Fetch.py
from model import generate_star_resume_section  # Import generate_star_resume_section from Model.py
from cvmodel import generate_cover_letter  # Import the AI function from cvmodel.py
from querydb import search_pinecone  # Import the search function from querydb.py

# Setup logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request models
class GitHubRepo(BaseModel):
    owner: str
    repo: str

class CoverLetterRequest(BaseModel):
    fullName: str
    jobTitle: str
    companyName: str
    jobDescription: str
    skills: list

class QueryRequest(BaseModel):
    query: str

# API Endpoints
@app.post("/api/github-project")
async def get_github_project(repo_data: GitHubRepo):
    """
    Fetches GitHub repository data and generates a STAR-based resume section.
    """
    try:
        logging.info(f"Fetching data for owner: {repo_data.owner}, repo: {repo_data.repo}")
        
        # Fetch GitHub data using aggregate_repo_data
        repo_details = aggregate_repo_data(repo_data.owner, repo_data.repo)
        
        if not repo_details:
            logging.error(f"Repository not found: {repo_data.owner}/{repo_data.repo}")
            raise HTTPException(status_code=404, detail="Repository not found")
        
        # Generate the STAR-based resume section
        star_resume = generate_star_resume_section(repo_details)
        
        if not star_resume:
            logging.error("Error generating STAR resume section.")
            raise HTTPException(status_code=500, detail="Failed to generate resume section")
        
        # Structure the response for the frontend
        result = {
            "repoName": star_resume["Name"],
            "date": star_resume["Date"],
            "descriptions": star_resume["Descriptions"]
        }
        
        logging.info(f"Successfully generated resume section for {repo_data.owner}/{repo_data.repo}")
        return result

    except Exception as e:
        logging.error(f"Error processing GitHub project request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/generate-cover-letter")
async def generate_cover_letter_endpoint(request: CoverLetterRequest):
    """
    Generates a cover letter based on user input.
    """
    try:
        logging.info(f"Received cover letter request for: {request.fullName}")

        # Generate cover letter
        cover_letter = generate_cover_letter(
            request.fullName,
            request.jobTitle,
            request.companyName,
            request.jobDescription,
            request.skills
        )

        if not cover_letter:
            logging.error("Failed to generate cover letter.")
            raise HTTPException(status_code=500, detail="Failed to generate cover letter")

        logging.info("Cover letter generated successfully.")
        return {"coverLetter": cover_letter}

    except Exception as e:
        logging.error(f"Error processing cover letter request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/search")
async def search_jobs(request: QueryRequest):
    """
    Searches for jobs based on the provided query.
    """
    try:
        logging.info(f"Searching jobs with query: {request.query}")
        results = search_pinecone(query=request.query, namespace="ns1", top_k=10)
        logging.info(f"Found {len(results)} job matches")
        return {"similarJobs": results}
    except Exception as e:
        logging.error(f"Error processing search request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/")
async def root():
    logging.info("Root endpoint accessed.")
    return {"message": "REPO2RESUME API is running"}