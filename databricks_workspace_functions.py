import requests
import json

# Replace the placeholders with your Databricks workspace URL and personal access token
workspace_url = "https://your-databricks-workspace-url"
token = "your-personal-access-token"
git_branch = "your-git-branch"
pipeline_keyword = f"your-pipeline-name {git_branch}"

# identify databricks pipeline by name and get job_id:

# Endpoint for listing all jobs
endpoint = f"{workspace_url}/api/2.0/jobs/list"

# Header with authorization token
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Make the GET request to list jobs
response = requests.get(endpoint, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    jobs_data = response.json()
    # Find pipelines containing the keyword in their names
    pipelines = [job for job in jobs_data["jobs"] if pipeline_keyword in job["settings"]["name"]]
    if pipelines:
        # Pipelines found, print their details
        print("Pipelines found:")
        for pipeline in pipelines:
            print(json.dumps(pipeline, indent=2))
            pipeline_name = pipeline['settings']['name']
            job_id = pipeline['job_id']
            print(f"pipeline_name: {pipeline_name}")
            print(f"job_id: {job_id}")
    else:
        print(f"No pipelines found containing the keyword '{pipeline_keyword}'")
else:
    # Print an error message if the request failed
    print(f"Error: {response.status_code} - {response.text}")


# get run_id

# Endpoint for listing runs of a specific job
endpoint = f"{workspace_url}/api/2.0/jobs/runs/list?job_id={job_id}"

# Header with authorization token
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Make the GET request
response = requests.get(endpoint, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Get the content of the response
    runs_data = response.json()
    # Check if runs_data contains the list of runs
    if 'runs' in runs_data and len(runs_data['runs']) > 0:
        # Get the most recent run (first entry in the list of runs)
        most_recent_run = runs_data['runs'][0]
        # Print information for the most recent run
        print(json.dumps(most_recent_run, indent=2))
    else:
        print("No runs found for the specified job.")
else:
    # Print an error message if the request failed
    print(f"Error: {response.status_code} - {response.text}")