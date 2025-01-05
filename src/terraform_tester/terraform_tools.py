import logging

from python_terraform import Terraform

# Set up logging
logger = logging.getLogger(__name__)


def apply_terraform(tf):
    approve = {"auto-approve": True}
    return_code, stdout, stderr = tf.apply(skip_plan=True, **approve)
    if return_code != 0:
        logger.error(f"Error applying Terraform: {stderr}")
        return False
    logger.info("Terraform apply successful")
    return True


def initialize_terraform(terraform_root):
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


def tf_destroy(TERRAFORM_ROOT):
    tf = Terraform(working_dir=TERRAFORM_ROOT)
    return_code, stdout, stderr = tf.cmd("destroy", "-auto-approve")

    if return_code != 0:
        logger.error(f"Error destroying Terraform infrastructure: {stderr}")
    else:
        logger.info("Terraform destroy successful")


def tf_run1(TERRAFORM_ROOT):
    tf = initialize_terraform(TERRAFORM_ROOT)
    if tf is None:
        return
    if not plan_terraform(tf):
        return
    if not apply_terraform(tf):
        return


def tf_run2(TERRAFORM_ROOT):
    ## Run Terraform commands ##
    tf = Terraform(working_dir=TERRAFORM_ROOT)

    # Initialize the Terraform working directory
    return_code, stdout, stderr = tf.init()

    if return_code != 0:
        logger.error(f"Error initializing Terraform: {stderr}")
    else:
        logger.info("Terraform initialized successfully")

    # Plan the Terraform changes
    return_code, stdout, stderr = tf.plan(refresh=False)

    if return_code != 0:
        logger.error(f"Error planning Terraform: {stderr}")
    else:
        logger.info("Terraform plan successful")

    # Apply the Terraform changes
    approve = {"auto-approve": True}
    return_code, stdout, stderr = tf.apply(skip_plan=True, **approve)

    if return_code != 0:
        logger.error(f"Error applying Terraform: {stderr}")
    else:
        logger.info("Terraform apply successful")


def tf_status(TERRAFORM_ROOT):
    resource_address = "aws_instance.test_01_ec2_instance"
    tf = Terraform(working_dir=TERRAFORM_ROOT)
    return_code, stdout, stderr = tf.cmd("state", "show", resource_address)

    if return_code != 0:
        logger.error(f"Error getting Terraform status: {stderr}")
    else:
        logger.info("Terraform status retrieved successfully")
        logger.info(stdout)
