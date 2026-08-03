# GhostJobDetection
This is a project where I attempt to use machine learning to solve a problem a lot of young people (including myself) are experiencing in the job market: ghost jobs. Common signs of ghost jobs include vague descriptions, frequent job reposts, long durations, and absence on websites. Thus, I will attempt to use those features to predict ghost jobs.

### Architecture
Below is the rough architecture that I planned for this application.

<img width="515" height="504" alt="image" src="https://github.com/user-attachments/assets/a57e4f6d-a3b4-4a18-ab7b-874ab723f852" />

The basic idea behind this project is simple. First, the user will send information of a job posting (job description, requirements, salary, ect) and the request will be received by a gunicorn+uvicorn powered fastapi backend. Afterwards, the LLM will evaluate the job description and a variety of text fields based on the following rubric to output a liklihood of the description being one of a ghost job. 

    1. Salary Transparency:
    - Missing or listed as "N/A" / "Competitive": +1.5 points
    - Unrealistically high or extreme range (e.g., $30,000 - $300,000): +2.0 points
    2. Role Definition & Responsibilities:
    - Extremely generic/copy-pasted bullet points (< 3 specific technical tools or key deliverables): +2.0 points
    - Mismatch between Position Title and actual Responsibilities: +2.0 points
    3. Company & Context:
    - Missing or overly generic Company Description: +1.5 points
    - Absence of specific team, project, or domain context: +1.0 point
    4. Requirements & Anomalies:
    - Contradictory experience requirements (e.g., "Entry-Level" requiring 5+ years experience): +2.0 points
    - Overly vague or missing requirements: +1.0 point

Afterwards, the LLM will output the results in the following JSON format:
{
"reasoning" : "the reason for the specific ranking",
"risk-factors" : "factors that make the job posting suspicious",
"final_rating" : "scale from 0 (definitely not a ghost job) to 10 (definitely a ghost job)",
}

The final rating will be combined with the rest of the unused information from the request to be evaluated by a gradient boosted tree for a final decision on whether the job posting is likely to be a ghost job or not. 

To make the process more efficient, I will also use a vector database to store the results of the LLM evaluation. This way, the responses become way faster (from my testing, response times seem to jump from ~30-50 seconds to ~5-8 seconds). 

### Dataset Issues and Solution

Unfortunately, a massive problem that I encountered is that there was simply no dataset that suits my requirements. Some of the fields I wanted to use for my gradient boosted tree, like job repost frequency and how many days a position has been active, simply don't exist in the vast majority of ghost job databases. For datasets that have such metadata, the tuples aren't labelled as ghost job or not. So if I had to use these datasets, I basically need to manually test each job posting by myself, which is highly impractical. 

To somewhat circumvent this issue, I used a python script to generate a dataset based on heuristics with a little bit of noise added. Some of these include how ghost job are more likely to be frequently reposted and ghost job postings are more likely to be active for more than 35 days. 

To account for future data changes (because I know that this heuristics based dataset will be far from perfect), I designed a script that automatically syphons data from a data lake/warehouse, uses the data to train new versions of GradientBoostedTrees, and evaluate the new models. To facilitate model training and evaluations, data will be collected by mlflow to be stored and viewed. 

### Component Analysis

This project utilizes a variety of external services.
* pinecone -- a very robust vector database that is perfect for storing job searches for semantic matching.
* mongodb -- a good database to serve as my data lake/warehouse when retraining my GradientBoostedTree model.
* glm 4.7 flash -- an open source LLM that is good enough at text analysis. Not to mention, very resource efficient (as the api is free).
* mlflow -- mlops gold standard, used to monitor model metrics and versions. 
