import logging
import os
from pathlib import Path

import click

from .authentication import AWSCredentials
from .terraform_tools import (
    tf_destroy,
    tf_run1,
    tf_run2,
    tf_status,
)

# Globals
PROJECT_ROOT = Path.cwd()
TERRAFORM_ROOT = Path.cwd() / "terraform"

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Terraform logging
# os.environ["TF_LOG"] = "DEBUG"


@click.command()
@click.option("--destroy", is_flag=True, help="Destroy Terraform infrastructure")
@click.option("--run-state1", is_flag=True, help="Run Terraform commands")
@click.option("--status", is_flag=True, help="Get Terraform status")
@click.option("--run-state2", is_flag=True, help="Run state")
@click.option(
    "-v",
    "--verbosity",
    count=True,
    help="Increase the verbosity level of Terraform logs. Use multiple 'v's for higher verbosity: -v for WARN, -vv for INFO, -vvv for DEBUG, -vvvv for TRACE.",
)
def main(destroy, run_state1, status, run_state2, verbosity):
    AWSCredentials.load_credentials_from_file(
        PROJECT_ROOT / "tests/configs/credentials.json"
    )
    aws_credentials = AWSCredentials()
    aws_credentials.verify_credentials()

    verbosity_levels = {0: "ERROR", 1: "WARN", 2: "INFO", 3: "DEBUG", 4: "TRACE"}
    if verbosity in verbosity_levels:
        os.environ["TF_LOG"] = verbosity_levels[verbosity]
    else:
        os.environ["TF_LOG"] = "TRACE"

    if destroy:
        tf_destroy(TERRAFORM_ROOT)
    elif run_state1:
        tf_run1(TERRAFORM_ROOT)
    elif status:
        tf_status(TERRAFORM_ROOT)
    elif run_state2:
        tf_run2(TERRAFORM_ROOT)
    else:
        print("Please provide a valid flag. Use --help to see all options.")

    AWSCredentials.remove_credentials_from_environment()


if __name__ == "__main__":
    main()
