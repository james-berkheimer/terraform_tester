provider "aws" {
    region = "us-west-1"
}

resource "aws_instance" "test_ec2_instance" {
    ami           = "ami-05057ffd3a8e2ef62"
    instance_type = "t2.micro"

    tags = {
        Name = "MC_EC2Instance"
    }

    ebs_block_device {
        device_name           = "/dev/sda1"
        volume_size           = 30
        delete_on_termination = true
        volume_type           = "gp3"
    }
}