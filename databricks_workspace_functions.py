import requests
import json

# Replace the placeholders with your Databricks workspace URL and personal access token
workspace_url = "https://your-databricks-workspace-url"
token = "your-personal-access-token"
git_branch = "your-git-branch"
pipeline_keyword = f"your-pipeline-name {git_branch}"

def get_pipeline_job_id_by_name(workspace_url: str, token: str, pipeline_keyword: str) -> str:
    """
    Retrieve the job ID of a Databricks pipeline by searching for a keyword in its name.

    Parameters:
        workspace_url (str): The URL of the Databricks workspace.
        token (str): The personal access token for accessing the Databricks API.
        pipeline_keyword (str): The keyword to search for in the pipeline names.

    Returns:
        str or None: The job ID of the first pipeline found containing the keyword in its name,
        or None if no such pipeline is found.
    """
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
            # Return the job_id of the first pipeline found
            return pipelines[0]['job_id']
        else:
            # If no pipelines found, return None
            print(f"No pipelines found containing the keyword '{pipeline_keyword}'")
            return None
    else:
        # Print an error message if the request failed
        print(f"Error: {response.status_code} - {response.text}")
        return None


def get_most_recent_run(job_id: str, token: str, workspace_url: str) -> dict:
    """
    Get the most recent run object for a specific job.

    Parameters:
        job_id (str): The ID of the job.
        token (str): Authorization token.
        workspace_url (str): URL of the workspace.

    Returns:
        dict: The most recent run object.
    """
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
            return most_recent_run
        else:
            print("No runs found for the specified job.")
    else:
        # Print an error message if the request failed
        print(f"Error: {response.status_code} - {response.text}")