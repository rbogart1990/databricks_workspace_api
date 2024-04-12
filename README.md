# databricks_workspace_api

functions for working with the databricks workspace

## Installation

Instructions for installing the project or any dependencies. (forthcoming...)

## Usage

### Example 1: Getting Pipeline Job ID by Name

```python
# Usage example for get_pipeline_job_id_by_name
workspace_url = "https://your-databricks-workspace-url"
token = "your-personal-access-token"
pipeline_keyword = "keyword-to-search-for-in-pipeline-names"

job_id = get_pipeline_job_id_by_name(workspace_url, token, pipeline_keyword)
if job_id:
    print(f"Pipeline job ID found: {job_id}")
else:
    print("No pipeline job ID found.")
```

### Example 2: Getting Specific Run Information
```python
# Usage example for get_specific_run
job_id = "your-job-id"
run_index = 0  # Index of the run to retrieve, default is 0 for the most recent run

run_details = get_specific_run(job_id, token, workspace_url, run_index)
if run_details:
    print("Run details:")
    for key, value in run_details.items():
        print(f"{key}: {value}")
else:
    print("No run details found.")
```

### Example 3: Getting Run Details
```python
# Usage example for get_run_details
run_id, run_name = get_run_details(job_id, token, workspace_url, run_index)
if run_id and run_name:
    print(f"Run ID: {run_id}, Run Name: {run_name}")
else:
    print("No run details found.")
```