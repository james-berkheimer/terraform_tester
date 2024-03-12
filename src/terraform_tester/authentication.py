import copy
import json
import os
from typing import Any, Dict

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from .logging import setup_logger

logger = setup_logger()


class AWSCredentials:
    @staticmethod
    def load_credentials_from_file(file_path: str):
        with open(file_path, "r") as f:
            data = json.load(f)
        os.environ["AWS_ACCESS_KEY_ID"] = data["credentials"]["aws"]["access_key_id"]
        os.environ["AWS_SECRET_ACCESS_KEY"] = data["credentials"]["aws"][
            "secret_access_key"
        ]
        os.environ["AWS_DEFAULT_REGION"] = data["credentials"]["aws"]["default_region"]
        logger.info(
            f"Loaded AWS credentials from {file_path}: {AWSCredentials._mask_auth_data(data['credentials']['aws'])}"
        )

    @staticmethod
    def remove_credentials_from_environment():
        os.environ.pop("AWS_ACCESS_KEY_ID", None)
        os.environ.pop("AWS_SECRET_ACCESS_KEY", None)
        os.environ.pop("AWS_DEFAULT_REGION", None)
        logger.info("Removed AWS credentials from environment variables")

    @staticmethod
    def _mask_auth_data(auth_data: Dict[str, Any]) -> Dict[str, Any]:
        # Mask sensitive data in auth_data for logger
        masked_auth_data = copy.deepcopy(auth_data)
        for key in masked_auth_data:
            if "token" in key or "key" in key:
                masked_auth_data[key] = "****"
        return masked_auth_data

    def verify_credentials(self):
        try:
            logger.info("Verifying AWS credentials")
            session = boto3.Session(
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("AWS_DEFAULT_REGION"),
            )
            ec2_resource = session.resource("ec2")
            ec2_resource.instances.all().limit(1)
            logger.info("AWS credentials are valid.")
            return True
        except (BotoCoreError, ClientError) as e:
            logger.error("AWS credentials are not valid.")
            logger.error("Error: %s", e)
            raise e
