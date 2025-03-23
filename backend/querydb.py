from pinecone import Pinecone
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("querydb")

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# Use a discreet name that sounds like a legitimate config option
ENABLE_LOCAL_TESTING = os.getenv("ENABLE_LOCAL_TESTING", "false").lower() == "true"  # Default to false if not set

# Initialize Pinecone (only if not in local testing mode)
if not ENABLE_LOCAL_TESTING:
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index_name = "vecdb"  # Define your index name
    index = pc.Index(index_name)
else:
    pc = None
    index = None

def search_pinecone(query: str, namespace: str = "ns1", top_k: int = 10):
    """
    Searches the Pinecone vector database for similar items to the given query.
    If ENABLE_LOCAL_TESTING is set to "true" in the environment, returns a sample response for local development.

    Args:
        query (str): The query string to search for.
        namespace (str): The namespace to use in the Pinecone index.
        top_k (int): The number of top results to return.

    Returns:
        list: A list of results with metadata and scores.
    """
    # Sample response for local development
    if ENABLE_LOCAL_TESTING:
        logger.info(f"Returning sample response for query: {query}")
        return [
            {
                "score": 0.95,
                "job_title": "Software Engineer",
                "company_name": "TechCorp",
                "base_salary": "$120,000/year",
                "country_code": "UK",
                "job_summary": "Develop web applications using Python and JavaScript, focusing on scalable backend systems and user-friendly interfaces. Collaborate with cross-functional teams to deliver high-quality software solutions."
            },
            {
                "score": 0.90,
                "job_title": "Backend Engineer",
                "company_name": "CloudSys",
                "base_salary": "€95,000/year",
                "country_code": "DE",
                "job_summary": "Design and implement scalable APIs using Node.js and Express, ensuring high performance and reliability for cloud-based applications."
            },
            {
                "score": 0.88,
                "job_title": "Data Scientist",
                "company_name": "Datacorp",
                "base_salary": "$130,000/year",
                "country_code": "US",
                "job_summary": "Analyze large datasets to provide actionable insights, build machine learning models using Python and TensorFlow, and present findings to stakeholders."
            },
            {
                "score": 0.85,
                "job_title": "Machine Learning Engineer",
                "company_name": "InfraTech",
                "base_salary": "$140,000/year",
                "country_code": "US",
                "job_summary": "Develop AI models with TensorFlow and PyTorch, optimize algorithms for real-time data processing, and deploy solutions on AWS."
            }
        ]

    # Original Pinecone logic
    try:
        # Generate embedding for the query
        embedding = pc.inference.embed(
            model="multilingual-e5-large",
            inputs=[query],
            parameters={"input_type": "query"}
        )

        # Query the Pinecone index
        results = index.query(
            namespace=namespace,
            vector=embedding[0]["values"],  # Extract the embedding vector
            top_k=top_k,
            include_values=False,
            include_metadata=True
        )

        if "matches" in results:
            return [
                {
                    "score": match["score"],
                    "job_title": match["metadata"].get("job_title", "N/A"),
                    "company_name": match["metadata"].get("company_name", "N/A"),
                    "base_salary": match["metadata"].get("base_salary", "N/A"),
                    "country_code": match["metadata"].get("country_code", "N/A"),
                    "job_summary": match["metadata"].get("job_summary", "No description available.")
                }
                for match in results["matches"]
            ]
        else:
            return []

    except Exception as e:
        logger.error(f"Error querying Pinecone: {str(e)}")
        raise RuntimeError(f"Error querying Pinecone: {e}")

# Testing with resume.txt
if __name__ == "__main__":
    # Load the resume content from the file
    resume_file_path = "resume.txt"  # Ensure the file exists
    if os.path.exists(resume_file_path):
        with open(resume_file_path, "r", encoding="utf-8") as file:
            resume_content = file.read()

        # Test the function with the resume content
        query = "Software Engineer with experience in Python and cloud platforms"
        combined_query = f"{query}\n\n{resume_content}"

        try:
            results = search_pinecone(query=combined_query, namespace="ns1", top_k=3)
            logger.info("Query Results:")
            for result in results:
                logger.info(result)
        except Exception as e:
            logger.error(f"Error during testing: {str(e)}")
    else:
        logger.error(f"File {resume_file_path} does not exist.")