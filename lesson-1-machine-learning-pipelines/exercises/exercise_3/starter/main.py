import mlflow
import os
import hydra
from omegaconf import DictConfig


import tempfile, shutil
from pathlib import Path


def _run_local(component_dir: Path, entry_point: str, parameters: dict):
    """Copy component to temp dir and run it so MLflow won't try git fetch."""
    component_dir = component_dir.resolve()
    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp) / component_dir.name
        shutil.copytree(component_dir, dest)
        return mlflow.run(uri=str(dest), entry_point=entry_point, parameters=parameters)



# This automatically reads in the configuration
@hydra.main(config_name='config')
def go(config: DictConfig):

    # Setup the wandb experiment. All runs will be grouped under this name
    os.environ["WANDB_PROJECT"] = config["main"]["project_name"]
    os.environ["WANDB_RUN_GROUP"] = config["main"]["experiment_name"]

    # You can get the path at the root of the MLflow project with this:
    #root_path = hydra.utils.get_original_cwd()
    root_path = Path(hydra.utils.get_original_cwd()).resolve()

    """
    dl_uri = (root_path / "download_data").resolve().as_uri()
    _ = mlflow.run(
        #os.path.join(root_path, "download_data"),
        uri=dl_uri,
        entry_point="main",
        parameters={
            "file_url": config["data"]["file_url"],
            "artifact_name": "iris.csv",
            "artifact_type": "raw_data",
            "artifact_description": "Input data"
        },
    ) 
    """

    def _run_local(component_dir: Path, entry_point: str, parameters: dict):
        """Copy component to temp dir (excluding .git) and run it so MLflow won't try git fetch."""
        component_dir = component_dir.resolve()
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / component_dir.name
            # Exclude any git metadata that would trigger mlflow's git flow
            shutil.copytree(
                component_dir,
                dest,
                ignore=shutil.ignore_patterns(".git", ".git*", ".github")
            )
            return mlflow.run(uri=str(dest), entry_point=entry_point, parameters=parameters)


    ##################
    # Your code here: use the artifact we created in the previous step as input for the `process_data` step
# and produce a new artifact called "cleaned_data".
# NOTE: use os.path.join(root_path, "process_data") to get the path
    # to the "process_data" component
    ##################

    """
    proc_uri = (root_path / "process_data").resolve().as_uri()
    _ = mlflow.run(
        #os.path.join(root_path, "process_data"),
        uri=proc_uri,
        entry_point="main",
        parameters={
            "input_artifact": "iris.csv:latest",
            "artifact_name": "clean_data.csv",
            "artifact_type": "processed_data",
            "artifact_description": "Cleaned Data"
        },
    )
    """

    # process_data
    _run_local(
        Path(root_path) / "process_data",
        "main",
        {
            "input_artifact": "iris.csv:latest",
            "artifact_name": "clean_data.csv",
            "artifact_type": "processed_data",
            "artifact_description": "Cleaned Data",
        },
    )

if __name__ == "__main__":
    go()
