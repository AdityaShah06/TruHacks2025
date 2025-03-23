import React, { useState, useEffect } from 'react';

const SwipeJob: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState<string>('Machine Learning Engineer');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [searchError, setSearchError] = useState<string | null>(null);

  // Skills from updated resume.txt
  const mySkills = [
    'Python', 'JavaScript', 'TypeScript', 'SQL',
    'TensorFlow', 'PyTorch', 'Scikit-learn', 'LangChain', 'Hugging Face', 'Pandas', 'NumPy',
    'AWS', 'Azure', 'PostgreSQL', 'MongoDB',
    'React.js', 'Next.js', 'Node.js', 'Express', 'Tailwind CSS',
    'Docker', 'GitHub', 'AWS DevOps', 'Version Control', 'Jira'
  ];

  // Function to extract matching skills from job summary
  const findMatchingSkills = (jobSummary: string) => {
    return mySkills.filter(skill => 
      jobSummary.toLowerCase().includes(skill.toLowerCase())
    );
  };

  // Fetch job matches on component mount
  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/search', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ query: searchQuery }),
        });

        if (!response.ok) {
          throw new Error('Failed to fetch search results');
        }

        const data = await response.json();
        setSearchResults(data.similarJobs);
      } catch (err: any) {
        setSearchError(err.message);
      }
    };

    fetchJobs();
  }, [searchQuery]);

  return (
    <div className="page-container">
      <h2 className="page-title">Swipe for Your Dream Job</h2>
      <div className="search-form">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Enter job title (e.g., Machine Learning Engineer)"
          className="search-input"
        />
        <button onClick={() => setSearchQuery(searchQuery)} className="search-button">Search Jobs</button>
      </div>

      {searchError && <p className="error">{searchError}</p>}

      {searchResults.length > 0 && (
        <div className="results">
          <h3>Job Matches</h3>
          <div className="job-list">
            {searchResults.map((job, index) => {
              const matchingSkills = findMatchingSkills(job.job_summary);
              return (
                <div key={index} className="job-card">
                  <h4>{job.job_title} at {job.company_name}</h4>
                  <p><strong>Location:</strong> {job.country_code}</p>
                  <p><strong>Salary:</strong> {job.base_salary}</p>
                  <p><strong>Match Score:</strong> {(job.score * 100).toFixed(1)}%</p>
                  <p><strong>Description:</strong> {job.job_summary}</p>
                  {matchingSkills.length > 0 && (
                    <p><strong>Your Matching Skills:</strong> {matchingSkills.join(', ')}</p>
                  )}