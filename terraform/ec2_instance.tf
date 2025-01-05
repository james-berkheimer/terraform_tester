terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.41.0"
    }
  }
}

provider "aws" {
    region = "us-west-1"
}

resource "aws_instance" "test_01_ec2_instance" {
    ami           = "ami-0830c9faf0efc29ff"
    instance_type = "t2.micro"

    tags = {
        Name = "Test_01"
    }

    ebs_block_device {
        device_name           = "/dev/sda1"
        volume_size           = 30
        delete_on_termination = true
        volume_type           = "gp3"
    }
}