import logging
import os
from pathlib import Path

import boto3
from python_terraform import Terraform

from .authentication import AWSCredentials

project_root = Path.cwd()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

os.environ["TF_LOG"] = "DEBUG"
terraform_root = Path.cwd() / "terraform"


def initialize_aws_credentials():
    AWSCredentials.load_credentials_from_file(
        project_root / "tests/configs/credentials.json"
    )
    aws_credentials = AWSCredentials()
    aws_credentials.verify_credentials()


def initialize_terraform():
    tf = Terraform(working_dir=terraform_root)
    return_code, stdout, stderr = tf.init()
    if return_code != 0:
        logger.error(f"Error initializing Terraform: {stderr}")
        return None
    logger.info("Terraform initialized successfully")
    return tf


def plan_terraform(tf):
    return_code, stdout, stderr = tf.plan(refresh=False)
    if return_code != 0:
        logger.error(f"Error planning Terraform: {stderr}")
        return False
    logger.info("Terraform plan successful")
    return True


def apply_terraform(tf):
    approve = {"auto-approve": True}
    return_code, stdout, stderr = tf.apply(skip_plan=True, **approve)
    if return_code != 0:
        logger.error(f"Error applying Terraform: {stderr}")
        return False
    logger.info("Terraform apply successful")
    return True


def main():
    initialize_aws_credentials()
    tf = initialize_terraform()
    if tf is None:
        return
    if not plan_terraform(tf):
        return
    if not apply_terraform(tf):
        return
    AWSCredentials.remove_credentials_from_environment()


def terraform_status():
    resource_address = "aws_instance.test_ec2_instance"
    tf = Terraform(working_dir=terraform_root)
    return_code, stdout, stderr = tf.cmd("state", "show", resource_address)

    if return_code != 0:
        logger.error(f"Error getting Terraform status: {stderr}")
        return None

    logger.info("Terraform status retrieved successfully")
    return stdout


def destroy_terraform(tf):
    approve = {"auto-approve": True}
    return_code, stdout, stderr = tf.destroy(**approve)
    if return_code != 0:
        logger.error(f"Error destroying Terraform infrastructure: {stderr}")
        return False
    logger.info("Terraform destroy successful")
    return True
