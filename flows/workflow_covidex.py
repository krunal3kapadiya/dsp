# Step 1: pip install prefect
# In the end, there are two ways to execute
# 1. python workflow_covidex.py which starts the prefect server and runs on prefect cloud dashboard
# 2a. > prefect deployment build flows/workflow_covidex.py:main_flow -n "Covid DS Workflow Deployment" --output deployment.yaml
# 2b. prefect deployment apply deployment.yaml   
# First step creates a deployment.yaml file in "flows directory" and second step applies the deployment to prefect cloud.
# It provides the UI to view the deployment in the cloud

from prefect import flow, task, get_run_logger
import subprocess
import os

@task
def run_task(script_name):
    logger = get_run_logger()
    
    # Define the full path to the script based on the project structure
    script_path = os.path.join(os.path.dirname(__file__), '../tasks', script_name)
    
    try:
        # Run the external Python script using its full path
        result = subprocess.run(['python', script_path], capture_output=True, text=True)
        logger.info(result.stdout)  # Log standard output
        if result.stderr:
            logger.error(f"Error in {script_name}: {result.stderr}")  # Log standard error
    except Exception as e:
        logger.error(f"Failed to execute {script_name}: {str(e)}")

@flow
def main_flow():
    run_task("BasicStats.py")
    run_task("Binning.py")
    run_task("PearsonCorrelation.py")
    run_task("FeatureImportanceMLAlgorithms.py")

# for CI/CD, since all details are mentioned in deployment.yaml file
if __name__ == "__main__":
    main_flow.serve()

# to run locally
""" if __name__ == "__main__":
    main_flow.serve(name="covid-ds-workflow",
                      tags=["covid datascience project workflow"],
                      parameters={},
                      interval=300)    """
