import requests
import logging

logging.basicConfig(level=logging.INFO)

# Replace the placeholders with your Databricks workspace URL and personal access token
workspace_url = "https://your-databricks-workspace-url"
token = "your-personal-access-token"
git_branch = "your-git-branch"
pipeline_keyword = f"your-pipeline-name {git_branch}"

import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)  # Set logging level to INFO


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
        pipelines = [job["job_id"] for job in jobs_data.get("jobs", []) if pipeline_keyword in job.get("settings", {}).get("name", "")]
        
        # Check if any pipelines were found
        if pipelines:
            logging.info(f"Found pipelines containing the keyword '{pipeline_keyword}'")
            return pipelines[0]
        else:
            logging.warning(f"No pipelines found containing the keyword '{pipeline_keyword}'")
            return None
    else:
        logging.error(f"Error: {response.status_code} - {response.text}")
        return None


def get_specific_run(job_id: str, token: str, workspace_url: str, run_index: int = 0) -> dict:
    """
    Get a specific run object for a specific job.

    Parameters:
        job_id (str): The ID of the job.
        token (str): Authorization token.
        workspace_url (str): URL of the workspace.
        run_index (int): Index of the run to retrieve. Default is 0 (most recent run).

    Returns:
        dict: The specified run object.
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
        # Get the list of runs
        runs_data = response.json().get("runs", [])

        # Check for the specified run
        if len(runs_data) > run_index:
            return runs_data[run_index]
        else:
            logging.warning("No runs found for the specified job or invalid run index.")
            return None
    else:
        logging.error(f"Error: {response.status_code} - {response.text}")
        return None


def get_run_details(job_id: str, token: str, workspace_url: str, run_index: int = 0) -> (str, str):
    """
    Get the run_id and run_name for a specific job run.

    Parameters:
        job_id (str): The ID of the job.
        token (str): Authorization token.
        workspace_url (str): URL of the workspace.
        run_index (int): Index of the run to retrieve. Default is 0 (most recent run).

    Returns:
        Tuple[str, str]: The run_id and run_name of the specified job run.
    """
    # Get the details of the specified run
    run_details = get_specific_run(job_id, token, workspace_url, run_index)

    # Extract run_id and run_name from run_details
    run_id = run_details.get('run_id', '') if run_details else ''
    run_name = run_details.get('run_name', '') if run_details else ''

    return run_id, run_name
