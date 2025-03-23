from pinecone import Pinecone, ServerlessSpec
import os
import json
from dotenv import load_dotenv
import time
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Define index name
index_name = "vecdb"

# Delete the existing index if it exists (optional, comment out if you don't want to recreate)
if index_name in pc.list_indexes().names():
    pc.delete_index(index_name)

# Create the index with the correct dimensionality for SentenceTransformers
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,  # Matches all-MiniLM-L6-v2
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# Connect to the Pinecone index
index = pc.Index(index_name)

# Initialize SentenceTransformers model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load data from Job.json
job_data_path = "Job.json"  # Ensure this file exists in backend/
try:
    with open(job_data_path, "r") as f:
        job_data = [json.loads(line) for line in f]
except FileNotFoundError:
    print(f"Error: {job_data_path} not found. Please provide the job data file.")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON format in {job_data_path}: {e}")
    exit(1)

# Extract text for embedding
try:
    texts = [entry["metadata"]["job_summary"] for entry in job_data]
except KeyError as e:
    print(f"Error: Missing key in job data: {e}")
    exit(1)

# Generate embeddings using SentenceTransformers
embeddings = model.encode(texts).tolist()

# Wait for the index to be ready
while not pc.describe_index(index_name).status['ready']:
    time.sleep(1)

# Prepare upsert data with embeddings
upsert_data = []
for entry, embedding in zip(job_data, embeddings):
    try:
        upsert_data.append({
            "id": entry["id"],
            "values": embedding,
            "metadata": entry["metadata"]
        })
    except KeyError as e:
        print(f"Error: Missing key in job entry: {e}")
        continue

# Upsert data into Pinecone
if upsert_data:
    index.upsert(vectors=upsert_data, namespace="ns1")
    print(f"Successfully upserted {len(upsert_data)} vectors into Pinecone.")
else:
    print("Error: No valid data to upsert.")

# Print index stats
print(index.describe_index_stats())