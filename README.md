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

### Components
This project utilizes a variety of external services.
* pinecone -- a very robust vector database that is perfect for storing job searches for semantic matching.
* mongodb -- a good database to serve as my data lake/warehouse when retraining my GradientBoostedTree model.
* glm 4.7 flash -- an open source LLM that is good enough at text analysis. Not to mention, very resource efficient (as the api is free).
* mlflow -- mlops gold standard, used to monitor model metrics and versions.

### File structure

* backend -- backend version of application
    * app -- app files
        * config -- configuration files
            * gunicorn_config -- config file used for gunicorn
            * settings -- config file used for general settings
        * error_handling -- error handlers for fastapi
        * infrastructure
            * databases
            * models
        * middlewares
        * routers
        * schemas
        * services
        * .containerignore
        * Containerfile
        * app.py
        * dependencies -- dependencies for fastapi routers
        * requirements.txt -- used for downloading dependencies in containers
    * tests -- testing files 
* machine learning -- resources used for training my ml models
    * artifacts -- model artifacts (.joblib files, configurations)
    * config -- config files for infrastructure
    * data -- training data
    * data_gen -- scripts for data generation
    * mlruns -- mlflow runs
    * models -- scripts for training ml models
* requirements.txt -- contains all the required python packages

### Example .env file
ZAI_API=
GLM_MODEL=
PINECONE_API=
PINECONE_INDEX_NAME=
PINECONE_NAMESPACE=
LOGGER_FILE=
MONGODB_USERNAME=
MONGODB_PASSWORD=
HOST=
PORT=
ENVIRONMENT=

### Running the backend application
1. start at the root
2. use python -m venv .venv
3. use pip install -r requirements
6. cd backend/app
7. 4. create a .env file using the example .env file format listed above.
8. go to .config/settings, uncomment lines 6 & 28 (adjusting the file path if necessary), and comment out line 29 (that is only used while containerized).
10. use uvicorn app:app --host 0.0.0.0 --port 8000 or gunicorn -c ./config/gunicorn_config.py app:app depending on which mode you want. Note: windows os users cannot use gunicorn

### Training the model
1. use steps 1-3 from "running the backend application"
2. cd machine_learning and open ./models/boosted_tree
   * In addition, if you choose to do it with mlflow, use the command in a seperate terminal before the ones in step 3: mlflow server --host 127.0.0.1 --port 5000 --backend-store-uri sqlite:///mlflow.db 
4. mongodb database with the necessary data, set line 140 to asyncio.run(train_model(version=version, dataset_type="non-heuristic")) and run the script using python -m models.boosted_tree. Otherwise, generate a heuristical dataset using python -m dat_gen.heuristic and then use python -m models.boosted_tree.
5. The resulting joblib file should be found in the artifacts directory. 

### Containization

To further assist with my mlops learning, I have containerized the backend of this repository. The image can be found through this link: https://hub.docker.com/repository/docker/helloworld485736/ghost_job_detector/general
